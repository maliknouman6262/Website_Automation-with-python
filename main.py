import os
import string
import random
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


# Function to create a random directory name
def random_directory_name(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


# Function to perform random scrolling
def load_site_and_random_scroll(driver, num_scrolls, max_pause, link):
    driver.get(link)
    time.sleep(2)
    driver.execute_script("document.body.style.zoom='40%'")
    time.sleep(2)
    try:
        agree_btn = driver.find_element(By.CSS_SELECTOR, '[mode="primary"')
        agree_btn.click()
    except:
        pass

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(num_scrolls):
        # Generate a random scroll position
        scroll_position = random.randint(0, total_height)
        print('Scroll position: ', scroll_position)
        for i in range(scroll_position):
            # Scroll to the random position
            driver.execute_script(f"window.scrollTo(0, {i});")

        # Pause for a random amount of time
        pause_duration = random.uniform(1, max_pause)
        time.sleep(pause_duration)


proxy_txt = input("Enter your proxy file path:")
links_txt = input("Enter your links file path:")

with open(proxy_txt.replace('"', ''), 'r', encoding='utf-8') as proxy_file:
    proxy_list = proxy_file.readlines()
    for PROXY in proxy_list:
        print('Selected Proxy is: ', PROXY)
        with open(links_txt.replace('"', ''), 'r', encoding='utf-8') as links_file:
            links_list = links_file.readlines()
            for link in links_list:
                try:
                    print('Selected link is: ', link)
                    options = uc.ChromeOptions()
                    # add proxy
                    options.add_argument(f'--proxy-server={PROXY}')

                    # Generate a random profile directory
                    new_profile_name = random_directory_name()

                    chrome_profile_path = r'C:\User Data'
                    options.add_argument(f"--user-data-dir={chrome_profile_path}")
                    options.add_argument(f'--profile-directory={new_profile_name}')

                    driver = uc.Chrome(options=options)
                    try:
                        driver.get('https://dnsleaktest.com/')
                        time.sleep(10)
                    except Exception as e:
                        print(e)

                    try:
                        try:
                            driver.find_element(By.CLASS_NAME, 'neterror')
                            Proxy_error = True

                            print('network error')

                        except:
                            Proxy_error = False

                        if not Proxy_error:
                            print('No error in proxy')
                            # Perform random scrolling 10 times with a maximum pause of 3 seconds
                            load_site_and_random_scroll(driver, num_scrolls=2, max_pause=2, link=link)
                        else:
                            print('Error in proxy')
                    except Exception as ex:
                        print('Error: ', ex)
                    print('close the driver..')
                    driver.close()
                    time.sleep(2)
                except:
                    pass
