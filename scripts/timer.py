#!/usr/bin/env python3
"""
Non-blocking timer with always-on-top popup
"""
import sys
import subprocess
import argparse
from datetime import datetime, timedelta

def create_timer_script(minutes: int, seconds: int, start_time: datetime, end_time: datetime) -> str:
    """Create the actual timer code that runs in background - SIMPLIFIED"""
    total_seconds = minutes * 60 + seconds
    
    # Format the times for display
    start_str = start_time.strftime('%Y-%m-%d %H:%M')
    end_str = end_time.strftime('%Y-%m-%d %H:%M')
    duration_str = f"{minutes}m {seconds}s"
    
    return f"""
import time, platform, subprocess

# Wait for the specified time
time.sleep({total_seconds})

# Notify with timing information
message = "Time's up!\\\\nStarted: {start_str}\\\\nEnded: {end_str}\\\\nDuration: {duration_str}"
print(f"\\\\n!!! Time's up! ({minutes}m {seconds}s) !!!")
print(f"Started: {start_str}")
print(f"Ended: {{time.strftime('%Y-%m-%d %H:%M')}}")
print(f"Duration: {duration_str}")

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
        ctypes.windll.user32.MessageBoxW(0, message, "Timer Complete", 0x1000)
    elif platform.system() == "Darwin":
        subprocess.run(['osascript', '-e', f'display dialog "{{message}}" buttons {{"OK"}}'])
    else:
        subprocess.run(['zenity', '--info', '--title=Timer Complete', f'--text={{message}}', '--timeout=30'])
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
    
    # Calculate times
    start_time = datetime.now()
    duration = timedelta(minutes=args.min, seconds=args.sec)
    end_time = start_time + duration
    
    # Print timing information
    print(f"⏰ Timer started at: {start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"⏰ Timer will end at: {end_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"⏰ Duration: {args.min}m {args.sec}s")
    
    # Create and launch background timer
    timer_script = create_timer_script(args.min, args.sec, start_time, end_time)
    
    # Launch in background
    if sys.platform == "win32":
        subprocess.Popen([
            sys.executable, "-c", timer_script
        ], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen([
            sys.executable, "-c", timer_script
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"✅ Timer set for {args.min}m {args.sec}s - running in background")

if __name__ == "__main__":
    main()