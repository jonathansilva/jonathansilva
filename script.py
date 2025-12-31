import datetime

from datetime import date
from collections import namedtuple
from typing import Optional

FILE = 'README.md'
TIMEZONE = datetime.timezone(datetime.timedelta(hours=-3))

months = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

holidays = {
    1: [{
        "day": 1,
        "name": "Ano novo",
        "emoji": "⬜️ "
    }],
    4: [{
        "day": 21,
        "name": "Dia de Tiradentes",
        "emoji": "🟧 "
    }],
    5: [{
        "day": 1,
        "name": "Dia do Trabalhador",
        "emoji": "🟧 "
    }],
    9: [{
        "day": 7,
        "name": "Dia da Independência do Brasil",
        "emoji": "🟧 "
    }],
    10: [{
        "day": 12,
        "name": "Dia de Nossa Senhora Aparecida",
        "emoji": "🟧 "
    }],
    11: [{
            "day": 2,
            "name": "Dia de Finados",
            "emoji": "🟧 "
        },{
            "day": 15,
            "name": "Dia da Proclamação da República",
            "emoji": "🟧 "
        },{
            "day": 20,
            "name": "Dia da Consciência Negra",
            "emoji": "🟧 "
        }],
    12: [{
        "day": 25,
        "name": "Natal",
        "emoji": "🟦 "
    }]
}

HolidayInfo = namedtuple('HolidayInfo', ['name', 'emoji'])

emoji_remaining = "⬛️ "
emoji_sunday = "🟥 "
emoji_worked = "✅ "
emoji_working = "🟪 "

def get_readme_file_content() -> str:
    with open(FILE, 'r', encoding='UTF-8') as file:
        return file.read()

def get_total_days(year: int) -> int:
    # Verifica se o ano é bissexto
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    if is_leap:
        return 366
    return 365

def get_holiday(date: date) -> Optional[HolidayInfo]:
    month = date.month
    day = date.day

    if month in holidays:
        for holiday in holidays[month]:
            if holiday.get('day') == day:
                return HolidayInfo(name=holiday.get('name'), emoji=holiday.get('emoji'))
    return None

def get_today_status(holiday: str, today: int, count: int) -> tuple[str, int]:
    # Feriado
    if holiday:
        return holiday.emoji, count

    # Domingo
    if today.weekday() == 6:
        return emoji_sunday, count

    # Dia útil
    count += 1

    return emoji_working, count

def format_progress_percentage(percentage: float) -> str:
    if percentage == 100.0:
        return f"{percentage:.0f} %"
    return f"{percentage:.2f} %"

def get_progress() -> str:
    brazil_tz = datetime.datetime.now(TIMEZONE)
    today_date = brazil_tz.date()

    current_year = today_date.year

    total_days = get_total_days(current_year)
    day_of_year = today_date.timetuple().tm_yday

    progress_percentage = (day_of_year / total_days) * 100.0

    passed_string = ""
    today_string = ""

    count = 0

    for day_index in range(1, day_of_year):
        past_date = today_date.replace(month=1, day=1) + datetime.timedelta(days=day_index-1)

        holiday = get_holiday(past_date)

        # Feriado
        if holiday:
            passed_string += holiday.emoji
            continue

        # Domingo
        if past_date.weekday() == 6:
            passed_string += emoji_sunday
            continue

        # Dia útil
        passed_string += emoji_worked
        count += 1

    holiday = get_holiday(today_date)

    today_string, count = get_today_status(holiday, today_date, count)

    # Dias restantes
    days_remaining_count = total_days - day_of_year
    remaining_string = emoji_remaining * days_remaining_count

    days_programming_count = f"**{current_year}** - Programando há {count} dias"

    progress = f"{passed_string}{today_string}{remaining_string}{format_progress_percentage(progress_percentage)}"

    guide = "✅ dias trabalhados 🟥 domingo\n\n⬜️ ano novo 🟦 natal 🟧 outros feriados\n\n🟪 programando ⬛️ dias restantes"

    current_day = f"Hoje, {today_date.day} de {months[today_date.month]}"

    if holiday:
        current_day += f" - {holiday.name}"

    return f"{days_programming_count}\n\n{progress}\n\n{guide}\n\n{current_day}"

def main() -> None:
    readme = get_readme_file_content()
    progress = get_progress()

    start_mark = "<!-- start -->"
    end_mark = "<!-- end -->"

    start_index = readme.index(start_mark) + len(start_mark)
    end_index = readme.index(end_mark)

    new_readme = readme[:start_index] + '\n' + progress + '\n' + readme[end_index:]

    with open(FILE, 'w', encoding='UTF-8') as file:
        file.write(new_readme)

if __name__ == '__main__':
    main()
