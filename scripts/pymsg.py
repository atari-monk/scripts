import json
import pyperclip
import sys
import os
from typing import Any

def extract_messages_with_location() -> None:
    try:
        clipboard_content = pyperclip.paste().strip()
        if not clipboard_content:
            print("Error: Clipboard is empty")
            sys.exit(1)
        
        data: list[dict[str, Any]] = json.loads(clipboard_content)
        
        results: list[str] = []
        for item in data:
            if 'message' in item:
                filename = os.path.basename(str(item.get('resource', ''))) or '<no-file>'
                line = str(item.get('startLineNumber', '?'))
                column = str(item.get('startColumn', '?'))
                
                location = f"{filename}:{line}:{column}"
                results.append(f"{location}: {item['message']}")
        
        if results:
            pyperclip.copy('\n'.join(results))
            print(f"Copied {len(results)} messages to clipboard")
        else:
            print("No messages found in JSON data")
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON in clipboard")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    extract_messages_with_location()

if __name__ == "__main__":
    extract_messages_with_location()