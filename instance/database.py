import jsoncfg
import traceback
import logging

# <editor-fold desc="Logging definitions">
from colorlog import ColoredFormatter

log = logging.getLogger(__name__)
LOG_LEVEL = logging.INFO
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
# </editor-fold>

config = jsoncfg.load_config('instance/config/dbconfig.json')


def trim_invoice(invoice):
    chars = "IN"
    inv = str(invoice)
    for c in chars:
        if c in invoice:
            inv = inv.replace(c, "")
    return inv


#  Invoice lookup for automated verification process
def find_invoice(invoice):
    inv = trim_invoice(invoice)
    result = db.find_invoice(inv)
    return result


#  If user has already registered an invoice
#  append new invoice otherwise create new entry
def add_invoice(username, invoice, package, purdate, email=''):
    inv = trim_invoice(invoice)
    result = db.add_invoice(username, inv, package, purdate, email)
    return result


#  Invoice lookup for automated verification process
def delete_invoice(invoice):
    inv = trim_invoice(invoice)
    result = db.delete_invoice(inv)
    return result,


#  ------------------------ Manual processes -------------------------------
def search_invoice(invoice):
    inv = trim_invoice(invoice)
    result, result2 = db.search_invoice(inv)
    return result, result2


def search_user(user):
    result = db.search_user(user)
    return result


def db_setup():
    d = config.database()
    d_low = d.lower().strip()
    print(d_low)
    if d_low == "internal":
        result = 'Setup is not necessary on the internal database.'
        return result
    else:
        result = db.db_setup()
        return result


#  ------------------------ Database selection -----------------------------
class Databases(object):
    def __init__(self):
        self.a = 1

    def db_switch(self, arg):
        low_arg = arg.lower().strip()
        dbn = {
            "internal": "conntinydb",
            "mysql": "connmysql",
            "azure": "connazure",
            "mongodb": "connmongodb",
        }
        dbt = dbn.get(low_arg, "error")

        if 'error' in dbt:
            exit("Database type missing or incorrect in dbconfig.json")
        dbm = getattr(self, dbt, lambda: "Error")

        return dbm()

    def conntinydb(self):
        print('Importing internal DB configuration')
        try:
            global db
            import instance.db.internal.conntinydb as db
        except Exception as e:
            traceback.print_exc()

        return 'InternalDB configuration loaded'

    def connmysql(self):
        print('Importing MySQL configuration')
        try:
            global db
            import instance.db.mysql.connmysql as db
        except Exception as e:
            traceback.print_exc()

        return 'MySQL configuration loaded'

    def connazure(self):
        print('Importing Azure SQL configuration')
        try:
            global db
            import instance.db.azure.connazure as db
        except Exception as e:
            traceback.print_exc()

        return 'MySQL configuration loaded'

    def determine_db(self):
        d = Databases.db_switch(self, config.database())
        return d


def main():
    database = Databases()
    database.determine_db()


if __name__ == "__main__":
    main()
