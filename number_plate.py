import cv2
from PIL import Image
import pytesseract
import numpy as np
import xml.etree.ElementTree as ET
import os

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the Haarcascade model
harcascade = "model/haarcascade_russian_plate_number.xml"

# Number plate prefix to district/state mapping for India
number_plate_prefix_mapping = {
    "AN": "Andaman and Nicobar Islands",
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CG": "Chhattisgarh",
    "CH": "Chandigarh",
    "DD": "Daman and Diu",
    "DL": "Delhi",
    "DN": "Dadra and Nagar Haveli",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HP": "Himachal Pradesh",
    "HR": "Haryana",
    "JH": "Jharkhand",
    "JK": "Jammu and Kashmir",
    "KA": "Karnataka",
    "KL": "Kerala",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "MH": "Maharashtra",
    "ML": "Meghalaya",
    "MN": "Manipur",
    "MP": "Madhya Pradesh",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OD": "Odisha",
    "PB": "Punjab",
    "PY": "Puducherry",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TR": "Tripura",
    "TS": "Telangana",
    "UK": "Uttarakhand",
    "UP": "Uttar Pradesh",
    "WB": "West Bengal"
}

cap = cv2.VideoCapture(0)

cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
count = 0

# Create XML root
root = ET.Element("Plates")

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y + h, x: x + w]
            cv2.imshow("ROI", img_roi)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        image_path = f"plates/scanned_img_{count}.jpg"
        cv2.imwrite(image_path, img_roi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Results", img)
        cv2.waitKey(500)
        count += 1

        # Preprocess the image for better OCR results
        img_pil = Image.open(image_path).convert('L')  # Convert to grayscale
        img_np = np.array(img_pil)
        
        # Enhance image for OCR
        _, img_thresh = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Save the preprocessed image (optional)
        preprocessed_image_path = f"plates/preprocessed_img_{count}.jpg"
        cv2.imwrite(preprocessed_image_path, img_thresh)

        # Use Tesseract to do OCR on the preprocessed image
        text = pytesseract.image_to_string(Image.fromarray(img_thresh))

        # Print the text
        print(f"Text from {image_path}: {text}")

        # Extract the prefix and determine the district
        prefix = text[:2].upper().strip()  # Ensure prefix is clean and uppercase
        print(f"Extracted Prefix: {prefix}")  # Debugging line
        district = number_plate_prefix_mapping.get(prefix, "Unknown District")

        # Print the district information
        print(f"District: {district}")

        # Save the text and district to XML
        plate_element = ET.SubElement(root, "Plate")
        img_path_element = ET.SubElement(plate_element, "ImagePath")
        img_path_element.text = image_path
        text_element = ET.SubElement(plate_element, "Text")
        text_element.text = text.strip()
        district_element = ET.SubElement(plate_element, "District")
        district_element.text = district

        # Save the XML to a file
        tree = ET.ElementTree(root)
        xml_path = "plates/plate_texts.xml"
        os.makedirs(os.path.dirname(xml_path), exist_ok=True)
        tree.write(xml_path)

cap.release()
cv2.destroyAllWindows()
