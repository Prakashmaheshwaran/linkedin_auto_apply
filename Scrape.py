from helpers import setup_driver, random_wait, save_to_csv, remove_duplicates_from_csv, mimic_mouse_scroll, filter_unprocessed_ids
from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Collects job links by scrolling through LinkedIn job listings.
# Filters job links based on H1B sponsorship if specified.
# Returns a list of collected job links.
def collect_jobs(driver, filter_h1b=False):
    try:
        job_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header'))
        )
        print("Job container located. Starting mouse scrolling...")

        job_links = set()
        filtered_links = set()
        prev_job_count = 0

        mimic_mouse_scroll(scroll_amount=-700, duration=0.7, repetitions=5, target_element=job_container)

        while True:
            job_listings = job_container.find_elements(By.XPATH, "//li[@data-occludable-job-id]")

            for job in job_listings:
                job_url = job.find_element(By.XPATH, ".//a[@href]").get_attribute("href")
                company_info = job.get_attribute("fh-webext-company-info")

                if filter_h1b and company_info:
                    try:
                        company_data = json.loads(company_info)
                        if company_data.get("h1b_history") == 100:
                            filtered_links.add(job_url)
                    except json.JSONDecodeError:
                        print(f"Failed to parse JSON for job: {job_url}")

                job_links.add(job_url)

            # mimic_mouse_scroll(scroll_amount=-1000, duration=0.2, repetitions=5)

            if len(job_links) == prev_job_count:
                print("No new jobs loaded. Reached the end of the job container.")
                break

            prev_job_count = len(job_links)

        print(f"Total job links found: {len(job_links)}")
        return list(filtered_links) if filter_h1b else list(job_links)

    except Exception as e:
        print(f"Error while scrolling to collect jobs: {e}")
        return []


driver = setup_driver()

try:
    base_url = "https://www.linkedin.com/jobs/search/"

    total_h1b_links = []

    open(current_run_csv, "w").close()

    for role in roles:
        print(f"Starting scrape for role: {role}")
        start = 0  # Reset pagination start index for each role

        while True:
            role_query = f"&keywords={role.replace(' ', '%20')}"
            url = f"{base_url}{query_params}{role_query}&start={start}"
            print(f"Scraping page with start={start} for role '{role}'...")

            driver.get(url)

            h1b_links = collect_jobs(driver, filter_h1b=True)
            total_h1b_links.extend(h1b_links)

            save_to_csv(current_run_csv, h1b_links, mode="a")

            if len(h1b_links) < 1:
                print(f"Fewer than 1 jobs found on page with start={start}. Stopping pagination for role '{role}'.")
                break

            random_wait()
            start += 25

    remove_duplicates_from_csv(current_run_csv)
    filter_unprocessed_ids(current_run_csv, processed_id_CSV)

    print(f"Total H1B job links collected this run: {len(total_h1b_links)}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if driver:
        driver.quit()
