import base64

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


class SiteAutoComplete:

    def __init__(self, user_data, driver):
        self.user_data = user_data
        self.driver = driver

    def click_element_function(self, element_locator_def):
        WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable(element_locator_def))
        element_def = self.driver.find_element(element_locator_def[0], element_locator_def[1])
        # Scroll the button into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element_def)
        time.sleep(0.2)
        element_def.click()

    def click_and_upload(self, anchor_id, input_id, file_path):
        try:
            # Find and click the anchor element to activate the file input
            anchor_element = self.driver.find_element(By.ID, anchor_id)
            anchor_element.click()  # Click the anchor

            # Now find the file input and upload the file
            file_input = self.driver.find_element(By.ID, input_id)
            file_input.send_keys(file_path)  # Upload the file

            print(f"Successfully uploaded file: {file_path}")

        except Exception as e:
            print(f"Error occurred during upload for {file_path}: {e}")

    def auto_complete_captcha(self, canvas_id, input_name, continue_button_id):
        sem = 0
        while sem == 0:


            canvas_data = self.driver.execute_script(f"""
                var canvas = document.getElementById('{canvas_id}');
                return canvas.toDataURL('image/png');
            """)
            canvas_data = canvas_data.split(',')[1]
            image_data = base64.b64decode(canvas_data)
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

            image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # Create a kernel

            # Apply morphological operations to remove thin lines (use a closing operation)
            morphed = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, kernel, iterations=1)

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

            # Save the processed image

            _, binary = cv2.threshold(result, 20, 255, cv2.THRESH_BINARY_INV)

            cv2.imwrite("cleaned_image.png", binary)

            # reader = easyocr.Reader(['en'])
            # result = reader.readtext(binary)

            captcha_text_processed = pytesseract.image_to_string(binary)

            # captcha_text_processed = ''
            # for (bbox, text, prob) in result:
            #     captcha_text_processed += text  # Combine detected text

            transformations = {
                ' ': '',
                '$': 'S',  # Replace '$' with 'S'
                '€': 'E',
                '/': 'l',
                '\\': 'l',
                '>': '7',
                '<': 'L',
                '*': 'x',
                "+": 'x',
                '|': 'l',
                # '&': 'S',
                # ')': '',
                # '(': 'L',
                '@': 'e',
                "\n": '',
                ',': '',
            }

            captcha_text_processed = ''.join(
                [transformations[char] if char in transformations else char for char in captcha_text_processed])

            # time.sleep(2)
            # self.driver.find_element(By.NAME, input_name).send_keys(captcha_text_processed)

            self.driver.execute_script(
                f"document.getElementsByName('{input_name}')[0].value = '{captcha_text_processed}';")


            # image = Image.open("cleaned_image.png")
            # text = pytesseract.image_to_string(image)
            # text = "".join([transformations[char] if char in transformations else char for char in text])
            # print(f'Captcha text Tesseract = {text}')

            time.sleep(1)
            # click continue button
            self.driver.find_element(By.ID, continue_button_id).click()
            time.sleep(0.5)

            # get error modal
            error_modal = self.driver.find_element(By.ID, "errorModal")

            # Get the display property of the error modal
            display_property = self.driver.execute_script("return window.getComputedStyle(arguments["
                                                          "0]).getPropertyValue('display');", error_modal)

            # Check if the modal is shown (display: block means it's visible)

            if display_property == 'none':
                sem = 1
            else:
                sem = 0
                self.driver.find_element(By.ID, 'BtnError').click()
                time.sleep(0.5)

    def begin_site_completion(self):

        self.driver.get(self.user_data["link"])

        # modal de inceput
        modal = self.driver.find_element(By.ID, "termsModal")

        if modal:
            checkbox_in_modal = modal.find_element(By.ID, "termsCheckbox")
            checkbox_in_modal.click()
            submit_modal_button = modal.find_element(By.ID, "submitTerms")
            submit_modal_button.click()

        # PAS 1

        self.driver.find_element(By.ID, "AdresaEmail").send_keys(self.user_data["email"])
        self.driver.find_element(By.ID, "ConfirmareAdresaEmail").send_keys(self.user_data["email_confirm"])

        # Pause for CAPTCHA solving (first CAPTCHA)

        self.auto_complete_captcha('canvasfirst', 'code', 'validate-step1')

        # PAS 2

        element = WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.ID, "Nume")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.send_keys(self.user_data["name"])

        self.driver.find_element(By.ID, "Prenume").send_keys(self.user_data["surname"])
        self.driver.find_element(By.ID, "SerieCI").send_keys(self.user_data["id_series"])
        self.driver.find_element(By.ID, "NumarCI").send_keys(self.user_data["id_number"])
        self.driver.find_element(By.ID, "CiValabilDeLa").send_keys(self.user_data["valid_from"])
        self.driver.find_element(By.ID, "CiValabilPanaLa").send_keys(self.user_data["valid_until"])
        self.driver.find_element(By.ID, "CNP").send_keys(self.user_data["cnp"])
        self.driver.find_element(By.ID, "Adresa").send_keys(self.user_data["address"])

        select_element = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located((By.ID, "Judet"))
        )
        # Create a Select object
        select = Select(select_element)

        # Select by visible text
        select.select_by_visible_text(self.user_data["county"])

        self.driver.execute_script("arguments[0].scrollIntoView(true);", select_element)

        self.driver.find_element(By.ID, "Telefon").send_keys(self.user_data["phone"])

        # Continue to the next step

        time.sleep(0.5)
        continue_button_locator = (By.ID, "validate-step2")
        self.click_element_function(continue_button_locator)

        # PAS 3
        time.sleep(0.5)

        # Upload document 1 (Copie CI)
        self.click_and_upload("document_1", "document_input_1", self.user_data["ci_pdf"])

        # Upload document 2 (Certificat ANAF)
        self.click_and_upload("document_2", "document_input_2", self.user_data["anaf_pdf"])

        # Upload document 3 (Taxe locale)
        self.click_and_upload("document_3", "document_input_3", self.user_data["local_tax_pdf"])

        # Upload document 4 (Carte funciara)
        self.click_and_upload("document_4", "document_input_4", self.user_data["land_registry_pdf"])

        # Continue to the next step
        continue_button_locator = (By.ID, "validate-step3")

        self.click_element_function(continue_button_locator)

        # PAS 4

        time.sleep(0.5)

        # click the checkboxes
        input_check_acord_2 = self.driver.find_element(By.ID, "CheckDeAcord2")
        input_check_acord_2.click()

        input_check_acord_3 = self.driver.find_element(By.ID, "CheckDeAcord3")
        input_check_acord_3.click()

        input_check_acord_4 = self.driver.find_element(By.ID, "CheckDeAcord4")
        input_check_acord_4.click()

        input_check_acord = self.driver.find_element(By.ID, "CheckDeAcord")
        input_check_acord.click()

        # Pause for CAPTCHA solving (second CAPTCHA)
        self.auto_complete_captcha('canvassecond', 'codesecond', 'validate-step4')

        time.sleep(5)
        self.driver.quit()
