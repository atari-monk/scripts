import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, ValidationError, Field
from pydantic import RootModel
import colorama
from colorama import Fore, Style

# Initialize colorama for Windows support
colorama.init()

class TaskEntry(BaseModel):
    Task: List[str]
    Time: Optional[str] = Field(default="0m")

class DayLog(RootModel[List[TaskEntry]]):
    pass

class ProjectLog(BaseModel):
    logs: Dict[str, DayLog]

def validate_yaml_content(data: Dict[str, Any]) -> Optional[ProjectLog]:
    try:
        return ProjectLog(**data)
    except ValidationError:
        return None

def convert_yaml_to_markdown(validated_data: ProjectLog, output_path: Path) -> None:
    markdown_content: List[str] = []
    
    for date, day_log in sorted(validated_data.logs.items(), reverse=True):
        markdown_content.append(f"## {date}\n")
        
        for entry in day_log.root:
            task_list = "\n".join([f"- {task}" for task in entry.Task])
            markdown_content.append(f"**Time:** {entry.Time}\n")
            markdown_content.append(task_list)
            markdown_content.append("")
        
        markdown_content.append("")
    
    output_path.write_text("\n".join(markdown_content).strip())

def process_yaml_files(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(exist_ok=True)
    
    for yaml_file in input_dir.glob("*.yaml"):
        # Skip the daily-projects.yaml file
        if yaml_file.name == "daily-projects.yaml":
            print(f"{Fore.YELLOW}Skipped daily-projects.yaml (ignored file){Style.RESET_ALL}")
            continue
            
        try:
            yaml_data = yaml.safe_load(yaml_file.read_text())
            validated_data = validate_yaml_content(yaml_data)
            
            if validated_data:
                md_file = output_dir / f"{yaml_file.stem}.md"
                convert_yaml_to_markdown(validated_data, md_file)
                print(f"{Fore.GREEN}Converted: {yaml_file.name} -> {md_file.name}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Skipped invalid YAML: {yaml_file.name}{Style.RESET_ALL}")
                
        except yaml.YAMLError:
            print(f"{Fore.RED}Skipped malformed YAML: {yaml_file.name}{Style.RESET_ALL}")

def main() -> None:
    input_path = Path(r"C:\Atari-Monk-Art\productivity\content")
    output_path = Path(r"C:\Atari-Monk-Art\dev-blog\content\projects\productivity\logs")
    
    if not input_path.exists():
        print("Input directory does not exist")
        return
    
    process_yaml_files(input_path, output_path)

if __name__ == "__main__":
    main()