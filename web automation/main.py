from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# --- Setup ---
driver = webdriver.Chrome()  # or use Firefox()

# --- Step 1: Open Website ---
driver.get("http://quotes.toscrape.com/login")
time.sleep(2)

# --- Step 2: Login ---
username = driver.find_element(By.NAME, "username")
password = driver.find_element(By.NAME, "password")

username.send_keys("admin")   # dummy login
password.send_keys("admin")
password.send_keys(Keys.RETURN)

time.sleep(2)

# --- Step 3: Scrape Quotes ---
quotes = []
authors = []

while True:
    quote_elements = driver.find_elements(By.CLASS_NAME, "text")
    author_elements = driver.find_elements(By.CLASS_NAME, "author")
    
    for q, a in zip(quote_elements, author_elements):
        quotes.append(q.text)
        authors.append(a.text)
    
    try:
        next_btn = driver.find_element(By.LINK_TEXT, "Next")
        next_btn.click()
        time.sleep(1)
    except:
        break

# --- Step 4: Save to CSV ---
with open("quotes.csv", "w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Quote", "Author"])
    for quote, author in zip(quotes, authors):
        writer.writerow([quote, author])

print("✅ Scraping completed. Data saved to 'quotes.csv'.")

driver.quit()
