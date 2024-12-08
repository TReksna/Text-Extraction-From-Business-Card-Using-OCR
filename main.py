import easyocr
import re
from PIL import Image
import numpy as np


# Function to process and extract information
def extract_business_card_data(image_path):
    # Load EasyOCR model
    reader = easyocr.Reader(['en'])

    # Read the image
    input_image = Image.open(image_path)
    result = reader.readtext(np.array(input_image))

    result_text = [text[1] for text in result]  # Extract detected text

    # Initialize fields
    email = None
    phone_numbers = []
    website = None
    address = []

    # Patterns for matching
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'\+?\d[\d\s\-\(\)]{7,}'
    website_pattern = r'((http|https):\/\/)?(www\.)?[\w\-]+\.[a-z]{2,}'

    # Extract relevant information
    for text in result_text:
        # Match email
        if not email and re.search(email_pattern, text.lower()):
            email = text

        # Match phone numbers
        if re.search(phone_pattern, text):
            phone_numbers.append(text)

        # Match website
        if not website and re.search(website_pattern, text.lower()):
            website = text.lower()

        # Match address keywords (basic matching)
        keywords = ['road', 'street', 'avenue', 'lane', 'district', 'city', 'state', 'country', 'zip', 'pincode']
        if any(keyword in text.lower() for keyword in keywords):
            address.append(text)

    # Return results
    return {
        'Email': email,
        'Phone Numbers': phone_numbers,
        'Website': website,
        'Address': ' '.join(address)
    }


# Example usage
if __name__ == "__main__":
    image_path = "path/to/your/business_card_image.jpg"  # Replace with the path to your image
    extracted_data = extract_business_card_data(image_path)
    print("Extracted Data:")
    for key, value in extracted_data.items():
        print(f"{key}: {value}")
