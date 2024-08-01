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
        <section>
"""


def finish_html_doc():
    return """
            </section>
        </main>
    </body>
</html>
"""


def start_month_table(month):
    return f"""
        <td>
            <table class="month" border="0" cellpadding="0" cellspacing="0">
            <tbody>
                <tr>
                    <th class="month" colspan="7">{calendar.month_name[month]}</th>
                </tr>
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


html_output = start_html_doc()
current_date = start_date
months_in_tr = 0  # hold up to three months per table row
while current_date <= end_date:
    if months_in_tr >= 3:
        # html_output += "</section><section>"
        months_in_tr = 0

    year = current_date.year
    month = current_date.month

    html_output += start_month_table(month)

    current_month_calendar = calendar.monthcalendar(year, month)
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

    days_in_month = lambda dt: calendar.monthrange(dt.year, dt.month)[1]
    # goes back to the first day of the current month
    # offset by the number of days in the current month
    first_day = current_date.replace(day=1) + timedelta(days_in_month(current_date))
    current_date = first_day
    months_in_tr += 1
html_output += finish_html_doc()

with open("index.html", mode="w") as file:
    file.write(html_output)
sys.exit(0)
