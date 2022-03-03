from os import getenv
from time import sleep
from requests import get
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with

# load mail and password
load_dotenv()

# driver
driver = webdriver.Chrome()

# urls
main_url = "https://www.easyname.at/"

# data-testids
tid_cookie = "cookie-accept"
tid_login_button = "login-header-button"
tid_confirm_login_button = "login-button"

# ids
id_email_field = "emailAddress"
id_password_field = "registrationPassword"

# classes
class_cookie_modal = "overlay--cookie-modal"
class_domainnames = "domainname"
class_success_message = "feedback-message--success"

# selectors
sel_css_dns_record = "tr.entity--dns-record>td.entity__name"
sel_dns_entry_edit = "//td[@class='entity__actions']/button[2]"
sel_css_ip_field = "table.intermediate-dns-edit>tbody>tr>td>input#content"
sel_save_button = "button[type=submit]"
sel_dns_button = ".entity__field>a[href*='dns']"

# text
text_dns_entry_edit = "DNS-Eintrag editieren"

# domains
domains_to_change = "sporetec.at"
dns_entries_to_change = "testeroni"


# helpers
def get_element_by_data_testid(data_testid):
    return driver.find_element(By.CSS_SELECTOR, f"[data-testid='{data_testid}']")


def does_element_exist(element: webelement):
    try:
        if element:
            return True
        else: 
            return False
    except NoSuchElementException:
        return False


def wait_for_clickable(element: webelement, timeout=5):
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(element)
    )
    return element


def wait_for_exists(element: webelement, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            does_element_exist(element)
        )
        return element
    except:
        raise DoesNotExistError(f"Element {element} did not exist after {timeout} seconds.")


def wait_for_not_exists(element: webelement, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.staleness_of(element)
        )
        return element
    except:
        raise DoesStillExistError(f"Element {element} does still exist after {timeout} seconds.")


# classes
class DoesNotExistError(Exception):
    pass


class DoesStillExistError(Exception):
    pass


# code
driver.get(main_url)

# close cookie modal
# wait_for_exists(driver.find_element_by_class_name("overlay--cookie-modal"))
get_element_by_data_testid(tid_cookie).click()
# wait_for_not_exists(driver.find_element_by_class_name("overlay--cookie-modal"))

# login
wait_for_clickable(get_element_by_data_testid(tid_login_button)).click()
driver.find_element(By.ID, id_email_field).send_keys(getenv("MAIL"))
driver.find_element(By.ID, id_password_field).send_keys(getenv("PASSWORD"))
get_element_by_data_testid(tid_confirm_login_button).click()

# sleep(5)
wait_for_exists(driver.find_element(By.CLASS_NAME, "menu--user-id"))
# open domain dns subpage
domains = driver.find_elements(By.CLASS_NAME, class_domainnames)
for domain in domains:
    if domain.text == domains_to_change:
        driver.find_element(locate_with(By.CSS_SELECTOR, sel_dns_button).to_right_of(domain)).click()

# edit domain entry
dns_entries = driver.find_elements(By.CSS_SELECTOR, sel_css_dns_record)


for dns_entry in dns_entries:
    if dns_entries_to_change in dns_entry.text:
        driver.find_element(locate_with(By.CSS_SELECTOR, "[data-original-title*='edit']").to_right_of(dns_entry)).click()
        break

# change ip
ip = get('https://icanhazip.com/').content.decode('utf8')
driver.find_element(By.CSS_SELECTOR, sel_css_ip_field).clear()
driver.find_element(By.CSS_SELECTOR, sel_css_ip_field).send_keys(ip)

# check save confirmation
# wait_for_exists(class_success_message)

driver.close()
