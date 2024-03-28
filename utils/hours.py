from datetime import datetime, timedelta
import calendar
import sys

def get_current_date():
    return datetime.now().date()

def calculate_time_difference(start_time, end_time):
    return end_time - start_time

def print_hours_and_minutes_difference(hours_difference):
    total_minutes = int(hours_difference * 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    print(f'The difference is {hours} hours and {minutes} minutes.')

def is_valid_day_in_current_month(day):
    current_date = datetime.now()
    last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[1]

    return 1 <= day <= last_day_of_month

if __name__ == "__main__":
    print(f'args {len(sys.argv)}, {sys.argv}')
    if len(sys.argv) not in [5, 7]:
        print("Usage: python script.py <start_hour> <start_minute> <end_hour> <end_minute> [start_day end_day]")
        sys.exit(1)

    current_date = get_current_date()

    if len(sys.argv) == 7:
        start_hour, start_minute, end_hour, end_minute, start_day, end_day = map(int, sys.argv[1:])
        if start_day > end_day:
            print('start_day must be before end_day')
            sys.exit(1)
        if not is_valid_day_in_current_month(start_day) or not is_valid_day_in_current_month(end_day):
            print('start_day and end_day must be current month days')
            sys.exit(1)
    else:
        start_day = end_day = current_date.day
        start_hour, start_minute, end_hour, end_minute = map(int, sys.argv[1:])

    start_time = datetime(current_date.year, current_date.month, start_day, start_hour, start_minute)
    end_time = datetime(current_date.year, current_date.month, end_day, end_hour, end_minute)

    time_difference = calculate_time_difference(start_time, end_time)
    hours_difference = time_difference.total_seconds() / 3600

    print_hours_and_minutes_difference(hours_difference)
