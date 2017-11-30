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
import base64

from parser import parse_timetable
import ical

# CONSTANTS ###################################################################

SALT = "bv8fFhizx31HKwbI<G:6Z7)<0(m]5n1z).^X}!-;y0VS)55]f-Hi-)hv?3:[DC)r"

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
    try:
        opener.open(login_url, login_data)
    except urllib2.URLError:
        print "No internet connection"
        sys.exit()

    return opener


def main():
    """ Execute all the routines """
    username = None
    password = None
    blocks = 1
    delete_duplicate = False

    # Process the arguments ################################

    # initiate the parser
    parser = argparse.ArgumentParser()

    # add long and short argument
    parser.add_argument("-s", "--passwd", help="Login using generated base64 encoded string", action="store_true")
    parser.add_argument("--username", "-u", help="UoL Username")
    parser.add_argument("--password", "-p", help="Password")
    parser.add_argument("--weeks", "-w", help="Number weeks to download")
    parser.add_argument("-d", "--delete", help="Delete duplicate cache events", action="store_true")
    parser.add_argument("-r", "--remove-cache", help="Delete all cache events", action="store_true")

    # read arguments from the command line
    args = parser.parse_args()

    # check for --width
    if args.username:
        username = args.username

    if args.password:
        password = args.password

    if args.weeks:
        blocks = int(args.weeks)

    if args.delete:
        delete_duplicate = True

    if args.remove_cache:
        ical.delete_cache()
        delete_duplicate = False

    if args.passwd:
        # Login using upasswd file
        f = open('passwd', 'r')
        creds = f.read().split(':')
        username = base64.decodestring(creds[0]).replace(SALT,'')
        password = base64.decodestring(creds[1]).replace(SALT,'')
        username = base64.decodestring(username)
        password = base64.decodestring(password)

    if username is None or password is None:
        print "run command: python main.py -h"
        sys.exit(1)

    # Execute the routines ################################

    print "Attempting to log into the website"
    session = login(username, password)
    print "Filtering events, please wait"
    events = parse_timetable(session, blocks)
    print "Caching events, please wait"
    new_events = ical.cache_ical_events(events, delete_duplicate)

    if len(new_events) > 0:
        print "Generating icalendar file"
        ical.generate_ical(new_events)
    else:
        print "No new events detected"

    print "Execution complete"

################################################################################

if __name__ == '__main__':
    main()
