from datetime import timedelta


def is_integer(x):
    try:
        int(x)
        return True
    except:
        return False


def format_timedelta(delta: timedelta, format_str: str) -> str:
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)  # 86400 seconds in a day
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Mapping for format specifiers
    replacements = {
        "%D": f"{days:02}",
        "%H": f"{hours:02}",
        "%M": f"{minutes:02}",
        "%S": f"{seconds:02}",
        "%f": f"{delta.microseconds:06}",
    }

    # Replace format specifiers in the format string
    for key, value in replacements.items():
        format_str = format_str.replace(key, value)

    return format_str
