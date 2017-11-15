"""
Generate iCalendar Valid File
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
import os
from icalendar import vDatetime
from datetime import datetime, date, time
from time import mktime
import sys

import sqlite3db

# New line
CRLF = '\r\n'

def print_event(e):
    """ print event """
    print 'Event ... {} {} {}'.format(e.name, e.start, e.end)


def cache_ical_events(events, delete_duplicate_cache):
    """ Generate cache events, filter new events , detect lecture changes """

    new_events = []
    # Iterate over each event
    for e in events:

        # Timestamp
        dt = vDatetime.from_ical(e.start)
        timestamp = mktime(dt.timetuple())

        # Count the number of times the event is at database
        csql = "SELECT COUNT(*) FROM `event` WHERE `uid` = ?;"
        count = int(sqlite3db.DB().fetch(csql, (e.uid,))[0][0])

        if count == 0: # The event is not in database
            sql = 'INSERT INTO `event` (`uid`, `name`, `room`, `start`, `end`, `timestamp`) VALUES (?,?,?,?,?,?)'
            sqlite3db.DB().execute(sql, (e.uid, e.name, e.room, e.start, e.end, timestamp))
            print 'Cached ... {} {} {}'.format(e.name, e.start, e.end)
            new_events.append(e)

    # Select all events from the day queried
    midnight = datetime.combine(date.today(), time.min)
    timestamp = mktime(midnight.timetuple())

    sql = 'SELECT COUNT(*) FROM event WHERE `timestamp` > ?';
    event_count = sqlite3db.DB().fetch(sql, (timestamp,))[0][0]

    # The amount of event should always match to the amount of cached events
    # If a lectrure is moved it will be cached twice, therefore will not match
    # Get all the event from the cache and match them one by one with the
    # cache, all the leftover events are duplicates print them to screen
    if event_count != len(events):
        cached_uid_events = []
        sql = "SELECT `uid` FROM `event`"

        # Get all event uids
        for e in sqlite3db.DB().fetch(sql):
            cached_uid_events.append(e[0])

        # Cross reference the cache uids with event uids
        for e in events:
            if e.uid in cached_uid_events:
                cached_uid_events.remove(e.uid)

        # Display remaining duplicates
        for uid in cached_uid_events:

            sql = "SELECT * FROM `event` WHERE `uid`=?"
            event = sqlite3db.DB().fetch(sql, (uid,))[0]
            print 'Duplicate Cache ...{} {} {} {} {}'.format(e[0], e[1], e[2], e[3], e[3])

            # Delete the duplicates
            if delete_duplicate_cache:
                sql = "DELETE FROM `event` WHERE `uid`=?"
                event = sqlite3db.DB().execute(sql, (uid,))

    return new_events

def generate_ical(events, debug=False):
    """ Generate iCalendar file from all events """

    if len(events) == 0:
        print "No new events registered"
        return


    ical = 'BEGIN:VCALENDAR' + CRLF
    ical += 'VERSION:2.0' + CRLF
    ical += 'PRODID:-//hacksw/handcal//NONSGML v1.0//EN' + CRLF

    # Iterate over each event
    for event in events:

        ical += 'BEGIN:VEVENT{}'.format(CRLF)
        now = vDatetime(datetime.now()).to_ical()
        ical += 'DTSTAMP:{}{}'.format(now, CRLF)
        ical += 'DTSTART:{}{}'.format(event.start, CRLF)
        ical += 'DTEND:{}{}'.format(event.end, CRLF)
        ical += 'ORGANIZER:{}{}'.format('University of Liverpool',CRLF)
        ical += 'SUMMARY: {}{}'.format(event.name, CRLF)
        ical += 'LOCATION:{}{}'.format('Liverpool UK', CRLF)
        ical += 'DESCRIPTION:{}{}'.format(event.room, CRLF)
        ical += 'UID:{}{}'.format(event.uid, CRLF)
        ical += 'TZID:{}{}'.format('Europe/London', CRLF)

        # ALARM
        ical += 'BEGIN:VALARM{}'.format(CRLF)
        ical += 'TRIGGER:-PT5M{}'.format(CRLF)
        ical += 'ACTION:DISPLAY{}'.format(CRLF)
        ical += 'DESCRIPTION:Reminder{}'.format(CRLF)
        ical += 'END:VALARM{}'.format(CRLF)
        ical += 'END:VEVENT{}'.format(CRLF)

        # Debug
        if debug:
            print_event(event)

    ical += 'END:VCALENDAR' + CRLF

    directory = os.path.expanduser('~/Downloads/')
    path = os.path.join(directory, 'uol_timetable.ics')
    f = open(path, 'wb')
    f.write(ical)
    f.close()
    print 'File saved at', path
