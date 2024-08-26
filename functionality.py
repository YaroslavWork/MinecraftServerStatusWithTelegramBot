def convert_seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


def relative_time(seconds):
    if seconds < 1:
        return "less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 120:
        return "a minute"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 7200:
        return "an hour"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 172800:
        return "a day"
    else:
        return f"{int(seconds // 86400)} days"


def read_log_file():
    with open('direction.txt') as f:
        log_directory = f.read().strip()

    with open(log_directory) as f:
        return f.readlines()

def writing_stats(json_string):
    with open('stats.json', 'w') as f:
        f.write(json_string)
