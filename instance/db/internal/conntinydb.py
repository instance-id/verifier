from tinydb import TinyDB, where
from datetime import datetime
import traceback
import logging
import re

# <editor-fold desc="Logging definitions">
from colorlog import ColoredFormatter

log = logging.getLogger(__name__)
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
# </editor-fold>

db = TinyDB('instance/db/db.json', default_table='validated_users')


#  Invoice lookup for automated verification process
def find_invoice(invnum):
    inv = db.contains(where('packages').any(where('invoice') == invnum))
    if inv:
        return True
    else:
        return False


#  If user has already registered an invoice
#  append new invoice otherwise create new entry
def add_invoice(username, invoice, package, purdate, email=''):
    user = db.search(where('username') == username)
    element = db.get(where('username') == username)
    if len(user) > 0:
        try:
            if user[0]['email'] is '':
               user[0].update({'email': email})
               user[0]['packages'].append(
                      {'invoice': invoice,
                       'package': package,
                       'purdate': purdate,
                       'verifydate': str(datetime.now().strftime("%Y-%m-%d"))})

            db.update(user[0], eids=[element.eid])
        except Exception as e:
            traceback.print_exc()
    else:
        try:
            db.insert({
                'username': username, 'email': email,
                'packages': [{'invoice': invoice,
                              'package': package,
                              'purdate': purdate,
                              'verifydate': str(datetime.now().strftime("%Y-%m-%d"))}
                ]
            })
        except Exception as e:
            traceback.print_exc()


#  Invoice lookup for automated verification process
def delete_invoice(invnum):
    user = db.search(where('packages').any(where('invoice') == invnum))
    inv = db.get(where('packages').any(where('invoice') == invnum))
    itemIndex = 0
    add = True
    if inv:
        try:
            for package in user[0]['packages']:
                if package['invoice'] == invnum:
                    add = False
                    break
                if add:
                    itemIndex += 1

            del (user[0]['packages'][itemIndex])
            db.update(user[0], eids=[inv.eid])
            return 'Deletion Completed'
        except:
            return 'Deletion Failed'
    else:
        return 'No invoice found.'


#  ------------------------ Manual lookup processes -------------------------------
def search_invoice(invnum):
    user = db.search(where('packages').any(where('invoice') == invnum))
    inv = db.get(where('packages').any(where('invoice') == invnum))
    itemIndex = 0
    add = True
    if inv:
        try:
            for package in user[0]['packages']:
                if package['invoice'] == invnum:
                    add = False
                    break
                if add:
                    itemIndex += 1

            name = inv['username']
            invoice = user[0]['packages'][itemIndex]
            return name, invoice
        except:
            return 'No invoice found.', False
    else:
        result = 'No invoice found.'
        return result, False


def search_user(user):
    usr = db.search(where('username').matches(user, flags=re.IGNORECASE))
    if usr:
        return usr
    else:
        result = 'No user found.'
        return result

