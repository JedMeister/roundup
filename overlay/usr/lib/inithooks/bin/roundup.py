#!/usr/bin/python
"""Set Roundup admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import os
import sys
import getopt
import inithooks_cache
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Roundup Password",
            "Enter new password for the Roundup 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "Roundup Email",
            "Enter email address for the Roundup 'admin' account.",
            "admin@example.com")

    inithooks_cache.write('APP_EMAIL', email)

    hashpass = "{SHA}" + hashlib.sha1(password).hexdigest()

    m = MySQL()
    m.execute('UPDATE roundup._user SET _address=\"%s\" WHERE _username=\"admin\";' % email)
    m.execute('UPDATE roundup._user SET _password=\"%s\" WHERE _username=\"admin\";' % hashpass)
    os.system('service apache2 restart')
    

if __name__ == "__main__":
    main()

