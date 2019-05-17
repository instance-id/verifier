#---------------------------------------------#
# Verifier - Discord/Unity Asset Verification #
# Created by isntance.id - http://instance.id #
# github.com/instance-id - system@instance.id #
#---------------------------------------------#
#                                             # 

import pymysql.cursors
import jsoncfg
from datetime import datetime
import traceback
import logging

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

config = jsoncfg.load_config('config/dbconfig.json')
# config = jsoncfg.load_config('../../../config/dbconfig.json')
dbdata = config.dbdata()


def dosql(sql, args=None, commit=False, response=None, num=0):
    conn = pymysql.connect(host=dbdata['address'],
                           user=dbdata['usename'],
                           password=dbdata['password'],
                           db=dbdata['dbname'],
                           charset=dbdata['charset'],
                           cursorclass=pymysql.cursors.DictCursor)

    result = 'Process ended before it was supposed to.'
    try:
        with conn.cursor() as cursor:
            if args is not None:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
            if commit:
                conn.commit()
            if response is not None:
                if response == 'single':
                    result = cursor.fetchone()
                elif response == 'many':
                    result = cursor.fetchmany(num)
                elif response == 'all':
                    result = cursor.fetchall()
                elif response == 'id':
                    result = cursor.lastrowid
            else:
                pass
    finally:
        conn.close()
    if response:
        return result


def db_setup():
    sql = "SELECT * FROM information_schema.tables WHERE `table_name`=%s"
    args = 'validated_users'
    usersresult = dosql(sql, args, False, 'single')

    sql = "SELECT * FROM information_schema.tables WHERE `table_name`=%s"
    args = 'packages'
    packagesresult = dosql(sql, args, False, 'single')
    if usersresult is None and packagesresult is None:
        sql = """CREATE TABLE IF NOT EXISTS validated_users ( 
                        user_id INT (10) NOT NULL auto_increment, 
                        username VARCHAR(50) NOT NULL,
                        email VARCHAR(75),
                        KEY(username),
                        PRIMARY KEY (user_id)
                        ) ENGINE=InnoDB;"""
        dosql(sql, None, True)

        sql = """CREATE TABLE IF NOT EXISTS packages ( 
                        user_id INT(10),
                        username VARCHAR(50) NOT NULL,                    
                        invoice VARCHAR (15) UNIQUE,
                        package VARCHAR(50),
                        purdate VARCHAR(10),
                        verifydate VARCHAR(10),
                        INDEX par_ind(user_id, username), 
                        CONSTRAINT fk_validated_users FOREIGN KEY (user_id) 
                        REFERENCES validated_users(user_id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                        )ENGINE=InnoDB;"""
        dosql(sql, None, True)
        return "Creation of database tables completed."
    else:
        return "Tables already exist: " + usersresult['TABLE_NAME'] + " and " + packagesresult['TABLE_NAME']

#  Invoice lookup for automated verification process
def find_invoice(invoice):
    sql = "SELECT * FROM `packages` WHERE `invoice`=%s"
    args = invoice
    invoiceresult = dosql(sql, args, False, 'single')
    if invoiceresult:
        return True
    else:
        return False


# #  If user has already registered an invoice
# #  append new invoice otherwise create new entry
def add_invoice(username, invoice, package, purdate, email=''):
    sql = "SELECT * FROM `packages` WHERE `invoice`=%s"
    args = invoice
    invoiceresult = dosql(sql, args, False, 'single')
    if invoiceresult is None:
        sql = "SELECT * FROM `validated_users` WHERE `username`=%s"
        args = username
        nameresult = dosql(sql, args, False, 'single')
        if nameresult is not None:
            if nameresult['email'] is None:
                sql = "UPDATE `validated_users` SET `email` = %s WHERE `username` = %s"
                args = email, username
                insertresult = dosql(sql, args, True)

            sql = "INSERT INTO `packages` (`user_id`, `username`, `invoice`, `package`, `purdate`, `verifydate`) VALUES (%s, %s, %s, %s, %s, %s)"
            args = nameresult['user_id'], username, invoice, package, purdate, str(datetime.now().strftime("%Y-%m-%d"))
            result = dosql(sql, args, True)
            return result

        if nameresult is None:
            sql = "INSERT INTO `validated_users` (`username`, `email`) VALUES (%s, %s)"
            args = username, email
            insertresult = dosql(sql, args, True, 'id')

            sql = "INSERT INTO `packages` (`user_id`, `username`, `invoice`, `package`, `purdate`, `verifydate`) VALUES (%s, %s, %s, %s, %s, %s)"
            args = insertresult, username, invoice, package, purdate, str(datetime.now().strftime("%Y-%m-%d"))
            result = dosql(sql, args, True)
            return result
    else:
        return 'Invoice number already registered. Please contact support.'


#  Invoice deletion - use carefully
def delete_invoice(invoice):
    sql = "DELETE FROM `packages` WHERE `invoice`=%s"
    args = invoice
    invoiceresult = dosql(sql, args, True)
    return 'Deletion Completed'


#  ------------------------ Manual lookup processes -------------------------------
def search_invoice(invoice):
    sql = "SELECT * FROM `packages` WHERE `invoice`=%s"
    args = invoice
    invoiceresult = dosql(sql, args, False, 'single')
    if invoiceresult:
        return invoiceresult['username'], invoiceresult
    else:
        return 'No invoice found', False


def search_user(username):
    sql = "SELECT `username` FROM `validated_users` WHERE `username` LIKE %s"
    args = ("%" + username + "%",)
    userresult = dosql(sql, args, False, 'all')
    sql = "SELECT `invoice`, `package`, `purdate`, `verifydate` FROM `packages` WHERE `username` LIKE %s"
    args = ("%" + username + "%",)
    userresult2 = dosql(sql, args, False, 'all')
    if len(userresult) is 0:
        return 'User not found.'
    elif len(userresult2) is 0:
        return userresult
    else:
        packlist = {'packages': userresult2}
        userresult[0].update(packlist)
        if userresult:
            return userresult
        else:
            return 'No User found'
