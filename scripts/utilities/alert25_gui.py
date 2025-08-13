import subprocess
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    
    duration = 1 if args.test else 1500  # 1s or 25m
    
    # Launch completely independent process
    subprocess.Popen([
        sys.executable, "-c",
        f"import time, tkinter.messagebox; "
        f"time.sleep({duration}); "
        "tkinter.messagebox.showinfo('Timer', 'Time\\'s up!')"
    ], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    
    print(f"{'TEST' if args.test else '25-minute'} GUI timer started")
    print("Close this console - popup will appear later")

if __name__ == "__main__":
    main()