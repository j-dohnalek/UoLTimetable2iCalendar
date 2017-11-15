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
# University of Liverpool username
USERNAME = '<USERNAME>'

# Account password
PASSWORD = '<PASSWORD>'

# How many 28 days block to download?
BLOCKS = 10
```
