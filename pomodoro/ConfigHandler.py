import json
import time

class ConfigHandler:
    def __init__(self, config_file_path='pomodoro.config.json', log_file_path='pomodoro_log.txt'):
        self.CONFIG_FILE_PATH = config_file_path
        self.LOG_FILE_PATH = log_file_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.CONFIG_FILE_PATH, 'r') as config_file:
                config = json.load(config_file)
            return config
        except FileNotFoundError:
            default_config = {'start_sound': 'start_sound.mp3', 'break_sound': 'break_sound.mp3'}
            print(f'Configuration file not found.\nUsing default configuration: {default_config}')
            return default_config

    def get_config(self):
        return self.config

    def update_config(self, new_config):
        self.config.update(new_config)
        formatted_config = json.dumps(self.config, indent=2)
        self.save_log(f'\nUpdated configuration:\n{formatted_config}')

    def save_config(self):
        with open(self.CONFIG_FILE_PATH, 'w') as config_file:
            json.dump(self.config, config_file, indent=2)

    def save_log(self, message):
        with open(self.LOG_FILE_PATH, 'a') as log_file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f'{timestamp}: {message}\n')
            print(f'{timestamp}: {message}')
