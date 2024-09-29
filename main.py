from tkinter import filedialog

from selenium import webdriver
import os

import customtkinter

from SiteAutoComplete import SiteAutoComplete

# Get the desktop path dynamically
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

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
    "land_registry_pdf": os.path.join("C:/Users/pallo/OneDrive/Desktop/", "extras_carte_funciara.pdf"),
    "link": "https://www.genway.ro/simulator_casa_verde/",
    # Land registry doc
}


def transfer_data():
    print("transfer data")

    email = email_entry.get()
    name = name_entry.get()
    surname = surname_entry.get()
    series = series_entry.get()
    number = number_entry.get()
    valid_from = valid_from_entry.get()
    valid_until = valid_until_entry.get()
    cnp = cnp_entry.get()
    address = address_entry.get()
    county = county_entry.get()
    phone = phone_entry.get()
    link = link_entry.get()

    if email:
        user_data["email"] = email
        user_data["email_confirm"] = email
    if name:
        user_data["name"] = name
    if surname:
        user_data["surname"] = surname
    if series:
        user_data["id_series"] = series
    if number:
        user_data["id_number"] = number
    if valid_from:
        user_data["valid_from"] = valid_from
    if valid_until:
        user_data["valid_until"] = valid_until
    if cnp:
        user_data["cnp"] = cnp
    if address:
        user_data["address"] = address
    if county:
        user_data["county"] = county
    if phone:
        user_data["phone"] = phone
    if link:
        user_data["link"] = link

    # Add the file paths (assuming file_paths will only be set if a file is chosen)
    if file_paths["Copie CI"]:
        user_data["ci_pdf"] = file_paths["Copie CI"]
    if file_paths["Certificat ANAF"]:
        user_data["anaf_pdf"] = file_paths["Certificat ANAF"]
    if file_paths["Certificat Taxe Locale"]:
        user_data["local_tax_pdf"] = file_paths["Certificat Taxe Locale"]
    if file_paths["Extras Carte Funciara"]:
        user_data["land_registry_pdf"] = file_paths["Extras Carte Funciara"]

    root.destroy()


file_paths = {
    "Copie CI": None,
    "Certificat ANAF": None,
    "Certificat Taxe Locale": None,
    "Extras Carte Funciara": None
}


# Function to open a file dialog and store the selected file path
def select_file(file_type):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_paths[file_type] = file_path
        # Display the file name or confirmation in the button text
        if file_type == "Copie CI":
            ci_button.configure(text=f"Selectat: {file_path.split('/')[-1]}")
        elif file_type == "Certificat ANAF":
            anaf_button.configure(text=f"Selectat: {file_path.split('/')[-1]}")
        elif file_type == "Certificat Taxe Locale":
            taxe_button.configure(text=f"Selectat: {file_path.split('/')[-1]}")
        elif file_type == "Extras Carte Funciara":
            carte_button.configure(text=f"Selectat: {file_path.split('/')[-1]}")


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x600")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

frame.grid_columnconfigure(0, weight=1)  # Make column 0 expandable
frame.grid_columnconfigure(1, weight=1)  # Make column 1 expandable

# Create a label at the top
label = customtkinter.CTkLabel(master=frame, text="Data")
label.grid(row=0, column=0, columnspan=2, pady=12, padx=10, sticky="nsew")

email_entry = customtkinter.CTkEntry(master=frame, placeholder_text="E-mail")
email_entry.grid(row=1, column=0, pady=12, padx=10, sticky="nsew")

name_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Nume")
name_entry.grid(row=1, column=1, pady=12, padx=10, sticky="nsew")

surname_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Prenume")
surname_entry.grid(row=2, column=0, pady=12, padx=10, sticky="nsew")

series_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Serie Buletin")
series_entry.grid(row=2, column=1, pady=12, padx=10, sticky="nsew")

number_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Numar Buletin")
number_entry.grid(row=3, column=0, pady=12, padx=10, sticky="nsew")

valid_from_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Valabil de la")
valid_from_entry.grid(row=3, column=1, pady=12, padx=10, sticky="nsew")

valid_until_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Valabil pana la")
valid_until_entry.grid(row=4, column=0, pady=12, padx=10, sticky="nsew")

cnp_entry = customtkinter.CTkEntry(master=frame, placeholder_text="CNP")
cnp_entry.grid(row=4, column=1, pady=12, padx=10, sticky="nsew")

address_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Adresa(localitate, strada, numar)")
address_entry.grid(row=5, column=0, pady=12, padx=10, sticky="nsew")

county_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Judet")
county_entry.grid(row=5, column=1, pady=12, padx=10, sticky="nsew")

phone_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Telefon")
phone_entry.grid(row=6, column=0, pady=12, padx=10, sticky="nsew")

link_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Link")
link_entry.grid(row=6, column=1, pady=12, padx=10, sticky="nsew")

ci_button = customtkinter.CTkButton(master=frame, text="Select Copie CI (PDF)", command=lambda: select_file("Copie CI"))
ci_button.grid(row=7, column=0, pady=12, padx=10, sticky="nsew")

anaf_button = customtkinter.CTkButton(master=frame, text="Select Certificat ANAF (PDF)",
                                      command=lambda: select_file("Certificat ANAF"))
anaf_button.grid(row=7, column=1, pady=12, padx=10, sticky="nsew")

taxe_button = customtkinter.CTkButton(master=frame, text="Select Certificat Taxe Locale (PDF)",
                                      command=lambda: select_file("Certificat Taxe Locale"))
taxe_button.grid(row=8, column=0, pady=12, padx=10, sticky="nsew")

carte_button = customtkinter.CTkButton(master=frame, text="Select Extras Carte Funciara (PDF)",
                                       command=lambda: select_file("Extras Carte Funciara"))
carte_button.grid(row=8, column=1, pady=12, padx=10, sticky="nsew")

# Button at the bottom, centered
button = customtkinter.CTkButton(master=frame, text="Gata", command=transfer_data)
button.grid(row=9, column=0, columnspan=2, pady=12, padx=10, sticky="nsew")

# Configure row weights to ensure centering of all rows
for i in range(10):
    frame.grid_rowconfigure(i, weight=1)

# Start the main loop
root.mainloop()

driver = webdriver.Chrome()
siteCompletion = SiteAutoComplete(user_data, driver)

siteCompletion.begin_site_completion()
