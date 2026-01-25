from datetime import datetime
import time, os
def remaining_date(date:datetime):
    
    current_date = datetime.now()
    remaining = date - current_date
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_days = days
    remaining_hours = hours if hours > 0 else 0
    remaining_minutes = minutes if minutes > 0 else 0
    remaining_seconds = seconds if seconds > 0 else 0
    return (remaining_days, remaining_hours, remaining_minutes, remaining_seconds)
    
def display_counnter(date:datetime):
    try:
        while True:
            remaining = remaining_date(date)
            days, hours, minutes, seconds = remaining
            if not (days >=0):
                break
            
            date_str = date.strftime("%d-%m-%Y %H:%M:%S")
            os.system("cls")
            print("=== Event Timer ===")
            print("Date to go:", date_str)
            print(f"Time remaining: {days} days, {'0' if hours < 10 else ''}{hours}:{'0' if minutes < 10 else ''}{minutes}:{'0' if seconds < 10 else ''}{seconds} seconds")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Timer stopped.")
    else:
        print("Event time reached!")

def main():
    print("=== Event Timer Setup ===")
    print("Enter the date and time for the event you want to count down to.")
    while True:
        try:

            print("Format: YYYY-MM-DD HH:MM:SS")
            date = input("Enter the event date and time (YYYY-MM-DD HH:MM:SS): ")
            event_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD HH:MM:SS")
        else:
            break
    display_counnter(event_date)

if __name__ == "__main__":
    main()