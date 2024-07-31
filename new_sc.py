from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

import imaplib
import email
from email import policy

def decode_email_body(part):
    # Decode the email body content here if necessary
    charset = part.get_content_charset()
    content_type = part.get_content_type()
    body = part.get_payload(decode=True).decode(charset, errors='replace')
    return body

def get_confirmation_code(email_id,password):
    imap = imaplib.IMAP4_SSL('pop.gmail.com')
    imap.login(email_id, password)
    imap.select('inbox')
    # Search for all emails in the inbox
    status, messages = imap.search(None, 'ALL')
    email_ids = messages[0].split()

    # Fetch the latest 10 emails
    latest_email_ids = reversed(email_ids[-10:])

    messages = []
    for e_id in latest_email_ids:
        _, msg_data = imap.fetch(e_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1], policy=policy.default)
                messages.append(msg)
    confirmation_code = None
    for message in messages:
        if 'Gravatar' in message['from'] :
            confirmation_code = message['subject'].split(" ")[0]
            return confirmation_code

    return confirmation_code

def register_and_edit_profile(email_id,email_password):
    website = "https://gravatar.com/"

    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(website)

    try:
        # Wait for and click the consent button if it appears
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, "g-signup-cta"))
        ).click()

        driver.find_element(By.CLASS_NAME, "form-text-input").send_keys("gauravthakur81711296@gmail.com")
        driver.find_element(By.CLASS_NAME, "form-button").click()

        time.sleep(4)

        confirmation_code = get_confirmation_code(email_id,email_password)
        print(confirmation_code)

        driver.find_element(By.ID, "verification-code").send_keys(confirmation_code)

        driver.find_element(By.CLASS_NAME, "form-button").click()
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'do this later')]"))
            ).click()

        except Exception as e:
            print(e)
            print("it is not")
        driver.find_element(By.CLASS_NAME, "profile-editor__navigation-item-top").click()
        driver.find_element(By.ID, "aboutMe").send_keys("<a href='https://novusaurelius.com/'> My Site </a>") 
        driver.find_element(By.CLASS_NAME, "gravatar-button-strip__vertical").click()


        # Wait for some time to ensure login process completes
        time.sleep(150)

    finally:
        driver.quit()

if __name__ == "__main__":
    email_id = 'gauravthakur81711296@gmail.com'
    email_password = 'otwe vqxk eoln opbk'
    register_and_edit_profile(email_id,email_password)
