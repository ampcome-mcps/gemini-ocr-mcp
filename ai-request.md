use taskmaster-ai to create a project in current project folder for: `a python mcp server doing upload image to gemini to do ocr (image to text)`

remind for planning only, do not start coding yet.

# taskmaster-ai model suggest
```json
"models": {
    "main": {
      "provider": "openrouter",
      "modelId": "anthropic/claude-sonnet-4",
    },
    "research": {
      "provider": "google",
      "modelId": "gemini-2.5-pro-preview-06-05",
    },
    "fallback": {
      "provider": "google",
      "modelId": "gemini-2.5-flash-preview-05-20",
    }
  }
```

---

# core logic

below provide bash example for your reference.

```
#config
GEMINI_MODEL=gemini-2.5-flash-preview-05-20
GEMINI_API_KEY=xxxxxxxxxxxx
IMAGE_MIME_TYPE="image/png" #hope able to auto detect in code (not hard coded)

#main logic
BASE64_IMAGE=$(base64 -w 0 "$IMAGE_FILE")

API_RESPONSE=$(curl -X POST \
  https://generativelanguage.googleapis.com/v1beta/models/$GEMINI_MODEL:generateContent?key=$GEMINI_API_KEY \
  --header "Content-Type: application/json" \
  --data-raw '{
  "contents": [
    {
      "parts": [
        {
          "text": "Please perform image OCR. Do not add any extra commentary, just the extracted text."
        },
        {
          "inline_data": {
                "mime_type": "$IMAGE_MIME_TYPE",
                "data": "$BASE64_IMAGE"
          }
        }
      ]
    }
  ]
}')

OCR_TEXT=$(echo "$API_RESPONSE" | jq -r '.candidates[0].content.parts[0].text')


echo -e "\n--- Extracted Text (OCR) ---"
echo "$OCR_TEXT"
echo "---------------------------"
```

---

# for MCP server

please follow the https://github.com/modelcontextprotocol/python-sdk (Python implementation of the Model Context Protocol (MCP))

use context7 to research the detail of [mcp\[cli\]](https://github.com/modelcontextprotocol/python-sdk)

[what is needed for python mcp server.](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#quickstart)

example code:
```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
```

---

# gor gemini library

use content7 to research the detail of [google-genai](https://github.com/googleapis/python-genai)

`google-generativeai` is Deprecated. don't use `google-generativeai`
