from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScanForm, RecruiterProfileForm, JobPostForm
from .ml.ml_model import predict_scam
from .utils.url_extractor import extract_text_from_url
from .utils.pdf_extractor import extract_text_from_pdf
from .ml.visualizations import get_dashboard_stats
from .models import Profile, RecruiterProfile, JobPost, JobApplication
from django.contrib.auth.decorators import login_required, user_passes_test


###################login sesSIon########################


from django.contrib.auth import authenticate, login


# HOME PAGE
def home(request):
    approved_jobs_qs = JobPost.objects.filter(status="approved").select_related("recruiter__recruiterprofile")
    approved_jobs = approved_jobs_qs.order_by("-created_at")[:12]

    category_counts = {row["category"]: row["count"] for row in approved_jobs_qs.values("category").annotate(count=Count("id"))}
    work_mode_counts = {row["work_mode"]: row["count"] for row in approved_jobs_qs.values("work_mode").annotate(count=Count("id"))}
    company_size_counts = {row["company_size"]: row["count"] for row in approved_jobs_qs.values("company_size").annotate(count=Count("id"))}
    experience_counts = {row["experience_level"]: row["count"] for row in approved_jobs_qs.values("experience_level").annotate(count=Count("id"))}

    category_cards = [
        {"slug": "remote", "label": "Remote", "icon": "🏠", "filter": "work_remote", "count": work_mode_counts.get("Remote", 0)},
        {"slug": "mnc", "label": "MNC", "icon": "🏢", "filter": "size_mnc", "count": company_size_counts.get("MNC", 0)},
        {"slug": "engineering", "label": "Engineering", "icon": "⚙️", "filter": "cat_engineering", "count": category_counts.get("Engineering", 0)},
        {"slug": "fortune", "label": "Fortune 500", "icon": "🏛️", "filter": "size_fortune", "count": company_size_counts.get("Fortune 500", 0)},
        {"slug": "marketing", "label": "Marketing", "icon": "📣", "filter": "cat_marketing", "count": category_counts.get("Marketing", 0)},
        {"slug": "hr", "label": "HR", "icon": "🧑‍💼", "filter": "cat_hr", "count": category_counts.get("HR", 0)},
        {"slug": "startup", "label": "Startup", "icon": "🚀", "filter": "size_startup", "count": company_size_counts.get("Startup", 0)},
        {"slug": "data", "label": "Data Science", "icon": "📊", "filter": "cat_data", "count": category_counts.get("Data Science", 0)},
        {"slug": "internship", "label": "Internship", "icon": "🎓", "filter": "exp_internship", "count": experience_counts.get("Internship", 0)},
        {"slug": "analytics", "label": "Analytics", "icon": "📈", "filter": "cat_analytics", "count": category_counts.get("Analytics", 0)},
        {"slug": "fresher", "label": "Fresher", "icon": "🌱", "filter": "exp_fresher", "count": experience_counts.get("Fresher", 0)},
    ]

    trending_categories = approved_jobs_qs.values("category").annotate(count=Count("id")).order_by("-count")[:6]

    company_stats = (
        approved_jobs_qs.values("recruiter__recruiterprofile__company_name", "recruiter__username")
        .annotate(count=Count("id"))
        .order_by("-count")[:8]
    )
    company_cards = []
    for row in company_stats:
        name = row.get("recruiter__recruiterprofile__company_name") or row.get("recruiter__username")
        if name:
            company_cards.append({"name": name, "count": row["count"]})

    stats = {
        "total": approved_jobs_qs.count(),
        "remote": work_mode_counts.get("Remote", 0),
        "internships": experience_counts.get("Internship", 0),
        "freshers": experience_counts.get("Fresher", 0),
    }

    return render(
        request,
        "home.html",
        {
            "approved_jobs": approved_jobs,
            "category_cards": category_cards,
            "trending_categories": trending_categories,
            "company_cards": company_cards,
            "stats": stats,
            "categories": JobPost.CATEGORY_CHOICES,
        },
    )

# LOGIN SELECTION PAGE (Choose Role)
def login_select(request):
    return render(request, "login_select.html")

# ABOUT PAGE
def about(request):
    return render(request, "about.html")

# CONTACT PAGE
def contact(request):
    return render(request, "contact.html")

# USER PROFILE PAGE
@login_required
def user_profile(request):
    msg = None
    recruiter_form = None

    if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
        try:
            recruiter_profile = request.user.recruiterprofile
        except ObjectDoesNotExist:
            recruiter_profile = None

        if request.method == "POST" and "company_name" in request.POST:
            recruiter_form = RecruiterProfileForm(request.POST, request.FILES, instance=recruiter_profile)
            if recruiter_form.is_valid():
                recruiter_form.save()
                msg = "Company profile updated successfully!"
        else:
            recruiter_form = RecruiterProfileForm(instance=recruiter_profile)

    if request.method == "POST" and "username" in request.POST:
        new_username = request.POST.get("username", "").strip()
        new_email = request.POST.get("email", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        if new_username and new_username != request.user.username:
            if User.objects.filter(username=new_username).exists():
                msg = "Username already taken."
            else:
                request.user.username = new_username

        if new_email and new_email != request.user.email:
            if User.objects.filter(email=new_email).exists():
                msg = "Email already registered."
            else:
                request.user.email = new_email

        request.user.first_name = first_name
        request.user.last_name = last_name

        if not msg:
            request.user.save()
            msg = "Profile updated successfully!"

    applications = JobApplication.objects.filter(applicant=request.user).order_by("-applied_at")
    return render(request, "user_profile.html", {
        "applications": applications, 
        "msg": msg,
        "recruiter_form": recruiter_form
    })

# USER LOGIN
def user_login(request):
    error = None
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user and user.profile.role == "user":
            login(request, user)
            return redirect("home")
        else:
            error = "Invalid user credentials"
    return render(request, "user_login.html", {"error": error})


# USER SIGNUP
def user_signup(request):
    error = None
    success = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm", "")

        if not username or not email or not password:
            error = "All fields are required."
        elif password != confirm:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already taken."
        elif User.objects.filter(email=email).exists():
            error = "Email already registered."
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, role="user", is_verified=True)
            login(request, user)
            return redirect("home")

    return render(request, "user_signup.html", {"error": error, "success": success})


import json
import random
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail

def recruiter_login(request):
    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            # Check if they have a profile and are a recruiter
            if not hasattr(user, 'profile') or user.profile.role != "recruiter":
                error = "Not a recruiter account"
            # Make sure they verified their OTP during registration
            elif not user.profile.is_verified:
                error = "Account not verified. Please check your email for the OTP sent during signup."
            else:
                login(request, user)
                return redirect("recruiter_dashboard")
        else:
            error = "Invalid email or password"

    return render(request, "recruiter_login.html", {"error": error})




# ADMIN LOGIN
from scanner.models import Profile

def admin_login(request):
    error = None

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            profile, created = Profile.objects.get_or_create(user=user)

            if profile.role == "admin" or user.is_superuser:
                profile.role = "admin"
                profile.save()
                login(request, user)
                return redirect("admin_dashboard")
            else:
                error = "Not authorized as admin"
        else:
            error = "Invalid credentials"

    return render(request, "admin_login.html", {"error": error})


def scan_job(request):
    result = None
    error = None

    if request.method == "POST":
        form = ScanForm(request.POST, request.FILES)

        if form.is_valid():
            description = form.cleaned_data.get("description", "").strip()
            job_url = form.cleaned_data.get("job_url", "").strip()
            pdf_file = request.FILES.get("pdf_file")

            text = None

            # PRIORITY ORDER
            if description:
                text = description
            elif pdf_file:
                text = extract_text_from_pdf(pdf_file)
            elif job_url:
                text = extract_text_from_url(job_url)

            if text:
                prob, level, note = predict_scam(text)
                result = {
                    "prob": prob,
                    "level": level,
                    "note": note
                }
            else:
                error = "Unable to extract text. Please provide valid text, URL, or PDF."

    else:
        form = ScanForm()

    stats = {
        "total": JobPost.objects.filter(status="approved").count(),
        "remote": JobPost.objects.filter(status="approved", work_mode="Remote").count(),
    }

    return render(request, "scan.html", {
        "form": form,
        "result": result,
        "error": error,
        "stats": stats,
    })



##############################recruiter session##########################


def is_recruiter(user):
    """Check if user is a recruiter"""
    return hasattr(user, 'profile') and user.profile.role == "recruiter"


@login_required
@user_passes_test(is_recruiter, login_url='login_select')
def recruiter_dashboard(request):
    jobs = JobPost.objects.filter(recruiter=request.user)
    applications = JobApplication.objects.filter(job__recruiter=request.user).order_by("-applied_at")

    stats = {
        "total": jobs.count(),
        "pending": jobs.filter(status="pending").count(),
        "approved": jobs.filter(status="approved").count(),
        "rejected": jobs.filter(status="rejected").count(),
    }

    return render(request, "recruiter/dashboard.html", {
        "jobs": jobs,
        "stats": stats,
        "applications": applications
    })

import json
import random
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib import messages
from .forms import JobPostForm

from django.urls import reverse

@login_required
@user_passes_test(is_recruiter, login_url='login_select')
def edit_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, recruiter=request.user)
    if request.method == "POST":
        form = JobPostForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            # Any edits push the job back to pending
            updated_job = form.save(commit=False)
            updated_job.status = "pending"
            updated_job.admin_note = ""
            updated_job.scam_probability = None
            updated_job.scam_level = ""
            updated_job.save()
            messages.success(request, "Job updated successfully! It is now pending admin review.")
            return redirect(reverse("recruiter_dashboard") + "#jobs")
    else:
        form = JobPostForm(instance=job)
    return render(request, "recruiter/edit_job.html", {"form": form, "job": job})

@login_required
@user_passes_test(is_recruiter, login_url='login_select')
def delete_job(request, job_id):
    if request.method == "POST":
        job = get_object_or_404(JobPost, id=job_id, recruiter=request.user)
        job.delete()
        messages.success(request, "Job deleted successfully.")
    return redirect(reverse("recruiter_dashboard") + "#jobs")

@login_required
@user_passes_test(is_recruiter, login_url='login_select')
def bulk_delete_jobs(request):
    if request.method == "POST":
        job_ids = request.POST.getlist("job_ids")
        if job_ids:
            jobs = JobPost.objects.filter(id__in=job_ids, recruiter=request.user)
            count = jobs.count()
            jobs.delete()
            messages.success(request, f"Successfully deleted {count} job(s).")
    return redirect(reverse("recruiter_dashboard") + "#jobs")

def recruiter_signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            confirm = data.get("confirm")
            company_name = data.get("company_name", "Unknown Company")

            if password != confirm:
                return JsonResponse({"status": "error", "message": "Passwords do not match."})
            
            # 1. Check if the email is already completely registered
            if User.objects.filter(username=email).exists():
                return JsonResponse({"status": "error", "message": "Email already registered. Please log in."})

            # 2. DO NOT CREATE THE USER YET! Generate OTP first.
            otp = str(random.randint(100000, 999999))
            
            # 3. Store the details temporarily in the session memory
            request.session["temp_registration_data"] = {
                "email": email,
                "password": password,
                "company_name": company_name,
                "otp": otp
            }

            # 4. Send the OTP email
            send_mail(
                "SafeCareer - Verify your Recruiter Account",
                f"Your OTP code is {otp}",
                "noreply@jobscamdetector.com",
                [email],
                fail_silently=False,
            )

            return JsonResponse({"status": "success"})
                
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return render(request, "recruiter_signup.html")


def recruiter_verify(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_otp = data.get("otp")
            
            # 1. Get the temporary data back from the session
            temp_data = request.session.get("temp_registration_data")

            if not temp_data:
                return JsonResponse({"status": "error", "message": "Session expired or invalid. Please refresh and register again."})

            # 2. Check if the OTP matches
            if user_otp == temp_data["otp"]:
                
                # 3. Create the user
                user = User.objects.create_user(
                    username=temp_data["email"],
                    email=temp_data["email"],
                    password=temp_data["password"],
                    is_active=True
                )
                
                Profile.objects.create(user=user, role="recruiter", is_verified=True, otp="")
                RecruiterProfile.objects.create(user=user, company_name=temp_data["company_name"], verified=True)

                # 4. Manually clean up the session BEFORE logging in
                if "temp_registration_data" in request.session:
                    del request.session["temp_registration_data"]

                # 5. Log the user in (this will flush the rest of the session safely)
                login(request, user)

                return JsonResponse({"status": "verified"})
            else:
                return JsonResponse({"status": "error", "message": "Invalid OTP code."})
                
        except Exception as e:
            # We print the error to the terminal so you can see if anything else breaks!
            print("Verification Error:", str(e)) 
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request."})

def is_user(user):
    """Check if user is a regular user"""
    return hasattr(user, 'profile') and user.profile.role == "user"


@login_required
@user_passes_test(is_recruiter, login_url='login_select')
def add_job(request):

    if request.method == "POST":
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.status = "pending"  # 🔒 IMPORTANT
            job.save()
            return redirect("recruiter_dashboard")
    else:
        form = JobPostForm()

    return render(request, "recruiter/add_job.html", {"form": form})


@login_required
@user_passes_test(is_recruiter, login_url='login_select')
def company_profile(request):
    profile = getattr(request.user, "recruiterprofile", None)
    if request.method == "POST":
        form = RecruiterProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            messages.success(request, "Company profile saved.")
            return redirect("company_profile")
    else:
        form = RecruiterProfileForm(instance=profile)

    return render(request, "recruiter/company_profile.html", {"form": form})

######################admin session###########################

def is_admin(user):
    return user.profile.role == "admin"


@login_required
@user_passes_test(is_admin, login_url='login_select')
def admin_dashboard(request):
    total_jobs = JobPost.objects.count()
    pending_jobs = JobPost.objects.filter(status="pending")
    approved_jobs = JobPost.objects.filter(status="approved").count()
    rejected_jobs = JobPost.objects.filter(status="rejected").count()
    total_users = Profile.objects.count()
    total_recruiters = RecruiterProfile.objects.count()
    total_applications = JobApplication.objects.count()

    profiles = Profile.objects.all()
    recruiters = RecruiterProfile.objects.select_related('user')
    
    # Generate visualizations
    charts = get_dashboard_stats()

    return render(request, "admins/dashboard.html", {
        "total_jobs": total_jobs,
        "pending_jobs": pending_jobs,
        "approved_jobs": approved_jobs,
        "rejected_jobs": rejected_jobs,
        "total_users": total_users,
        "total_recruiters": total_recruiters,
        "total_applications": total_applications,
        "profiles": profiles,
        "recruiters": recruiters,
        "charts": charts,
    })


@login_required
@user_passes_test(is_admin, login_url='login_select')
def review_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)

    text = None
    result = None

    # 🔍 FIXED EXTRACTION LOGIC
    if job.description and job.description.strip():
        text = job.description.strip()
    elif job.pdf:
        text = extract_text_from_pdf(job.pdf)
    elif job.job_url:
        text = extract_text_from_url(job.job_url)

    if text:
        prob, label, note = predict_scam(text)

        result = {
            "prob": round(prob, 2),
            "label": label,
            "note": note
        }

        job.scam_probability = result["prob"]
        job.scam_label = label
        job.admin_note = note
        job.save()

    if request.method == "POST":
        if "approve" in request.POST:
            job.status = "approved"
        elif "reject" in request.POST:
            job.status = "rejected"

        job.save()
        from django.urls import reverse
        return redirect(reverse("admin_dashboard") + "#reviews")

    return render(request, "admins/review_job.html", {
        "job": job,
        "result": result
    })

@login_required
@user_passes_test(is_admin, login_url='login_select')
def toggle_user_status(request, user_id):
    if request.method == "POST":
        user_to_toggle = get_object_or_404(User, id=user_id)
        # Prevent admins from blocking themselves or other admins accidentally
        if user_to_toggle.is_superuser:
            messages.error(request, "Cannot modify superuser accounts.")
        else:
            user_to_toggle.is_active = not user_to_toggle.is_active
            user_to_toggle.save()
            action = "unblocked" if user_to_toggle.is_active else "blocked"
            messages.success(request, f"User {user_to_toggle.username} has been {action}.")
    
    from django.urls import reverse
    return redirect(reverse("admin_dashboard") + "#users")

@login_required
@user_passes_test(is_admin, login_url='login_select')
def toggle_recruiter_verify(request, recruiter_id):
    if request.method == "POST":
        recruiter = get_object_or_404(RecruiterProfile, id=recruiter_id)
        recruiter.verified = not recruiter.verified
        recruiter.save()
        
        action = "verified" if recruiter.verified else "unverified"
        messages.success(request, f"Recruiter {recruiter.company_name} is now {action}.")
    
    from django.urls import reverse
    return redirect(reverse("admin_dashboard") + "#recruiters")


# JOB DETAIL PAGE
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, status="approved")
    already_applied = False
    if request.user.is_authenticated:
        already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    return render(request, "job_detail.html", {"job": job, "already_applied": already_applied})


# APPLY FOR JOB - Users only
@login_required
@user_passes_test(is_user, login_url='home')
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, status="approved")

    # Check if already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        return redirect("job_detail", job_id=job.id)

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        cover_letter = request.POST.get("cover_letter", "").strip()
        resume = request.FILES.get("resume")

        if full_name and email:
            JobApplication.objects.create(
                job=job,
                applicant=request.user,
                full_name=full_name,
                email=email,
                cover_letter=cover_letter,
                resume=resume,
            )
            return render(request, "apply_success.html", {"job": job})

    return render(request, "apply_job.html", {"job": job})


############################### ERROR HANDLERS ###############################


def page_not_found(request, exception=None):
    """Handle 404 - Page Not Found"""
    return render(request, '404.html', status=404)


def permission_denied(request, exception=None):
    """Handle 403 - Permission Denied / Access Forbidden"""
    return render(request, '403.html', status=403)


def server_error(request, exception=None):
    """Handle 500 - Server Error"""
    return render(request, '500.html', status=500)


# SEARCH (jobs + companies)
def search_jobs(request):
    q = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    category = request.GET.get("category", "").strip()
    work_mode = request.GET.get("work_mode", "").strip()
    company = request.GET.get("company", "").strip()

    jobs = JobPost.objects.filter(status="approved").select_related("recruiter__recruiterprofile")
    if q:
        jobs = jobs.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(recruiter__recruiterprofile__company_name__icontains=q)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)
    if category:
        jobs = jobs.filter(category__iexact=category)
    if work_mode:
        jobs = jobs.filter(work_mode__iexact=work_mode)
    if company:
        jobs = jobs.filter(recruiter__recruiterprofile__company_name__icontains=company)

    jobs = jobs.order_by("-created_at")

    companies = RecruiterProfile.objects.filter(verified=True)
    if company or q:
        companies = companies.filter(company_name__icontains=company or q)
    companies = companies.order_by("company_name")[:20]

    stats = {
        "count": jobs.count(),
        "companies": companies.count(),
    }

    return render(
        request,
        "search_results.html",
        {
            "jobs": jobs,
            "companies": companies,
            "query": q,
            "location_query": location,
            "category_query": category,
            "work_mode_query": work_mode,
            "company_query": company,
            "categories": JobPost.CATEGORY_CHOICES,
            "stats": stats,
        },
    )

