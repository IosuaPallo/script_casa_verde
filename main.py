import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
import cv2
from easyocr import easyocr
import numpy as np
import time
import os
import pytesseract
from PIL import Image

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
    # input("Please solve the first CAPTCHA manually and press Enter to continue...")

    canvas_data = driver.execute_script("""
        var canvas = document.getElementById('canvasfirst');
        return canvas.toDataURL('image/png');
    """)
    canvas_data = canvas_data.split(',')[1]
    image_data = base64.b64decode(canvas_data)
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("preprocessed_captcha.png", image)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # Create a kernel

    # Apply morphological operations to remove thin lines (use a closing operation)
    morphed = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, kernel, iterations=1)
    cv2.imwrite("morphed_open.png", morphed)

    # Step 5: Find contours of the morphologically processed image
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask to hold the areas we want to keep
    mask = np.zeros_like(morphed)

    # Step 6: Filter contours based on width
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Remove thin or oblique lines
        if w < 6 or h < 10 or w > 80 or h > 80:
            cv2.drawContours(morphed, [contour], contourIdx=-1, color=(0,), thickness=cv2.FILLED)

    # Step 7: Combine the mask with the original image
    result = morphed

    cv2.imwrite("morphed.png", result)

    # scale_factor = 3  # Change this value to increase or decrease the size
    # new_width = int(result.shape[1] * scale_factor)
    # new_height = int(result.shape[0] * scale_factor)
    # result = cv2.resize(result, (new_width, new_height))

    # Save the processed image

    reader = easyocr.Reader(['en'])
    _, binary = cv2.threshold(result, 20, 255, cv2.THRESH_BINARY_INV)

    cv2.imwrite("cleaned_image.png", binary)

    result = reader.readtext(binary)

    captcha_text_processed = ''
    for (bbox, text, prob) in result:
        captcha_text_processed += text  # Combine detected texts

    transformations = {
        ' ': '',
        '$': 'S',  # Replace '$' with 'S'
        '€': 'E',
        '/': 'l',
        '\\': 'l',
        '>': '7',
        '*': 'x',
        "+": 'x',
        '|': 'l'
    }

    captcha_text_processed = ''.join(
        [transformations[char] if char in transformations else char for char in captcha_text_processed])

    # for index, char in enumerate(captcha_text_processed):
    #     if char==' ':

    print(f'Captcha text cleansed = {captcha_text_processed}')

    image = Image.open("cleaned_image.png")
    text = pytesseract.image_to_string(image)
    text = "".join([transformations[char] if char in transformations else char for char in text])
    print(f'Captcha text Tesseract = {text}')

    input("First capcha, press enter after....")

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
