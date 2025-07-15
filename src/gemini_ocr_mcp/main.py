import os
import io
import asyncio
import aiohttp
from PIL import Image as PILImage
from mcp.server.fastmcp import FastMCP
from google import genai
from dotenv import load_dotenv
import fitz  # PyMuPDF
from typing import Optional

load_dotenv(override=True)

# Create an MCP server
mcp = FastMCP("Gemini OCR")

@mcp.tool(title="OCR Image from URL")
async def ocr_image_url(image_url: str) -> str:
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

        # Fetch image from URL asynchronously
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            try:
                async with session.get(image_url) as response:
                    response.raise_for_status()
                    image_bytes = await response.read()
            except aiohttp.ClientError as e:
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


@mcp.tool(title="OCR PDF from URL")
async def ocr_pdf_url(pdf_url: str, page_number: Optional[int] = None) -> str:
    """
    Performs OCR on a PDF from a URL using the Google Gemini API.
    Converts PDF pages to images and then performs OCR.

    Args:
        pdf_url: URL of the PDF to perform OCR on.
        page_number: Optional page number to process (1-indexed). If None, processes all pages.

    Returns:
        Extracted text from the PDF as a string.
        If no text is found, returns "No text found in the PDF."
        If an error occurs, returns an error message string.
    """
    try:
        # Validate URL format
        if not pdf_url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format. URL must start with 'http://' or 'https://'")

        # Fetch PDF from URL asynchronously
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as session:
            try:
                async with session.get(pdf_url) as response:
                    response.raise_for_status()
                    pdf_bytes = await response.read()
            except aiohttp.ClientError as e:
                raise ValueError(f"Failed to fetch PDF from URL: {e}")

        # Open PDF with PyMuPDF
        try:
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        except Exception as e:
            raise ValueError(f"Failed to open PDF: {e}")

        # Initialize Gemini client
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        client = genai.Client(api_key=gemini_api_key)
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-preview-05-20")

        extracted_texts = []
        
        # Determine which pages to process
        if page_number is not None:
            if page_number < 1 or page_number > pdf_document.page_count:
                raise ValueError(f"Page number {page_number} is out of range. PDF has {pdf_document.page_count} pages.")
            pages_to_process = [page_number - 1]  # Convert to 0-indexed
        else:
            pages_to_process = range(pdf_document.page_count)

        # Process each page
        for page_index in pages_to_process:
            try:
                page = pdf_document[page_index]
                
                # Convert PDF page to image
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for better quality
                img_data = pix.tobytes("png")
                
                # Prepare content for Gemini API
                contents = [
                    genai.types.Part.from_text(text=f"Please perform OCR on this PDF page {page_index + 1}. Extract all text content. Do not add any extra commentary, just the extracted text."),
                    genai.types.Part.from_bytes(data=img_data, mime_type="image/png")
                ]

                # Send to Gemini API for OCR
                response = client.models.generate_content(
                    model=gemini_model,
                    contents=contents
                )

                # Extract OCR text
                if response.candidates and response.candidates[0].content.parts:
                    page_text = response.candidates[0].content.parts[0].text
                    if page_text.strip():
                        extracted_texts.append(f"--- Page {page_index + 1} ---\n{page_text}")
                
                # Add a small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                extracted_texts.append(f"--- Page {page_index + 1} ---\nError processing page: {str(e)}")

        pdf_document.close()

        # Combine all extracted text
        if extracted_texts:
            return "\n\n".join(extracted_texts)
        else:
            return "No text found in the PDF."

    except Exception as e:
        return f"Error performing PDF OCR: {str(e)}"

def run():
    mcp.run()

if __name__ == "__main__":
    run()
