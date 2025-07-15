# Gemini OCR MCP Server

This project provides a comprehensive OCR (Optical Character Recognition) service through a FastMCP server, leveraging the capabilities of the Google Gemini API. It allows you to extract text from both images and PDFs using URLs or local files.

## Objective

**Extract the text from the following image:**

![CAPTCHA](CAPTCHA.png "CAPTCHA CODE")

**and convert it to plain text, e.g., fbVk**

## Features

- **Image OCR from URLs:** Extract text from images hosted online
- **Image OCR from Local Files:** Extract text from local image files
- **PDF OCR from URLs:** Extract text from PDF documents hosted online
- **PDF OCR from Local Files:** Extract text from local PDF files
- **Async Support:** All operations are asynchronous to prevent timeouts
- **Page-specific PDF Processing:** Process individual pages or entire PDF documents
- **Easy to Use:** Exposes OCR functionality as simple tools in an MCP server
- **Powered by Gemini:** Utilizes Google's advanced Gemini models for high-accuracy text recognition

## Prerequisites

- Python 3.11 or higher
- A Google Gemini API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/).

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WindoC/gemini-ocr-mcp
   cd gemini-ocr-mcp
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Install uv standalone if needed

   ## On macOS and Linux.
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   ## On Windows.
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install the required dependencies:**
   ```bash
   uv sync
   ```

   Or using the installation script:
   ```bash
   chmod +x install_deps.sh
   ./install_deps.sh
   ```

4. **Configure your environment:**
   Copy `.env.example` to `.env` and set your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash-preview-05-20
   ```

## MCP Configuration Example

If you are running this as a server for a parent MCP application, you can configure it in your main MCP `config.json`.

**Windows Example:**
```json
{
  "mcpServers": {
    "gemini-ocr-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "x:\\path\\to\\your\\project\\gemini-ocr-mcp",
        "run",
        "gemini-ocr-mcp"
      ],
      "env": {
        "GEMINI_MODEL": "gemini-2.5-flash-preview-05-20",
        "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

**Linux/macOS Example:**
```json
{
  "mcpServers": {
    "gemini-ocr-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/project/gemini-ocr-mcp",
        "run",
        "gemini-ocr-mcp"
      ],
      "env": {
        "GEMINI_MODEL": "gemini-2.5-flash-preview-05-20",
        "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```
**Note:** Remember to replace the placeholder paths with the absolute path to your project directory.

## Tools Provided

### `ocr_image_url`

Performs OCR on an image from a URL.

- **Parameter:** `image_url` (string): The URL of the image to perform OCR on.
- **Returns:** (string) The extracted text from the image.

### `ocr_image_file`

Performs OCR on a local image file.

- **Parameter:** `file_path` (string): The absolute or relative path to the image file.
- **Returns:** (string) The extracted text from the image.

### `ocr_pdf_url`

Performs OCR on a PDF from a URL.

- **Parameters:** 
  - `pdf_url` (string): The URL of the PDF to perform OCR on.
  - `page_number` (Optional[int]): Specific page to process (1-indexed). If None, processes all pages.
- **Returns:** (string) The extracted text from the PDF.

### `ocr_pdf_file`

Performs OCR on a local PDF file.

- **Parameters:** 
  - `file_path` (string): The absolute or relative path to the PDF file.
  - `page_number` (Optional[int]): Specific page to process (1-indexed). If None, processes all pages.
- **Returns:** (string) The extracted text from the PDF.

## Dependencies

- `google-genai` - Google Gemini API client
- `mcp[cli]` - MCP framework
- `pillow` - Image processing
- `python-dotenv` - Environment variable management
- `aiohttp` - Async HTTP client for URL fetching
- `PyMuPDF` - PDF processing and conversion

## Async Support

All OCR operations are now asynchronous to prevent timeout issues:
- Longer timeout values (60s for images, 120s for PDFs)
- Non-blocking operations
- Rate limiting protection with delays between PDF page processing

## Error Handling

The server provides comprehensive error handling for:
- Invalid URLs or file paths
- Unsupported file formats
- Network timeouts
- API rate limiting
- PDF processing errors

## Usage Examples

### Image OCR from URL
```python
result = await ocr_image_url("https://example.com/image.jpg")
```

### PDF OCR from local file (specific page)
```python
result = await ocr_pdf_file("/path/to/document.pdf", page_number=1)
```

### PDF OCR from URL (all pages)
```python
result = await ocr_pdf_url("https://example.com/document.pdf")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
