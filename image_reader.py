from PIL import Image
from gemini_helper import client

def extract_text_from_image(uploaded_image):
    try:
        image = Image.open(uploaded_image)

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=[
                "Extract all text from this image. Preserve headings and formatting where possible.",
                image
            ]
        )

        return response.text

    except Exception as e:
        return f"Image processing failed: {e}"