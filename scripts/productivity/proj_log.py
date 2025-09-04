import argparse
from datetime import datetime
from pathlib import Path
from typing import List

class ProjectLogger:
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        self.base_path = Path("C:/Atari-Monk-Art/productivity/content/format-2/")
        self.file_path = self.base_path / f"{project_name}.md"
        
    def ensure_file_exists(self) -> None:
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, 'w') as f:
                f.write(f"# {self.project_name}\n\n")
                
    def append_session_start(self) -> None:
        self.ensure_file_exists()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        with open(self.file_path, 'r') as f:
            content = f.read()
        
        needs_empty_line = content.strip() and not content.endswith('\n\n')
        
        with open(self.file_path, 'a') as f:
            if needs_empty_line:
                f.write('\n')
            f.write(f"## Session {timestamp}\n")
            
    def append_note(self, note: str) -> None:
        self.ensure_file_exists()
        
        with open(self.file_path, 'r') as f:
            content = f.readlines()
        
        is_first_note = True
        for i in range(len(content)-1, -1, -1):
            if content[i].startswith("## Session"):
                break
            elif content[i].startswith("-"):
                is_first_note = False
                break
        
        with open(self.file_path, 'a') as f:
            if is_first_note:
                f.write('\n')
            f.write(f"- {note}\n")
            
    def calculate_duration(self, start_time_str: str) -> str:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        end_time = datetime.now()
        duration = end_time - start_time
        
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        return f"{hours}h {minutes}m"
        
    def end_session(self) -> None:
        self.ensure_file_exists()
        
        with open(self.file_path, 'r') as f:
            content = f.readlines()
            
        for i in range(len(content)-1, -1, -1):
            if content[i].startswith("## Session"):
                session_line = content[i].strip()
                if " - " not in session_line:
                    start_time = session_line.split(" ")[2] + " " + session_line.split(" ")[3]
                    duration = self.calculate_duration(start_time)
                    content[i] = f"{session_line} - {datetime.now().strftime('%H:%M')} {duration}\n"
                    
                    has_content_after = any(
                        line.strip() and not line.startswith('#') 
                        for line in content[i+1:] 
                        if line.strip()
                    )
                    
                    if has_content_after and (i == len(content) - 1 or content[i + 1].strip()):
                        content.insert(i + 1, '\n')
                    break
                    
        with open(self.file_path, 'w') as f:
            f.writelines(content)
            
    def show_state(self, num_sessions: int = 1) -> None:
        if not self.file_path.exists():
            print(f"No log file found for project: {self.project_name}")
            return
            
        with open(self.file_path, 'r') as f:
            content = f.read()
            
        sessions: List[List[str]] = []
        current_session: List[str] = []
        in_session = False
        
        for line in content.split('\n'):
            if line.startswith("## Session"):
                if current_session:
                    sessions.append(current_session)
                current_session = [line]
                in_session = True
            elif in_session and line.strip() and not line.startswith("#"):
                current_session.append(line)
                
        if current_session:
            sessions.append(current_session)
            
        for session in sessions[-num_sessions:]:
            print("\n".join(session))
            print()

def main() -> None:
    parser = argparse.ArgumentParser(description="Project logging utility")
    parser.add_argument("project", help="Project name")
    parser.add_argument("-start", action="store_true", help="Start new session")
    parser.add_argument("-note", help="Add note to current session")
    parser.add_argument("-end", action="store_true", help="End current session")
    parser.add_argument("-state", nargs='?', const=1, type=int, help="Show last N sessions")
    
    args = parser.parse_args()
    
    logger = ProjectLogger(args.project)
    
    if args.start:
        logger.append_session_start()
        print(f"Started new session for project: {args.project}")
    elif args.note:
        logger.append_note(args.note)
        print(f"Added note to project: {args.project}")
    elif args.end:
        logger.end_session()
        print(f"Ended session for project: {args.project}")
    elif args.state is not None:
        logger.show_state(args.state)
    else:
        print("No action specified. Use -start, -note, -end, or -state")

if __name__ == "__main__":
    main()