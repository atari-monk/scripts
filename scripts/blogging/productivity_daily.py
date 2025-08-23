import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, field_validator
import colorama
from colorama import Fore, Style

# Initialize colorama for Windows support
colorama.init()

class ProjectEntry(BaseModel):
    projects: List[str]
    Time: Optional[str] = Field(default=None)
    Start: Optional[str] = Field(default=None)
    End: Optional[str] = Field(default=None)
    
    @field_validator('Time', mode='before')
    @classmethod
    def set_default_time(cls, v: Optional[str]) -> str:
        """Set default time to '0m' if not provided"""
        return v if v is not None and v != "" else "0m"

class DailyStats(BaseModel):
    logs: Dict[str, ProjectEntry]

class DailyStatsProcessor:
    def __init__(self, input_file: Path, output_dir: Path):
        self.input_file = input_file
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
    
    def validate_daily_stats(self, data: Dict[str, Any]) -> Optional[DailyStats]:
        """Validate YAML data with flexible schema handling"""
        try:
            return DailyStats(**data)
        except Exception as e:
            print(f"{Fore.RED}Validation error: {e}{Style.RESET_ALL}")
            return None
    
    def calculate_total_time(self, time_str: str) -> int:
        """Convert time string to total minutes, handle various formats"""
        if not time_str or time_str == "0m":
            return 0
        
        try:
            # Handle empty strings
            time_str = time_str.strip()
            if not time_str:
                return 0
            
            # Handle different time formats
            if 'h' in time_str and 'm' in time_str:
                parts = time_str.split()
                hours = int(parts[0].replace('h', ''))
                minutes = int(parts[1].replace('m', ''))
                return hours * 60 + minutes
            elif 'h' in time_str:
                return int(time_str.replace('h', '')) * 60
            elif 'm' in time_str:
                return int(time_str.replace('m', ''))
            else:
                # Assume it's already in minutes
                return int(time_str)
        except (ValueError, AttributeError):
            print(f"{Fore.YELLOW}Warning: Could not parse time '{time_str}', using 0 minutes{Style.RESET_ALL}")
            return 0
    
    def generate_daily_summary(self, validated_data: DailyStats) -> Dict[str, Any]:
        """Generate summary statistics for the daily stats"""
        summary: Dict[str, Any] = {
            "total_days": len(validated_data.logs),
            "total_projects": 0,
            "total_time_minutes": 0,
            "projects_count": {},
            "days_with_time_data": 0,
            "days_with_full_time_data": 0,
            "daily_average": 0
        }
        
        project_count: Dict[str, int] = {}
        
        # Use underscore for unused variable
        for _, entry in validated_data.logs.items():
            summary["total_projects"] += len(entry.projects)
            
            time_minutes = self.calculate_total_time(entry.Time or "0m")
            summary["total_time_minutes"] += time_minutes
            
            # Track data completeness
            if time_minutes > 0:
                summary["days_with_time_data"] += 1
            if entry.Start and entry.End:
                summary["days_with_full_time_data"] += 1
            
            for project in entry.projects:
                project_count[project] = project_count.get(project, 0) + 1
        
        summary["projects_count"] = dict(sorted(project_count.items(), 
                                              key=lambda x: x[1], reverse=True))
        
        if summary["total_days"] > 0:
            summary["daily_average"] = summary["total_time_minutes"] / summary["total_days"]
        
        return summary
    
    def format_time_display(self, entry: ProjectEntry) -> str:
        """Format time information for display"""
        time_parts: List[str] = []
        
        if entry.Time and entry.Time != "0m":
            time_parts.append(f"Time: {entry.Time}")
        
        if entry.Start:
            time_parts.append(f"Start: {entry.Start}")
        
        if entry.End:
            time_parts.append(f"End: {entry.End}")
        
        if time_parts:
            return f"**{', '.join(time_parts)}**"
        return "**Time: Not recorded**"
    
    def convert_to_markdown(self, validated_data: DailyStats, output_path: Path) -> None:
        """Convert YAML data to markdown format with evolution awareness"""
        markdown_content: List[str] = [
            "# Daily Project Statistics\n",
            "## Summary\n"
        ]
        
        # Generate summary
        summary = self.generate_daily_summary(validated_data)
        
        markdown_content.extend([
            f"- **Total Days Tracked:** {summary['total_days']}",
            f"- **Total Projects Worked On:** {summary['total_projects']}",
            f"- **Total Time Invested:** {summary['total_time_minutes']} minutes "
            f"({summary['total_time_minutes']/60:.1f} hours)",
            f"- **Daily Average:** {summary['daily_average']:.1f} minutes",
            f"- **Days with Time Data:** {summary['days_with_time_data']}/{summary['total_days']}",
            f"- **Days with Full Time Data:** {summary['days_with_full_time_data']}/{summary['total_days']}\n",
            "## Project Frequency\n"
        ])
        
        for project, count in summary["projects_count"].items():
            markdown_content.append(f"- {project}: {count} days")
        
        markdown_content.extend(["\n", "## Daily Log (Chronological Order)\n"])
        
        # Add daily entries in chronological order
        for date_str, entry in sorted(validated_data.logs.items()):
            markdown_content.append(f"### {date_str}\n")
            
            # Format time information based on available data
            markdown_content.append(self.format_time_display(entry))
            
            markdown_content.append("**Projects:**")
            for project in entry.projects:
                markdown_content.append(f"- {project}")
            
            markdown_content.append("")
        
        output_path.write_text("\n".join(markdown_content).strip())
    
    def process_daily_stats(self) -> None:
        """Process only the daily-projects.yaml file"""
        try:
            yaml_data = yaml.safe_load(self.input_file.read_text())
            if yaml_data is None:
                print(f"{Fore.YELLOW}Skipped empty YAML: {self.input_file.name}{Style.RESET_ALL}")
                return
                
            validated_data = self.validate_daily_stats(yaml_data)
            
            if validated_data:
                md_file = self.output_dir / f"{self.input_file.stem}_stats.md"
                self.convert_to_markdown(validated_data, md_file)
                print(f"{Fore.GREEN}Processed: {self.input_file.name} -> {md_file.name}{Style.RESET_ALL}")
                
                # Also generate a summary file
                summary_file = self.output_dir / "project_summary.md"
                self.generate_summary_file(validated_data, summary_file)
                
            else:
                print(f"{Fore.RED}Skipped invalid YAML: {self.input_file.name}{Style.RESET_ALL}")
                
        except yaml.YAMLError as e:
            print(f"{Fore.RED}Skipped malformed YAML: {self.input_file.name} - {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error processing {self.input_file.name}: {e}{Style.RESET_ALL}")
    
    def generate_summary_file(self, validated_data: DailyStats, output_path: Path) -> None:
        """Generate a comprehensive summary file"""
        summary = self.generate_daily_summary(validated_data)
        
        content: List[str] = [
            "# Project Statistics Summary\n",
            "## Overview\n",
            f"- **Tracking Period:** {min(validated_data.logs.keys())} to {max(validated_data.logs.keys())}",
            f"- **Total Days:** {summary['total_days']}",
            f"- **Total Projects:** {summary['total_projects']}",
            f"- **Total Time:** {summary['total_time_minutes']/60:.1f} hours",
            f"- **Daily Average:** {summary['daily_average']/60:.1f} hours",
            f"- **Data Completeness:** {summary['days_with_time_data']}/{summary['total_days']} days have time data",
            f"- **Detailed Tracking:** {summary['days_with_full_time_data']}/{summary['total_days']} days have start/end times\n",
            "## Project Ranking (Most Active)\n"
        ]
        
        for project, count in summary["projects_count"].items():
            content.append(f"1. {project}: {count} days")
        
        content.extend(["\n", "## Format Evolution\n",
            "The tracking format has evolved over time:",
            "- Early days: Only project lists",
            "- Middle period: Added Time field",
            "- Recent days: Added Start and End times for detailed tracking"
        ])
        
        output_path.write_text("\n".join(content))

def main() -> None:
    # Target only the specific file
    input_file = Path(r"C:\Atari-Monk-Art\productivity\content\daily-projects.yaml")
    output_path = Path(r"C:\Atari-Monk-Art\dev-blog\content\projects\productivity\stats")
    
    if not input_file.exists():
        print("Input file does not exist")
        return
    
    processor = DailyStatsProcessor(input_file, output_path)
    processor.process_daily_stats()

if __name__ == "__main__":
    main()