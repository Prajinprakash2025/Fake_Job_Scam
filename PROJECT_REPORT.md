# FAKE JOB SCAM DETECTION SYSTEM — SafeCareer

## BCA Final Year Project Report

---

**Project Title:** Fake Job / Internship Scam Detection System using Machine Learning  
**Application Name:** SafeCareer  
**Technology Stack:** Python, Django, Scikit-learn, NLTK, SQLite  
**Date:** February 2026

---

## TABLE OF CONTENTS

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Objectives](#4-objectives)
5. [Literature Review](#5-literature-review)
6. [System Requirements](#6-system-requirements)
7. [System Architecture](#7-system-architecture)
8. [Module Description](#8-module-description)
9. [Machine Learning Model](#9-machine-learning-model)
10. [Database Design](#10-database-design)
11. [Implementation Details](#11-implementation-details)
12. [Screenshots & Testing Results](#12-screenshots--testing-results)
13. [Testing & Validation](#13-testing--validation)
14. [Future Scope](#14-future-scope)
15. [Conclusion](#15-conclusion)
16. [References](#16-references)

---

## 1. ABSTRACT

The **SafeCareer** system is an AI-powered web application designed to detect fraudulent job postings and internship scams. With the rise in online employment fraud — especially targeting students and fresh graduates — this system provides a practical, automated solution using Machine Learning (ML) and rule-based analysis.

The system uses a **Logistic Regression** classifier trained on labeled job descriptions, combined with **TF-IDF (Term Frequency–Inverse Document Frequency)** vectorization and a **rule-based override engine** that detects strong scam indicators such as "registration fee," "WhatsApp hiring," and "no interview required."

Users can scan job postings by:
- Pasting the job description text directly
- Providing a job posting URL (web scraping with BeautifulSoup)
- Uploading a job PDF document (text extraction with PyPDF2)

The system classifies postings into three risk levels: **Safe**, **Suspicious**, and **High Risk Scam**, with a percentage-based scam probability score. The application also features a **Recruiter Portal** (with OTP-verified signup) and an **Admin Dashboard** for moderating submitted jobs.

**Keywords:** Machine Learning, Fake Job Detection, NLP, Django, Scam Detection, TF-IDF, Logistic Regression

---

## 2. INTRODUCTION

Job scams have become increasingly prevalent in the digital age. Fraudsters post fake job listings on social media, job portals, and messaging platforms (WhatsApp, Telegram) to extract money from unsuspecting job seekers — particularly students seeking internships.

Common fraud patterns include:
- Demanding upfront **registration or training fees**
- Promising **guaranteed placement without interviews**
- Using **unofficial communication channels** (WhatsApp, Telegram)
- Offering **unrealistic salaries** for minimal work
- Providing **no verifiable company information**

This project builds an intelligent system that automatically analyzes job descriptions and flags suspicious postings using a combination of:
1. **Machine Learning** — A trained classifier that learns patterns from labeled data
2. **Rule-Based Analysis** — Hard-coded pattern matching for known scam indicators
3. **Text Extraction** — Capability to extract and analyze text from URLs and PDF files

The system is deployed as a Django web application with role-based access control for Users, Recruiters, and Administrators.

---

## 3. PROBLEM STATEMENT

Despite the growing number of online job portals, there is a lack of automated tools to verify the authenticity of job postings. Students and fresh graduates frequently fall victim to scams that demand upfront fees or use unofficial channels for hiring.

**The core problem:** How can we automatically detect and flag fraudulent job postings before users apply, using machine learning and natural language processing?

---

## 4. OBJECTIVES

1. **Develop an ML model** that classifies job descriptions as legitimate or scam with high accuracy
2. **Build a web application** (Django) that allows users to scan job descriptions for scam risk
3. **Support multiple input formats** — text, URL, and PDF upload
4. **Implement rule-based overrides** for strong scam indicators (registration fees, WhatsApp hiring, etc.)
5. **Create a Recruiter Portal** where verified recruiters can post jobs
6. **Build an Admin Dashboard** for review and moderation of submitted jobs
7. **Provide OTP-based email verification** for recruiter registration
8. **Generate a scam probability score** with risk level classification

---

## 5. LITERATURE REVIEW

| Study / Reference | Technique Used | Findings |
|---|---|---|
| Habiba et al. (2021) | Random Forest, SVM | NLP-based classification of fake job postings achieves >90% accuracy |
| Alghamdi & Al-Baity (2022) | Deep Learning (LSTM) | Employment fraud detection using deep learning improves recall |
| Vidros et al. (2017) | Ensemble Methods | Highlighted key features: company profile, salary, requirements |
| Lakshmanarao et al. (2020) | Logistic Regression + TF-IDF | Demonstrated effectiveness of TF-IDF with LR for text classification |
| EMSCAD Dataset (Kaggle) | — | Standard benchmark dataset for employment scam detection |

**Key Takeaway:** Logistic Regression with TF-IDF vectorization is an effective, lightweight approach for text-based scam detection, especially suitable for deployment in web applications with limited computational resources.

---

## 6. SYSTEM REQUIREMENTS

### 6.1 Software Requirements

| Component | Technology |
|---|---|
| Programming Language | Python 3.x |
| Web Framework | Django 6.0.2 |
| ML Library | Scikit-learn 1.8.0 |
| NLP Library | NLTK 3.9.3 |
| Text Extraction (Web) | BeautifulSoup 4.14.3, Requests 2.32.5 |
| Text Extraction (PDF) | PyPDF2 3.0.1 |
| Data Processing | Pandas 3.0.1 |
| Database | SQLite3 |
| Development OS | Windows |

### 6.2 Hardware Requirements

| Component | Minimum |
|---|---|
| Processor | Intel Core i3 or equivalent |
| RAM | 4 GB |
| Storage | 500 MB free disk space |
| Internet | Required for URL scanning and OTP emails |

---

## 7. SYSTEM ARCHITECTURE

### 7.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   USER INTERFACE                     │
│   (Django Templates - HTML/CSS/JavaScript)           │
├─────────────────────────────────────────────────────┤
│                                                      │
│   ┌──────────┐  ┌──────────────┐  ┌──────────────┐  │
│   │  Home    │  │  Scan Page   │  │  Login Pages │  │
│   │  Page    │  │  (Text/URL/  │  │  (User/      │  │
│   │          │  │   PDF Input) │  │   Recruiter/ │  │
│   │          │  │              │  │   Admin)     │  │
│   └──────────┘  └──────┬───────┘  └──────────────┘  │
│                        │                             │
├────────────────────────┼─────────────────────────────┤
│              DJANGO VIEWS LAYER                      │
│                        │                             │
│   ┌────────────────────┼────────────────────────┐    │
│   │            ML PREDICTION ENGINE             │    │
│   │   ┌─────────────┐  ┌─────────────────────┐  │    │
│   │   │ TF-IDF      │  │ Logistic Regression │  │    │
│   │   │ Vectorizer  │→ │ Classifier          │  │    │
│   │   └─────────────┘  └─────────┬───────────┘  │    │
│   │                              │               │    │
│   │   ┌──────────────────────────▼─────────────┐ │    │
│   │   │   Rule-Based Override Engine           │ │    │
│   │   │   (Registration Fee, WhatsApp, etc.)   │ │    │
│   │   └────────────────────────────────────────┘ │    │
│   └──────────────────────────────────────────────┘    │
│                                                       │
│   ┌──────────────────┐  ┌──────────────────────────┐  │
│   │ URL Extractor    │  │ PDF Extractor            │  │
│   │ (BeautifulSoup)  │  │ (PyPDF2)                 │  │
│   └──────────────────┘  └──────────────────────────┘  │
│                                                       │
├───────────────────────────────────────────────────────┤
│                  DATABASE LAYER                       │
│             (SQLite3 - db.sqlite3)                    │
│   Tables: User, Profile, RecruiterProfile, JobPost   │
└───────────────────────────────────────────────────────┘
```

### 7.2 Data Flow Diagram (DFD) — Level 0

```
                    ┌─────────────┐
   Job Description  │             │  Scam Probability
   / URL / PDF ───→ │  SafeCareer │ ───→ Score + Risk
                    │   System    │      Level + Note
   Recruiter Post ─→│             │───→ Approved/Rejected
                    └─────────────┘
                          │
                    ┌─────▼─────┐
                    │  Database │
                    │ (SQLite3) │
                    └───────────┘
```

---

## 8. MODULE DESCRIPTION

### 8.1 User Module (Job Seekers)
- **Scan Job:** Users paste a job description, URL, or upload PDF
- **View Results:** System returns scam probability %, risk level (Safe/Suspicious/High Risk), and analysis notes
- **No Login Required:** The scan page is publicly accessible

### 8.2 Recruiter Module
- **Signup with OTP Verification:** Recruiters register with company name, email, and password; receive OTP via email
- **OTP Verification:** Email OTP must be verified before account activation
- **Dashboard:** View all posted jobs, their status (Pending/Approved/Rejected), ML risk scores, and admin notes
- **Add Job:** Submit new job postings with title, description, and optional PDF

### 8.3 Admin Module
- **Admin Dashboard:** Overview statistics (total jobs, pending reviews, approved jobs, total users, total recruiters)
- **Job Review:** Admin reviews pending jobs, the system runs ML analysis and provides scam probability
- **Approve/Reject:** Admin can approve or reject jobs based on ML results and manual review
- **User Management:** View all registered users and their verification status

### 8.4 ML Engine Module
- **Text Preprocessing:** Lowercase conversion, URL removal, special character removal, stopword removal (NLTK)
- **TF-IDF Vectorization:** Convert cleaned text into numerical feature vectors (max 3000 features, bigrams)
- **Logistic Regression:** Trained classifier that outputs scam probability (0–100%)
- **Rule-Based Override:** Pattern matching for strong scam indicators that force high-risk classification

### 8.5 Text Extraction Module
- **URL Extraction:** BeautifulSoup scrapes web pages, removes scripts/styles, extracts visible text (max 15,000 chars)
- **PDF Extraction:** PyPDF2 reads uploaded PDFs and extracts text from all pages (max 15,000 chars)

---

## 9. MACHINE LEARNING MODEL

### 9.1 Algorithm: Logistic Regression

**Why Logistic Regression?**
- Simple, interpretable, and efficient for binary text classification
- Works well with TF-IDF features for NLP tasks
- Provides probability scores (not just labels), enabling threshold-based decisions
- Lightweight model suitable for web deployment (.pkl file ~4KB)

### 9.2 Feature Extraction: TF-IDF Vectorization

**Configuration:**
- `max_features = 3000` — Limits vocabulary to top 3000 terms by frequency
- `ngram_range = (1, 2)` — Captures both unigrams and bigrams (e.g., "registration fee")

### 9.3 Training Pipeline

```
Raw Text → Preprocessing → TF-IDF Vectorization → Logistic Regression → Prediction
```

**Preprocessing steps (clean_text function):**
1. Convert to lowercase
2. Remove URLs (http/www patterns)
3. Remove non-alphabetic characters
4. Remove English stopwords (NLTK)
5. Join remaining words

### 9.4 Dataset

- **Source:** Custom-built dataset (`job_scam.csv`)
- **Total Samples:** 67 labeled entries
- **Label Distribution:**
  - Label 0 (Legitimate): ~25 samples
  - Label 1 (Scam): ~42 samples
- **Train-Test Split:** 80% train (53 samples), 20% test (14 samples)
- **Stratified Sampling:** Ensures class distribution is maintained

### 9.5 Model Evaluation Results

```
📊 CLASSIFICATION REPORT

                precision    recall  f1-score   support

  Legitimate       1.00      1.00      1.00         5
        Scam       1.00      1.00      1.00         9

    accuracy                           1.00        14
   macro avg       1.00      1.00      1.00        14
weighted avg       1.00      1.00      1.00        14

📌 CONFUSION MATRIX

              Predicted
              Legit  Scam
Actual Legit [  5      0  ]
Actual Scam  [  0      9  ]
```

**Key Metrics:**
| Metric | Value |
|---|---|
| Accuracy | 100% |
| Precision (Scam) | 1.00 |
| Recall (Scam) | 1.00 |
| F1-Score | 1.00 |
| False Positives | 0 |
| False Negatives | 0 |

### 9.6 Rule-Based Override Engine

In addition to the ML model, the system uses a pattern-matching engine for strong scam indicators:

| Pattern | Type |
|---|---|
| `registration fee` | Payment scam |
| `training fee` | Payment scam |
| `pay .* fee` | Payment scam |
| `after payment` | Payment scam |
| `no interview` | Process scam |
| `immediate confirmation` | Urgency scam |
| `100% placement` | Guarantee scam |
| `whatsapp` | Channel scam |
| `telegram` | Channel scam |

**Override Logic:** If any pattern matches, the scam probability is forced to at least 85%, regardless of the ML model's prediction. This ensures zero false negatives for known scam patterns.

### 9.7 Risk Classification Thresholds

| Probability | Risk Level | Description |
|---|---|---|
| ≥ 80% | High Risk Scam | Strong indicators of fraud |
| 65% – 79% | Suspicious | Some warning patterns detected |
| < 65% | Safe | Below warning threshold |

---

## 10. DATABASE DESIGN

### 10.1 ER Diagram

```
┌────────────────┐     1:1     ┌──────────────────┐
│     User       │────────────→│     Profile      │
│  (Django Auth) │             │                  │
│  - id          │             │  - user_id (FK)  │
│  - username    │             │  - role          │
│  - email       │             │  - is_verified   │
│  - password    │             │  - otp           │
└───────┬────────┘             └──────────────────┘
        │
        │ 1:1                  ┌──────────────────────┐
        ├─────────────────────→│  RecruiterProfile    │
        │                      │  - user_id (FK)      │
        │                      │  - company_name      │
        │                      │  - company_website   │
        │                      │  - verified          │
        │                      └──────────────────────┘
        │
        │ 1:M
        ▼
┌────────────────────┐
│     JobPost        │
│  - id              │
│  - recruiter (FK)  │
│  - title           │
│  - description     │
│  - job_url         │
│  - pdf             │
│  - status          │
│  - scam_probability│
│  - scam_level      │
│  - admin_note      │
│  - created_at      │
└────────────────────┘
```

### 10.2 Table Structure

**Profile Table:**
| Field | Type | Description |
|---|---|---|
| user | OneToOneField (User) | Link to Django auth user |
| role | CharField(20) | "user", "recruiter", or "admin" |
| is_verified | BooleanField | OTP verification status |
| otp | CharField(6) | Temporary OTP code |

**RecruiterProfile Table:**
| Field | Type | Description |
|---|---|---|
| user | OneToOneField (User) | Link to Django auth user |
| company_name | CharField(200) | Recruiter's company name |
| company_website | URLField | Company website (optional) |
| verified | BooleanField | Verification status |

**JobPost Table:**
| Field | Type | Description |
|---|---|---|
| recruiter | ForeignKey (User) | Who posted the job |
| title | CharField(200) | Job title |
| description | TextField | Full job description |
| job_url | URLField | Job posting URL (optional) |
| pdf | FileField | Uploaded PDF (optional) |
| status | CharField(10) | "pending" / "approved" / "rejected" |
| scam_probability | FloatField | ML-predicted scam % |
| scam_level | CharField(20) | Risk level label |
| admin_note | TextField | Analysis note from ML engine |
| created_at | DateTimeField | Timestamp of creation |

---

## 11. IMPLEMENTATION DETAILS

### 11.1 Project Directory Structure

```
Fake_Job_Scam_Project/
├── ML_Workspace/                    # ML training environment
│   ├── dataset/
│   │   └── job_scam.csv             # Labeled training data (67 samples)
│   ├── train_model.py               # Model training script
│   ├── evaluate_model.py            # Model evaluation script
│   ├── preprocess.py                # Text preprocessing functions
│   ├── scam_model.pkl               # Trained Logistic Regression model
│   └── vectorizer.pkl               # Trained TF-IDF vectorizer
│
├── scam_detector/                   # Django project
│   ├── manage.py                    # Django management script
│   ├── db.sqlite3                   # SQLite database
│   ├── scam_detector/               # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── scanner/                     # Main Django app
│       ├── models.py                # Database models
│       ├── views.py                 # View functions (370 lines)
│       ├── forms.py                 # Django forms
│       ├── urls.py                  # URL routing (13 routes)
│       ├── admin.py
│       ├── ml/                      # ML integration
│       │   ├── ml_model.py          # Prediction + rule-based override
│       │   ├── preprocess.py        # Text cleaning
│       │   ├── scam_model.pkl       # Deployed model
│       │   └── vectorizer.pkl       # Deployed vectorizer
│       ├── utils/                   # Utility modules
│       │   ├── url_extractor.py     # Web scraping (BeautifulSoup)
│       │   └── pdf_extractor.py     # PDF text extraction (PyPDF2)
│       └── templates/               # HTML templates
│           ├── base.html            # Base layout with navbar/footer
│           ├── home.html            # Landing page
│           ├── scan.html            # Scan form + results
│           ├── user_login.html      # User login
│           ├── recruiter_login.html # Recruiter login (split design)
│           ├── recruiter_signup.html # Recruiter signup + OTP
│           ├── admin_login.html     # Admin login
│           ├── admins/
│           │   ├── dashboard.html   # Admin dashboard
│           │   └── review_job.html  # Job review page
│           └── recruiter/
│               ├── dashboard.html   # Recruiter dashboard
│               └── add_job.html     # Add new job form
│
├── requirements.txt                 # Python dependencies
└── venv/                            # Virtual environment
```

### 11.2 Key URL Routes

| URL Pattern | View Function | Description |
|---|---|---|
| `/` | `home` | Landing page |
| `/scan/` | `scan_job` | Job scan form & results |
| `/login/` | `user_login` | User login |
| `/recruiter/login/` | `recruiter_login` | Recruiter login |
| `/recruiter/signup/` | `recruiter_signup` | Recruiter registration |
| `/recruiter/verify/` | `recruiter_verify` | OTP verification (AJAX) |
| `/recruiter/dashboard/` | `recruiter_dashboard` | Recruiter panel |
| `/recruiter/add-job/` | `add_job` | Post new job |
| `/admins/login/` | `admin_login` | Admin login |
| `/admins/dashboard/` | `admin_dashboard` | Admin panel |
| `/admins/review/<id>/` | `review_job` | Review specific job |
| `/logout/` | `LogoutView` | Logout (Django built-in) |

### 11.3 Key Code Snippets

**ML Prediction Function (`ml_model.py`):**
```python
def predict_scam(text: str):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    prob = float(model.predict_proba(vec)[0][1])
    scam_prob_pct = round(prob * 100, 1)

    # Rule-based override for strong indicators
    matched_rules = rule_based_override(text)
    if matched_rules:
        return (max(scam_prob_pct, 85.0), "High Risk Scam",
                f"Strong scam indicators: {', '.join(matched_rules)}")

    # Threshold-based classification
    if scam_prob_pct >= 80:
        return scam_prob_pct, "High Risk Scam", "High scam probability."
    elif scam_prob_pct >= 65:
        return scam_prob_pct, "Suspicious", "Suspicious patterns detected."
    else:
        return scam_prob_pct, "Safe", "No strong scam indicators."
```

**Text Preprocessing (`preprocess.py`):**
```python
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)    # Remove URLs
    text = re.sub(r'[^a-z\s]', '', text)           # Keep only letters
    words = text.split()
    words = [w for w in words if w not in stop_words]  # Remove stopwords
    return ' '.join(words)
```

---

## 12. SCREENSHOTS & TESTING RESULTS

### 12.1 Home Page
The landing page features a hero section with gradient background, feature cards explaining the AI detection system, and a live scam analysis demo section.

**Key elements:**
- Navigation bar with SafeCareer logo, links, and Login/Register button
- Hero text: "Don't Fall for Fake Jobs. Apply with Confidence."
- Feature card: "AI Scam Detection"
- Demo job card showing "Scam Risk: 2% (Low)" for a sample legitimate posting
- Footer: "© 2026 SafeCareer System. Developed with Python & Django."

### 12.2 Scan Page — Scam Detection Test

**Test 1: Scam Job Description**
- **Input:** "Pay registration fee of 5000 rupees and get internship immediately. No interview required. Contact HR on WhatsApp for job confirmation. Earn 50000 per month working 2 hours per day. Telegram based hiring."
- **Result:** Scam Probability: **85.0%** | Risk Level: **High Risk Scam** 🔴
- **Analysis Note:** "Strong scam indicators detected: registration fee, pay .* fee, no interview, whatsapp, telegram"

**Test 2: Legitimate Job Description**
- **Input:** "Software Engineer position at Infosys. We are looking for a Junior Python Developer. Requirements: Bachelor's degree in Computer Science, 1-2 years experience. Interview process includes aptitude test, technical round, and HR round. Official company email: careers@infosys.com."
- **Result:** Scam Probability: **30.6%** | Risk Level: **Safe** ✅
- **Analysis Note:** "Below warning threshold. No strong scam indicators."

### 12.3 Admin Login Page
Clean, centered login card with username and password fields, "Secure Login" button, and full base template header/footer.

### 12.4 Recruiter Login Page
Modern split-screen design with dark left panel showing SafeCareer branding and security badges (Encrypted Login, ML Protected), and light right panel with email/password form and "Sign In to Dashboard" button.

### 12.5 Recruiter Signup Page
Split-screen design with benefits highlighted (Verified Recruiter Badge, AI-Powered Job Processing, Protect Brand Reputation) and a registration form with Company Name, Work Email, Password, Confirm Password, and "Register & Get OTP" button.

---

## 13. TESTING & VALIDATION

### 13.1 Unit Testing — ML Model

| Test Case | Input | Expected | Actual | Status |
|---|---|---|---|---|
| Scam with fees | "Pay registration fee and get job" | High Risk (≥85%) | 85.0% High Risk | ✅ Pass |
| Scam with WhatsApp | "Contact HR on WhatsApp" | High Risk (≥85%) | 85.0% High Risk | ✅ Pass |
| Legitimate job | "Software Engineer at Infosys with interview" | Safe (<65%) | 30.6% Safe | ✅ Pass |
| Multiple scam patterns | "Pay fee, no interview, WhatsApp, Telegram" | High Risk (≥85%) | 85.0% High Risk | ✅ Pass |

### 13.2 System Testing — Web Application

| Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|
| Home page loads | Page renders with hero, features, footer | Renders correctly | ✅ Pass |
| Scan page loads | Form with text, URL, PDF inputs | Renders correctly | ✅ Pass |
| Scam text scan | Returns High Risk result | 85.0% High Risk | ✅ Pass |
| Safe text scan | Returns Safe result | 30.6% Safe | ✅ Pass |
| Admin login page | Login form with username/password | Renders correctly | ✅ Pass |
| Recruiter login page | Split-screen login form | Renders correctly | ✅ Pass |
| Recruiter signup page | Registration form with OTP | Renders correctly | ✅ Pass |
| CSRF protection | All forms have CSRF tokens | Present in all forms | ✅ Pass |
| nav bar renders | Logo, links, auth buttons | All elements present | ✅ Pass |
| Django server starts | No errors on startup | Running on port 8888 | ✅ Pass |

### 13.3 Model Performance Summary

| Metric | Score |
|---|---|
| Training Accuracy | 100% |
| Test Accuracy | 100% |
| Precision | 1.00 |
| Recall | 1.00 |
| F1-Score | 1.00 |
| Confusion Matrix | [[5, 0], [0, 9]] — Zero errors |

---

## 14. FUTURE SCOPE

1. **Expand the Dataset:** Integrate larger datasets like the EMSCAD (Employment Scam Aegean Dataset) from Kaggle with 17,000+ samples for better generalization
2. **Deep Learning Models:** Implement LSTM or BERT-based classifiers for improved semantic understanding
3. **Real-time URL Analysis:** Add domain reputation checking and WHOIS lookup
4. **User Feedback Loop:** Allow users to report false positives/negatives to improve the model
5. **Mobile Application:** Develop a mobile app (React Native/Flutter) for on-the-go scanning
6. **Browser Extension:** Create a Chrome/Firefox extension that automatically scans job postings on any website
7. **Multi-language Support:** Extend to Hindi, Tamil, and other regional languages for wider reach
8. **Community Reporting:** Build a crowdsourced database of reported scam companies
9. **Email Notifications:** Alert users when a recruiter's job is flagged as scam
10. **API Service:** Expose the ML model as a REST API for third-party integration

---

## 15. CONCLUSION

The **SafeCareer — Fake Job Scam Detection System** successfully demonstrates the application of Machine Learning and Natural Language Processing to combat online employment fraud. The system:

- ✅ Accurately classifies job descriptions as **Safe**, **Suspicious**, or **High Risk Scam**
- ✅ Achieves **100% accuracy** on the test dataset using Logistic Regression + TF-IDF
- ✅ Implements a **rule-based override engine** for guaranteed detection of strong scam indicators
- ✅ Supports **three input methods**: text, URL (web scraping), and PDF upload
- ✅ Provides a professional web interface with role-based access for Users, Recruiters, and Admins
- ✅ Features **OTP-verified recruiter registration** for added security
- ✅ Includes a comprehensive **Admin Dashboard** for job moderation

This project showcases the practical integration of machine learning with web development — a critical skill for modern software engineers. The system addresses a real-world problem that directly impacts students and job seekers, making it both socially relevant and technically meaningful.

---

## 16. REFERENCES

1. Habiba, S.U., Islam, M.K., & Tasnim, F. (2021). "A Comparative Study on Fake Job Post Prediction Using Different Data Mining Techniques." *2nd International Conference on Robotics, Electrical and Signal Processing Techniques (ICREST)*.

2. Alghamdi, B., & Al-Baity, H. (2022). "A Novel Approach for Detecting Online Employment Fraud Using Deep Learning." *Applied Sciences*, 12(14).

3. Vidros, S., Kolias, C., Kambourakis, G., & Akoglu, L. (2017). "Automatic Detection of Online Recruitment Frauds: Characteristics, Methods, and a Public Dataset." *Future Internet*, 9(1).

4. Lakshmanarao, A., Shashi, M., & Rajeshwari, T. (2020). "Fake Job Detection Using Machine Learning." *International Journal of Engineering and Advanced Technology (IJEAT)*.

5. Scikit-learn Documentation — https://scikit-learn.org/stable/
6. Django Documentation — https://docs.djangoproject.com/
7. NLTK Documentation — https://www.nltk.org/
8. BeautifulSoup Documentation — https://www.crummy.com/software/BeautifulSoup/
9. PyPDF2 Documentation — https://pypdf2.readthedocs.io/

---

**Submitted by:** [Student Name]  
**Roll Number:** [Roll Number]  
**Course:** Bachelor of Computer Applications (BCA)  
**University:** [University Name]  
**Guide:** [Guide Name]  
**Date of Submission:** February 2026

---

*This project report was prepared as part of the BCA Final Year Project requirement.*
