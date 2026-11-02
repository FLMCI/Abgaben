"""Program using the local module mydates."""
import mydates

dates = [("02.11.2026", "eu"), ("11/02/2026", "us"), ("29.02.2024", "eu"), ("2027-01-01", "eu")]

for date, style in dates:
    info = mydates.date_info(date, style)
    print(f"{date:>11} ({style}): leap year -> {str(info['leapyear']).lower()}, "
          f"{info['weekday']}, week {info['week']}")
