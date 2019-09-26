import json
import mysql.connector

def format_timedelta_to_string(delta):
    return  '0' + str(delta) if len(str(delta)) == 7 else str(delta)


def format_query_result(cursor, type='many'):
    columns = [col[0] for col in cursor.description]
    if type == 'many':
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    elif type == 'one':
        rows = dict(zip(columns, cursor.fetchone()))
    else:
        rows = []
    return rows


def get_ivr_by_time(time, ivrs):
    selected_ivr = {}
    for ivr in ivrs:
        start_time = format_timedelta_to_string(ivr['start_time'])
        end_time = format_timedelta_to_string(ivr['end_time'])
        if start_time < end_time:
            if start_time <= time < end_time:
                selected_ivr = ivr
        else:
            if ((start_time <= time) and (time < '24:00:00')) or (
                    ('00:00:00' <= time) and (time < end_time)):
                selected_ivr = ivr
    return selected_ivr


def get_call_details(caller_id):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    details = {}
    sql = ''' select callers.*, companies.name as company_name from callers 
        left join companies on callers.company_id = companies.id 
        where dnid = '{}' '''.format(caller_id)

    try:
        cur.execute(sql)
        myconn.commit()
        details = format_query_result(cur, 'one')
    except Exception as exception:
        print(exception)
        myconn.rollback()

    myconn.close()
    return details


def get_ivr_details(company_id, time_now):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    details = {}
    ivrs = []
    sql = ''' select * from ivrs where company_id = {} '''.format(company_id)
    try:
        cur.execute(sql)
        myconn.commit()
        ivrs = format_query_result(cur, 'many')
    except Exception as exception:
        print(exception)
        myconn.rollback()
    details = get_ivr_by_time(time_now, ivrs)
    myconn.close()
    return details


def get_nodes(ivr_id, parent_node_id, last_input):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    details = []
    sql = ''' select * from ivr_nodes where ivr_id = {} and parent_node_id = {} and 
          last_input = {} '''.format(ivr_id, parent_node_id, last_input)
    try:
        cur.execute(sql)
        myconn.commit()
        details = format_query_result(cur, 'many')
    except Exception as exception:
        print(exception)
        myconn.rollback()

    myconn.close()
    return details


def get_users_by_tag(tag_name):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="my_operator")
    cur = myconn.cursor(buffered=True)
    details = []
    sql = ''' select * from peers where tag = '{}' '''.format(tag_name)
    try:
        cur.execute(sql)
        myconn.commit()
        details = format_query_result(cur, 'many')
    except Exception as exception:
        print(exception)
        myconn.rollback()

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

    data['trace'] = json.dumps(data['trace'])

    sql = ''' insert into sessions (unique_id, dnid, context, extension, call_log, timestamp, trace) 
            values ('{}', '{}', '{}', '{}', {}, '{}', '{}') '''.format(data['unique_id'],data['dnid'],
            data['context'],data['extension'],data['call_log'],data['timestamp'],data['trace'])

    try:
        cur.execute(sql)
        myconn.commit()
    except Exception as exception:
        print(exception)
        myconn.rollback()

    myconn.close()
