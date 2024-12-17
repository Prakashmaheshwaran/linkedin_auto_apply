# **LinkedIn Job Apply Automation**

This project automates job scraping and job applications on LinkedIn. It utilizes Selenium for browser automation, handles Easy Apply workflows, and applies dynamic filtering based on user-configurable criteria.

---

## **Table of Contents**

1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [Requirements](#requirements)  
4. [Setup](#setup)  
5. [Usage](#usage)  
6. [Configuration](#configuration)  
7. [Key Features](#key-features)  
8. [Error Handling](#error-handling)  
9. [Known Issues](#known-issues)  
10. [Future Improvements](#future-improvements)

---

## **Overview**

The LinkedIn Job Apply Automation project helps in:  
1. Scraping job postings from LinkedIn based on predefined roles, filters, and locations.  
2. Processing each job post to determine eligibility (filtering blocked companies, keywords, and experience requirements).  
3. Automating the **Easy Apply** process or logging **External Apply** links for manual applications.

---

## **Project Structure**

```
LinkedIn-Apply-Automation/
├── config.py         # Contains user settings and job search configurations
├── helpers.py        # Utility functions for automation
├── Scrape.py         # Script to scrape job links
├── apply_jobs.py     # Automates the application process
├── Resumes/          # Directory for resumes (default and generated)
├── CSV/              # Stores job links and processed IDs
└── README.md         # Project documentation
```

---

## **Requirements**

- Python 3.8 or higher  
- Google Chrome Browser  
- Selenium  
- undetected_chromedriver  
- Additional Python packages: `numpy`, `requests`, `pyautogui`  

---

## **Setup**

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/linkedin-apply-automation.git
   cd linkedin-apply-automation
   ```

2. Install the required libraries:  
   ```bash
   pip install -r requirements.txt
   ```

3. Update `config.py` with your settings:  
   - Preferred roles, experience levels, and locations.  
   - User-specific details like contact information and LinkedIn profile.  
   - Resume paths and other configurations.  

4. Set up a Chrome profile:  
   - Modify `setup_driver()` in `helpers.py` to include your Chrome profile path.

---

## **Usage**

### **1. Scrape Job Listings**  
Run the `Scrape.py` script to collect job IDs based on search criteria:  
```bash
python Scrape.py
```  
Output:  
- The script saves filtered job links in `CSV/collected_links_run.csv`.  

### **2. Automate Job Applications**  
Run the `apply_jobs.py` script to apply for the jobs:  
```bash
python apply_jobs.py
```  
Output:  
- The script processes the jobs and automates **Easy Apply** applications.  
- External job URLs are saved to `CSV/external_URL.csv`.  

---

## **Configuration**

The `config.py` file allows you to customize all settings:  

### **General Settings**
- **`additional_time`**: Extra delay for slow networks.  
- **`current_run_csv`**: File path to store current job links.  

### **Query Settings**
- **`query_params`**: Filters for LinkedIn job search (distance, experience, etc.).  
- **`roles`**: Job titles to search for (e.g., `Machine Learning Intern`, `Python Developer`).  

### **Filters**
- **`BLOCKED_COMPANY_NAMES`**: Companies to exclude.  
- **`BLOCKED_DESCRIPTION_WORDS`**: Keywords to skip job descriptions.  

### **User Details**
- Personal information, resume path, years of experience, work authorization, and salary expectations.  

---

## **Key Features**

1. **Scraping LinkedIn Jobs**  
   - Mimics human-like scrolling and interaction to collect job listings.  
   - Supports pagination to fetch jobs across multiple pages.

2. **Dynamic Filtering**  
   - Filters blocked companies, keywords, unpaid internships, and high-experience roles.

3. **Easy Apply Automation**  
   - Detects and automates the **Easy Apply** process.  
   - Uploads resumes dynamically based on the job description via a webhook.

4. **External Apply Logging**  
   - Saves links for jobs that redirect to external applications.

5. **Resume Customization**  
   - Uses a webhook to fetch tailored resumes for each application.

---

## **Error Handling**

- **Network Errors**: The script retries connections automatically.  
- **Missing Elements**: If LinkedIn page structure changes, missing elements are logged and skipped.  
- **Duplicate IDs**: Duplicate job IDs are automatically removed from CSV files.

---

## **Known Issues**

1. LinkedIn may temporarily block your account if excessive automation is detected.  
   **Solution**: Use `undetected_chromedriver` and human-like delays (`random_wait`).  
2. External apply processes are logged but not automated.  

---

## **Future Improvements**

1. Add support for **cover letter customization**.  
2. Automate **external applications** where possible.  
3. Enhance error handling for CAPTCHA or multi-step applications.

---

## **Author**

**Prakash Maheshwaran**  
- LinkedIn: [Prakash Maheshwaran](https://www.linkedin.com/in/prakash-maheshwaran/)  
- Portfolio: [prakash.dynoxglobal.com](https://prakash.dynoxglobal.com/)  

---

### **Disclaimer**  
This tool is for personal use only. Automating applications on LinkedIn may violate their terms of service. Use responsibly.

--- 
