"""This script generates the lungodar.html file with the calendar.

In order for a day to be recorded, add a file named DD-MM-YYYY.txt where the
first line is either yes or no, and the rest is the comment.

Then run `python3 lungodar.py` and upload the modified index.html"""

import calendar
from datetime import date, datetime, timedelta
import sys
import os
from html import escape


directory = os.fsencode(os.getcwd())

records = {}
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    name, extension = os.path.splitext(filename)
    if extension != ".txt":
        continue
    file_date = None
    try:
        file_date = datetime.strptime(name, "%d-%m-%Y").date()
    except ValueError:
        # invalid file
        continue
    with open(filename, "r") as f:
        f_contents = f.read().split("\n")
        smoked = f_contents[0]
        thoughts = "\n".join(f_contents[1:])
        records[file_date] = {"smoked": smoked, "thoughts": thoughts}

start_date = date(2024, 7, 29)
start_day = start_date.day
start_month = start_date.month
end_date = date.today()


def start_html_doc():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Lung-o-dar | 🦝 guites webpage</title>
   <link rel="stylesheet" type="text/css" href="calendar.css">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li>
                    <a href="/">Homepage</a>
                </li>
                <li>
                    <a href="https://guites.bearblog.dev/blog/">my blog (aka deepest, most shameful thoughts)</a>
                </li>
                <li>
                    <a href="https://bolha.us/@guites">mastodon (aka slice of life)</a>
                </li>
                <li>Lung-o-dar (or how I stopped coughing and started to love the lung)</li>
                <li>
                    <a href="/whatsup">what's up (with me lately)?</a>
                </li>
            </ul>
        </nav>
        <hr>
    </header>
   <main>
        <h1>guites' official Lung-o-dar 🫁</h1>
        <p>This is a very anxious page where I track my life as a non smoker. There are skulls <sup>💀</sup> on days I've had a cigarette, and a sticker <sup>🚭</sup> on the ones I haven't.</p>
        <p>You can put your mouse on the recorded days to get a glimpse of how I was feeling that particular moment.</p>
        <p><strong>My last day as a smoker was 28/07/2024</strong>. Every cigarette from there on can be seen as a misstep =P.</p>
        <p>Let's fucking go!</p>
        <div class="year">
        <h2>2024</h2>
        <p>amidst the haze</p>
        </div>
        <section class="calendars">
"""


def days_in_month(dt):
    return calendar.monthrange(dt.year, dt.month)[1]


def get_month_statistics(month, num_days, _records):
    smoke_free_days = 0
    for d, r in _records.items():
        if r["smoked"] != "no":
            continue
        if d.month == month:
            smoke_free_days += 1
    pctg_free = (smoke_free_days / num_days) * 100
    return f"""
        <tr>
            <th colspan="7">
                <label>{'%.2f'%(pctg_free)}% smoke free
                    <progress max="{num_days}" value="{smoke_free_days}">
                        {'%.2f'%(pctg_free)}%
                    </progress>
                </label>
            </th>
        </tr>"""


def finish_tables_section():
    return """
            </section>
"""


def start_month_table(month, stats):
    return f"""
        <td>
            <table class="month" border="0" cellpadding="0" cellspacing="0">
            <tbody>
                <tr>
                    <th class="month" colspan="7">{calendar.month_name[month]}</th>
                </tr>
                {stats}
                <tr>
                    <th class="mon">Mon</th>
                    <th class="tue">Tue</th>
                    <th class="wed">Wed</th>
                    <th class="thu">Thu</th>
                    <th class="fri">Fri</th>
                    <th class="sat">Sat</th>
                    <th class="sun">Sun</th>
                </tr>"""


def finish_month_table():
    return """
            </tbody>
        </table>
    </td>
    """


def add_day_td(day, day_obj):
    day_abbr = calendar.day_abbr[day_obj.weekday()]
    return f"""
        <td class='{day_abbr.lower()}'>
            <span>{day}</span>
        </td>"""


def add_recorded_day(day, day_obj, record):
    day_abbr = calendar.day_abbr[day_obj.weekday()]
    smoked = record["smoked"] != "no"
    thoughts = escape(record["thoughts"])
    tool_tip = f"data-tooltip='{thoughts}'" if thoughts else ""
    emoji = "<sup>💀</sup>" if smoked else "<sup>🚭</sup>"
    return f"""
        <td class='{day_abbr.lower()}' >
            <span {tool_tip}>{day}{emoji}</span>
        </td>"""


def add_noday_td():
    return "<td class='noday'></td>"


def get_streak_from_records(_records, streak, curr_day):
    if streak is None:
        streak = 0
    if curr_day is None:
        curr_day = datetime.now().date() - timedelta(days=1)

    if curr_day not in _records:
        return streak
    record = _records[curr_day]
    smoked = record["smoked"] != "no"
    if smoked:
        return streak

    streak += 1
    curr_day = curr_day - timedelta(days=1)
    return get_streak_from_records(_records, streak, curr_day)


def badges_section(streak):
    badge_html = f"""
        <section class="badges">
            <h2>Streak</h2>
            <p>Not smoking for <strong>{streak}</strong> consecutive days!</p>"""
    badges = [{"min_streak": 15, "src": "badges/smoke-free-15.png", "alt": "Sem cigarro - 15 dias"}]
    for badge in badges:
        if streak >= badge["min_streak"]:
            badge_html += f"""
                <img class="badge" src='{badge["src"]}' loading="lazy" alt='{badge["alt"]}'>"""
    badge_html += "</section>"
    return badge_html


html_output = start_html_doc()
current_date = start_date

# holds the current number of days without smoking in a row
streak = get_streak_from_records(records, None, None)

months_in_tr = 0  # hold up to three months per table row
while current_date <= end_date:
    if months_in_tr >= 3:
        # html_output += "</section><section>"
        months_in_tr = 0

    year = current_date.year
    month = current_date.month

    current_month_num_days = days_in_month(current_date)
    current_month_calendar = calendar.monthcalendar(year, month)

    current_month_stats = get_month_statistics(
        month,
        current_month_num_days,
        records,
    )

    html_output += start_month_table(month, current_month_stats)

    for week in current_month_calendar:
        html_output += "<tr>"
        for day in week:
            if day == 0:
                html_output += add_noday_td()
                continue
            day_obj = date(year, month, day)
            if day_obj in records:
                html_output += add_recorded_day(day, day_obj, records[day_obj])
            else:
                html_output += add_day_td(day, day_obj)
        html_output += "</tr>"
    html_output += finish_month_table()

    # goes back to the first day of the current month
    # offset by the number of days in the current month
    first_day = current_date.replace(day=1) + timedelta(current_month_num_days)
    current_date = first_day
    months_in_tr += 1
html_output += finish_tables_section()

html_output += badges_section(streak)

html_output += """
        </main>
    </body>
</html>"""

with open("index.html", mode="w") as file:
    file.write(html_output)
sys.exit(0)
