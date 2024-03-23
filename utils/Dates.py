import logging
import argparse
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def convert_from_UTC_to_CET(timestamp_str):
    timestamp_utc = datetime.fromisoformat(timestamp_str)
    timestamp_cet = timestamp_utc + timedelta(hours=1)
    return timestamp_cet

def main():
    parser = argparse.ArgumentParser(description="Convert UTC to CET time zone")
    parser.add_argument("-utc", metavar="datetime", type=str, help="Timestamp in ISO format (e.g., '2024-03-23T08:30:00')")
    args = parser.parse_args()

    if args.utc:
        timestamp_str_input = args.utc
    else:
        timestamp_str_input = input("Enter a timestamp in ISO format: ")

    logger.debug(f"Timestamp input: {timestamp_str_input}")

    try:
        cet_time = convert_from_UTC_to_CET(timestamp_str_input)
        print("Corresponding date and time in Cracow:", cet_time)
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
