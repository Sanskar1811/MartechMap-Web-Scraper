from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://martechmap.com/int_supergraphic")
    driver.maximize_window()
    time.sleep(8)

    log_in = driver.find_element(By.XPATH, "//button[text()='Log In']")
    log_in.click()
    time.sleep(8)

    email = driver.find_element(By.XPATH, '//input[@type="email"]')
    email.clear()
    email.send_keys("akash.padhi17@gmail.com")
    time.sleep(4)

    password = driver.find_element(By.XPATH, '//input[@type="password"]')
    password.clear()
    password.send_keys("Akash@9756.")
    time.sleep(6)

    log_in_click = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/div/div[3]/div/div/div[3]/div/button")
    log_in_click.click()

    time.sleep(20)

    # Step 2: Switch to iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"✅ Found {len(iframes)} iframe(s)")
    driver.switch_to.frame(iframes[0])
    print("✅ Switched to iframe")

    # Step 3: Wait for categories to appear
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'column_title')]")))
    print("✅ Landscape loaded inside iframe")

    # Prepare CSV file
    filename = "martechmap_data.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Company Name", "Company Website", "Source", "Sub Source"])
        
        # Write header only if file does not exist
        if not file_exists:
            writer.writeheader()

        # Scraping starts
        categories = driver.find_elements(By.CSS_SELECTOR, "div.column.category")

        for category in categories:
            try:
                source = category.find_element(By.XPATH, ".//div[contains(@class,'column_title')]/h3").text.strip()
            except:
                source = "N/A"

            subcats = category.find_elements(By.XPATH, ".//div[contains(@class,'subcat')]")

            for subcat in subcats:
                sub_source = subcat.get_attribute("title") or "N/A"
                # ❗ Skip if Sub Source is "N/A"
                if sub_source.strip() == "N/A":
                    continue
                vendors = subcat.find_elements(By.XPATH, ".//a[contains(@class,'vendor')]")

                for vendor in vendors:
                    try:
                        name = vendor.find_element(By.TAG_NAME, "img").get_attribute("alt").strip()
                        website = vendor.get_attribute("href").replace("https://", "").replace("http://", "").strip("/")
                        row = {
                            "Company Name": name,
                            "Company Website": website,
                            "Source": source,
                            "Sub Source": sub_source
                        }
                        writer.writerow(row)  # ✅ Write each row immediately
                        print(f"✅ Saved: {row}")
                    except Exception as e:
                        print("⚠️ Vendor parse error:", e)

except Exception as e:
    print("❌ Issue occurred:", e)

finally:
    driver.quit()
    input("Press Enter to Exit..! Your data has been saved in CSV file. Thank you.")
