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
from bs4 import BeautifulSoup

# My own libraries
from parser import Event
import ical

# University of Liverpool username
USERNAME = '<USERNAME>'
# Account password
PASSWORD = '<PASSWORD>'


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

def filter_schedules(opener):
    """
    GET NEXT 28 DAYS
    :param opener: access to the website including the session
    :return filtered list of all events
    """
    lectures = []
    labs = []
    specials = []

    urls = []
    url = 'https://timetables.liv.ac.uk/Home/Next28Days'

    for multiplier in range(0, 11):
        now = datetime.datetime.now() + datetime.timedelta(days=28*multiplier)
        next_date = now.strftime("%d%m%Y")
        urls.append(url + '?date={}'.format(next_date))

    for url in urls:
        print 'Downloading', url
        resp = opener.open(url)
        soup = BeautifulSoup(resp.read(), 'lxml')

        for link in soup.find_all('a'):
            if link.get('href')[:7] == 'Details':
                event = Event(link.contents[1], link.contents[3].text)
                if event.special and event.type == 'LEC':
                    lectures.append(event)
                elif event.special and event.type == 'LAB':
                    labs.append(event)
                else:
                    specials.append(event)

    return [lectures, labs, specials]


def main():
    print "Attempting to log into the website"
    session = login()
    print "Filtering events"
    events = filter_schedules(session)
    print "Generating icalendar file"
    ical.generate_ical(events, debug=True)
    print "All Done"

################################################################################

if __name__ == '__main__':
    main()
