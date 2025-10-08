import json
from datetime import datetime
import os
import argparse
from typing import TypedDict, List, Dict, Optional

# Define type annotations for the JSON structure
class Command(TypedDict):
    alias: str
    description: str
    category: str

class CommandData(TypedDict):
    commands: List[Command]

def generate_readme(json_file_path: str, output_file: str = "C:/Atari-Monk/scripts/README.md") -> Optional[List[str]]:
    """
    Generate a README.md file from JSON file containing command information
    
    Args:
        json_file_path: Path to the JSON file containing command data
        output_file: Path where the README file will be created
        
    Returns:
        List of strings representing the README content, or None if error occurs
    """
    # Load JSON data from file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data: CommandData = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{json_file_path}': {e}")
        return None
    
    commands: List[Command] = json_data["commands"]
    
    # Group commands by category
    categories: Dict[str, List[Command]] = {}
    for cmd in commands:
        category = cmd["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(cmd)
    
    # Generate README content
    content: List[str] = []
    
    # Header
    content.append("# Command Reference")
    content.append("")
    content.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    content.append("")
    content.append("This document provides a reference for all available commands and scripts.")
    content.append("")
    
    # Table of Contents
    content.append("## Table of Contents")
    content.append("")
    for category in sorted(categories.keys()):
        content.append(f"- [{category}](#{category.lower()})")
    content.append("")
    
    # Commands by category
    for category in sorted(categories.keys()):
        content.append(f"## {category}")
        content.append("")
        content.append("| Command | Description |")
        content.append("|---------|-------------|")
        
        for cmd in sorted(categories[category], key=lambda x: x["alias"]):
            content.append(f"| `{cmd['alias']}` | {cmd['description']} |")
        
        content.append("")
    
    # Write to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
    except IOError as e:
        print(f"Error writing to file '{output_file}': {e}")
        return None
    
    print(f"README generated successfully: {output_file}")
    print(f"Commands processed: {len(commands)}")
    print(f"Categories found: {list(categories.keys())}")
    
    return content

def main() -> None:
    parser = argparse.ArgumentParser(description='Generate README from JSON commands data')
    parser.add_argument('--input', '-i', default='C:/Atari-Monk/scripts/data/info.json', 
                       help='Input JSON file path (default: C:/Atari-Monk/scripts/data/info.json)')
    parser.add_argument('--output', '-o', default='C:/Atari-Monk/scripts/README.md',
                       help='Output README file path (default: C:/Atari-Monk/scripts/README.md)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: JSON file '{args.input}' not found.")
        print("Please provide a valid JSON file path using --input argument")
        return
    
    generate_readme(args.input, args.output)

if __name__ == "__main__":
    main()