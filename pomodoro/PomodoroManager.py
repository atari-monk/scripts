import threading
import json
from ConfigHandler import ConfigHandler
from Logger import Logger
from SoundPlayer import SoundPlayer
from Timer import Timer

class PomodoroManager:
    def __init__(self):
        self.logger = Logger('pomodoro_log.txt')
        self.config_handler = ConfigHandler()
        self.config = self.config_handler.get_config()

        formatted_config = json.dumps(self.config, indent=2)
        self.logger.save_log(f'\nConfiguration:\n{formatted_config}')

        self.work_interval = self.config.get('work_interval', 25)
        self.break_interval = self.config.get('break_interval', 5)
        self.session_count = self.config.get('pomodoro_count', 3)

        self.interval_count = 0
        self.timer = None
        self.timer_thread = None
        self.exit_event = None
        self.skip_break = False
        self.sound_player = SoundPlayer(self.config.get('break_sound'))

    def start_timer_thread(self, timer):
        thread = threading.Thread(target=timer.run)
        thread.start()
        return thread

    def start_pomodoro(self):
        self.interval_count += 1
        self.logger.save_log(f'Starting Pomodoro {self.interval_count}')
        self.exit_event = threading.Event()
        self.timer = Timer('Pomodoro', self.work_interval, self.config['start_sound'], self.exit_event, self.logger,
                           self.interval_count, self.pomodoro_callback)
        self.timer_thread = self.start_timer_thread(self.timer)

    def pomodoro_callback(self):
        if self.interval_count < self.session_count:
            self.start_break()
        else:
            self.logger.save_log(f'Completed {self.session_count} Pomodoros. Session complete!')
            self.sound_player.play()

    def break_callback(self):
        if self.interval_count < self.session_count:
            self.start_pomodoro()
        else:
            self.logger.save_log(f'Completed {self.session_count} Pomodoros. Session complete!')
            self.sound_player.play()

    def start_break(self):
        self.logger.save_log(f'Starting Break {self.interval_count}')
        self.exit_event = threading.Event()
        self.timer = Timer('Break', self.break_interval, self.config['break_sound'], self.exit_event, self.logger,
                           self.interval_count, self.break_callback)
        self.timer_thread = self.start_timer_thread(self.timer)

    def menu_thread(self):
        while True:
            user_input = input('Enter "i" to start pomodoro, "p" to pause, "u" to unpause, "s" to skip break, or "q" to quit: \n')

            if user_input.lower() == 'i':
                self.interval_count = 0
                self.skip_break = False
                self.start_pomodoro()
            elif user_input.lower() == 'p':
                if self.timer and self.timer_thread and self.timer_thread.is_alive:
                    self.timer.pause()
                else:
                    self.logger.save_log('No active timer to pause.')
            elif user_input.lower() == 'u':
                if self.timer and self.timer_thread and self.timer_thread.is_alive:
                    self.timer.unpause()
                else:
                    self.logger.save_log('No paused timer to unpause.')
            elif user_input.lower() == 's':
                self.skip_break = True
                if self.timer and self.timer_thread and self.timer_thread.is_alive:
                    self.timer.skip()
                else:
                    self.logger.save_log('No active timer to skip break.')
            elif user_input.lower() == 'q':
                if self.timer_thread:
                    self.exit_event.set()
                    self.timer_thread.join()
                    self.logger.save_log('Quitting.')
                break
            else:
                print('Invalid input. Please enter "i", "p", "u", or "q".')

    def run(self):
        menu_thread = threading.Thread(target=self.menu_thread)
        menu_thread.start()

if __name__ == "__main__":
    pomodoro_manager = PomodoroManager()
    pomodoro_manager.run()
