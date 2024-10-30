from datetime import date, timedelta, datetime
import os


# source: https://stackoverflow.com/a/1060330
def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)


directory = os.fsencode(os.getcwd())
records = []
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
    records.append(file_date)

records = sorted(records, reverse=True)

# start one day after the latest registered date
start_date = records[0] + timedelta(1)
# go up until today
end_date = date.today()

for single_date in daterange(start_date, end_date):
    filename = f"{single_date.strftime('%d-%m-%Y')}.txt"
    filepath = os.path.join(directory.decode('utf-8'), filename)

    # skip existing files
    if os.path.exists(filepath):
        continue

    with open(filepath, "w", encoding='utf-8') as f:
        # defaults to "no" because I'm feeling lucky
        f.write('no')
