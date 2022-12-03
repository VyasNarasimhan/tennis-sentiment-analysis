import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

tennis_player = "Rafael Nadal"

PATH = "./chromedriver"
# driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
driver = webdriver.Chrome(PATH)

driver.get("https://www.atptour.com/")

search = driver.find_element(By.ID, "controlSearch")
search.click()

query = driver.find_element(By.CLASS_NAME, "search")
query.send_keys(tennis_player)

try:
    result = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.LINK_TEXT, tennis_player))
    )
    result.click()
except:
    print("Query not found")
    driver.quit()

profile = driver.find_element(By.CLASS_NAME, "player-profile-hero-ranking")
ranking = profile.find_element(By.CLASS_NAME, "data-number")
country = profile.find_element(By.CLASS_NAME, "player-flag-code")

print(f'{tennis_player}\nRanking: {ranking.text}\nCountry: {country.text}')
