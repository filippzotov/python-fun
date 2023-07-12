def convert_time_to_minutes(time):
    add_pm = 0
    if len(time.split()) == 2:
        time, ampm = time.split()
        add_pm = 0 if ampm == "AM" else 12 * 60

    hours, minutes = time.split(":")
    time = int(hours) * 60 + int(minutes) + add_pm
    return time


def convert_minutes_to_12h(time):
    hours = time // 60
    minutes = time % 60
    pm = "AM"
    if hours > 12:
        hours -= 12
        pm = "PM"
    if hours == 0:
        hours = 12
    elif hours == 12:
        pm = "PM"

    return f"{hours}:{minutes:02d} {pm}"


def calculate_day_of_the_week(day_name, days):
    week_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    return week_days[(week_days.index(day_name) + days) % 7]


def add_time(start_time, add_time, day=None):
    day_minutes = 24 * 60
    start_time = convert_time_to_minutes(start_time)
    add_time = convert_time_to_minutes(add_time)
    new_time = start_time + add_time

    days = new_time // day_minutes
    new_time = new_time % day_minutes
    days_later = (
        "" if days == 0 else f"(next day)" if days == 1 else f"({days} days later)"
    )
    answer = convert_minutes_to_12h(new_time)
    if day:
        answer += f", {calculate_day_of_the_week(day.lower().capitalize(), days)}"
    answer += " " + days_later
    return answer


print(add_time("11:40 AM", "0:25"))
