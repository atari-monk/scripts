import time

class Logger:
    def __init__(self, log_file_path):
        self.LOG_FILE_PATH = log_file_path

    def save_log(self, message):
        with open(self.LOG_FILE_PATH, 'a') as log_file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f'{timestamp}: {message}\n')
            print(f'{timestamp}: {message}')
