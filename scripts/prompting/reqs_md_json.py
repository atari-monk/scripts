import argparse
import pyperclip
from typing import List

class TextConverter:
    def __init__(self, debug: bool = False):
        self.debug = debug
        
    def convert(self, text: str) -> str:
        if self.debug:
            print(f"Input text:\n{text}")
            
        lines = self._parse_input(text)
        converted = self._format_output(lines)
        
        if self.debug:
            print(f"Output text:\n{converted}")
            
        return converted
    
    def _parse_input(self, text: str) -> List[str]:
        lines = text.strip().split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('- '):
                cleaned_lines.append(stripped_line[2:])
            elif stripped_line.endswith(','):
                cleaned_lines.append(stripped_line.strip('"').rstrip(','))
            else:
                cleaned_lines.append(stripped_line.strip('"'))
                
        return cleaned_lines
    
    def _format_output(self, lines: List[str]) -> str:
        return ',\n'.join(f'"{line}"' for line in lines if line) + ','

class ClipboardManager:
    @staticmethod
    def get_text() -> str:
        return pyperclip.paste()
    
    @staticmethod
    def set_text(text: str) -> None:
        pyperclip.copy(text)

def main():
    parser = argparse.ArgumentParser(description="Convert text between bullet point and quoted list formats")
    parser.add_argument('--debug', action='store_true', help='Print input and output for debugging')
    
    args = parser.parse_args()
    
    converter = TextConverter(debug=args.debug)
    clipboard = ClipboardManager()
    
    input_text = clipboard.get_text()
    converted_text = converter.convert(input_text)
    
    clipboard.set_text(converted_text)

if __name__ == "__main__":
    main()