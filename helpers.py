import csv, re, random, pyautogui, time, os, requests
import numpy as np
from time import sleep
from config import *
from helpers import *
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException)

# Sets up and returns a Chrome driver configured with a specified profile
# The driver bypasses automation detection and enables options for smooth execution
def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
    options.add_argument(f"--profile-directory={chrome_profile_directory}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4]});
            """
        },
    )
    print("Driver has been successfully initiated with Profile 3.")
    return driver

# Pauses execution for a random amount of time between min_time and max_time
# Includes small optional jitter for human-like delays and adds configurable additional time
def random_wait(min_time=1, max_time=3, jitter=True):
    delay = np.random.uniform(min_time, max_time)

    if jitter:
        delay += np.random.uniform(-0.2, 0.2)  # Add jitter for variability

    delay += additional_time  # Add configurable additional time
    delay = max(min_time, delay)  # Ensure delay doesn't drop below min_time

    print("Sleeping for:", delay)
    time.sleep(delay)

# Mimics human-like mouse scrolling using pyautogui
# Scrolls a specified amount, with optional cursor positioning and variable delays
def mimic_mouse_scroll(scroll_amount=-500, duration=0.5, repetitions=10, target_element=None):
    try:
        if target_element:
            location = target_element.location
            size = target_element.size
            x = location['x'] + size['width'] // 2
            y = location['y'] + size['height'] // 2
            
            pyautogui.moveTo(x, y + 300, duration=random.uniform(0.2, 0.5))
            random_wait(0.5, 1.0)

        for i in range(repetitions):
            scroll_variation = random.randint(-50, 50)
            pyautogui.scroll(scroll_amount + scroll_variation)
            time.sleep(duration + random.uniform(-0.1, 0.2))
            
            if i % 5 == 0 and i > 0:
                random_wait(1, 2)

    except Exception as e:
        print(f"Error during mouse scrolling: {e}")

# Saves extracted job IDs to a CSV file while ensuring duplicates are avoided
def save_to_csv(file_path, data, mode="a"):
    if not data:
        print("No data to save to CSV. Skipping...")
        return

    try:
        extracted_ids = [extract_job_id(item) for item in data if extract_job_id(item)]

        if not extracted_ids:
            print("No valid job IDs to save.")
            return

        with open(file_path, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for job_id in set(extracted_ids):  # Avoid duplicates using a set
                writer.writerow([job_id])

        print(f"Data successfully saved to {file_path}. Total saved: {len(extracted_ids)}")
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")

# Removes duplicate entries from a CSV file and keeps only unique rows
def remove_duplicates_from_csv(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            rows = file.readlines()

        unique_rows = list(dict.fromkeys(rows))  # Remove duplicates while preserving order

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(unique_rows)

        print(f"Duplicates removed from {file_path}. Total unique entries: {len(unique_rows)}")
    except FileNotFoundError:
        print(f"File {file_path} not found. Nothing to clean.")
    except Exception as e:
        print(f"Error cleaning duplicates in {file_path}: {e}")

# Reads job IDs from a CSV file and returns a list of valid job IDs
def read_job_ids_from_csv(file_path):
    job_ids = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip():  # Ensure the row is not empty
                    job_ids.append(row[0].strip())
                else:
                    print(f"Skipped invalid or empty row: {row}")
        print(f"Loaded {len(job_ids)} valid job IDs from {file_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the file path.")
    except Exception as e:
        print(f"Error reading job IDs from {file_path}: {e}")
    return job_ids

# Log processed job IDs into a CSV file
def log_processed_id(file_path,job_id):
    with open(file_path, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([job_id])
# Filter out already processed job IDs from the current run list
def filter_unprocessed_ids(current_run_list_csv, processed_id_csv):
    try:
        with open(processed_id_csv, "r", encoding="utf-8") as processed_file:
            processed_reader = csv.reader(processed_file)
            processed_ids = {row[0] for row in processed_reader}

        with open(current_run_list_csv, "r", encoding="utf-8") as current_file:
            current_reader = csv.reader(current_file)
            current_ids = [row[0] for row in current_reader if row]

        unprocessed_ids = [job_id for job_id in current_ids if job_id not in processed_ids]

        with open(current_run_list_csv, "w", newline='', encoding="utf-8") as current_file:
            writer = csv.writer(current_file)
            for job_id in unprocessed_ids:
                writer.writerow([job_id])

        print(f"Filtered current run list. Remaining unprocessed IDs: {len(unprocessed_ids)}")

    except Exception as e:
        print(f"Error filtering unprocessed IDs: {e}")
        
# Extracts the job ID (number) from a LinkedIn job URL
def extract_job_id(url):
    try:
        match = re.search(r'view/(\d+)/', url)
        if match:
            return match.group(1)
        print(f"No job ID found in URL: {url}")
        return None
    except Exception as e:
        print(f"Error extracting job ID from URL: {url} | Error: {e}")
        return None
    
# Handles the progression through application buttons like 'Next', 'Review', or 'Submit Application'.
def handle_application_buttons(driver, modal):
    try:
        # Check for the "Submit application" button
        try:
            submit_button = modal.find_element(By.XPATH, ".//button[@aria-label='Submit application' and contains(@class, 'artdeco-button--primary')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            print("found submit button now sleeping.. since it is a testing run we dont want to submit the application")
            submit_button.click()
            print("Clicked 'Submit Application'.")
            return "Submit", True
        except NoSuchElementException:
            pass

        # Check for the "Review" button
        try:
            review_button = modal.find_element(By.XPATH, ".//button[@aria-label='Review your application' and contains(@class, 'artdeco-button--primary')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", review_button)
            review_button.click()
            print("Clicked 'Review'.")
            return "Review", False
        except NoSuchElementException:
            pass

        # Check for the "Next" button
        try:
            next_button = modal.find_element(By.XPATH, ".//button[contains(@aria-label, 'Continue to next step') or contains(@class, 'artdeco-button--primary')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            next_button.click()
            print("Clicked 'Next'.")
            return "Next", False
        except NoSuchElementException:
            pass

        print("No relevant button found in the modal.")
        return "No Button Found", False

    except ElementClickInterceptedException as e:
        print(f"Error clicking button: {e}")
        return "Error", False

# Uploads a resume to the specified input field in the HTML structure.  
def upload_resume(driver, resume_path: str) -> bool:
    try:
        # Ensure the resume file exists
        absolute_path = os.path.abspath(resume_path)
        if not os.path.exists(absolute_path):
            print(f"File not found: {absolute_path}")
            return False

        # Locate the input field dynamically using XPath
        file_input = driver.find_element(
            By.XPATH,
            "//*[contains(@id, 'jobs-document-upload-file-input-upload-resume-urn:li:fsu_jobApplicationFileUploadFormElement:urn:li:jobs_applyformcommon_easyApplyFormElement') and contains(@id, ',document')]"
        )
        file_input.send_keys(absolute_path)
        print(f"Resume uploaded successfully: {absolute_path}")
        return True

    except Exception as e:
        print(f"Error uploading resume: {e}")
        return False
    
# Sends the job description and page URL to the webhook and downloads the returned resume.
def fetch_resume_from_webhook(page_url: str, job_description: str) -> str:
    payload = {"htmlBody": job_description, "pageUrl": page_url}
    retries = 3

    for _ in range(retries):
        try:
            response = requests.post(RESUME_WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                with open(generated_resume_path, "wb") as file:
                    file.write(response.content)
                print(f"Resume downloaded and saved to {generated_resume_path}")
                return generated_resume_path
            else:
                print(f"Webhook error: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching resume: {e}. Retrying...")
            time.sleep(2)
    return default_resume_path
    
# Function to safely locate elements using XPath
def try_xp(element, xpath, raise_exception=True):
    try:
        return element.find_element(By.XPATH, xpath)
    except NoSuchElementException as e:
        if raise_exception:
            raise e
        return None

# Function to answer common questions for Easy Apply
def answer_common_questions(label: str, answer: str) -> str:
    if 'sponsorship' in label or 'visa' in label: answer = "yes"
    return answer

# Handles answering all types of Easy Apply questions.
# Dynamically supports dropdowns, radio buttons, checkboxes, and text fields using config parameters.
# Does not overwrite answers if already filled.
def answer_questions(modal: WebElement, questions_list: set, driver) -> set:

    actions = ActionChains(driver)
    all_questions = modal.find_elements(By.XPATH, ".//div[@data-test-form-element]")

    print("\n--- Debug: Printing All Questions ---")
    for idx, question in enumerate(all_questions):
        print(f"Question {idx + 1}: {question.text.strip()}")

        # 1. Handle Dropdown (Select) Questions
        select = try_xp(question, ".//select", False)
        if select:
            label = try_xp(question, ".//label", False).text.lower() if try_xp(question, ".//label", False) else "Unknown"
            select_element = Select(select)
            current_value = select_element.first_selected_option.text.strip()

            if current_value and current_value.lower() != "select an option":
                print(f"Dropdown '{label}' already filled with '{current_value}'. Skipping.")
            else:
                answer = "Yes"
                if "proficiency" in label:
                    answer = languages.get("english", default_proficiency_level)
                elif "experience" in label:
                    key = next((k for k in industry if k.lower() in label), None)
                    if key:
                        answer = str(industry.get(key, industry["default"]))
                    else:
                        tech_key = next((k for k in technology if k.lower() in label), None)
                        answer = str(technology.get(tech_key, technology["default"]))
                try:
                    select_element.select_by_visible_text(answer)
                    print(f"Selected '{answer}' for dropdown '{label}'")
                    questions_list.add((label, answer, "select"))
                except Exception as e:
                    print(f"Error selecting dropdown '{label}': {e}. Waiting for intervention...")
                    sleep(5)  # Wait for human intervention
            continue

        # 2. Handle Radio Button Questions
        radio_buttons = question.find_elements(By.XPATH, './/fieldset//input[@type="radio"]')
        if radio_buttons:
            label = try_xp(question, ".//span", False).text.lower() if try_xp(question, ".//span", False) else "Unknown"
            selected = any(button.is_selected() for button in radio_buttons)

            if selected:
                print(f"Radio question '{label}' already answered. Skipping.")
            else:
                answer = "Yes"
                if "citizenship" in label: answer = eeo.get("citizenship", "Yes")
                elif "gender" in label: answer = eeo.get("gender", "Prefer not to say")
                elif "disability" in label: answer = eeo.get("disability", "No")
                elif "veteran" in label: answer = eeo.get("veteran", "No")
                elif "visa" in label: answer = "Yes" if checkboxes.get("requireVisa", False) else "No"

                for button in radio_buttons:
                    button_label = try_xp(question, f".//label[@for='{button.get_attribute('id')}']", False).text.lower()
                    if answer.lower() in button_label:
                        actions.move_to_element(button).click().perform()
                        print(f"Selected '{answer}' for radio question '{label}'")
                        questions_list.add((label, answer, "radio"))
                        break
            continue

        # 3. Handle Checkboxes
        checkbox = try_xp(question, ".//input[@type='checkbox']", False)
        if checkbox:
            label = try_xp(question, ".//label", False).text.lower() if try_xp(question, ".//label", False) else "Unknown"
            if checkbox.is_selected():
                print(f"Checkbox '{label}' already checked. Skipping.")
            else:
                checked = False
                if "driver's licence" in label and checkboxes.get("driversLicence", False): checked = True
                elif "background check" in label and checkboxes.get("backgroundCheck", False): checked = True
                elif "commute" in label and checkboxes.get("commute", False): checked = True
                elif "legally authorized" in label and checkboxes.get("legallyAuthorized", True): checked = True

                if checked:
                    checkbox.click()
                    print(f"Checked '{label}' checkbox")
                    questions_list.add((label, "Checked", "checkbox"))
            continue

        # 4. Handle Text Inputs
        text_input = try_xp(question, ".//input[@type='text']", False)
        if text_input:
            current_value = text_input.get_attribute("value").strip()
            label = try_xp(question, ".//label", False).text.lower() if try_xp(question, ".//label", False) else "Unknown"

            if current_value:
                print(f"Text input '{label}' already filled with '{current_value}'. Skipping.")
            else:
                answer = "2"  # Default fallback
                if "experience" in label:
                    key = next((k for k in industry if k.lower() in label), None)
                    if key:
                        answer = str(industry.get(key, industry["default"]))
                    else:
                        tech_key = next((k for k in technology if k.lower() in label), None)
                        answer = str(technology.get(tech_key, technology["default"]))
                elif "gpa" in label: answer = str(university_gpa)
                elif "phone" in label: answer = personal_info.get("Mobile Phone Number", "1234567890")
                elif "city" in label: answer = personal_info.get("City", "New York")
                elif "state" in label: answer = personal_info.get("State", "NY")
                elif "zip" in label: answer = personal_info.get("Zip", "10001")

                text_input.clear()
                text_input.send_keys(answer)
                print(f"Entered '{answer}' for text input '{label}'")
                questions_list.add((label, answer, "text"))
            continue

    return questions_list