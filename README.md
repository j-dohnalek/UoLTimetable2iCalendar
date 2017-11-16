# UoLTimetable2iCalendar
Automatically download lecture timetable for computer science students and generate iCalendar file.
The file is saved into the Downloads folder
<p>Tested on Ubuntu Linux 16.04</p>

## Features
* Download all lectures for a given number of 28 day blocks
* Saves files into ***.ical** file compatible with most calendar applications
* Creates cache file to filter duplicate events before creating the ical file
* Detects lecture change and highlights it to the user

## Available Information
* Module
* Start Time
* End Time
* Room

## Dependencies
**requests** (pip install requests)<br>
**BeautifulSoup** (pip install beautifulsoup4)
**iCalendar** (pip install icalendar)

## Usage
```
python main.py -u <username> -p <password> -b <blocs>
```

```
usage: main.py [-h] [-s] [--username USERNAME] [--password PASSWORD]
               [--weeks WEEKS] [-d] [-r]

optional arguments:
  -h, --help            show this help message and exit
  -s, --passwd          Login using generated base64 encoded string
  --username USERNAME, -u USERNAME
                        UoL Username
  --password PASSWORD, -p PASSWORD
                        Password
  --weeks WEEKS, -w WEEKS
                        Number weeks to download
  -d, --delete          Delete duplicate cache events
  -r, --remove-cache    Delete all cache events
```
