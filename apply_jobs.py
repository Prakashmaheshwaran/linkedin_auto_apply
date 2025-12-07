from helpers import *
from config import *
import re, csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Regex for extracting years of experience
re_experience = re.compile(r'[(]?\s*(\d+)\s*[)]?\s*[-to]*\s*\d*[+]*\s*year[s]?', re.IGNORECASE)

# Processes job criteria to check if the job is suitable based on blocked names, descriptions, and experience level
def process_job_criteria(job_id, company_name, job_description):
    try:
        if any(blocked_name.lower() in company_name.lower() for blocked_name in BLOCKED_COMPANY_NAMES):
            print(f"Job ID {job_id}: Blocked company '{company_name}'. Skipping...")
            return False, "Blocked Company"

        if any(blocked_word.lower() in job_description.lower() for blocked_word in BLOCKED_DESCRIPTION_WORDS):
            print(f"Job ID {job_id}: Blocked words found in job description. Skipping...")
            return False, "Blocked Description Words"

        if any(keyword in job_description.lower() for keyword in ["polygraph", "clearance", "secret"]):
            print(f"Job ID {job_id}: Security clearance keywords found. Skipping...")
            return False, "Security Clearance Required"

        found_masters = 2 if did_masters and "master" in job_description.lower() else 0
        experience_required = max(re.findall(re_experience, job_description.lower()), default=0)
        if current_experience > -1 and int(experience_required) > current_experience + found_masters:
            print(f"Job ID {job_id}: Requires {experience_required} years of experience. Skipping...")
            return False, "Experience Too High"

        return True, "Suitable"
    except Exception as e:
        print(f"Error processing job criteria for Job ID {job_id}: {e}")
        return False, "Processing Error"


# Extracts company name, job Title and job description from the job page
def extract_job_details(driver, job_id):
    company_name, job_title, job_description = "Unknown", "Unknown", "Unknown"

    try:
        # Company Name XPath
        company_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'job-details-jobs-unified-top-card__company-name')]//a"))
        ).text.strip()
    except Exception:
        print(f"Job ID {job_id}: Company name not found.")

    try:
        # Job Title XPath
        job_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'job-details-jobs-unified-top-card__job-title')]//h1"))
        ).text.strip()
    except Exception:
        print(f"Job ID {job_id}: Job title not found.")

    try:
        # Job Description XPath
        job_description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'jobs-description-content__text--stretch')]"))
        ).text.strip()
    except Exception:
        print(f"Job ID {job_id}: Job description not found.")

    if company_name == "Unknown" and job_title == "Unknown" and job_description == "Unknown":
        print(f"Job ID {job_id}: All details missing. Skipping...")
        return None, None, None

    return company_name, job_title, job_description


# Handles Easy Apply button actions
def handle_easy_apply(driver, job_id, job_url, job_details):
    """
    Handles the complete Easy Apply process for a job while preserving logging flow.
    """
    try:
        # Step 1: Locate Easy Apply button
        easy_apply_button = driver.find_element(
            By.XPATH, ".//button[contains(@class,'jobs-apply-button') and contains(@aria-label, 'Easy')]"
        )
        if easy_apply_button:
            print(f"Job ID {job_id}: Easy Apply button found.")
            easy_apply_button.click()
            random_wait(2, 4)
            log_processed_id(processed_id_CSV, job_id)
        else:
            print(f"Job ID {job_id}: Easy Apply button not found.")
            return False

        # Step 2: Wait for modal to load
        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-easy-apply-modal"))
        )
        print(f"Job ID {job_id}: Easy Apply modal loaded successfully.")

        button_status, is_submit = handle_application_buttons(driver, modal)
        print(f"Job ID {job_id}: Button clicked - {button_status}")
        random_wait(1, 3)

        if is_submit:
            print(f"Job ID {job_id}: Application submitted successfully!")
            return True

        # Step 3: Upload Resume
        resume_path = fetch_resume_from_webhook(job_url,job_details)
        if not upload_resume(driver, resume_path):
            print(f"Job ID {job_id}: Failed to upload resume. Aborting...")
            return True
        
        print(f"Job ID {job_id}: Resume uploaded successfully.")
        random_wait(2, 4)

        # Step 4: Handle Application Buttons and Questions
        answered_questions = set()
        while True:
            try:
                # Click Next/Review/Submit buttons
                button_status, is_submit = handle_application_buttons(driver, modal)
                print(f"Job ID {job_id}: Button clicked - {button_status}")
                random_wait(1, 3)

                if is_submit:
                    print(f"Job ID {job_id}: Application submitted successfully!")
                    return True

                # Answer questions dynamically
                answer_questions(modal, answered_questions, driver)
                # print(f"Job ID {job_id}: Questions answered - {answered_questions}")

            except Exception as e:
                print(f"Job ID {job_id}: Error processing application flow: {e}")
                return False

    except Exception as e:
        print(f"Job ID {job_id}: Error during Easy Apply process: {e}")
    return False


# Main script to process job IDs
def main():
    driver = setup_driver()
    try:        
        job_ids = read_job_ids_from_csv(current_run_csv)

        for job_id in job_ids:
            print(f"Processing Job ID: {job_id}")

            base_url = "https://www.linkedin.com/jobs/search/?currentJobId="
            job_url = f"{base_url}{job_id}"
            driver.get(job_url)
            random_wait(2, 5)

            company_name, job_title, job_description = extract_job_details(driver, job_id)

            if company_name == "Unknown" or job_description == "Unknown":
                log_processed_id(processed_id_CSV, job_id)
                continue

            suitable, reason = process_job_criteria(job_id, company_name, job_description)
            if not suitable:
                log_processed_id(processed_id_CSV, job_id)
                continue

            try:
                easy_apply_button = driver.find_element(By.XPATH, ".//button[contains(@class,'jobs-apply-button') and contains(@aria-label, 'Easy')]")
                if easy_apply_button:
                    handle_easy_apply(driver, job_id, job_url, job_details = f"job title: {job_title}\njob description:{job_description}")
                else:
                    print(f"Job ID {job_id}: Easy Apply button not found. Skipping...")
                    log_processed_id(processed_id_CSV, job_id)
            except Exception as e:
                print(f"Job ID {job_id}: Error while checking for Easy Apply: {e}")
                log_processed_id(processed_id_CSV, job_id)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
