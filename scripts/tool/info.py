import argparse
from typing import Dict, List, Tuple

commands: Dict[str, List[Tuple[str, str]]] = {
    "Blog": [
        ("blog_index", "Generates index for md blog files"),
    ],
    "Command-Box": [
        ("command_box_run", "Locally runs app command-box")
    ],
    "Dev-Blog": [
        ("dev_blog_push", "Commit and push dev-blog repository")
    ],
    "Development": [
        ("code_to_clipboard", "Copies code snippets to clipboard"),
        ("tree_to_clipboard", "Copies directory tree structure to clipboard"),
    ],
    "Other": [
        ("text_adventure", "Starts a text-based adventure game"),
    ],
    "Productivity":[
        ("productivity_to_blog", "Publish productivity logs to dev-blog"),       
        ("proj_log", "Productivity log for projects")
    ],
    "Prompt Project":[
        ("prompt_dequeue", "Moves record form promt queue to history"),
        ("list_md_json", "Converts list in md to array in json"),
        ("open_llm", "Opens favorite llm client"),
        ("prompt_tool", "Prompting tool, compose prompt from template and queue to clipboard")
    ],
    "Prompt Tool": [
        ("clipboard_collector", "Collects and manages clipboard history"),
        ("load_paths", "Load paths.md file and stores files in clipboard"),
        ("merge_paths", "Load paths and store files content in clipboard"),
        ("scan_and_save_paths", "Saves paths of project to paths.md"),
    ],
    "Tool": [
        ("alert25_cli", "Cli notification after 25 min"),
        ("alert25_gui", "Gui notification after 25 min"),
        ("info", "Displays system information"),
        ("pascal_to_kebab", "Converts pascal to kebab format in current folder"),
        ("fix_path", "/ for path that is in clipboard"),
    ],
    "Turbo Laps Scenelet":[
        ("turbo_laps_scenelet_prompt", "Opens prompt files for project"),
    ]
}

def main() -> None:
    parser = argparse.ArgumentParser(
        description="📘 Info Tool – Displays categorized command references.",
        epilog="Example usage:\n  info --verbose",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Show command descriptions"
    )
    args = parser.parse_args()

    for category, items in commands.items():
        print(f"\n=== {category} ===")
        for name, desc in items:
            if args.verbose:
                print(f"┌─ {name}")
                print(f"│  {desc}")
                print("└" + "─" * (len(desc) + 3))
            else:
                print(f"- {name}")
