import threading
import json
from ConfigHandler import ConfigHandler
from Logger import Logger
from SoundPlayer import SoundPlayer
from Timer import Timer

logger = Logger('pomodoro_log.txt')
config_handler = ConfigHandler()
config = config_handler.get_config()

formatted_config = json.dumps(config, indent=2)
logger.save_log(f'\nConfiguration:\n{formatted_config}')

work_interval = config.get('work_interval', 25)
break_interval = config.get('break_interval', 5)
session_count = config.get('pomodoro_count', 3)

def start_timer_thread(timer):
    thread = threading.Thread(target=timer.run)
    thread.start()
    return thread

interval_count = 0
timer = None
timer_thread = None
exit_event = None
skip_break = False
sound_player = SoundPlayer(config.get('break_sound'))

def start_pomodoro():
    global interval_count, exit_event, logger, timer, timer_thread
    interval_count += 1
    logger.save_log(f'Starting Pomodoro {interval_count}')
    exit_event = threading.Event()
    timer = Timer('Pomodoro', work_interval, config['start_sound'], exit_event, logger, interval_count, pomodoro_callback)
    timer_thread = start_timer_thread(timer)

def pomodoro_callback():
    global sound_player
    if interval_count < session_count:
        start_break()
    else:
        logger.save_log(f'Completed {session_count} Pomodoros. Session complete!')
        sound_player.play()

def break_callback():
    global sound_player
    if interval_count < session_count:
        start_pomodoro()
    else:
        logger.save_log(f'Completed {session_count} Pomodoros. Session complete!')
        sound_player.play()

def start_break():
    global interval_count, exit_event, logger, timer, timer_thread
    logger.save_log(f'Starting Break {interval_count}')
    exit_event = threading.Event()
    timer = Timer('Break', break_interval, config['break_sound'], exit_event, logger, interval_count, break_callback)
    timer_thread = start_timer_thread(timer)

def menu_thread():
    global logger, interval_count, skip_break
    while True:
        user_input = input('Enter "i" to start pomodoro, "p" to pause, "u" to unpause, "s" to skip break, or "q" to quit: \n')
        
        if user_input.lower() == 'i':
            interval_count = 0
            skip_break = False
            start_pomodoro()
        elif user_input.lower() == 'p':
            if timer and timer_thread and timer_thread.is_alive:
                timer.pause()
            else:
                logger.save_log('No active timer to pause.')
        elif user_input.lower() == 'u':
            if timer and timer_thread and timer_thread.is_alive:
                timer.unpause()
            else:
                logger.save_log('No paused timer to unpause.')
        elif user_input.lower() == 's':
            skip_break = True
            if timer and timer_thread and timer_thread.is_alive:
                timer.skip()
            else:
                logger.save_log('No active timer to skip break.')
        elif user_input.lower() == 'q':
            if timer_thread:
                exit_event.set()
                timer_thread.join()
                logger.save_log('Quiting.')
            break
        else:
            print('Invalid input. Please enter "i", "p", "u", or "q".')

menu_thread = threading.Thread(target=menu_thread)
menu_thread.start()