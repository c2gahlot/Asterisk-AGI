import mysql.connector


def format_query_result(cursor, type='many'):
    columns = [col[0] for col in cursor.description]
    if type=='many':
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    else:
        rows = dict(zip(columns, cursor.fetchone()))
    return rows


def get_call_details(caller_id):

    # create the connection object
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")

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

    details = format_query_result(cur, 'one')
    myconn.close()

    return details
