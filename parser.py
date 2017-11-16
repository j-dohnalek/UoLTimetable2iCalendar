"""
Prepare the data for the iCalendar file generation
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
from datetime import datetime, timedelta
import re
import hashlib
from bs4 import BeautifulSoup


# format of the outputted date of the lecture
DATE_FORMAT = '%Y%m%dT%H%M00'


def parse_timetable(opener, blocks):
    """
    GET NEXT WEEK/s
    :param opener: access to the website including the session
    :param blocks: how many weeks to download
    :return filtered list of all events
    """
    events = []
    urls = []
    url = 'https://timetables.liv.ac.uk/Home/Next7Days'
    event_ids = []

    for multiplier in range(0, blocks):
        now = datetime.now() + timedelta(days=7*multiplier)
        next_date = now.strftime("%d%m%Y")
        urls.append(url + '?date={}'.format(next_date))

    # Fetch 28 day block
    for url in urls:

        print 'Downloading', url
        resp = opener.open(url)
        soup = BeautifulSoup(resp.read(), 'lxml')

        # Fetch each event of the 28 day block details
        for link in soup.find_all('a'):

            if link.get('href')[:7] == 'Details':

                # Isolate the event id
                event_id = link.get('href').replace('Details?event=','')

                # Fetch the event id information
                _url = 'https://timetables.liv.ac.uk/Home/Details?event={}'.format(event_id)
                event_details = opener.open(_url)
                html = event_details.read()
                _soup = BeautifulSoup(html, 'lxml')

                # isolate the div containing information
                event_div =  _soup.findAll("div", { "class" : "event" })[0]

                # Parse event name
                event_name = event_div.find('h1').contents[0]

                # Parse date
                event_date = event_div.find('h2').contents[0]

                # Parse the remaining information
                info_map = {1: 'start', 3: 'end', 5: 'room', 7: 'module' }
                event_info = {}
                event_info['name'] = event_name
                event_info['date'] = event_date
                count_iteration = 0

                for tag in event_div.find_all('span'):
                    if count_iteration % 2 != 0 and count_iteration < 9:
                        try:
                            event_info[info_map[count_iteration]] = tag.contents[0]
                        except IndexError:
                            event_info[info_map[count_iteration]] = ''
                    count_iteration += 1
                e = Parser(event_info)
                events.append(e)

    return events


class Parser:
    """ Parse the all the key event information """


    __default_event = -1

    __event_types = ['lecture', 'laboratory', 'class test']

    # Not parsed information provided from the website
    __name = None

    # Raw website string
    __event_info = None

    # Isolated module code
    __room = None

    # Event start time
    __start = None

    # Event end time
    __end = None

    def __init__(self, event_info):
        """ Define the raw event info, event time """
        self.__event_info = event_info
        # EVENT NAME
        self.parse_name()
        # EVENT TIME
        self.parse_time()

    def parse_name(self):
        self.__name = self.__event_info['name']
        self.__room = self.__event_info['room']

        for event_type in self.__event_types:
            if event_type in self.__name.lower():
                self.__default_event = event_type


    def parse_time(self):
        """ Parse the raw event time information to date and start & end time """
        parsed_date  = self.__event_info['date'].replace(',','').split(' ')
        day = str(int(parsed_date[1]))
        month = parsed_date[2]
        year = parsed_date[3]

        start = self.__event_info['start']
        end = self.__event_info['end']

        start_time = '{} {} {} {}'.format(day, month, year, start)
        end_time = '{} {} {} {}'.format(day, month, year, end)
        # Event Start
        self.__start = datetime.strptime(start_time, '%d %B %Y %H:%M').strftime(DATE_FORMAT)
        self.__end = datetime.strptime(end_time, '%d %B %Y %H:%M').strftime(DATE_FORMAT)

    @property
    def uid(self):
        """ Generate unique id """
        s = '{}{}{}'.format(self.__name, self.__start, self.__end)
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

    @property
    def name(self):
        """ Event name """
        return self.__name

    @property
    def type(self):
        """ Lecture, Lab, Class test """
        if self.__default_event == -1:
            return self.__name
        else:
            return self.__default_event.title()

    @property
    def module(self):
        """ Module """
        return self.__event_info['module']


    @property
    def room(self):
        """ end time of the lecture """
        return self.__room


    @property
    def start(self):
        """ Start time of the event """
        return self.__start

    @property
    def end(self):
        """ end time of the lecture """
        return self.__end
