# Gemini OCR MCP Server

This project provides a simple yet powerful OCR (Optical Character Recognition) service through a FastMCP server, leveraging the capabilities of the Google Gemini API. It allows you to extract text from images either by providing a file path or a base64 encoded string.

## Objective

**Extract the text from the following image:**

![CAPTCHA](CAPTCHA.png "CAPTCHA CODE")

**and convert it to plain text, e.g., fbVk**

## Features

-	**File-based OCR:** Extract text directly from an image file on your local system.
-	**Base64 OCR:** Extract text from a base64 encoded image string.
-	**Easy to Use:** Exposes OCR functionality as simple tools in an MCP server.
-	**Powered by Gemini:** Utilizes Google's advanced Gemini models for high-accuracy text recognition.

## Prerequisites

-	Python 3.8 or higher
-	A Google Gemini API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/).

## Setup and Installation

1.	**Clone the repository:**
    ```bash
    git clone https://github.com/WindoC/gemini-ocr-mcp
    cd gemini-ocr-mcp
    ```

2.	**Create and activate a virtual environment:**

    ```bash
    # Install uv standalone if needed

    ## On macOS and Linux.
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    ## On Windows.
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

3.	**Install the required dependencies:**
    ```bash
    uv sync
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
        "gemini-ocr-mcp.py"
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
        "gemini-ocr-mcp.py"
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

### `ocr_image_file`

Performs OCR on a local image file.

-	**Parameter:** `image_file` (string): The absolute or relative path to the image file.
-	**Returns:** (string) The extracted text from the image.

### `ocr_image_base64`

Performs OCR on a base64 encoded image.

-	**Parameter:** `base64_image` (string): The base64 encoded string of the image.
-	**Returns:** (string) The extracted text from the image.
