from flask import Flask, jsonify, request
import cv2
import pytesseract
import re
import numpy as np
from flask_cors import CORS
import copy
import csv
import pandas as pd

app = Flask(__name__)
CORS(app)

#API Endpoint
@app.route('/detect-aadhar-front', methods=['POST'])
def extract_aadhaar():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image'].read()
    nparr = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    img_front = copy.copy(img)

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    csv_file = r"D:\Personal (Office HDFC)\aadhar_autofill_frontend\aadhar_info_log.csv"

    extracted_text_image = pytesseract.image_to_string(img)

    def extract_aadhaar_number(text):
        # Aadhaar number regular expression pattern
        aadhaar_pattern = r"\b(\d{4}\s\d{4}\s\d{4})\b"
        match = re.search(aadhaar_pattern, text)
        if match:
            return match.group(1)
        else:
            return None

    k = 0
    c = 0

    def extract_aadhaar_name(text):
        # Aadhaar name regular expression pattern
        # pattern = r"([A-Za-z]{2,25}\s[A-Za-z]{2,25}\s[A-Za-z]{2,25})"
        # pattern = r"(?<=\n)(.*?)(?=\n)"
        # pattern = r"(?<=\n)(.*?)(?=\n)"
        # pattern = r"^(.*?)(?=\n)"
        pattern1 = r"([A-Z][a-z]{2,25}\s[A-Z][a-z]{2,25}\s[A-Z][a-z]{2,25})"
        pattern2 = r"([A-Z][a-z]{2,25}\s[A-Z][a-z]{2,25})"
        pattern3 = r"([A-Z][a-z]{2,25}\s[A-Z][a-z]{0,25})"
        pattern4 = r"[A-Z][a-z]{3,25}"
        match1 = re.search(pattern1, text)
        match2 = re.search(pattern2, text)
        match3 = re.search(pattern3, text)
        match4 = re.search(pattern4, text, re.DOTALL)
        if k == 0 and match1:
            return match1.group(1)
        if k == 1 and match2:
            return match2.group(1)
        elif k == 2 and match3:
            return match3.group(1)
        elif k == 3 and match4:
            return match4.group()
        else:
            return None

    def extract_aadhaar_dob(text):
        dob_pattern = r'(\d{2})/(\d{2})/(\d{4})'
        match1 = re.search(dob_pattern, text)
        yob_pattern = r'yob[\s\S]*d{4}'
        match2 = re.search(yob_pattern, text)
        yob2_pattern = r'birth[\s\S]*d{4}'
        match3 = re.search(yob2_pattern, text)
        if match1:
            return match1.group()
        elif match2:
            return match2.group()
        elif match3:
            return match3.group()
        else:
            return None

    def extract_aadhaar_address(text):
        address_pattern = r'address[\s\S]*\d{5}'
        match = re.search(address_pattern, text, re.IGNORECASE)
        if match:
            return match.group()
        else:
            return None

    genderm = ['Male', 'MALE']
    genderf = ['Female', 'FEMALE']
    aadhaar_gender = None

    # Text processing and Aadhaar number extraction
    aadhaar_number = extract_aadhaar_number(extracted_text_image)
    aadhaar_address = extract_aadhaar_address(extracted_text_image)
    aadhaar_name = extract_aadhaar_name(extracted_text_image)
    aadhaar_dob = extract_aadhaar_dob(extracted_text_image)

    for g in genderm:
        if g in extracted_text_image:
            aadhaar_gender = "Male"
    for g in genderf:
        if g in extracted_text_image:
            aadhaar_gender = "Female"

    while k < 4:
        while c < 3:
            if (aadhaar_name is None):
                rotated_image_front = cv2.rotate(img_front, cv2.ROTATE_90_COUNTERCLOCKWISE)
                extracted_text_front = pytesseract.image_to_string(rotated_image_front)
                aadhaar_name = extract_aadhaar_name(extracted_text_front)
                img_front = rotated_image_front
                c = c + 1
            else:
                break
        c = 0
        k = k + 1

    j = 0
    while j < 3:
        if (aadhaar_number is None):
            rotated_image = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            extracted_text_front = pytesseract.image_to_string(rotated_image)
            aadhaar_number = extract_aadhaar_number(extracted_text_front)
            aadhaar_address = extract_aadhaar_address(extracted_text_front)
            aadhaar_dob = extract_aadhaar_dob(extracted_text_front)
            for g in genderm:
                if g in extracted_text_front:
                    aadhaar_gender = "Male"
            for g in genderf:
                if g in extracted_text_front:
                    aadhaar_gender = "Female"

            img = rotated_image
            # aadhaar_name = re.sub(r'[^a-zA-Z\s]', '', aadhaar_name)
            j = j + 1
        else:
            break

    #Output data
    if (aadhaar_number):
        ans = "Yes"
        if aadhaar_address is None:
            ans_back = "No"
            ans_front = "Yes"
        else:
            ans_back = "Yes"
            ans_front = "No"
    else:
        ans = "No"
        ans_back = "No"
        ans_front = "No"

    # if (ans == "Yes" and ans_front == "Yes"):
    #     new_data = [aadhaar_number, aadhaar_name, aadhaar_gender, aadhaar_dob]
    #     existing = pd.read_csv(csv_file) if pd.read_csv(csv_file).shape[0] > 0 else None
    #     new = pd.DataFrame(new_data, columns=['Aadhar_Number', 'Name', 'Gender', 'DOB'])
    #
    #     if existing is not None:
    #         concatenated = pd.concat([existing, new], ignore_index=True)
    #     else:
    #         concatenated = new
    #
    #     concatenated.to_csv(csv_file, index=False)

    return jsonify({'Aadhar': ans,
                    'Front': ans_front,
                    'Back': ans_back,
                    'Aadhar_Number': aadhaar_number,
                    'Address': aadhaar_address,
                    'Name': aadhaar_name,
                    'Gender': aadhaar_gender,
                    'DOB': aadhaar_dob})




if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    app.run(host=host, port=port)