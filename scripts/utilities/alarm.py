import argparse
import sys
import time
import winsound


class AlarmClock:
    def __init__(self, duration_minutes: int) -> None:
        self.duration_seconds = duration_minutes * 60

    def _beep(self) -> None:
        for _ in range(5):
            winsound.Beep(1000, 1000)
            time.sleep(1)

    def run(self) -> None:
        time.sleep(self.duration_seconds)
        self._beep()


def parse_args(args: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Simple alarm clock that beeps after specified minutes"
    )
    parser.add_argument(
        "minutes",
        type=int,
        help="Number of minutes until alarm goes off",
    )
    parsed = parser.parse_args(args)
    return parsed.minutes


def validate_minutes(minutes: int) -> None:
    if minutes <= 0:
        raise ValueError("Minutes must be a positive integer")


def main() -> None:
    try:
        minutes = parse_args(sys.argv[1:])
        validate_minutes(minutes)
        alarm = AlarmClock(minutes)
        print(f"Alarm set for {minutes} minute(s)")
        alarm.run()
        print("Time's up!")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()