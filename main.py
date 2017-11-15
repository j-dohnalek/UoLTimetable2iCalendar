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

# IMPORTS ###################################################################

import requests
import urllib, urllib2, cookielib
import argparse
import sys

from parser import parse_timetable
import ical

# FUNCTIONS ###################################################################

def login(username, password):
    """ LOGIN TO WEBSITE """
    session = requests.Session()
    session.cookies.get_dict()

    login_url = 'https://timetables.liv.ac.uk/Home/Login'
    values = {'username': username,
              'password': password,
              'action': 'login',
              'submit':'continue' }

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    login_data = urllib.urlencode(values)
    opener.open(login_url, login_data)

    return opener


def main():

    username = None
    password = None
    blocks = 1
    delete_duplicate = False

    # Process the arguments ################################

    # initiate the parser
    parser = argparse.ArgumentParser()

    # add long and short argument
    parser.add_argument("--username", "-u", help="UoL Username")
    parser.add_argument("--password", "-p", help="Password")
    parser.add_argument("--blocks", "-b", help="Number of 28 day blocks")
    parser.add_argument("-d", "--delete", help="Delete duplicate cache events", action="store_true")

    # read arguments from the command line
    args = parser.parse_args()

    # check for --width
    if args.username:
        username = args.username
    if args.password:
        password = args.password
    if args.blocks:
        blocks = int(args.blocks)
    if args.delete:
        delete_duplicate = True

    if username is None or password is None:
        print "run command: python main.py -h"
        sys.exit(1)

    # Execute the routines ################################

    print "Attempting to log into the website"
    session = login(username, password)
    print "Filtering events, please wait"
    events = parse_timetable(session, blocks)
    print "Caching events, please wait"
    cached_events = ical.cache_ical_events(events, delete_duplicate)
    print "Generating icalendar file"
    ical.generate_ical(cached_events)
    print "Success"

################################################################################

if __name__ == '__main__':
    main()
