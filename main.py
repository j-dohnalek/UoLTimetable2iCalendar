"""
Login to https://timetables.liv.ac.uk website and grab upcomming 28 days timetable
Copyright (C) 2017  Jiri Dohnalek
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import requests
import urllib, urllib2, cookielib

# My own libraries
from parser import parse_timetable
import ical

# University of Liverpool username
USERNAME = '<USERNAME>'

# Account password
PASSWORD = '<PASSWORD>'

# How many 28 days block to download?
BLOCKS = 1

def login():
    """ LOGIN TO WEBSITE """
    session = requests.Session()
    session.cookies.get_dict()

    login_url = 'https://timetables.liv.ac.uk/Home/Login'
    values = {'username': USERNAME,
              'password': PASSWORD,
              'action': 'login',
              'submit':'continue' }

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    login_data = urllib.urlencode(values)
    opener.open(login_url, login_data)

    return opener


def main():
    print "Attempting to log into the website"
    session = login()
    print "Filtering events, please wait ..."
    events = parse_timetable(session, BLOCKS)
    print "Generating icalendar file"
    ical.generate_ical(events)
    print "All Done"

################################################################################

if __name__ == '__main__':
    main()
