from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def fetch_instructors(driver):
    instructors = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "authorlistTb"))
        )

        while True:
            # Scrape the current page
            table = driver.find_element(By.ID, "authorlistTb")
            rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 3:
                    info = cols[2]
                    title = info.find_element(By.TAG_NAME, "h6").text
                    full_name = info.find_element(By.TAG_NAME, "h4").find_element(By.TAG_NAME, "a").text
                    faculty_department = info.find_elements(By.TAG_NAME, "h6")[1].text if len(info.find_elements(By.TAG_NAME, "h6")) > 1 else None

                    faculty, department = "Unknown", "Unknown"
                    if faculty_department:
                        parts = faculty_department.split("/")
                        if len(parts) > 2:
                            faculty = parts[1].strip()
                            department = parts[2].strip()

                    instructors.append({
                        "title": title,
                        "full_name": full_name,
                        "faculty": faculty,
                        "department": department
                    })

            # Handle pagination
            pagination = driver.find_element(By.CLASS_NAME, "pagination")
            page_links = pagination.find_elements(By.TAG_NAME, "a")

            current_page = pagination.find_element(By.CLASS_NAME, "active")
            next_page = None
            for btn in page_links:
                if btn.text.strip().isdigit() and int(btn.text.strip()) > int(current_page.text.strip()):
                    next_page = btn
                    break

            if not next_page:
                for btn in page_links:
                    if btn.text.strip() == "»":
                        next_page = btn
                        break

            if not next_page:
                print("No more pages.")
                break

            ActionChains(driver).move_to_element(next_page).perform()
            next_page.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "authorlistTb"))
            )

    except Exception as e:
        print(f"Error fetching instructors: {e}")

    return instructors