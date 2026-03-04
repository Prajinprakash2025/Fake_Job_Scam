from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("choose-login/", views.login_select, name="login_select"),

    # USER
    path("scan/", scan_job, name="scan_job"),
    path("search/", views.search_jobs, name="search_jobs"),
    path("login/", user_login, name="user_login"),
    path("signup/", views.user_signup, name="user_signup"),
    path("job/<int:job_id>/", views.job_detail, name="job_detail"),
    path("job/<int:job_id>/apply/", views.apply_job, name="apply_job"),
    path("profile/", views.user_profile, name="user_profile"),

    # RECRUITER

    path("recruiter/dashboard/", recruiter_dashboard, name="recruiter_dashboard"),
    path("recruiter/signup/", recruiter_signup, name="recruiter_signup"),
    path("recruiter/verify/", recruiter_verify, name="recruiter_verify"),

    path('recruiter/login/', views.recruiter_login, name='recruiter_login'),
    path("recruiter/add-job/", add_job, name="add_job"),
    path("recruiter/company/", company_profile, name="company_profile"),
    path("recruiter/edit-job/<int:job_id>/", edit_job, name="edit_job"),
    path("recruiter/delete-job/<int:job_id>/", delete_job, name="delete_job"),
    path("recruiter/bulk-delete-jobs/", bulk_delete_jobs, name="bulk_delete_jobs"),


    # ADMIN
    path("admins/login/", admin_login, name="admin_login"),
    path("admins/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admins/review/<int:job_id>/", review_job, name="review_job"),
    path("admins/user/<int:user_id>/toggle-status/", views.toggle_user_status, name="toggle_user_status"),
    path("admins/recruiter/<int:recruiter_id>/toggle-verify/", views.toggle_recruiter_verify, name="toggle_recruiter_verify"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),




]
