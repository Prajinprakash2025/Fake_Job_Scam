from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.username


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True)
    company_logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    company_description = models.TextField(blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name or self.user.username


class JobPost(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    JOB_TYPE_CHOICES = (
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
        ("Contract", "Contract"),
        ("Internship", "Internship"),
        ("Freelance", "Freelance"),
    )

    CATEGORY_CHOICES = (
        ("Engineering", "Engineering"),
        ("Marketing", "Marketing"),
        ("HR", "HR"),
        ("Product", "Product"),
        ("Data Science", "Data Science"),
        ("Analytics", "Analytics"),
        ("Design", "Design"),
        ("Sales", "Sales"),
        ("Operations", "Operations"),
        ("General", "General / Other"),
    )

    WORK_MODE_CHOICES = (
        ("Remote", "Remote"),
        ("Hybrid", "Hybrid"),
        ("Onsite", "Onsite"),
    )

    COMPANY_SIZE_CHOICES = (
        ("Startup", "Startup"),
        ("MNC", "MNC"),
        ("Fortune 500", "Fortune 500"),
        ("SME", "SME / Mid-size"),
    )

    EXPERIENCE_CHOICES = (
        ("Internship", "Internship"),
        ("Fresher", "Fresher"),
        ("Entry", "Entry Level"),
        ("Mid", "Mid Level"),
        ("Senior", "Senior"),
    )

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="General")
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES, default="Startup")
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default="Onsite")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default="Mid")
    description = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default="Full-time")
    salary_range = models.CharField(max_length=100, blank=True)
    job_url = models.URLField(blank=True)
    pdf = models.FileField(upload_to="job_pdfs/", blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    scam_probability = models.FloatField(null=True, blank=True)
    scam_level = models.CharField(max_length=20, blank=True)
    admin_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.full_name} -> {self.job.title}"
