from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import datetime, timedelta


def get_options():
    options = Options()
    # Optional: headless mode — but more detectable
    # options.add_argument("--headless")  

    # 1. Pretend to be a real browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 2. Start maximized like a real user
    options.add_argument("--start-maximized")

    # 3. Disable automation flags (important)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # 4. Disable headless-specific features
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 5. Enable JavaScript
    # (enabled by default, but keep in mind some frameworks need this to function)

    # 6. Use real window size
    options.add_argument("--window-size=1920,1080")

    # 7. Optional: Disable extensions for simplicity
    options.add_argument("--disable-extensions")

    # 8. Optional: Disable GPU if not needed
    options.add_argument("--disable-gpu")

    # 9. Optional: Avoid sandboxing (some servers detect this too)
    options.add_argument("--no-sandbox")
    return options


def get_date_string():
    today=datetime.today()
    weekday_number=today.weekday()
    if weekday_number==5:
            today=today-timedelta(1)
    if weekday_number==6:
            today=today-timedelta(2)
    one_year_before=today-timedelta(365)
    weekday_number=one_year_before.weekday()
    if weekday_number==5:
            one_year_before=today-timedelta(1)
    if weekday_number==6:
            one_year_before=today-timedelta(2)
    formatted = today.strftime("%b %d, %Y")
    past_formatted=one_year_before.strftime("%b %d, %Y")
    return past_formatted+' - '+formatted
    # Apr 14, 2024 - Apr 14, 2025



def anti_bot(driver):
     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
     
# when a website checks: navigator.webdriver==True ?
# It will return undefined — just like a real human browser.


def get():
    path='./utils/chromedriver'
    service = Service(path) 
    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=get_options())
    anti_bot(driver)
    # driver.get('https://www.google.com/?hl=en')
    driver.get("https://finance.yahoo.com/quote/TSLA/")
    time.sleep(2)

    driver.refresh()
    time.sleep(3)
    driver.execute_script("window.scrollBy(0,100);")
    time.sleep(1)

    driver.find_element(
        By.CSS_SELECTOR,
        "a[title='Historical Data'] > span"
    ).click()
    time.sleep(2)

    driver.execute_script("window.scrollBy(0, 100);")
    time.sleep(3)

    driver.find_element(
          By.CSS_SELECTOR,
          f'div > button[title="{get_date_string()}"]'
    ).click()
    time.sleep(2)

    driver.execute_script("window.scrollBy(0,100);")
    time.sleep(1)

    driver.find_element(
          By.CSS_SELECTOR,
          "button[value='MAX']"
    ).click()
    time.sleep(1)

    
    ths=driver.find_elements(
          By.CSS_SELECTOR,
          "table > thead > tr >th"
    )
    heads=[]
    for h in ths:
          heads.append(h.text)

    # heads = [h.text for h in driver.find_elements(
    #       By.CSS_SELECTOR,
    #       "table > thead > tr > th")]

    df=pd.DataFrame(columns=heads)
    print('finish creating dataframe with its heading')

        # Initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for content to load (adjust as needed)
        time.sleep(2)
        
        # Get new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Check if page height changed
        if new_height == last_height:
            break  # No new content = done scrolling
        last_height = new_height

    print("Scrolling finished!")

    rows=driver.find_elements(
          By.CSS_SELECTOR,
          "tbody > tr"
    )
    for r in rows:
        temp=[]
        cols=r.find_elements(
            By.CSS_SELECTOR,
            "td")
          
        for c in cols:
            temp.append(c.text)
        
        if len(temp) == len(df.columns):
             df.loc[len(df)]=temp
    df=df[::-1]
    df=df.reset_index(drop=True)
    return df
        
        
                
    




    
    # search_box=driver.find_element(
    #     By.CSS_SELECTOR,
    #     "textarea[aria-label='Search']"
    # )
    # for char in "tsla yahoo finance":
    #     search_box.send_keys(char)
    #     time.sleep(0.1)
    # time.sleep(2)
    # search_box.send_keys(Keys.RETURN)
    # time.sleep(5)
    
    # driver.find_elements(

    # )
    

