"""
Visualization utilities for the admin dashboard
Uses matplotlib, seaborn, and pandas to create charts
"""

import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from django.db.models import Count, Q
from scanner.models import JobPost, Profile, RecruiterProfile, JobApplication

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


def get_chart_image():
    """Convert matplotlib figure to base64 image string"""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close()
    return f"data:image/png;base64,{image_base64}"


def get_job_status_distribution():
    """Generate pie chart for job status distribution"""
    try:
        status_counts = JobPost.objects.values('status').annotate(count=Count('id'))
        
        statuses = [item['status'].capitalize() for item in status_counts]
        counts = [item['count'] for item in status_counts]
        
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        
        plt.figure(figsize=(8, 6))
        plt.pie(counts, labels=statuses, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Job Postings by Status', fontsize=14, fontweight='bold')
        
        return get_chart_image()
    except Exception as e:
        print(f"Error in get_job_status_distribution: {e}")
        return None


def get_scam_level_distribution():
    """Generate bar chart for scam level distribution"""
    try:
        scam_levels = JobPost.objects.values('scam_level').annotate(count=Count('id')).filter(scam_level__isnull=False)
        
        if not scam_levels:
            return None
            
        levels = [item['scam_level'] for item in scam_levels]
        counts = [item['count'] for item in scam_levels]
        
        colors_map = {
            'Low': '#2ecc71',
            'Medium': '#f39c12',
            'High': '#e74c3c'
        }
        bar_colors = [colors_map.get(level, '#95a5a6') for level in levels]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(levels, counts, color=bar_colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title('Jobs by Scam Risk Level', fontsize=14, fontweight='bold')
        plt.xlabel('Scam Level', fontsize=12)
        plt.ylabel('Number of Jobs', fontsize=12)
        plt.xticks(rotation=0)
        
        return get_chart_image()
    except Exception as e:
        print(f"Error in get_scam_level_distribution: {e}")
        return None


def get_recruiter_statistics():
    """Generate bar chart for recruiter job postings"""
    try:
        recruiters = RecruiterProfile.objects.select_related('user').annotate(
            job_count=Count('user__jobpost')
        ).filter(job_count__gt=0).order_by('-job_count')[:10]
        
        if not recruiters:
            return None
        
        companies = [r.company_name[:20] for r in recruiters]  # Truncate long names
        job_counts = [r.job_count for r in recruiters]
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(companies, job_counts, color='#3498db', edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f' {int(width)}',
                    ha='left', va='center', fontweight='bold')
        
        plt.title('Top 10 Recruiters by Job Postings', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Jobs Posted', fontsize=12)
        plt.ylabel('Company Name', fontsize=12)
        plt.tight_layout()
        
        return get_chart_image()
    except Exception as e:
        print(f"Error in get_recruiter_statistics: {e}")
        return None


def get_user_role_distribution():
    """Generate pie chart for user role distribution"""
    try:
        role_counts = Profile.objects.values('role').annotate(count=Count('id'))
        
        roles = [item['role'].capitalize() for item in role_counts]
        counts = [item['count'] for item in role_counts]
        
        colors = {
            'User': '#3498db',
            'Recruiter': '#9b59b6',
            'Admin': '#e74c3c'
        }
        pie_colors = [colors.get(role, '#95a5a6') for role in roles]
        
        plt.figure(figsize=(8, 6))
        wedges, texts, autotexts = plt.pie(counts, labels=roles, autopct='%1.1f%%', 
                                            colors=pie_colors, startangle=90)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.title('User Distribution by Role', fontsize=14, fontweight='bold')
        
        return get_chart_image()
    except Exception as e:
        print(f"Error in get_user_role_distribution: {e}")
        return None


def get_job_applications_timeline():
    """Generate line chart for job applications over time"""
    try:
        applications = JobApplication.objects.filter(
            applied_at__isnull=False
        ).extra(
            select={'date': 'DATE(applied_at)'}
        ).values('date').annotate(count=Count('id')).order_by('date')[:30]
        
        if not applications:
            return None
        
        dates = [str(app['date']) for app in applications]
        app_counts = [app['count'] for app in applications]
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, app_counts, marker='o', linewidth=2, markersize=6, color='#2ecc71')
        plt.fill_between(range(len(dates)), app_counts, alpha=0.3, color='#2ecc71')
        
        plt.title('Job Applications Timeline (Last 30 Days)', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Applications', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return get_chart_image()
    except Exception as e:
        print(f"Error in get_job_applications_timeline: {e}")
        return None


def get_job_probability_distribution():
    """Generate histogram for scam probability distribution"""
    try:
        probabilities = JobPost.objects.filter(
            scam_probability__isnull=False
        ).values_list('scam_probability', flat=True)
        
        if not probabilities:
            return None
        
        probs = list(probabilities)
        
        plt.figure(figsize=(10, 6))
        plt.hist(probs, bins=20, color='#e74c3c', edgecolor='black', alpha=0.7)
        plt.axvline(x=sum(probs)/len(probs), color='blue', linestyle='--', 
                   linewidth=2, label=f'Mean: {sum(probs)/len(probs):.2f}')
        
        plt.title('Scam Probability Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Scam Probability Score', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.legend()
        
        return get_chart_image()
    except Exception as e:
        print(f"Error in get_job_probability_distribution: {e}")
        return None


def get_dashboard_stats():
    """Get all statistics for dashboard"""
    return {
        'job_status_chart': get_job_status_distribution(),
        'scam_level_chart': get_scam_level_distribution(),
        'recruiter_chart': get_recruiter_statistics(),
        'user_role_chart': get_user_role_distribution(),
        'applications_chart': get_job_applications_timeline(),
        'probability_chart': get_job_probability_distribution(),
    }
