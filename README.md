# UoLTimetable2iCalendar
Automatically download lecture timetable for computer science students and generate iCalendar file.
The file is saved into the Downloads folder
<p>Tested on Ubuntu Linux 16.04</p>

## Available Information
Module, Start Time, End Time, Room

## Dependencies
**requests** (pip install requests)<br>
**BeautifulSoup** (pip install beautifulsoup4)

## Usage
Edit the lines in main.py
```python
usage: main.py [-h] [--username USERNAME] [--password PASSWORD]
               [--blocks BLOCKS] [-d]

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME, -u USERNAME
                        UoL Username
  --password PASSWORD, -p PASSWORD
                        Password
  --blocks BLOCKS, -b BLOCKS
                        Number of 28 day blocks
  -d, --delete          Delete duplicate cache events
```
