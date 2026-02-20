from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from services.db_service import get_db

db = get_db()

driver = webdriver.Edge()
driver.get("https://gectcr.ac.in/academics#programs")

time.sleep(6)

DEPT_MAP = {
    "CSE": "Computer Science and Engineering",
    "ECE": "Electronics and Communication Engineering",
    "EEE": "Electrical and Electronics Engineering",
    "ME": "Mechanical Engineering",
    "CE": "Civil Engineering",
    "CHE": "Chemical Engineering",
    "MCA": "Department of Computer Applications",
    "PE": "Production Engineering",
    "Civil": "Civil Engineering",
    "Production": "Production Engineering",
    "Electrical": "Electrical and Electronics Engineering",
    "Electronics": "Electronics and Communication Engineering",
    "Mechanical": "Mechanical Engineering",
    "Electronics and Engineering": "Electrical and Electronics Engineering",
    "Chemical": "Chemical Engineering"
}


###################################
# -------- UG SCRAPING ----------
###################################

cards = driver.find_elements(By.XPATH, "//div[contains(text(),'B.Tech in')]")

for i in range(len(cards)):
    cards = driver.find_elements(By.XPATH, "//div[contains(text(),'B.Tech in')]")

    cards[i].click()
    time.sleep(3)

    page_text = driver.page_source

    title_match = re.search(r"B\.Tech in .+", page_text)
    intake_match = re.search(r"Intake:\s*(\d+)", page_text)
    dept_match = re.search(r"Department of (.+)", page_text)

    if title_match and intake_match and dept_match:
        title = title_match.group()
        intake = int(intake_match.group(1))
        dept_name = dept_match.group(1)

        program = {
            "program_name": title,
            "intake": intake
        }

        print("UG:", dept_name, program)

        db.departments.update_one(
            {"name": {"$regex": dept_name, "$options": "i"}},
            {"$set": {"ug_programs": [program]}}
        )

    driver.back()
    time.sleep(2)

###################################
# -------- PG SCRAPING ----------
###################################

pg_cards = driver.find_elements(By.XPATH, "//*[contains(text(),'M.Tech') or contains(text(),'Master')]")

for card in pg_cards:
    parent = card.find_element(By.XPATH, "./ancestor::div[1]")
    text = parent.text

    title_match = re.search(r"(M\.Tech in .+|Master  .+)", text)
    intake_match = re.search(r"Intake:\s*(\d+)", text)
    dept_match = re.search(r"Under (.+?) Department", text)

    if title_match and intake_match and dept_match:
        title = title_match.group()
        intake = int(intake_match.group(1))
        dept_abbr = dept_match.group(1).strip()

        dept_name = DEPT_MAP.get(dept_abbr, dept_abbr)

        program = {
            "program_name": title,
            "intake": intake
        }

        print("PG:", dept_name, program)

        db.departments.update_one(
            {"branch": {"$regex": dept_name, "$options": "i"}},
            {"$set": {"pg_programs": [program]}}
        )

driver.quit()

print("\nAll departments updated successfully!")
