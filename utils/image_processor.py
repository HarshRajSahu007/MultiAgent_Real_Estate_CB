import base64
from io import BytesIO
from PIL import Image
import numpy as np

def encode_image_to_base64(image_file):
    """
    Encode an image file to base64 for API submission
    
    Args:
        image_file: The uploaded image file (from Streamlit)
        
    Returns:
        str: Base64 encoded image
    """
    if hasattr(image_file, 'read'):
        # For file objects from Streamlit
        bytes_data = image_file.getvalue()
        base64_encoded = base64.b64encode(bytes_data).decode('utf-8')
        return base64_encoded
    else:
        # For direct file paths
        with open(image_file, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

def preprocess_image(image_file, max_size=1024):
    """
    Preprocess image for optimization
    
    Args:
        image_file: The uploaded image file
        max_size: Maximum dimension size
        
    Returns:
        BytesIO: Processed image as BytesIO object
    """

    img = Image.open(image_file)
    

    width, height = img.size
    if max(width, height) > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        img = img.resize((new_width, new_height), Image.LANCZOS)
    

    if img.mode != 'RGB':
        img = img.convert('RGB')
    

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    
    return buffer

def prepare_image_for_api(image_file):
    """
    Prepare image for OpenAI API submission
    
    Args:
        image_file: The uploaded image file
        
    Returns:
        dict: Image data formatted for OpenAI API
    """
    processed_image = preprocess_image(image_file)
    base64_image = base64.b64encode(processed_image.getvalue()).decode('utf-8')
    
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    }