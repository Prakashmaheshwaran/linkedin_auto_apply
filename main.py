from helpers import *
from config import *
import json
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apply_jobs import process_job_criteria, extract_job_details, handle_easy_apply
from job_tracker import JobTracker

# Regex for extracting years of experience
re_experience = re.compile(r'[(]?\s*(\d+)\s*[)]?\s*[-to]*\s*\d*[+]*\s*year[s]?', re.IGNORECASE)

def main():
    driver = setup_driver()
    tracker = JobTracker()
    
    try:
        base_url = "https://www.linkedin.com/jobs/search/"
        
        for role in roles:
            print(f"Starting scrape and apply for role: {role}")
            start = 0
            
            while True:
                role_query = f"&keywords={role.replace(' ', '%20')}"
                url = f"{base_url}{query_params}{role_query}&start={start}"
                print(f"Scraping page with start={start} for role '{role}'...")
                
                driver.get(url)
                random_wait()
                
                try:
                    job_container = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header'))
                    )
                    
                    mimic_mouse_scroll(scroll_amount=-700, duration=0.7, repetitions=5, target_element=job_container)
                    
                    job_listings = job_container.find_elements(By.XPATH, "//li[@data-occludable-job-id]")
                    
                    if not job_listings:
                        print("No jobs found on this page.")
                        break
                        
                    current_page_job_ids = []
                    
                    for job in job_listings:
                        try:
                            job_url = job.find_element(By.XPATH, ".//a[@href]").get_attribute("href")
                            job_id = extract_job_id(job_url)
                            if job_id:
                                current_page_job_ids.append(job_id)
                                # Add to tracker as COLLECTED if not exists
                                tracker.add_job(job_id, status="COLLECTED")
                        except Exception as e:
                            print(f"Error extracting job URL: {e}")
                            
                    print(f"Found {len(current_page_job_ids)} jobs on this page. Starting application process...")
                    
                    # Apply to jobs found on this page immediately
                    for job_id in current_page_job_ids:
                        # Check if already processed using JobTracker
                        if tracker.is_processed(job_id):
                            print(f"Job ID {job_id} already processed. Skipping.")
                            continue
                            
                        print(f"Processing Job ID: {job_id}")
                        job_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
                        driver.get(job_url)
                        random_wait(2, 5)
                        
                        company_name, job_title, job_description = extract_job_details(driver, job_id)

                        if company_name == "Unknown" or job_description == "Unknown":
                            tracker.update_job(job_id, "FAILED")
                            continue

                        suitable, reason = process_job_criteria(job_id, company_name, job_description)
                        if not suitable:
                            tracker.update_job(job_id, "SKIPPED")
                            continue

                        try:
                            easy_apply_button = driver.find_element(By.XPATH, ".//button[contains(@class,'jobs-apply-button') and contains(@aria-label, 'Easy')]")
                            if easy_apply_button:
                                success = handle_easy_apply(driver, job_id, job_url, job_details = f"job title: {job_title}\njob description:{job_description}")
                                if success:
                                    tracker.update_job(job_id, "APPLIED")
                                else:
                                    tracker.update_job(job_id, "FAILED")
                            else:
                                print(f"Job ID {job_id}: Easy Apply button not found. Skipping...")
                                tracker.update_job(job_id, "EXTERNAL")
                        except Exception as e:
                            print(f"Job ID {job_id}: Error while checking for Easy Apply: {e}")
                            tracker.update_job(job_id, "FAILED")
                            
                        # Navigate back to search page to continue (optional, but safer to just reload url in next loop iteration)
                        
                    if start > guess_count:
                        break
                        
                    start += 25
                    
                except Exception as e:
                    print(f"Error processing page: {e}")
                    break

    except Exception as e:
        print(f"An error occurred in main execution: {e}")
    finally:
        if driver:
            driver.quit()
        if tracker:
            tracker.close()

if __name__ == "__main__":
    main()
