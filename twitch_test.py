from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup Mobile Emulation ---
mobile_emulation = { "deviceName": "Pixel 2" }

options = webdriver.ChromeOptions()
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# --- Step 1: Go to Twitch ---
driver.maximize_window()  # Maximize the browser
driver.get("https://www.twitch.tv/directory")
driver.implicitly_wait(10)

# --- Step 2: Click the search icon ---
search_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@data-a-target='tw-input']")))
search_icon.click()

# --- Step 3: Input "StarCraft II" ---
search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-a-target='tw-input']")))
search_input.send_keys("StarCraft II")
search_input.click()
search_input.send_keys(Keys.RETURN)

# --- Step 4: Scroll down twice ---
for _ in range(2):
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(2)

# --- Step 5: Select one streamer ---
streamer_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/videos') or contains(@href, '/live')]"))
)
streamer_link.click()
driver.implicitly_wait(5)

# --- Step 6: Handle modal popup if exists ---
try:
    modal_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@data-a-target,'player-overlay-mature-accept')]"))
    )
    modal_button.click()
except:
    print("No modal popup appeared.")

# --- Step 7: Wait for video to load and take screenshot ---
wait.until(EC.presence_of_element_located((By.XPATH, "//video")))
time.sleep(3)  # Wait for full rendering
driver.save_screenshot("twitch_streamer_page.png")
print("Screenshot saved as 'twitch_streamer_page.png'.")


