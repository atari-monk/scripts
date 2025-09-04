import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple

class ProjectFileValidator:
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        self.format1_path = Path("C:/Atari-Monk-Art/productivity/content/format-1")
        self.format2_path = Path("C:/Atari-Monk-Art/productivity/content/format-2")
    
    def validate_project_file_exists(self) -> Tuple[bool, Path]:
        yaml_file = self.format1_path / f"{self.project_name}.yaml"
        return yaml_file.exists(), yaml_file

class YAMLDataLoader:
    @staticmethod
    def load_yaml_data(file_path: Path) -> Dict[str, Any]:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

class TimeCalculator:
    @staticmethod
    def parse_duration(duration_str: str) -> Tuple[int, int]:
        hours = 0
        minutes = 0
        
        if 'h' in duration_str:
            hours_part = duration_str.split('h')[0]
            hours = int(hours_part) if hours_part else 0
        
        if 'm' in duration_str:
            minutes_part = duration_str.split('h')[-1].split('m')[0]
            minutes = int(minutes_part) if minutes_part else 0
        
        return hours, minutes

class MarkdownGenerator:
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
    
    def generate_markdown_content(self, logs_data: Dict[str, List[Dict[str, Any]]]) -> str:
        markdown_lines = [f"# {self.project_name}\n"]
        
        for date_str, sessions in logs_data.items():
            for session in sessions:
                task_list = session.get('Task', [])
                time_str = session.get('Time', '0h0m')
                
                hours, minutes = TimeCalculator.parse_duration(time_str)
                duration_display = f"{hours}h {minutes}m"
                
                markdown_lines.append(f"## Session {date_str} {duration_display}\n")
                
                for task in task_list:
                    markdown_lines.append(f"- {task}")
                
                markdown_lines.append("")
        
        return "\n".join(markdown_lines)

class FileSaver:
    @staticmethod
    def save_markdown_file(content: str, file_path: Path) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)

def main() -> None:
    try:
        project_name = input("Enter project name: ").strip()
        
        # Handle empty input
        if not project_name:
            print("No project name provided. Exiting.")
            return
        
        validator = ProjectFileValidator(project_name)
        file_exists, yaml_file_path = validator.validate_project_file_exists()
        
        if not file_exists:
            print(f"Error: File {yaml_file_path} does not exist.")
            return
        
        yaml_data = YAMLDataLoader.load_yaml_data(yaml_file_path)
        logs_data = yaml_data.get('logs', {})
        
        generator = MarkdownGenerator(project_name)
        markdown_content = generator.generate_markdown_content(logs_data)
        
        output_file = validator.format2_path / f"{project_name}.md"
        FileSaver.save_markdown_file(markdown_content, output_file)
        
        print(f"Successfully converted {yaml_file_path} to {output_file}")
        
    except KeyboardInterrupt:
        print("Operation cancelled by user. Exiting gracefully.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()