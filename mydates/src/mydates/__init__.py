"""mydates - small calendar helper module.

Provides functions to
* check whether a year is a leap year,
* compute the day of the week of a date (key value method, almanac.com),
* compute the ISO week number of a date.

Only the Gregorian calendar is supported.

Example:
    >>> import mydates
    >>> mydates.is_leap_year(2024)
    True
    >>> mydates.day_of_week(2, 11, 2026)
    'Monday'
    >>> mydates.week_number(2, 11, 2026)
    45
"""

# key values of the months for the day-of-week algorithm
MONTH_KEYS = {1: 1, 2: 4, 3: 4, 4: 0, 5: 2, 6: 5,
              7: 0, 8: 3, 9: 6, 10: 1, 11: 4, 12: 6}

# century codes repeat every 400 years: 1700s -> 4, 1800s -> 2, 1900s -> 0, 2000s -> 6
CENTURY_CODES = {0: 6, 1: 4, 2: 2, 3: 0}

# remainder of the algorithm -> name of the weekday
WEEKDAYS = {0: "Saturday", 1: "Sunday", 2: "Monday", 3: "Tuesday",
            4: "Wednesday", 5: "Thursday", 6: "Friday"}

DAYS_IN_MONTH = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def is_leap_year(year: int) -> bool:
    """Return True if `year` is a leap year.

    A year is a leap year if it is divisible by 4, except for years
    divisible by 100 that are not divisible by 400.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_of_week(day: int, month: int, year: int) -> str:
    """Return the name of the weekday of the given date (key value method).

    Steps:
    1. take the last two digits of the year and divide them by 4 (integer division)
    2. add the day of the month
    3. add the key value of the month
    4. subtract 1 for January or February of a leap year
    5. add the century code
    6. add the last two digits of the year
    7. the remainder of the division by 7 gives the weekday
    """
    yy = year % 100
    total = yy // 4 + day + MONTH_KEYS[month]
    if month in (1, 2) and is_leap_year(year):
        total -= 1
    total += CENTURY_CODES[(year // 100) % 4] + yy
    return WEEKDAYS[total % 7]


def day_of_year(day: int, month: int, year: int) -> int:
    """Return the ordinal day of the year (1 = January 1st)."""
    days = sum(DAYS_IN_MONTH[m] for m in range(1, month)) + day
    if month > 2 and is_leap_year(year):
        days += 1
    return days


def _iso_weekday(day: int, month: int, year: int) -> int:
    """Return the ISO weekday number (Monday = 1, ..., Sunday = 7)."""
    names = ["Monday", "Tuesday", "Wednesday", "Thursday",
             "Friday", "Saturday", "Sunday"]
    return names.index(day_of_week(day, month, year)) + 1


def _weeks_in_year(year: int) -> int:
    """Return the number of ISO weeks (52 or 53) of a year."""
    # a year has 53 weeks if it starts on Thursday,
    # or if it is a leap year starting on Wednesday
    jan1 = _iso_weekday(1, 1, year)
    return 53 if jan1 == 4 or (jan1 == 3 and is_leap_year(year)) else 52


def week_number(day: int, month: int, year: int) -> int:
    """Return the ISO 8601 week number of the given date.

    Weeks start on Monday, and week 1 is the week containing the first
    Thursday of the year. Formula: (day_of_year - weekday + 10) // 7.
    Dates at the start of January can belong to the last week of the
    previous year, dates at the end of December to week 1 of the next year.
    """
    week = (day_of_year(day, month, year) - _iso_weekday(day, month, year) + 10) // 7
    if week < 1:
        return _weeks_in_year(year - 1)
    if week > _weeks_in_year(year):
        return 1
    return week


def parse_date(date: str, style: str = "eu") -> tuple[int, int, int]:
    """Split a date string into (day, month, year).

    style="eu": day first, e.g. "02.11.2026" or "02/11/2026"
    style="us": month first, e.g. "11/02/2026"
    ISO dates "2026-11-02" are always recognised (year first).
    """
    if "-" in date:                       # ISO 8601: YYYY-MM-DD
        year, month, day = map(int, date.split("-"))
        return day, month, year
    first, second, year = map(int, date.replace("/", ".").split("."))
    if style.lower() == "eu":
        return first, second, year
    if style.lower() == "us":
        return second, first, year
    raise ValueError("style must be 'eu' or 'us'")


def date_info(date: str, style: str = "eu") -> dict:
    """Return information about a date as a dictionary.

    Keys: "leapyear" (bool), "weekday" (str), "week" (int).

    >>> date_info("02.11.2026")
    {'leapyear': False, 'weekday': 'Monday', 'week': 45}
    >>> date_info("11/02/2026", style="us")
    {'leapyear': False, 'weekday': 'Monday', 'week': 45}
    """
    day, month, year = parse_date(date, style)
    return {
        "leapyear": is_leap_year(year),
        "weekday": day_of_week(day, month, year),
        "week": week_number(day, month, year),
    }
