from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AutoLiker:
    def __init__(self, chrome_driver_path, profile_path, profile_name="Default", website_url="https://boo.world/match"):
        """Initialize the Selenium bot with Chrome options."""
        self.chrome_driver_path = chrome_driver_path
        self.profile_path = profile_path
        self.profile_name = profile_name
        self.website_url = website_url
        self.driver = None

    def start_browser(self):
        """Start Chrome with a user profile."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"--user-data-dir={self.profile_path}")  
        chrome_options.add_argument(f"--profile-directory={self.profile_name}")  

        service = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(self.website_url)

    def click_like_button(self):
        """Find and click the like button."""
        try:
            like_button_xpath = "/html/body/div[1]/main/div[2]/div[7]/div/div[2]/div[2]/div[3]/div[4]/div"
            like_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, like_button_xpath))
            )

            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", like_button)
            time.sleep(2)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, like_button_xpath))
            )
            self.driver.execute_script("arguments[0].click();", like_button)

            print("✅ Like clicked successfully!")
            return True  # Indicates successful click

        except Exception as e:
            print(f"❌ Error clicking like: {e}")
            return False  # Indicates failure

    def run(self, num_likes=200, loop_forever=True, delay=7):
        """Run the bot to like profiles continuously or for a fixed number of times."""
        try:
            self.start_browser()
            likes_done = 0

            while loop_forever or likes_done < num_likes:
                if self.click_like_button():
                    likes_done += 1
                    print(f"👍 Liked {likes_done}/{num_likes if not loop_forever else '∞'}")
                else:
                    print("⚠️ Skipping this like due to an error.")

                time.sleep(delay)  # Wait between likes

        except Exception as e:
            print(f"❌ Critical error: {e}")

        finally:
            self.close_browser()
            print("🔄 Restarting in 10 seconds...")
            time.sleep(10)  # Short pause before restart
            self.run(num_likes, loop_forever, delay)  # Restart loop

    def close_browser(self):
        """Close the browser cleanly."""
        if self.driver:
            self.driver.quit()
            print("🚪 Browser closed.")

# 🛠️ Set up bot parameters
chrome_driver_path = r"C:\WebDriver\chromedriver-win64\chromedriver.exe"     #change path per your computer
profile_path = r"C:\Users\hp\AppData\Local\Google\Chrome\User Data"          #change path per your computer

# 🎯 Start the bot
bot = AutoLiker(chrome_driver_path, profile_path)
bot.run(num_likes=200, loop_forever=False, delay=7)
