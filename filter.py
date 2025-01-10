from helpers import *
from config import *
import re, csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Regex for extracting years of experience
re_experience = re.compile(r'[(]?\s*(\d+)\s*[)]?\s*[-to]*\s*\d*[+]*\s*year[s]?', re.IGNORECASE)

# Processes job criteria
def process_job_criteria(job_id, company_name, job_description):
    try:
        if any(blocked_name.lower() in company_name.lower() for blocked_name in BLOCKED_COMPANY_NAMES):
            print(f"Job ID {job_id}: Blocked company '{company_name}'. Skipping...")
            return False

        if any(blocked_word.lower() in job_description.lower() for blocked_word in BLOCKED_DESCRIPTION_WORDS):
            print(f"Job ID {job_id}: Blocked words found in job description. Skipping...")
            return False

        if any(keyword in job_description.lower() for keyword in ["polygraph", "clearance", "secret"]):
            print(f"Job ID {job_id}: Security clearance keywords found. Skipping...")
            return False

        found_masters = 2 if did_masters and "master" in job_description.lower() else 0
        experience_required = max(re.findall(re_experience, job_description.lower()), default=0)
        if current_experience > -1 and int(experience_required) > current_experience + found_masters:
            print(f"Job ID {job_id}: Requires {experience_required} years of experience. Skipping...")
            return False

        return True
    except Exception as e:
        print(f"Error processing job criteria for Job ID {job_id}: {e}")
        return False

# Extracts job details
def extract_job_details(driver, job_id):
    try:
        company_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'job-details-jobs-unified-top-card__company-name')]//a"))
        ).text.strip()

        job_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'job-details-jobs-unified-top-card__job-title')]//h1"))
        ).text.strip()

        job_description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'jobs-description-content__text--stretch')]"))
        ).text.strip()

        return company_name, job_title, job_description
    except Exception:
        print(f"Job ID {job_id}: Failed to extract job details.")
        return "Unknown", "Unknown", "Unknown"

# Determines apply type
def determine_apply_type(driver):
    try:
        easy_apply_button = driver.find_element(By.XPATH, ".//button[contains(@class,'jobs-apply-button') and contains(@aria-label, 'Easy')]")
        if easy_apply_button:
            return "easy"
    except Exception:
        pass

    try:
        external_apply_button = driver.find_element(By.XPATH, ".//button[contains(@class,'jobs-apply-button') and not(contains(@aria-label, 'Easy'))]")
        if external_apply_button:
            return "external"
    except Exception:
        pass

    return "none"

# Filters jobs and saves them to CSV
def filter_jobs():
    driver = setup_driver()
    try:
        job_ids = read_job_ids_from_csv(current_run_csv)

        for job_id in job_ids:
            print(f"Processing Job ID: {job_id}")
            job_url = f"https://www.linkedin.com/jobs/search/?currentJobId={job_id}"
            driver.get(job_url)
            random_wait(2, 5)

            company_name, job_title, job_description = extract_job_details(driver, job_id)

            if company_name == "Unknown" or job_description == "Unknown":
                log_processed_id(processed_id_CSV, job_id)
                continue

            if not process_job_criteria(job_id, company_name, job_description):
                log_processed_id(processed_id_CSV, job_id)
                continue

            apply_type = determine_apply_type(driver)
            if apply_type == "easy":
                with open("appliable_jobs.csv", "a", newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([job_id, job_title, company_name, job_description])
                print(f"Job ID {job_id}: Saved to Easy Apply jobs.")
            elif apply_type == "external":
                external_url = driver.current_url
                with open("manual_apply.csv", "a", newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([job_id, external_url])
                print(f"Job ID {job_id}: Saved to Manual Apply jobs.")

            log_processed_id(processed_id_CSV, job_id)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    filter_jobs()
