#!/usr/bin/env python3
"""
Non-blocking timer with always-on-top popup
"""
import sys
import subprocess
import argparse

def create_timer_script(minutes: int, seconds: int) -> str:
    """Create the actual timer code that runs in background - SIMPLIFIED"""
    total_seconds = minutes * 60 + seconds
    
    return f"""
import time, platform, subprocess

# Wait for the specified time
time.sleep({total_seconds})

# Notify
message = "Time's up! ({minutes}m {seconds}s)"
print(f"\\\\n!!! {{message}} !!!")

# Sound notification
try:
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 1000)
        winsound.Beep(1500, 500)
    else:
        for _ in range(3):
            print('\\a')
            time.sleep(0.2)
except:
    pass

# Popup notification
try:
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, "Timer", 0x1000)
    elif platform.system() == "Darwin":
        subprocess.run(['osascript', '-e', f'display dialog "{{message}}" buttons {{"OK"}}'])
    else:
        subprocess.run(['zenity', '--info', '--title=Timer', f'--text={{message}}', '--timeout=30'])
except:
    pass  # Fail silently if popup doesn't work
"""

def main() -> None:
    parser = argparse.ArgumentParser(description="Start a background timer")
    parser.add_argument('-m', '--min', type=int, default=0, help='Minutes')
    parser.add_argument('-s', '--sec', type=int, default=0, help='Seconds')
    
    args = parser.parse_args()
    
    if args.min == 0 and args.sec == 0:
        parser.print_help()
        sys.exit(1)
    if args.min < 0 or args.sec < 0:
        print("Error: Time cannot be negative")
        sys.exit(1)
    
    # Create and launch background timer
    timer_script = create_timer_script(args.min, args.sec)
    
    # Launch in background
    if sys.platform == "win32":
        subprocess.Popen([
            sys.executable, "-c", timer_script
        ], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen([
            sys.executable, "-c", timer_script
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"⏰ Timer set for {args.min}m {args.sec}s")

if __name__ == "__main__":
    main()