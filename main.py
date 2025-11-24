import keyboard
import json
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pyautogui
from dotenv import load_dotenv
import os

load_dotenv()

with open("settings.json", "r") as f:
    settings = json.load(f)

options = webdriver.FirefoxOptions()
options.profile = os.getenv("PROFILE_PATH") 

driver = webdriver.Firefox(options=options)

driver.get("https://monkeytype.com")

start_key = settings.get("start_key", "ctrl+alt+k")
start_delay = settings.get("start_delay", 5000)

print("Typing bot started.\nPress '" + start_key + "' to start")

keyboard.wait(start_key)

print("Starting in",start_delay/1000,"seconds")

time.sleep(start_delay/1000)

print("Started")


def read_words():
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".word.active"))
        )
        elements = driver.find_elements(By.CSS_SELECTOR, ".word:not(.typed)") 

        words = [word.text + " " for word in elements] 
        return words
    except Exception as e:
        return False

def read_active_word():
    try:
        content = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".word.active"))
        )
        
        return content.text
    except Exception as e:
        return False
    
def type_words():
    while True:
        words = read_words()
        print(words)
        print(" ")
        if words:
            pyautogui.typewrite("".join(words), interval=0.01)
        else:
            break

def type_active_word():
    while True:
        word = read_active_word()
        if word:
            pyautogui.typewrite(word + " ", interval=0.01)
        else:
            break

type_words()