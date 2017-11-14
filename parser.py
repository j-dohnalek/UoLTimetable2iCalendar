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
from datetime import datetime
import re
import hashlib

# format of the outputted date of the lecture
DATE_FORMAT = '%Y%m%dT%H%M00'

# match pattern of standard module code
# help to determine if the schedule event is something special
# (i.e. Year in industry lecture)
PATTERN = r'([A-Z]{4})([0-9]{3})'

class Event:
    """ Parse the all the key event information """

    # Filter words from event name
    __replace = ['(Lecture)', '(Laboratory)']

    # Special lecture not matching standard lecture or Laboratory
    __special = False

    # Determine if the event is lecture or lab
    __is_lecture = True

    # Not parsed information provided from the website
    __full_name = None

    # Raw website string
    __raw_event_info = None
    __raw_event_time_info = None

    # Isolated module code
    __module_code = None

    # Event start time
    __start = None

    # Event end time
    __end = None

    def __init__(self, module, timeinfo):
        """ Define the raw event info, event time """

        # EVENT NAME
        self.__raw_event_info =  module.text.strip()
        self.parse_module()
        # EVENT TIME
        self.__raw_event_time_info = timeinfo.strip().replace('\r\n', '').split()
        self.parse_time()

    def parse_time(self):
        """ Parse the raw event time information to date and start & end time """
        day = str(int(self.__raw_event_time_info[1]))
        month = self.__raw_event_time_info[2]
        year = self.__raw_event_time_info[3]
        start = self.__raw_event_time_info[4]
        end = self.__raw_event_time_info[6]

        start_time = '{} {} {} {}'.format(day, month, year, start)
        end_time = '{} {} {} {}'.format(day, month, year, end)
        # Event Start
        self.__start = datetime.strptime(start_time, '%d %B %Y %H:%M').strftime(DATE_FORMAT)
        self.__end = datetime.strptime(end_time, '%d %B %Y %H:%M').strftime(DATE_FORMAT)

    def parse_module(self):
        """ Parse the raw event name to module code """

        # Module code
        module_split = self.__raw_event_info.split('-')
        self.__module_code = module_split[0]
        for s in self.__replace:
            self.__module_code = self.__module_code.replace(s, '').strip()

        # Pattern matches LLLLNNN i.e. COMP211 not special event else yes
        pattern = re.compile(PATTERN)
        self.__special = pattern.match(self.__module_code) is None

        # Determine if lecture or Lab
        self.__is_lecture = 'Lecture' in self.__raw_event_info

        # Filter words from the event name
        self.__replace.append(self.__module_code + ' -')
        self.__name = self.__raw_event_info
        for s in self.__replace:
            self.__name = self.__name.replace(s, '').strip()

    @property
    def uid(self):
        """ Generate unique id """
        s = '{}{}{}'.format(self.__name, self.__start, self.__end)
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

    @property
    def type(self):
        """ Lecture or lab """
        if self.__is_lecture:
            return 'LEC'
        else:
            return 'LAB'

    @property
    def module_code(self):
        """ Standard module code """
        return self.__module_code

    @property
    def name(self):
        """ RAW string from the website """
        return self.__name

    @property
    def start(self):
        """ Start time of the event """
        return self.__start

    @property
    def end(self):
        """ end time of the lecture """
        return self.__end

    @property
    def special(self):
        """ Special event (i.e. year in industry lecture) """
        return self.__special
