import time
from SoundPlayer import SoundPlayer

class Timer:
    def __init__(self, name, minutes, sound, exit_event, logger, interval_count, callback):
        self.name = name
        self.minutes = minutes
        self.sound_player = SoundPlayer(sound)
        self.exit_event = exit_event
        self.logger = logger
        self.paused = False
        self.interval_count = interval_count
        self.callback = callback

    def run(self):
        self.sound_player.play()
        
        seconds = self.minutes * 60
        while seconds > 0:
            if self.exit_event.is_set():
                break
            elif not self.exit_event.is_set() and not self.paused:
                time.sleep(1)
                seconds -= 1
            else:
                time.sleep(1)

        if not self.exit_event.is_set():
            self.logger.save_log(f'{self.name} {self.interval_count} complete.')
            if self.callback:
                self.callback()

    def skip(self):
        self.logger.save_log(f'{self.name} {self.interval_count} skipped.')
        self.exit_event.set()
        if self.callback:
            self.callback()
            
    def pause(self):
        if not self.paused:
            self.logger.save_log(f'{self.name} {self.interval_count} paused.')
            self.paused = True

    def unpause(self):
        if self.paused:
            self.logger.save_log(f'{self.name} {self.interval_count} unpaused.')
            self.paused = False
