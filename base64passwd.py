"""
Generate base 64 encoded login file
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

import base64
import sys

def encode(s):
    return base64.encodestring(s)

def decode(s):
    return base64.decodestring(s)

SALT = "bv8fFhizx31HKwbI<G:6Z7)<0(m]5n1z).^X}!-;y0VS)55]f-Hi-)hv?3:[DC)r"

def main():

    username = ''
    password = ''

    try:
        username = sys.argv[1]
        password = sys.argv[2]
    except IndexError:
        print "usage: python base64passwd.py <username> <password>"
        sys.exit()

    base64_username = encode(encode(username) + SALT)
    base64_password = encode(encode(password) + SALT)

    w = '{}:{}'.format(base64_username, base64_password)
    w = w.replace('\n','')
    f = open('passwd', 'w')
    f.write(w)
    f.close()
    print "Ok"

########################################################

if __name__ == '__main__':
    main()
