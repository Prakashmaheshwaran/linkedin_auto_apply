# Environment Setup Guide

## Quick Setup (Recommended)

### 1. Create and Activate Conda Environment
```bash
# Create environment with Python 3.10
conda create --name linkedin-auto-apply python=3.10 -y

# Activate the environment
conda activate linkedin-auto-apply
```

### 2. Install Dependencies
```bash
# Install essential dependencies only (recommended)
pip install -r requirements.txt

# OR install all dependencies for exact reproduction
pip install -r requirements-full.txt
```

### 3. Verify Installation
```bash
python -c "
import selenium, undetected_chromedriver, pyautogui, requests, numpy
print('✅ All dependencies working!')
"
```

## Requirements Files Explained

### `requirements.txt` (Essential Only)
- Contains only the core dependencies your project directly uses
- Cleaner and easier to maintain
- **Recommended for most users**

### `requirements-full.txt` (Complete Environment)
- Contains all installed packages with exact versions
- Use this for exact environment reproduction
- Good for debugging dependency conflicts

## Dependencies Overview

| Package | Purpose | Files Used In |
|---------|---------|---------------|
| `selenium` | Web browser automation | All Python files |
| `undetected-chromedriver` | Bypass bot detection | helpers.py |
| `pyautogui` | Mouse/keyboard automation | helpers.py |
| `requests` | HTTP requests to webhook | helpers.py |
| `numpy` | Random number generation | helpers.py |

## Usage Commands

```bash
# Activate environment
conda activate linkedin-auto-apply

# Run your scripts
python apply_jobs.py
python Scrape.py
python filter.py

# Deactivate when done
conda deactivate
```

## Troubleshooting

### Chrome Browser Issues
Make sure you have Google Chrome installed and update the profile path in `config.py`:
```python
chrome_user_data_dir = r"YOUR_CHROME_USER_DATA_PATH"
chrome_profile_directory = "YOUR_PROFILE_NAME"
```

### PyAutoGUI on macOS
Grant accessibility permissions to your terminal/IDE for PyAutoGUI to work:
1. System Preferences → Security & Privacy → Privacy → Accessibility
2. Add your terminal/IDE application

### Environment Recreation
If you need to recreate the environment elsewhere:
```bash
# Export current environment
pip freeze > requirements-snapshot.txt

# Recreate on another machine
conda create --name linkedin-auto-apply python=3.10 -y
conda activate linkedin-auto-apply
pip install -r requirements-snapshot.txt
```

## System Requirements
- Python 3.10+
- Google Chrome browser
- macOS/Windows/Linux
- At least 2GB free disk space 