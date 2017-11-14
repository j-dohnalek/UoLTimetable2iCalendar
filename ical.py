from icalendar import Calendar, Event, vDatetime, vText
import os

# New line
CRLF = '\r\n'


def print_event(e):
    """ print event """
    if not e.special:
        print 'Standard .. {} {} {} {} {}'.format(e.module_code, e.name, e.type, e.start, e.end)
    else:
        print 'Special .. {} {} {} {}'.format(e.name, e.type, e.start, e.end)


def generate_ical(events, debug=False):
    """ Generate iCalendar file from all events """
    ical = 'BEGIN:VCALENDAR' + CRLF
    ical += 'VERSION:2.0' + CRLF
    ical += 'PRODID:-//hacksw/handcal//NONSGML v1.0//EN' + CRLF

    # Iterate all event types (lecture, labs, special events)
    for event_types in events:

        # Iterate over each event
        for event in event_types:

            ical += 'BEGIN:VEVENT{}'.format(CRLF)
            ical += 'DTSTART:{}{}'.format(event.start, CRLF)
            ical += 'DTEND:{}{}'.format(event.end, CRLF)
            ical += 'ORGANIZER:{}{}'.format('University of Liverpool',CRLF)

            if not event.special:
                ical += 'SUMMARY: {} {} ({}){}'.format(event.module_code, event.name, event.type, CRLF)

            else:
                ical += 'SUMMARY: {}{}'.format(event.name, CRLF)

            ical += 'LOCATION:{}{}'.format('Liverpool UK', CRLF)
            ical += 'UID:{}{}'.format(event.uid, CRLF)
            ical += 'TZID:{}{}'.format('Europe/London', CRLF)

            # ALARM
            ical += 'BEGIN:VALARM{}'.format(CRLF)
            ical += 'TRIGGER:-PT5M{}'.format(CRLF)
            ical += 'ACTION:DISPLAY{}'.format(CRLF)
            ical += 'END:VALARM{}'.format(CRLF)
            ical += 'END:VEVENT{}'.format(CRLF)

            # Debug
            if debug:
                print_event(event)

    ical += 'END:VCALENDAR' + CRLF

    directory = os.path.expanduser('~/Downloads/')
    f = open(os.path.join(directory, 'uol_timetable.ics'), 'wb')
    f.write(ical)
    f.close()
