import argparse
from typing import Dict, List, Tuple

commands: Dict[str, List[Tuple[str, str]]] = {
    "Blogging": [
        ("blog_index_h", "Generates blog index with heading tags"),
        ("blog_index_nested", "Generates nested blog index structure"),
        ("blog_index_ul", "Generates blog index with unordered list"),
        ("productivity_daily", "Generates productivity daily stats in dev-log"),
        ("productivity_logs", "Generates productivity project logs in dev-log"),
    ],
    "Command-Box": [
        ("run_command_box", "Locally runs app command-box")
    ],
    "Dev-Blog": [
        ("push_dev_blog", "Commit and push dev-blog repository")
    ],
    "Development": [
        ("build_zippy_test", "Tool for building projects (Out of order!)"),
        ("code_to_clipboard", "Copies code snippets to clipboard"),
        ("pascal_to_kebab", "Converts pascal to kebab format"),
        ("tree_to_clipboard", "Copies directory tree structure to clipboard"),
    ],
    "Other": [
        ("focus_drone", "Focuses coder on a specific target (Out of order!)"),
        ("text_adventure", "Starts a text-based adventure game"),
    ],
    "Productivity":[
        ("convert_to_format2", "Productivity format convesion tool"),
        ("productivity_to_blog", "Publish productivity logs to dev-blog"),
        ("proj_log", "Productivity log for projects")
    ],
    "Prompt Tools Collection": [
        ("class_maintenance_prompts", "Generates class maintenance prompts for AI"),
        ("clipboard_collector", "Collects and manages clipboard history"),
        ("load_paths", "Load paths.md file and stores files in clipboard"),
        ("merge_paths", "Load paths and store files content in clipboard"),
        ("scan_and_save_paths", "Saves paths of project to paths.md"),
    ],
    "Prompting Project":[("list_md_json", "Converts list in md to array in json"), ("open_llm", "Opens favorite llm client"), ("prompt_tool", "Prompting tool")],
    "Utilities": [
        ("alarm", "Sets an alarm or timer"),
        ("alert25_cli", "Cli notification after 25 min"),
        ("alert25_gui", "Gui notification after 25 min"),
        ("info", "Displays system information"),
        ("fix_path", "/ for path that is in clipboard"),
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
