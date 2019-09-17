import mysql.connector


def format_query_result(cursor, type='many'):
    columns = [col[0] for col in cursor.description]
    if type == 'many':
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    elif type == 'one':
        rows = dict(zip(columns, cursor.fetchone()))
    else:
        rows = []
    return rows


def get_call_details(caller_id):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    sql = ''' select callers.*, companies.name as company_name from callers 
        left join companies on callers.company_id = companies.id 
        where dnid = '{}' '''.format(caller_id)

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


def get_extension_plan(company_id, context, time_now):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    sql = ''' select * from ivrs where company_id = {} and context = '{}' 
        and ((start_time <= '{}' and end_time > '{}') 
        or (start_time = '00:00:00' and end_time = '00:00:00')) '''.format(company_id, context, time_now, time_now)

    try:
        cur.execute(sql)
        myconn.commit()
    except Exception as exception:
        print(exception)
        myconn.rollback()

    details = format_query_result(cur, 'one')
    myconn.close()
    return details
