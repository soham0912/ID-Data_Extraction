from flask import Flask, jsonify, request
import cv2
import pytesseract
import re
import numpy as np
from flask_cors import CORS
import copy
import pandas as pd

app = Flask(__name__)
CORS(app)

#API Endpoint
@app.route('/detect-aadhar-back', methods=['POST'])
def extract_aadhaar():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image'].read()
    nparr = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

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

    def extract_aadhaar_address(text):
        address_pattern = r'address[\s\S]*\d{5}'
        match = re.search(address_pattern, text, re.IGNORECASE)
        if match:
            return match.group()
        else:
            return None

    aadhaar_address = extract_aadhaar_address(extracted_text_image)
    aadhaar_number = extract_aadhaar_number(extracted_text_image)

    l = 0
    while l < 3:
        if (aadhaar_number is None):
            rotated_image = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            extracted_text_back = pytesseract.image_to_string(rotated_image)
            aadhaar_number = extract_aadhaar_number(extracted_text_back)
            aadhaar_address = extract_aadhaar_address(extracted_text_back)
            img = rotated_image
            l = l + 1
        else:
            break

    if aadhaar_address is not None:
        if "\n" in aadhaar_address:
            aadhaar_address = aadhaar_address.replace("\n", " ")
        if ",," in aadhaar_address:
            aadhaar_address = aadhaar_address.replace(",,", ",")
        if "=" in aadhaar_address:
            aadhaar_address = aadhaar_address.replace("=", "")
        if "!" in aadhaar_address:
            aadhaar_address = aadhaar_address.replace("!", "l")
        if "Address: " in aadhaar_address:
            aadhaar_address = aadhaar_address.replace("Address: ", "")

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
    #     e_data = [aadhaar_address]
    #     df = pd.read_csv(csv_file)
    #     num_rows = df.shape[0]
    #     df.loc[num_rows:, 'Address'] = e_data
    #     df.to_csv(csv_file, index=False)

    return jsonify({'Aadhar': ans,
                    'Front': ans_front,
                    'Back': ans_back,
                    'Address': aadhaar_address,
                    'Aadhar Number': aadhaar_number})


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 4200
    app.run(host=host, port=port)

