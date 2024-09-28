from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os

# Get the desktop path dynamically
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Initialize the WebDriver (e.g., for Chrome)
driver = webdriver.Chrome()

# Define your user details here
user_data = {
    "email": "your_email@example.com",
    "email_confirm": "your_email@example.com",  # Confirm the email
    "name": "Your Name",
    "surname": "Your Surname",
    "id_series": "AB",
    "id_number": "123456",
    "valid_from": "12.12.2023",
    "valid_until": "12.12.2025",
    "cnp": "5020924323952",
    "address": "Localitate, Street Name, 123",
    "county": "Sibiu",
    "phone": "1234567890",
    "ci_pdf": os.path.join("C:/Users/pallo/OneDrive/Desktop/", "copie_CI.pdf"),  # Copie CI from desktop
    "anaf_pdf": os.path.join("C:/Users/pallo/OneDrive/Desktop/", "certificat_ANAF.pdf"),  # ANAF Cert from desktop
    "local_tax_pdf": os.path.join("C:/Users/pallo/OneDrive/Desktop/", "certificat_taxe_locale.pdf"),  # Local tax cert
    "land_registry_pdf": os.path.join("C:/Users/pallo/OneDrive/Desktop/", "extras_carte_funciara.pdf")
    # Land registry doc
}


def click_element_function(element_locator_def):
    WebDriverWait(driver, 15).until(
        ec.element_to_be_clickable(element_locator_def))

    element_def = driver.find_element(element_locator_def[0], element_locator_def[1])
    # Scroll the button into view
    driver.execute_script("arguments[0].scrollIntoView(true);", element_def)
    time.sleep(1)
    element_def.click()


def click_and_upload(anchor_id, input_id, file_path):
    try:
        # Find and click the anchor element to activate the file input
        anchor_element = driver.find_element(By.ID, anchor_id)
        driver.execute_script("arguments[0].scrollIntoView(true);", anchor_element)
        anchor_element.click()  # Click the anchor

        # Now find the file input and upload the file
        file_input = driver.find_element(By.ID, input_id)
        file_input.send_keys(file_path)  # Upload the file

        print(f"Successfully uploaded file: {file_path}")

    except Exception as e:
        print(f"Error occurred during upload for {file_path}: {e}")


# Step 1: Open the registration page
# driver.get("https://inscrierionline.afm.ro/")
driver.get("https://www.genway.ro/simulator_casa_verde/")


def begin_site_completion(site_completion):
    # modal de inceput
    modal = driver.find_element(By.ID, "termsModal")

    if modal:
        checkbox_in_modal = modal.find_element(By.ID, "termsCheckbox")
        checkbox_in_modal.click()
        submit_modal_button = modal.find_element(By.ID, "submitTerms")
        submit_modal_button.click()

    # PAS 1

    # Fill in the email and confirm email fields
    driver.find_element(By.ID, "AdresaEmail").send_keys(user_data["email"])
    driver.find_element(By.ID, "ConfirmareAdresaEmail").send_keys(user_data["email_confirm"])

    # Pause for CAPTCHA solving (first CAPTCHA)
    input("Please solve the first CAPTCHA manually and press Enter to continue...")

    # Click the button to continue to the next step
    WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.ID, "validate-step1")))
    time.sleep(1)

    continue_button = driver.find_element(By.ID, "validate-step1")
    continue_button.click()

    # PAS 2

    element = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.ID, "Nume")))
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.send_keys(user_data["name"])

    driver.find_element(By.ID, "Prenume").send_keys(user_data["surname"])
    driver.find_element(By.ID, "SerieCI").send_keys(user_data["id_series"])
    driver.find_element(By.ID, "NumarCI").send_keys(user_data["id_number"])
    driver.find_element(By.ID, "CiValabilDeLa").send_keys(user_data["valid_from"])
    driver.find_element(By.ID, "CiValabilPanaLa").send_keys(user_data["valid_until"])
    driver.find_element(By.ID, "CNP").send_keys(user_data["cnp"])
    driver.find_element(By.ID, "Adresa").send_keys(user_data["address"])

    select_element = WebDriverWait(driver, 15).until(
        ec.visibility_of_element_located((By.ID, "Judet"))
    )
    # Create a Select object
    select = Select(select_element)

    # Select by visible text
    select.select_by_visible_text(user_data["county"])

    driver.execute_script("arguments[0].scrollIntoView(true);", select_element)

    driver.find_element(By.ID, "Telefon").send_keys(user_data["phone"])

    # Continue to the next step

    continue_button_locator = (By.ID, "validate-step2")
    time.sleep(1)
    click_element_function(continue_button_locator)

    # PAS 3

    # Upload document 1 (Copie CI)
    click_and_upload("document_1", "document_input_1", user_data["ci_pdf"])

    # Upload document 2 (Certificat ANAF)
    click_and_upload("document_2", "document_input_2", user_data["anaf_pdf"])

    # Upload document 3 (Taxe locale)
    click_and_upload("document_3", "document_input_3", user_data["local_tax_pdf"])

    # Upload document 4 (Carte funciara)
    click_and_upload("document_4", "document_input_4", user_data["land_registry_pdf"])

    # Continue to the next step
    continue_button_locator = (By.ID, "validate-step3")

    time.sleep(1)
    click_element_function(continue_button_locator)

    # PAS 4

    input_check_acord_2 = driver.find_element(By.ID, "CheckDeAcord2")
    input_check_acord_2.click()

    input_check_acord_3 = driver.find_element(By.ID, "CheckDeAcord3")
    input_check_acord_3.click()

    input_check_acord_4 = driver.find_element(By.ID, "CheckDeAcord4")
    input_check_acord_4.click()

    input_check_acord = driver.find_element(By.ID, "CheckDeAcord")
    input_check_acord.click()

    # Pause for CAPTCHA solving (second CAPTCHA)
    input("Solve the second CAPTCHA  and press Enter to finish the process...")

    # Step 4: Submit the form
    # submit_button = WebDriverWait(driver, 15).until(
    #     ec.element_to_be_clickable((By.ID, "validate-step4"))
    # )
    # driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    # submit_button.click()

    # Close the browser after successful submission
    time.sleep(5)
    driver.quit()


site_completion = 1

begin_site_completion(site_completion)
