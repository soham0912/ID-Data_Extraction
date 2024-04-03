# ID-Data_Extraction
A working webpage model with integrated backend flask APIs for data extraction and seamless auto form filling for a smooth user experience.

Welcome to the Seamless Auto Form Filling Webpage with integrated backend Flask APIs! This project provides a user-friendly interface that allows users to easily fill out forms by extracting data from uploaded images of national ID documents. This not only saves time but also minimizes the risk of manual data entry errors. Read on to learn how to set up and use this application.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed:
- Python (3.6+)
- Flask (Web framework for backend)
- Tesseract OCR (Optical Character Recognition)
- OpenCV

## Usage

### Selecting ID Document
1. Run the file `index.html`
2. On the landing page, you will be presented with a list of available national ID Documents to choose from (e.g., Aadhar card, Passport, Driver's License, etc.). This project is a work in progress therefore at the moment data extraction of only Aadhar card is being done.
3. Click on the document type that corresponds to the ID you want to use.

![image](https://github.com/soham0912/ID-Data_Extraction/assets/59016312/ba2eb9d8-6ed7-4139-9766-a163bb248ff7)

### Uploading Images
1. After selecting the ID document, option to upload image/s will appear.
2. Follow the on-screen instructions to upload the necessary images of your ID document. These images may include the front and back sides of the document.
3. Once the images are uploaded, click the "Submit" button.

![image](https://github.com/soham0912/ID-Data_Extraction/assets/59016312/30229b55-805d-4204-82aa-b6aaf3bec752)


### Auto Form Filling
1. After submitting the images, the system will automatically extract relevant data from the images using Optical Character Recognition (OCR) and populate the corresponding form fields.
2. Review the populated form to ensure accuracy and completeness.
3. Make any necessary corrections or additions if required.
4. Click the "Submit Form" button to complete the process.

![image](https://github.com/soham0912/ID-Data_Extraction/assets/59016312/3288662e-d08a-47c5-a7c0-596331320a1a)



