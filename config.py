import os

# ---------------- General Settings -------------------
# Increase this if the internet is slow
additional_time = 2

default_resume_path = "./Resumes/default/master-resume.pdf"
generated_resume_path = "./Resumes/taylored-resume.pdf"

guess_count = 75
# If you need a custom resume and cover letter
RESUME_WEBHOOK_URL = "https://auto.dynoxglobal.com/webhook/cf8846b6-21c3-4c0f-9276-4dcbf4a5da8f"

# ---------------- Browser Settings -------------------
# Path to your Chrome User Data directory.
# MacOS example: "/Users/yourname/Library/Application Support/Google/Chrome"
# Windows example: r"C:\Users\yourname\AppData\Local\Google\Chrome\User Data"
# chrome_user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome") 

# Profile directory name. Use "Default" for the main profile, or "Profile 1", "Profile 2", etc.
# chrome_profile_directory = "Default"
# ---------------- Query and Roles Settings -------------------
# Add the Filter You want to apply here
query_params = (
    "?distance=100"
    "&f_LF=f_AL"
    "&f_E=1,2,3"  # Experience levels: Entry level, Associate, and Mid-Senior
    "&f_TPR=r604800"  # r86400 - 24 hours, r604800 - 1 week
    "&geoId=103644278"  # United States
    "&sortBy=DD"  # Sort by Date Posted
)

# Add The roles You want to update here
roles = [
    "Machine Learning Summer 2025 Intern",
    "AI Summer 2025 Intern",
    "Data Analyst Summer 2025 Intern",
    "Software Engineer Summer 2025 Intern",
    "Data Scientist Summer 2025 Intern",
    "Backend Developer Summer 2025 Intern",
    "Frontend Developer Summer 2025 Intern",
    "Full Stack Developer Summer 2025 Intern",
    "Cybersecurity Summer 2025 Intern",
    "Cloud Engineer Summer 2025 Intern",
    "DevOps Summer 2025 Intern",
    "Artificial Intelligence Research Intern Summer 2025",
    "Deep Learning Summer 2025 Intern",
    "Natural Language Processing Summer 2025 Intern",
    "Business Analyst Summer 2025 Intern",
    "Data Engineer Summer 2025 Intern",
    "Software Development Engineer Summer 2025 Intern",
    "Mobile App Developer Summer 2025 Intern",
    "Computer Vision Summer 2025 Intern",
    "Robotics Summer 2025 Intern",
    "Embedded Systems Summer 2025 Intern",
    "Autonomous Systems Summer 2025 Intern",
    # "Product Manager Summer 2025 Intern",
    "Web Developer Summer 2025 Intern",
    "Game Developer Summer 2025 Intern",
    "AI Product Development Intern Summer 2025",
    "AI Software Engineer Intern Summer 2025",
    "Cloud Solutions Summer 2025 Intern",
    "IT Support Summer 2025 Intern",
    "Research Scientist Summer 2025 Intern"
]

# Blocked companies and keywords
BLOCKED_COMPANY_NAMES = ["Revature", "ExampleCompany1", "ExampleCompany2"]
BLOCKED_DESCRIPTION_WORDS = [
    "internship unpaid",
    "training required",
    # "visa sponsorship not available",
    "US Citizen",
    "USA Citizen",
    "No C2C",
    "No Corp2Corp",
    "US Person Required",
    "Active SECRET Clearance Required"
]

# ---------------- User-specific Information -------------------
current_experience = 3  # User's years of experience
did_masters = True      # Whether the user holds a master's degree

# Experience and Work Information
years_of_experience = current_experience  # Default years of experience
phone_number = "6072970129"  # Contact phone number
current_city = "New York"  # Current city
state = "NY"  # State
zipcode = "13903"  # ZIP code
country = "United States"  # Country

# Cover Letter and LinkedIn Information
cover_letter = "I am excited to apply for this position. With my expertise and experience, I am confident in contributing to your team."
linkedin_summary = "Experienced software engineer with expertise in Python, Selenium automation, and backend development."

# ---------------- Proficiency Levels -------------------
default_proficiency_level = "Professional"  # General fallback proficiency level
languages = {
    "english": "Native or bilingual",  # Specific language proficiency
    "french": "Conversational"
}

# ---------------- Work Authorization -------------------
work_authorization = {
    "us_citizenship": "No",  # Authorized to work in the US
    "require_visa": "Yes",   # Requires visa sponsorship
    "disability_status": "No",  # Disability status
    "veteran_status": "No"  # Veteran status
}

# ---------------- Salary Expectations -------------------
current_ctc = "80000"  # Current salary (annual)
desired_salary = "80000"  # Desired salary (annual)
notice_period = "0 weeks"  # Notice period for availability
notice_period_weeks = "0"
notice_period_months = "0.0"

# ---------------- Personal Information -------------------
personal_info = {
    "First Name": "Prakash",
    "Middle Name": "",
    "Last Name": "Maheshwaran",
    "Full Name": "Prakash Maheshwaran",
    "Phone Country Code": "United States (+1)",  # Update with your correct code
    "Mobile Phone Number": "1234567890",
    "Street Address": "123 street ave",
    "City": "Binghamton, New York",  # Include state/province
    "State": "NY",
    "Zip": "13903",
    "Linkedin": "https://www.linkedin.com/in/prakash-maheshwaran/",
    "Website": "https://prakash.dynoxglobal.com/"
}

# ---------------- QA Section -------------------
checkboxes = {
    "driversLicence": True,  # Do you have a valid driver's license?
    "requireVisa": True,  # Will you now, or in the future, require visa sponsorship?
    "legallyAuthorized": True,  # Are you legally authorized to work in the country?
    "urgentFill": True,  # Can you start immediately?
    "commute": True,  # Are you comfortable commuting to the job's location?
    "degreeCompleted": ["High School Diploma", "Bachelor's Degree", "Master's Degree"],  # Completed degrees
    "backgroundCheck": True  # Willingness to undergo a background check
}

# ---------------- University GPA -------------------
university_gpa = 3.4

# ---------------- INDUSTRY Experience -------------------
industry = {
    "Accounting/Auditing": 0,
    "Administrative": 0,
    "Advertising": 0,
    "Analyst": 0,
    "Art/Creative": 0,
    "Business Development": 0,
    "Consulting": 0,
    "Customer Service": 0,
    "Distribution Design": 0,
    "Education": 0,
    "Engineering": 0,
    "Finance": 0,
    "General Business": 0,
    "Health Care Provider": 0,
    "Human Resources": 0,
    "Information Technology": 0,
    "Legal": 0,
    "Management": 0,
    "Manufacturing": 0,
    "Marketing": 0,
    "Public Relations": 0,
    "Purchasing": 0,
    "Product Management": 0,
    "Project Management": 0,
    "Production": 0,
    "Quality Assurance": 0,
    "Research": 0,
    "Sales": 0,
    "Science": 0,
    "Strategy/Planning": 0,
    "Supply Chain": 0,
    "Training": 0,
    "Writing/Editing": 0,
    "default": 1  # Default years for unspecified industries
}

# ---------------- TECHNOLOGY Experience -------------------
technology = {
    "python": 1,
    "selenium": 1,
    "DoD": 1,
    "Algorithms": 4,
    "default": 2  # Default years for unspecified technologies
}

# ---------------- Equal Employment Opportunity (EEO) -------------------
eeo = {
    "gender": "Male",
    "race": "Asian",
    "veteran": "None",
    "disability": "None",
    "citizenship": "Indian"
}

# ---------------- Confidence and Ratings -------------------
confidence_level = "9"  # Default rating on a scale of 1-10
