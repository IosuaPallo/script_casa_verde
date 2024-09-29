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
        time.sleep(0.5)
        element_def.click()

    def click_and_upload(self, anchor_id, input_id, file_path):
        try:
            # Find and click the anchor element to activate the file input
            anchor_element = self.driver.find_element(By.ID, anchor_id)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", anchor_element)
            anchor_element.click()  # Click the anchor

            # Now find the file input and upload the file
            file_input = self.driver.find_element(By.ID, input_id)
            file_input.send_keys(file_path)  # Upload the file

            print(f"Successfully uploaded file: {file_path}")

        except Exception as e:
            print(f"Error occurred during upload for {file_path}: {e}")

    def begin_site_completion(self):

        self.driver.get("https://www.genway.ro/simulator_casa_verde/")

        # modal de inceput
        modal = self.driver.find_element(By.ID, "termsModal")

        if modal:
            checkbox_in_modal = modal.find_element(By.ID, "termsCheckbox")
            checkbox_in_modal.click()
            submit_modal_button = modal.find_element(By.ID, "submitTerms")
            submit_modal_button.click()

        # PAS 1

        # Fill in the email and confirm email fields
        self.driver.find_element(By.ID, "AdresaEmail").send_keys(self.user_data["email"])
        self.driver.find_element(By.ID, "ConfirmareAdresaEmail").send_keys(self.user_data["email_confirm"])

        input("First capcha, press enter after....")

        # Click the button to continue to the next step
        time.sleep(0.3)
        continue_button = self.driver.find_element(By.ID, "validate-step1")
        continue_button.click()

        # PAS 2

        element = WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.ID, "Nume")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.send_keys(self.user_data["name"])

        self.driver.find_element(By.ID, "Prenume").send_keys(self.user_data["surname"])
        self.driver.find_element(By.ID, "SerieCI").send_keys(self.user_data["id_series"])
        self.driver.find_element(By.ID, "NumarCI").send_keys(self.user_data["id_number"])
        self.driver.find_element(By.ID, "CiValabilDeLa").send_keys(self.user_data["valid_from"])
        self.driver.find_element(By.ID, "CiValabilPanaLa").send_keys(self.user_data["valid_until"])
        self.driver.find_element(By.ID, "CNP").send_keys(self.user_data["cnp"])
        self.driver.find_element(By.ID, "Adresa").send_keys(self.user_data["address"])

        select_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.ID, "Judet"))
        )
        # Create a Select object
        select = Select(select_element)

        # Select by visible text
        select.select_by_visible_text(self.user_data["county"])

        self.driver.execute_script("arguments[0].scrollIntoView(true);", select_element)

        self.driver.find_element(By.ID, "Telefon").send_keys(self.user_data["phone"])

        # Continue to the next step

        continue_button_locator = (By.ID, "validate-step2")
        time.sleep(0.3)
        self.click_element_function(continue_button_locator)

        # PAS 3

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

        time.sleep(0.3)
        self.click_element_function(continue_button_locator)

        # PAS 4

        time.sleep(0.3)

        input_check_acord_2 = self.driver.find_element(By.ID, "CheckDeAcord2")
        input_check_acord_2.click()

        input_check_acord_3 = self.driver.find_element(By.ID, "CheckDeAcord3")
        input_check_acord_3.click()

        input_check_acord_4 = self.driver.find_element(By.ID, "CheckDeAcord4")
        input_check_acord_4.click()

        input_check_acord = self.driver.find_element(By.ID, "CheckDeAcord")
        input_check_acord.click()

        # Pause for CAPTCHA solving (second CAPTCHA)
        input("Solve the second CAPTCHA  and press Enter to finish the process...")

        # Step 4: Submit the form
        # submit_button = WebDriverWait(self.driver, 15).until(
        #     ec.element_to_be_clickable((By.ID, "validate-step4"))
        # )
        # self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        # submit_button.click()

        # Close the browser after successful submission
        time.sleep(5)
        self.driver.quit()
