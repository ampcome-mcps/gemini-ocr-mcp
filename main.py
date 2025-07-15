import os
import io
import requests
from PIL import Image as PILImage
from mcp.server.fastmcp import FastMCP
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

# Create an MCP server
mcp = FastMCP("Gemini OCR")

@mcp.tool(title="OCR Image from URL")
def ocr_image_url(image_url: str) -> str:
    """
    Performs OCR on an image from a URL using the Google Gemini API.

    Args:
        image_url: URL of the image to perform OCR on.

    Returns:
        Extracted text from the image as a string.
        If no text is found, returns "No text found in the image."
        If an error occurs, returns an error message string.
    """
    try:
        # Validate URL format
        if not image_url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format. URL must start with 'http://' or 'https://'")

        # Fetch image from URL
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            image_bytes = response.content
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch image from URL: {e}")

        # Determine MIME type dynamically using Pillow
        image_stream = io.BytesIO(image_bytes)
        try:
            pil_image = PILImage.open(image_stream)
            
            # Check if the format is supported
            if pil_image.format is None:
                raise ValueError("Unable to determine image format")
            
            # Map PIL format to MIME type with fallback handling
            if pil_image.format in PILImage.MIME:
                mime_type = PILImage.MIME[pil_image.format]
            else:
                # Handle formats not in PIL.Image.MIME dictionary
                format_to_mime = {
                    'WEBP': 'image/webp',
                    'BMP': 'image/bmp',
                    'TIFF': 'image/tiff',
                    'ICO': 'image/x-icon'
                }
                mime_type = format_to_mime.get(pil_image.format, f'image/{pil_image.format.lower()}')
                
        except (PILImage.UnidentifiedImageError, OSError) as e:
            raise ValueError(f"Invalid or unsupported image format: {e}")

        # Initialize Gemini client
        # API key and model are expected to be set as environment variables
        # GOOGLE_API_KEY for Gemini Developer API
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        client = genai.Client(api_key=gemini_api_key)

        # Prepare content for Gemini API
        contents = [
            genai.types.Part.from_text(text="Please perform image OCR. Do not add any extra commentary, just the extracted text."),
            genai.types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        ]

        # Get Gemini model from environment variable
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-preview-05-20")

        # Send to Gemini API for OCR
        response = client.models.generate_content(
            model=gemini_model,
            contents=contents
        )

        # Extract and return OCR text
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "No text found in the image."

    except Exception as e:
        return f"Error performing OCR: {str(e)}"
    
def run():
    mcp.run()

if __name__ == "__main__":
    run()
