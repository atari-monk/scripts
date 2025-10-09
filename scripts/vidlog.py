import sys
from datetime import datetime
from pathlib import Path
import textwrap
from typing import List

def get_log_file(lang: str) -> Path:
    if lang == "pl":
        return Path("C:/Atari-Monk/logs/vid-log-2025-pl.txt")
    else:
        return Path("C:/Atari-Monk/logs/vid-log-2025-en.txt")

def format_note(note: str, max_chars: int = 100) -> str:
    if not note:
        return ""
    
    paragraphs = note.split('\n')
    formatted_lines: List[str] = []
    
    for paragraph in paragraphs:
        if paragraph.strip():
            wrapped_lines = textwrap.wrap(paragraph, width=max_chars, break_long_words=False)
            formatted_lines.extend(wrapped_lines)
        else:
            formatted_lines.append("")
    
    return '\n'.join(formatted_lines)

def add_entry(date: str, title: str, link: str, note: str, lang: str) -> None:
    log_file = get_log_file(lang)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{date}\n{title}\n{link}\n")
        if note:
            formatted_note = format_note(note)
            f.write(formatted_note)
            f.write("\n")
        f.write("\n")
    print(f"Added to {lang.upper()} log: {title} ({date})")

def parse_arguments() -> tuple[str, str, str, str, str]:
    if len(sys.argv) < 3:
        print("Usage: vid_log <title> <link> [note] [--pl|--en]")
        print("       vid_log <date> <title> <link> [note] [--pl|--en]")
        sys.exit(1)

    lang = "en"
    
    has_lang_flag = len(sys.argv) > 1 and sys.argv[-1] in ["--en", "--pl"]
    
    if has_lang_flag:
        lang = sys.argv[-1][2:]
        args = sys.argv[1:-1]
    else:
        args = sys.argv[1:]
    
    if len(args) >= 3 and args[0].count('-') == 2:
        date = args[0]
        title = args[1]
        link = args[2]
        note = ' '.join(args[3:]) if len(args) > 3 else ""
    else:
        date = datetime.now().strftime('%Y-%m-%d')
        title = args[0]
        link = args[1]
        note = ' '.join(args[2:]) if len(args) > 2 else ""

    return date, title, link, note, lang

def main() -> None:
    date, title, link, note, lang = parse_arguments()
    add_entry(date, title, link, note, lang)

if __name__ == "__main__":
    main()