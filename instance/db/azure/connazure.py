import pyodbc
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

config = jsoncfg.load_config('instance/config/dbconfig.json')
# config = jsoncfg.load_config('../../../config/dbconfig.json')

dbdata = config.dbdata()
dbprefix = dbdata['dbprefix']


def dosql(sql, args=None, commit=False, response=None, num=0, curret=False):

    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = 'DRIVER=' + driver
    cnxn += ';PORT=1433;SERVER=' + dbdata['address']
    cnxn += ';PORT=1443;DATABASE=' + dbdata['dbname']
    cnxn +=';UID=' + dbdata['usename']
    cnxn +=';PWD=' + dbdata['password']

    conn = pyodbc.connect(cnxn)
    finish = False
    result = 'Process ended before it was supposed to.'
    try:
        with conn.cursor() as cursor:
            if args is not None:
                cur = cursor.execute(sql, args)
            else:
                cur = cursor.execute(sql)
            if curret is True:
                return cur
            if commit is True:
                conn.commit()
            if response is not None:
                if response == 'single':
                    result = cursor.fetchone()
                elif response == 'many':
                    result = cursor.fetchmany(num)
                elif response == 'all':
                    result = cursor.fetchall()
                elif response == 'id':
                    result = cursor.fetchone()
            else:
                pass
    finally:
        conn.close()
    if response:
        return result


# (sql, args=None, commit=False, response=None, num=0)
def db_setup():
    validated_users = dbprefix + 'validated_users'
    packages = dbprefix + 'packages'

    args = validated_users
    sql = "SELECT * FROM information_schema.tables WHERE table_name= '%s'" % args
    usersresult = dosql(sql, None, False, 'single')

    args = packages
    sql = "SELECT * FROM information_schema.tables WHERE table_name = '%s'" % args
    packagesresult = dosql(sql, None, False, 'single')

    if usersresult is None:
        args = (validated_users, validated_users)
        sql = f"""
        IF NOT EXISTS 
          (select * from INFORMATION_SCHEMA.TABLES where TABLE_NAME = '%s')
            CREATE TABLE %s ( 
            user_id int IDENTITY PRIMARY KEY, 
            username VARCHAR(50) NOT NULL,
            email VARCHAR(75),
          )""" % args

        dosql(sql, None, True)

    if packagesresult is None:
        args = (packages, packages, validated_users)
        sql = f"""
        IF NOT EXISTS 
         (select * from INFORMATION_SCHEMA.TABLES where TABLE_NAME = '%s')
           CREATE TABLE %s ( 
           ID INT IDENTITY PRIMARY KEY,
           user_id int FOREIGN KEY REFERENCES %s (user_id),
           username VARCHAR(50) NOT NULL,                    
           invoice VARCHAR (15) UNIQUE,
           package VARCHAR(50),
           purdate VARCHAR(10),
           verifydate VARCHAR(10),
         )""" % args

        dosql(sql, None, True)
        return "Creation of database tables completed."
    else:
        return "Tables already exist: " + usersresult[2] + " and " + packagesresult[2]


#  Invoice lookup for automated verification process
# (sql, args=None, commit=False, response=None, num=0)
def find_invoice(invoice):
    args = dbprefix, invoice
    sql = "SELECT * FROM [%spackages] WHERE [invoice] = '%s'" % args
    invoiceresult = dosql(sql, None, False, 'single')
    if invoiceresult:
        return True
    else:
        return False


#  If user has already registered an invoice
#  append new invoice otherwise create new entry
# (sql, args=None, commit=False, response=None, num=0)
def add_invoice(username, invoice, package, purdate, email=''):
    args = dbprefix, invoice
    sql = "SELECT * FROM [%spackages] WHERE [invoice] = '%s'" % args
    invoiceresult = dosql(sql, None, False, 'single')
    if invoiceresult is None:
        args = dbprefix, username
        sql = "SELECT * FROM [%svalidated_users] WHERE [username] = '%s'" % args
        nameresult = dosql(sql, None, False, 'single')
        if nameresult is not None:
            if nameresult:
                args = dbprefix, email, username,
                sql = "UPDATE [%svalidated_users] SET [email] = '%s' WHERE [username] = '%s'" % args
                dosql(sql, None, True)
            args = dbprefix, int(nameresult[0]), username, invoice, package, purdate, str(datetime.now().strftime("%Y-%m-%d"))
            sql = "INSERT INTO [%spackages] ([user_id], [username], [invoice], [package], [purdate], [verifydate]) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % args
            result = dosql(sql, None, True)
            return result
        if nameresult is None:
            try:
                args = dbprefix, username, email
                sql = "INSERT INTO [%svalidated_users] ([username],[email]) VALUES ('%s', '%s')" % args
                dosql(sql, None, True)
                args = dbprefix, username
                sql = "SELECT [user_id] FROM [%svalidated_users] WHERE [username] = '%s'" % args
                insertresult = dosql(sql, None, False, 'single')
                if insertresult:
                    args = dbprefix, int(insertresult.user_id), username, invoice, package, purdate, str(
                        datetime.now().strftime("%Y-%m-%d"))
                    sql = "INSERT INTO [%spackages] ([user_id], [username], [invoice], [package], [purdate], [verifydate]) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s')" % args
                    result = dosql(sql, None, True)
                    return result
            except Exception as e:
                print(f'Could not insert row.')
                traceback.print_exc()
    else:
        return 'Invoice number already registered. Please contact support.'


#  Invoice deletion - use carefully
def delete_invoice(invoice):
    args = dbprefix, invoice
    sql = "DELETE FROM [%spackages] WHERE [invoice] = '%s'" % args
    invoiceresult = dosql(sql, None, True)
    return 'Deletion Completed'


#  ------------------------ Manual lookup processes -------------------------------
def search_invoice(invoice):
    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = 'DRIVER=' + driver
    cnxn += ';PORT=1433;SERVER=' + dbdata['address']
    cnxn += ';PORT=1443;DATABASE=' + dbdata['dbname']
    cnxn +=';UID=' + dbdata['usename']
    cnxn +=';PWD=' + dbdata['password']
    conn = pyodbc.connect(cnxn)

    with conn.cursor() as cursor:
        args = dbprefix, invoice
        sql = "SELECT * FROM [%spackages] WHERE [invoice] = '%s'" % args
        invoiceresult = cursor.execute(sql)
        if invoiceresult is not None:
            data1 = []
            columns = [column[0] for column in invoiceresult.description]
            for row in invoiceresult.fetchall():
                data1.append(dict(zip(columns, row)))
                if not data1:
                    conn.close()
                    return 'No invoice found', False
    if invoiceresult is not None:
        conn.close()
        if not data1:
            return 'No invoice found', False
        data2 = [d for d in data1][0]
        return data2['username'], data2
    else:
        conn.close()
        return 'No invoice found', False


def search_user(username):
    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = 'DRIVER=' + driver
    cnxn += ';PORT=1433;SERVER=' + dbdata['address']
    cnxn += ';PORT=1443;DATABASE=' + dbdata['dbname']
    cnxn +=';UID=' + dbdata['usename']
    cnxn +=';PWD=' + dbdata['password']

    conn = pyodbc.connect(cnxn)

    with conn.cursor() as cursor:
        args = (dbprefix, username + '%',)
        sql = "SELECT [username] FROM [%svalidated_users] WHERE [username] LIKE '%s'" % args
        userresult = cursor.execute(sql)
        data1 = []
        columns = [column[0] for column in userresult.description]
        for row in userresult.fetchall():
            data1.append(dict(zip(columns, row)))

    with conn.cursor() as cursor:
        args = (dbprefix, username + '%',)
        sql = "SELECT [invoice], [package], [purdate], [verifydate] FROM [%spackages] WHERE [username] LIKE '%s'" % args
        userresult2 = cursor.execute(sql)
        data2 = []
        columns2 = [column[0] for column in userresult2.description]
        for row in userresult2.fetchall():
            data2.append(dict(zip(columns2, row)))
    conn.close()
    if len(data1) is 0:
        return 'User not found.'
    elif len(data2) is 0:
        return data1
    else:
        packlist = {'packages': data2}
        data1[0].update(packlist)
        if data1:
            return data1
        else:
            return 'No User found'
