from django import forms
from .models import JobPost, RecruiterProfile


class ScanForm(forms.Form):
    description = forms.CharField(required=False)
    job_url = forms.URLField(required=False)
    pdf_file = forms.FileField(required=False, help_text="Upload job PDF")

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ["company_name", "company_website", "company_description", "company_logo"]
        widgets = {
            "company_name": forms.TextInput(attrs={"placeholder": "e.g. Acme Corp", "class": "form-control"}),
            "company_website": forms.URLInput(attrs={"placeholder": "https://www.example.com", "class": "form-control"}),
            "company_description": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe your company and its mission...", "class": "form-control"}),
            "company_logo": forms.FileInput(attrs={"class": "form-control"})
        }

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            "title",
            "category",
            "company_size",
            "work_mode",
            "experience_level",
            "location",
            "job_type",
            "salary_range",
            "description",
            "job_url",
            "pdf",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Senior Software Engineer"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "company_size": forms.Select(attrs={"class": "form-control"}),
            "work_mode": forms.Select(attrs={"class": "form-control"}),
            "experience_level": forms.Select(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"placeholder": "e.g. Remote, or New York, NY"}),
            "salary_range": forms.TextInput(attrs={"placeholder": "e.g. $100k - $120k"}),
            "job_url": forms.URLInput(attrs={"placeholder": "Link to the official job posting (optional)"}),
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Paste the full job description here..."}),
        }
