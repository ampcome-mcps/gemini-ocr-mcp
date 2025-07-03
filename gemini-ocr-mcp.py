import os
import base64
import io
from PIL import Image as PILImage
from mcp.server.fastmcp import FastMCP
from google import genai
from mcp.server.fastmcp import Image as MCPImage

# Create an MCP server
mcp = FastMCP("Gemini OCR")

@mcp.tool(title="OCR Image (Base64)")
def ocr_image_base64(base64_image: str) -> str:
    """
    Performs OCR on a base64 encoded image using the Google Gemini API.

    Args:
        base64_image: Base64-encoded string representing the image.

    Returns:
        Extracted text from the image as a string.
        If no text is found, returns "No text found in the image."
        If an error occurs, returns an error message string.
    """
    try:
        # Decode the base64 image string
        try:
            image_bytes = base64.b64decode(base64_image, validate=True)
        except base64.binascii.Error as e:
            raise ValueError(f"Invalid base64 string: {e}")

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
        # GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION for Vertex AI
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


@mcp.tool(title="OCR Image (File)")
def ocr_image_file(image_file: str) -> str:
    """
    Performs OCR on an image file using the Google Gemini API.

    Args:
        image_file: Path to the image file (full path).

    Returns:
        Extracted text from the image as a string.
        If no text is found, returns "No text found in the image."
        If an error occurs, returns an error message string.
    """
    # open the image file
    try:
        with open(image_file, "rb") as file:
            image_bytes = file.read()

        # Convert bytes to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        # Call the ocr_image_base64 function
        return ocr_image_base64(base64_image)
    
    except FileNotFoundError:
        return f"Error: The file '{image_file}' was not found."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
