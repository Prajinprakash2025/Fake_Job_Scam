import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scam_detector.settings')
django.setup()

from django.contrib.auth.models import User
from scanner.models import JobPost

user = User.objects.filter(email='dsoft@gmail.com').first()
if not user:
    user = User.objects.first()

job_titles = [
    "Software Engineer II",
    "Data Scientist - Remote",
    "Senior Frontend Developer (React)",
    "Backend Developer (Django/Python)",
    "DevOps Engineer",
    "Product Manager",
    "UI/UX Designer",
    "Machine Learning Engineer",
    "QA Automation Engineer",
    "Cloud Architecture Consultant"
]

descriptions = [
    "We are looking for a skilled professional with 3+ years of experience in the required tech stack. Great compensation and benefits.",
    "Join our fast-paced startup building next-gen AI tools for the healthcare sector. Remote work options available.",
    "Seeking a passionate frontend developer to build sleek user interfaces. Must have deep knowledge of React and modern CSS.",
    "Architect and build robust web APIs. Experience with Django, PostgreSQL, and Redis is highly preferred.",
    "Looking for a candidate with strong experience in CI/CD, AWS/GCP, Kubernetes, and Terraform. Competitive salary offered.",
    "Drive product development from ideation to launch. Work closely with engineering, design, and marketing teams.",
    "We need a creative designer with an impressive portfolio. Must have experience with Figma and user research methodologies.",
    "Train and deploy ML models into production. Familiarity with PyTorch or TensorFlow, and MLOps tools is required.",
    "Ensure top-notch quality for our web and native apps. Experience with Playwright or Cypress is a huge plus.",
    "Consult top-tier clients on migrating their monoliths to the cloud. AWS certifications are mandatory."
]

scam_probs = [10.5, 8.2, 5.1, 75.3, 12.0, 95.8, 15.6, 9.4, 45.2, 82.5]
scam_levels = ["Low", "Low", "Low", "High", "Low", "High", "Low", "Low", "Medium", "High"]

statuses = ["approved", "approved", "approved", "pending", "approved", "rejected", "approved", "approved", "pending", "rejected"]

count = 0
for i in range(10):
    JobPost.objects.create(
        recruiter=user,
        title=job_titles[i],
        description=descriptions[i],
        job_url="https://example.com/job/" + str(i+1),
        status=statuses[i],
        scam_probability=scam_probs[i],
        scam_level=scam_levels[i],
        admin_note="Automatically generated for testing."
    )
    count += 1

print(f"Successfully added {count} sample jobs for user {user.username}.")
