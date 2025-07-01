# Gemini OCR MCP Server

This project provides a simple yet powerful OCR (Optical Character Recognition) service through a FastMCP server, leveraging the capabilities of the Google Gemini API. It allows you to extract text from images either by providing a file path or a base64 encoded string.

## Features

-	**File-based OCR:** Extract text directly from an image file on your local system.
-	**Base64 OCR:** Extract text from a base64 encoded image string.
-	**Easy to Use:** Exposes OCR functionality as simple tools in an MCP server.
-	**Powered by Gemini:** Utilizes Google's advanced Gemini models for high-accuracy text recognition.

## Prerequisites

-	Python 3.8 or higher
-	A Google Gemini API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/).

## Setup and Installation

1.	**Clone the repository (optional):**
    ```bash
    git clone <repository_url>
    cd gemini-ocr-mcp
    ```

2.	**Create and activate a virtual environment:**

    ```bash
    # install virtualenv if needed
    pip3 install virtualenv
    
    # Create the virtual environment
    python -m venv .venv

    # Activate on Windows
    .venv\Scripts\activate

    # Activate on macOS/Linux
    source .venv/bin/activate
    ```

3.	**Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

This application requires a Google Gemini API key to function. You can either set it in a `.env` file or directly in your MCP configuration.

### 1. Using a `.env` file (Recommended)

1.	**Create a `.env` file:**
    You can copy the example file:
    ```bash
    cp .env.example .env
    ```

2.	**Set your API Key:**
    Open the `.env` file and add your Google Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

    # Optional: Specify a different Gemini model
    # GEMINI_MODEL="gemini-pro-vision"
    ```
    The application will load these environment variables automatically. The default model is `gemini-2.5-flash-preview-05-20` if not specified.

### 2. Using MCP Configuration

If you are running this as a server for a parent MCP application, you can configure it in your main MCP `config.json`.

**Windows Example:**
```json
{
  "mcpServers": {
    "gemini-ocr-mcp": {
      "command": "x:\\path\\to\\your\\project\\gemini-ocr-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "x:\\path\\to\\your\\project\\gemini-ocr-mcp\\gemini-ocr-mcp.py"
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
      "command": "/path/to/your/project/gemini-ocr-mcp/.venv/bin/python",
      "args": [
        "/path/to/your/project/gemini-ocr-mcp/gemini-ocr-mcp.py"
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

## Usage

1.	**Start the MCP Server:**
    Run the `gemini-ocr-mcp.py` script from your terminal:
    ```bash
    python gemini-ocr-mcp.py
    ```
    The server will start and be ready to accept tool calls.

2.	**Using the OCR Tools (from another terminal):**
    You can use the `mcp` CLI to interact with the server's tools.

    *	**Example with an image file:**
        ```bash
        mcp ocr_image_file --image_file "path/to/your/image.png"
        ```
        Replace `"path/to/your/image.png"` with the actual path to your image file (e.g., `驗證碼.png`).

    *	**Example with a base64 string:**
        First, get the base64 representation of your image. Then, you can call the tool:
        ```bash
        mcp ocr_image_base64 --base64_image "YOUR_BASE64_ENCODED_STRING"
        ```

## Tools Provided

### `ocr_image_file`

Performs OCR on a local image file.

-	**Parameter:** `image_file` (string): The absolute or relative path to the image file.
-	**Returns:** (string) The extracted text from the image.

### `ocr_image_base64`

Performs OCR on a base64 encoded image.

-	**Parameter:** `base64_image` (string): The base64 encoded string of the image.
-	**Returns:** (string) The extracted text from the image.
