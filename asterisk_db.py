import pickle
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
        cur.execute(sql)
        myconn.commit()
    except Exception as exception:
        print(exception)
        myconn.rollback()

    details = format_query_result(cur, 'one')
    myconn.close()
    return details


def get_ivr_details(company_id, time_now):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    sql = ''' select * from ivrs where company_id = {} 
          and ((start_time <= '{}' and end_time > '{}') 
          or (start_time = '00:00:00' and end_time = '00:00:00')) '''.format(company_id, time_now, time_now)
    try:
        cur.execute(sql)
        myconn.commit()
    except Exception as exception:
        print(exception)
        myconn.rollback()

    details = format_query_result(cur, 'one')
    myconn.close()
    return details


def get_nodes(ivr_id, parent_node_id, last_input):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    sql = ''' select * from ivr_nodes where ivr_id = {} and parent_node_id = {} and 
          last_input = {} '''.format(ivr_id, parent_node_id, last_input)
    try:
        cur.execute(sql)
        myconn.commit()
    except Exception as exception:
        print(exception)
        myconn.rollback()

    details = format_query_result(cur, 'many')
    myconn.close()
    return details


def get_users_by_tag(tag_name):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    sql = ''' select * from peers where tag = '{}' '''.format(tag_name)

    try:
        cur.execute(sql)
        myconn.commit()
    except Exception as exception:
        print(exception)
        myconn.rollback()

    details = format_query_result(cur, 'many')
    myconn.close()
    return details


def insert_call_details(data):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor()

    keys = ','.join(data.keys())
    values = '"' + '","'.join(data.values()) + '"'

    sql = ''' insert into call_details ({}) values ({}) '''.format(keys, values)

    try:
        cur.execute(sql)
        myconn.commit()
    except Exception as exception:
        print(exception)
        myconn.rollback()

    myconn.close()


def insert_session(data):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor()

    data['trace'] = pickle.dumps(data['trace'])

    sql = ''' insert into sessions (unique_id, caller_id, context, extension, call_log, timestamp, trace) 
            values ("{}", "{}", "{}", "{}", {}, "{}", "{}") '''.format(data['unique_id'],data['caller_id'],
            data['context'],data['extension'],data['call_log'],data['timestamp'],data['trace'])

    try:
        cur.execute(sql)
        myconn.commit()
    except Exception as exception:
        print(exception)
        myconn.rollback()

    myconn.close()
