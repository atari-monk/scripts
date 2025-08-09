import pyperclip
import sys
import argparse
import toml
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Prompt:
    name: str
    input_description: str
    task: str
    output_description: str

    def __str__(self) -> str:
        return f"""### **Prompt Name:** {self.name}

**Input:**

{self.input_description}

**Task:**

{self.task}

**Output:**

{self.output_description}"""

@dataclass
class AppInfo:
    help_text: str
    prompt_info: str
    version: str

def load_app_data() -> tuple[list[Prompt], AppInfo]:
    prompts_file = Path("C:/Atari-Monk-Art/app-data/class_maintenance_prompts.toml")
    try:
        data = toml.load(prompts_file)
        prompts = [Prompt(**prompt) for prompt in data["prompts"]]
        app_info = AppInfo(
            help_text=data["app_info"]["help_text"],
            prompt_info=data["app_info"]["prompt_info"],
            version=data["app_info"]["version"]
        )
        
        return prompts, app_info
    except FileNotFoundError:
        print(f"Error: Prompts file not found at {prompts_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading prompts: {str(e)}")
        sys.exit(1)

def display_help(app_info: AppInfo) -> None:
    print(app_info.help_text)

def list_prompts(prompts: list[Prompt]) -> None:
    print("\nAvailable Prompts:")
    print("="*50)
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. {prompt.name}")
    print("="*50)
    print("\nUse '-n NUMBER' to copy a prompt to clipboard")
    print("Use '-i' to view about prompt information")

def copy_prompt(prompts: list[Prompt], number: int) -> None:
    try:
        index = number - 1
        if 0 <= index < len(prompts):
            pyperclip.copy(str(prompts[index]))
            print(f"\nCopied prompt {number} to clipboard")
            # print("="*50)
            # print(prompts[index])
            # print("="*50)
        else:
            print(f"Error: Please enter a number between 1 and {len(prompts)}")
            sys.exit(1)
    except Exception as e:
        print(f"Error copying prompt: {str(e)}")
        sys.exit(1)

def show_prompt_info(app_info: AppInfo) -> None:
    print(app_info.prompt_info)

def main():
    prompts, app_info = load_app_data()
    
    parser = argparse.ArgumentParser(description='Prompt Helper - Quickly access frequently used prompts')
    parser.add_argument('-l', '--list', action='store_true', help='list all available prompts')
    parser.add_argument('-n', '--number', type=int, help='select prompt by number to copy to clipboard')
    parser.add_argument('-i', '--info', action='store_true', help='display information about prompts')
    parser.add_argument('-v', '--version', action='store_true', help='show program version')
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Prompt Helper {app_info.version}")
        sys.exit(0)
    
    if args.list:
        list_prompts(prompts)
        sys.exit(0)
    
    if args.number:
        copy_prompt(prompts, args.number)
        sys.exit(0)
        
    if args.info:
        show_prompt_info(app_info)
        sys.exit(0)
    
    display_help(app_info)
    sys.exit(0)
