#!/home/vagrant/code/Asterisk-AGI/.vagenv/bin/python

import sys
import mysql.connector 
from asterisk.agi import AGI

agi = AGI()

unique_id = sys.argv[1]
caller_id = sys.argv[2]
context = sys.argv[3]
extension = sys.argv[4]
timestamp = sys.argv[5]

def format_query_result(cursor, type='many'):
    columns = [col[0] for col in cursor.description]
    if type=='many':
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    else:
        rows = dict(zip(columns, cursor.fetchone()))
    return rows

# create the connection object   
myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "root", database = "my_operator")  
# creating the cursor object  
cur = myconn.cursor(buffered=True)
# creating query string 
sql = '''select callers.*, companies.name as company_name from callers left join companies on callers.company_id = companies.id where dnid = '{dnid}' '''.format(dnid=caller_id)

try:
    # inserting the values into the table
    cur.execute(sql)  
    # commit the transaction
    myconn.commit()
except Exception as exception:
    print(exception)
    myconn.rollback()

dial_str = 'SIP/shubham'
agi.answer()
result = agi.execute('EXEC DIAL {dial_str}'.format(dial_str=dial_str))
agi.verbose(result, level=4)

myconn.close()
