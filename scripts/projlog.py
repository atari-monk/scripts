import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

LOG_FILE = Path("C:/Atari-Monk/logs/proj-log-2025.txt")


def read_entries() -> List[str]:
    """Return all log entries as a list of blocks (each block = one record)."""
    if not LOG_FILE.exists():
        return []
    text = LOG_FILE.read_text(encoding="utf-8")
    return [b.strip() for b in text.split("\n\n") if b.strip()]


def write_entries(entries: List[str]) -> None:
    """Persist all entries back to file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text("\n\n".join(entries) + "\n\n", encoding="utf-8")


def split_entry(entry: str) -> Tuple[str, str]:
    """Split an entry into (header, note)."""
    if "\n" in entry:
        h, n = entry.split("\n", 1)
        return h.strip(), n.strip()
    return entry.strip(), ""


def entry_ended(header: str) -> bool:
    """True if header contains a time range (start-end)."""
    parts = header.split()
    return len(parts) > 1 and "-" in parts[1]


def duration(start: str, end: datetime) -> str:
    """
    Return duration string like '1h30m'.
    Always returns '0m' when zero to avoid a blank gap before the project name.
    """
    start_dt = datetime.strptime(end.strftime("%Y-%m-%d") + " " + start, "%Y-%m-%d %H:%M")
    secs = int((end - start_dt).total_seconds())
    h, m = divmod(secs // 60, 60)
    if not h and not m:
        return "0m"
    return (f"{h}h" if h else "") + (f"{m}m" if m else "")


def cmd_print(entries: List[str], count: int) -> None:
    for e in entries[-count:]:
        print(e + "\n")


def cmd_start(entries: List[str], project: str, note: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    record = f"{now}  {project}"
    if note:
        record += f"\n{note}"
    entries.append(record)
    print(f"Started: {project}")


def cmd_note(entries: List[str], note: str) -> None:
    if not entries:
        return print("Error: no active project")
    header, old = split_entry(entries[-1])
    if entry_ended(header):
        return print("Error: last project already ended")
    body = "\n".join(filter(None, [old, note]))
    entries[-1] = f"{header}\n{body}"
    print("Note added")


def cmd_end(entries: List[str], note: str) -> None:
    if not entries:
        return print("Error: no active project")
    header, old = split_entry(entries[-1])
    if entry_ended(header):
        return print("Error: last project already ended")

    parts = header.split()
    date, start = parts[0], parts[1]
    project = parts[2] if len(parts) > 2 else "project"
    end_time = datetime.now()
    dur = duration(start, end_time)
    new_header = f"{date} {start}-{end_time.strftime('%H:%M')} {dur} {project}"
    body = "\n".join(filter(None, [old, note]))
    entries[-1] = f"{new_header}\n{body}" if body else new_header
    print("Project ended")


def main() -> None:
    p = argparse.ArgumentParser(description="Simple project logger")
    p.add_argument("-p", "--print", type=int, metavar="N",
                   help="print last N records")
    p.add_argument("-s", "--start", nargs="+", metavar=("PROJECT", "[NOTE...]"),
                   help="start project with optional note")
    p.add_argument("-n", "--note", nargs="+", metavar="NOTE",
                   help="add note to last record")
    # allow zero or more note words; user may run just `-e`
    p.add_argument("-e", "--end", nargs="*", metavar="NOTE",
                   help="end project with optional note")
    args = p.parse_args()

    entries = read_entries()

    if args.print is not None:
        cmd_print(entries, max(1, args.print))
    elif args.start:
        project, *rest = args.start
        cmd_start(entries, project, " ".join(rest))
    elif args.note:
        cmd_note(entries, " ".join(args.note))
    elif args.end is not None:
        cmd_end(entries, " ".join(args.end))
    else:
        p.print_help()
        return

    write_entries(entries)


if __name__ == "__main__":
    main()
