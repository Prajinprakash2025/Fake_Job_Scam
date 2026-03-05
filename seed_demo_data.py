import os
import re
import struct
import zlib
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scam_detector.settings")

import django

django.setup()

from django.contrib.auth.models import User  # noqa: E402
from scanner.models import JobPost, Profile, RecruiterProfile  # noqa: E402


BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / "media"
LOGO_DIR = MEDIA_ROOT / "company_logos"

PASSWORD = "123456lp"


def ensure_dirs():
    LOGO_DIR.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "logo"


def png_bytes(color):
    """Return a simple 120x120 PNG byte string for the given RGB tuple."""
    w = h = 120
    r, g, b = color
    # Each row starts with filter byte 0
    row = bytes([0] + list([r, g, b] * w))
    raw = row * h

    def chunk(chunk_type, data):
        chunk_body = chunk_type + data
        return struct.pack(">I", len(data)) + chunk_body + struct.pack(">I", zlib.crc32(chunk_body) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    idat = zlib.compress(raw, 9)

    png_header = b"\x89PNG\r\n\x1a\n"
    return png_header + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def write_logo(name: str, color: tuple) -> str:
    ensure_dirs()
    filename = f"{slugify(name)}.png"
    path = LOGO_DIR / filename
    if not path.exists():
        path.write_bytes(png_bytes(color))
    return f"company_logos/{filename}"


def ensure_recruiter(email, company_name, website, color, description):
    user, created = User.objects.get_or_create(username=email, defaults={"email": email, "first_name": company_name.split()[0]})
    if created:
        user.set_password(PASSWORD)
        user.save()

    profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": "recruiter", "is_verified": True})
    if profile.role != "recruiter":
        profile.role = "recruiter"
    profile.is_verified = True
    profile.save()

    logo_name = write_logo(company_name, color)

    recruiter_profile, _ = RecruiterProfile.objects.get_or_create(user=user, defaults={"company_name": company_name})
    recruiter_profile.company_name = company_name
    recruiter_profile.company_website = website
    recruiter_profile.company_description = description
    recruiter_profile.verified = True
    recruiter_profile.company_logo.name = logo_name
    recruiter_profile.save()
    return user


def seed_jobs(recruiter_user, jobs):
    for job in jobs:
        JobPost.objects.update_or_create(
            title=job["title"],
            recruiter=recruiter_user,
            defaults={
                "category": job.get("category", "General"),
                "company_size": job.get("company_size", "Startup"),
                "work_mode": job.get("work_mode", "Onsite"),
                "experience_level": job.get("experience_level", "Mid"),
                "description": job.get("description", ""),
                "location": job.get("location", ""),
                "job_type": job.get("job_type", "Full-time"),
                "salary_range": job.get("salary_range", ""),
                "job_url": job.get("job_url", ""),
                "status": "approved",
                "scam_probability": job.get("scam_probability", 12.0),
                "scam_level": job.get("scam_level", "Low"),
                "admin_note": "Demo seeded content",
            },
        )


def main():
    companies = [
        {
            "email": "aurora@demo.co",
            "name": "Aurora Labs",
            "website": "https://aurora.demo",
            "color": (37, 99, 235),
            "desc": "AI-first product studio shipping reliable cloud platforms.",
        },
        {
            "email": "northwind@demo.co",
            "name": "Northwind Analytics",
            "website": "https://northwind.demo",
            "color": (14, 165, 233),
            "desc": "Data and BI powerhouse serving global enterprises.",
        },
        {
            "email": "vantage@demo.co",
            "name": "Vantage Bank",
            "website": "https://vantage.demo",
            "color": (249, 115, 22),
            "desc": "Fortune 500 financial leader modernizing digital experiences.",
        },
        {
            "email": "zenith@demo.co",
            "name": "Zenith People",
            "website": "https://zenith.demo",
            "color": (16, 185, 129),
            "desc": "HR services group focused on global talent mobility.",
        },
    ]

    job_matrix = [
        # Aurora Labs (Startup / Remote friendly)
        ("aurora@demo.co",
         [
             {"title": "Remote Backend Engineer", "category": "Engineering", "company_size": "Startup", "work_mode": "Remote", "experience_level": "Mid", "location": "Remote", "salary_range": "$110k - $140k", "job_url": "https://aurora.demo/jobs/backend"},
             {"title": "Product Trainee (Fresher)", "category": "Product", "company_size": "Startup", "work_mode": "Hybrid", "experience_level": "Fresher", "location": "Austin, TX", "salary_range": "$55k - $65k", "job_url": "https://aurora.demo/jobs/product-trainee"},
             {"title": "Cloud DevOps Engineer", "category": "Engineering", "company_size": "Startup", "work_mode": "Hybrid", "experience_level": "Senior", "location": "Denver, CO", "salary_range": "$125k - $155k", "job_url": "https://aurora.demo/jobs/devops"},
         ]),
        # Northwind Analytics (MNC)
        ("northwind@demo.co",
         [
             {"title": "Data Science Intern", "category": "Data Science", "company_size": "MNC", "work_mode": "Remote", "experience_level": "Internship", "location": "Remote", "job_type": "Internship", "salary_range": "$1,200/mo", "job_url": "https://northwind.demo/careers/ds-intern"},
             {"title": "Analytics Specialist", "category": "Analytics", "company_size": "MNC", "work_mode": "Onsite", "experience_level": "Entry", "location": "Chicago, IL", "job_url": "https://northwind.demo/careers/analytics"},
             {"title": "Data Platform Engineer", "category": "Engineering", "company_size": "MNC", "work_mode": "Hybrid", "experience_level": "Mid", "location": "Seattle, WA", "job_url": "https://northwind.demo/careers/platform"},
         ]),
        # Vantage Bank (Fortune 500)
        ("vantage@demo.co",
         [
             {"title": "Marketing Manager - Cards", "category": "Marketing", "company_size": "Fortune 500", "work_mode": "Onsite", "experience_level": "Senior", "location": "New York, NY", "job_url": "https://vantage.demo/careers/marketing"},
             {"title": "HR Business Partner", "category": "HR", "company_size": "Fortune 500", "work_mode": "Hybrid", "experience_level": "Mid", "location": "Dallas, TX", "job_url": "https://vantage.demo/careers/hrbp"},
             {"title": "Operations Coordinator", "category": "Operations", "company_size": "Fortune 500", "work_mode": "Onsite", "experience_level": "Entry", "location": "Phoenix, AZ", "job_url": "https://vantage.demo/careers/ops"},
         ]),
        # Zenith People (SME / Services)
        ("zenith@demo.co",
         [
             {"title": "Talent Acquisition Specialist", "category": "HR", "company_size": "SME", "work_mode": "Remote", "experience_level": "Mid", "location": "Remote", "job_url": "https://zenith.demo/careers/ta"},
             {"title": "Sales Executive - Staffing", "category": "Sales", "company_size": "SME", "work_mode": "Hybrid", "experience_level": "Mid", "location": "Miami, FL", "job_url": "https://zenith.demo/careers/sales"},
             {"title": "UI/UX Designer", "category": "Design", "company_size": "SME", "work_mode": "Remote", "experience_level": "Mid", "location": "Remote", "job_url": "https://zenith.demo/careers/design"},
             {"title": "General Support Associate", "category": "General", "company_size": "SME", "work_mode": "Onsite", "experience_level": "Entry", "location": "Raleigh, NC", "job_url": "https://zenith.demo/careers/support"},
         ]),
    ]

    for company in companies:
        ensure_recruiter(
            company["email"],
            company["name"],
            company["website"],
            company["color"],
            company["desc"],
        )

    for email, jobs in job_matrix:
        recruiter_user = User.objects.get(username=email)
        seed_jobs(recruiter_user, jobs)

    print("Seeding complete.")
    print("Created/updated companies:", ", ".join(c["name"] for c in companies))
    print("Default recruiter password:", PASSWORD)


if __name__ == "__main__":
    main()
