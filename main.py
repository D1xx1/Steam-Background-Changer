from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from config import _steamLogin, _steamPassword
import datetime
import os


_steamProfileEditUrl = "https://steamcommunity.com/id/<your_profile_id>/edit/background"
_dayBackground = "https://community.fastly.steamstatic.com/economy/profilebackground/items/2861720/87fd4f413d9ad44e19cd2876a48e25b4025dce74.jpg?size=252x160"
_nightBackground = "https://community.fastly.steamstatic.com/economy/profilebackground/items/2861720/386c658bc267ea1a1973abd8f40990d66233caae.jpg?size=252x160"

_options = webdriver.ChromeOptions()
_options.add_argument("--headless")
_options.add_argument("--no-sandbox")
_options.add_argument("--disable-blink-features=AutomationControlled")

_service = Service(ChromeDriverManager().install())
_driver = webdriver.Chrome(service=_service, options=_options)
_wait = WebDriverWait(_driver, 10)

def login_steam():
    _driver.get("https://steamcommunity.com/login/home/")
    time.sleep(3)

    elements = _driver.find_elements(By.CLASS_NAME, "_2GBWeup5cttgbTw8FM3tfx")   # Находим все элементы класса формы входа
    elements[0].send_keys(_steamLogin)
    elements[1].send_keys(_steamPassword)
    elements[1].send_keys(Keys.ENTER)
    print("Logged in!")

#_189ERe_A-jhzSSRw4f2Hw _3muY5fT_nvt4gikS1bVHmO evPn26xhwAuh_SlWNY26E РЅРѕС‡РЅРѕР№
#_189ERe_A-jhzSSRw4f2Hw _3muY5fT_nvt4gikS1bVHmO РґРЅРµРІРЅРѕР№

def change_background_to_day():
    _driver.get(_steamProfileEditUrl)
    time.sleep(3)
    _element = _driver.find_element(By.CSS_SELECTOR, f'img[src*="{_dayBackground}"]')
    _element.click()
    time.sleep(3)
    print("Chosen to Day")
    

def change_background_to_night():
    _driver.get(_steamProfileEditUrl)
    time.sleep(3)
    _element = _driver.find_element(By.CSS_SELECTOR, f'img[src*="{_nightBackground}"]')
    _element.click()
    time.sleep(3)
    print("Chosen to Night")
    
    
def save_profile_background():
    _saveButton = _driver.find_element(By.CSS_SELECTOR, 'button.DialogButton.Primary')
    _saveButton.click()
    print("Applied and saved")

def get_last_change():
    if os.path.exists("last_change.log"):
        with open("last_change.log", "r") as file:
            return file.read().strip()
    return ""

def set_last_change(value):
    with open("last_change.log", "w") as file:
        file.write(value)

def check_and_change():
    now = datetime.datetime.now()
    _currentHour = now.hour
    _lastChange = get_last_change()

    if 8 <= _currentHour < 22 and _lastChange != "morning":
        change_background_to_day()
        set_last_change("morning")

    elif (_currentHour >=22 or _currentHour < 8) and _lastChange !="night":
        change_background_to_night()
        set_last_change("night")
    
    save_profile_background()
        

def check_and_change_background():
    now = datetime.datetime.now()
    _currentHour = now.hour

    try:
        with open("last_change.log", "r") as file:
            _lastChange = file.read().strip()
    except FileNotFoundError:
        _lastChange = ""

    if "morning" not in _lastChange and 8 <= _currentHour < 22:
        change_background_to_day()
        with open("last_change.log", "w"):
            file.write("morning")
        print("Changed to Day")

    elif "night" not in _lastChange and _currentHour >= 22:
        change_background_to_night()
        with open("last_change.log", "w") as file:
            file.write("night")
        print("Changed to Night")

    save_profile_background()


if __name__ == "__main__":
    login_steam()
    input("Access in mobile app and press Enter")
    # change_background_to_day()
    # input()
    while True:
        check_and_change()
        time.sleep(600)