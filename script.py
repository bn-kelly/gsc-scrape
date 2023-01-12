import re
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from pyvirtualdisplay import Display
from constants import x_target_urls, x_sites, x_page, x_target_url_if_different, x_btn_next, x_domains


def get_num_pages(total, limit_per_page):
    return int(total / limit_per_page) if total % limit_per_page == 0 else int(total / limit_per_page + 1)


def main():
    site_url = 'https://brickfilms.com/'
    url = f'https://search.google.com/search-console/links/drilldown?resource_id={urllib.parse.quote(site_url)}&type=EXTERNAL&target=&domain='
    profile_dir = '/home/brian/.mozilla/firefox/q6h997k2.default-release-1646795451268'

    # setup display
    display = Display(visible=True, size=(1920, 1080))
    display.start()
    # init firefox profile
    profile = webdriver.FirefoxProfile(profile_dir)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    # init driver
    options = webdriver.FirefoxOptions()
    options.binary_location = GeckoDriverManager().install()
    options.headless = True
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                               firefox_profile=profile,
                               desired_capabilities=DesiredCapabilities.FIREFOX,
                               options=options)
    driver.maximize_window()

    # open initial page
    driver.get(url)

    target_urls = [el.text for el in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, x_target_urls)))]
    num_target_pages = get_num_pages(len(target_urls), 25)
    for i in range(num_target_pages):
        target_urls = [re.sub('\\s+', '', el.text) for el in
                       WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, x_target_urls)))]
        target_urls = [x for x in target_urls if x != '']

        for target_url in target_urls:
            target_page = [x for x in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, f'{x_target_urls}[contains(., "{target_url}")]'))) if x.is_displayed()]
            time.sleep(0.5)
            target_page[0].click()
            domains = [el.text for el in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, x_domains)))]
            num_domain_pages = get_num_pages(len(domains), 25)

            for j in range(num_domain_pages):
                domains = [re.sub('\\s+', '', el.text) for el in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, x_domains)))]
                domains = [x for x in domains if x != '']
                for domain in domains:
                    site = [x for x in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, f'{x_sites}[contains(., "{domain}")]'))) if x.is_displayed()]
                    time.sleep(0.5)
                    site[0].click()

                    page = re.sub('\\s+', '', WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, x_page))).text)
                    target_url_if_different = re.sub('\\s+', '', WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, x_target_url_if_different))).text)
                    print(f'Target Url: {target_url}, Linking page: {page}, Target URL (if different): {target_url_if_different}')

                    driver.back()
                    time.sleep(0.5)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, x_btn_next))).click()
            driver.back()
            time.sleep(0.5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, x_btn_next))).click()

    driver.close()


if __name__ == '__main__':
    main()
