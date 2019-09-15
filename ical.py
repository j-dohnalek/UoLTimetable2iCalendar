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

# Date format of duplicate cache event
EVENT_DATE_FORMAT = '%a %d-%b-%Y %H:%M:00'


def print_event(e):
    """ print event """
    start = vDatetime.from_ical(e.start).strftime(EVENT_DATE_FORMAT)
    end = vDatetime.from_ical(e.end).strftime(EVENT_DATE_FORMAT)
    print 'Event ... {} {} {}'.format(e.name, start, end)


def is_event_cached(event_id):
    sql = 'SELECT COUNT(*) FROM event WHERE `event_id` = ?'
    event_count = sqlite3db.DB().fetch(sql, (event_id,))

    if event_count is None:
        return False

    return event_count[0][0] > 0


def delete_cache():
    """ Delete all cached events """
    sql = "DELETE FROM `event` WHERE 1"
    sqlite3db.DB().execute(sql)
    print "Cache cleared"


def cache_ical_events(events, delete_duplicate_cache):
    """ Generate cache events, filter new events , detect lecture changes """

    new_events = []
    # Iterate over each event
    for e in events['events']:

        # Timestamp
        dt = vDatetime.from_ical(e.start)
        timestamp = mktime(dt.timetuple())

        # Count the number of times the event is at database
        csql = "SELECT COUNT(*) FROM `event` WHERE `uid` = ?;"
        count = int(sqlite3db.DB().fetch(csql, (e.uid,))[0][0])

        if count == 0:  # The event is not in database
            sql = """
              INSERT INTO `event`
              (`uid`, `name`, `room`, `start`, `end`, `timestamp`, `event_id`)
              VALUES (?,?,?,?,?,?,?)
              """
            sqlite3db.DB().execute(sql, (e.uid, e.name, e.room, e.start, e.end, timestamp, e.event_id))
            start = vDatetime.from_ical(e.start).strftime(EVENT_DATE_FORMAT)
            print 'New ... {} - {}'.format(start, e.name)
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
    if event_count != len(events['event_ids']):
        cached_event_ids = []
        sql = "SELECT `event_id` FROM `event`"

        # Get all event uids
        if sqlite3db.DB().fetch(sql) is None:
            print 'Can not cache events'
            return new_events

        for e in sqlite3db.DB().fetch(sql):
            cached_event_ids.append(e[0])

        # Cross reference the cache uids with event uids
        for uid in events['event_ids']:
            if uid in cached_event_ids:
                cached_event_ids.remove(uid)

        # Display remaining duplicates
        print '---- DUPLICATE EVENTS ------------------------------------------'
        for event_id in cached_event_ids:

            sql = "SELECT `start`, `name`, `room` FROM `event` WHERE `event_id`=?"
            e = sqlite3db.DB().fetch(sql, (event_id,))[0]

            start = vDatetime.from_ical(e[0]).strftime(EVENT_DATE_FORMAT)
            print 'Duplicate ... {} - {}, {}'.format(start, e[1], e[2])

            # Delete the duplicates
            if delete_duplicate_cache:
                sql = "DELETE FROM `event` WHERE `event_id`=?"
                sqlite3db.DB().execute(sql, (event_id),)
        print '----------------------------------------------------------------'

    return new_events

def generate_ical(events, debug=False):
    """ Generate iCalendar file from all events """

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
        ical += 'ORGANIZER:{}{}'.format('University of Liverpool', CRLF)
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
