import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    
    duration = 1 if args.test else 1500  # 1s or 25m
    
    # Launch a completely separate process
    subprocess.Popen([
        sys.executable, "-c",
        f"import time, winsound; time.sleep({duration}); "
        "print('\\n' + '='*50); "
        "print('!!! TIME\\'S UP !!!'); "
        "print('='*50); "
        "winsound.Beep(1000, 1000)"
    ], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    
    print(f"{'TEST' if args.test else '25-minute'} timer started")
    print("Console is now free - notification will appear later")

if __name__ == "__main__":
    main()