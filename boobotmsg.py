from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# 🎯 Target website
website_url = "https://boo.world/match"

# 📌 ChromeDriver Path
chrome_driver_path = r"C:\WebDriver\chromedriver-win64\chromedriver.exe"

# ✅ Chrome Options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(r"--user-data-dir=C:\Users\hp\AppData\Local\Google\Chrome\User Data")  
chrome_options.add_argument("--profile-directory=Default")

# 🚀 Start WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 🌍 Open website
driver.get(website_url)

# 📝 Message to send
message_text = """Adding you to my pretty girl list

P.S You are the only one there ;)"""

def click_element(xpath, retries=3):
    """Tries to click an element using different strategies."""
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(random.uniform(1, 2))  # ⏳ Delay to avoid bot detection
            driver.execute_script("arguments[0].click();", element)  # 🔥 JavaScript Click
            print(f"✅ Clicked element at {xpath}")
            return True
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1}/{retries} failed: {e}")
            time.sleep(2)  # Wait before retrying
    return False

try:
    # 🎯 Click SVG button
    if not click_element("/html/body/div[1]/main/div[2]/div[7]/div/div[2]/div[2]/div[3]/div[5]/svg"):
        print("❌ Failed to click SVG button. Exiting.")
        driver.quit()
    
    # ⏳ Wait for input box
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div/div/div/div[4]/div[1]/textarea"))
    )

    # ✍ Type the message
    input_box.send_keys(message_text)
    time.sleep(random.uniform(1, 2))

    # 📩 Click submit button
    if not click_element("/html/body/div[3]/div/div/div/div[2]/div/div/div/div[4]/div[2]"):
        print("❌ Failed to click Submit button.")

except Exception as e:
    print(f"❌ Fatal Error: {e}")

# 🔒 Close browser
driver.quit()
print("🎉 Script finished successfully!")
