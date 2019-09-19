#!/home/vagrant/code/Asterisk-AGI/.vagenv/bin/python

import sys
import datetime
import asterisk_db
from asterisk.agi import AGI

agi = AGI()

unique_id = sys.argv[1]
caller_id = sys.argv[2]
context = sys.argv[3]
extension = sys.argv[4]
timestamp = sys.argv[5]

parent_node_id = 0
node_input = 0


session = {
    'unique_id' : unique_id,
    'dnid' : caller_id,
    'context' : context,
    'extension' : extension,
    'timestamp' : timestamp,
    'call_log' : False,
    'trace' : []
}


def start_ivr_interation(ivr_id, parent_node_id=0, last_input=0):
    nodes = asterisk_db.get_nodes(ivr_id, parent_node_id, last_input)
    for node in nodes:
        command_handler(node)


def command_handler(node):
    global node_input, session

    if node['action'] == 'dial':
        agents = asterisk_db.get_users_by_tag(node['users_tag'])
        agent_list = []
        for agent in agents:
            agent_list.append('{}/{}'.format(agent['type'], agent['name']))
        agent_string = '&'.join(agent_list)

        session['trace'].append({
            'action' : node['action'],
            'agent_string' : agent_string
        })

        filename = '/home/vagrant/code/Asterisk-AGI/storage/recordings/{} {}.wav'.format(node['users_tag'], str(datetime.datetime.now()))
        agi.execute('EXEC MIXMONITOR "{}"'.format(filename))
        agi.execute('EXEC DIAL {},20,g'.format(agent_string))

        call_data = {
            'unique_id': agi.get_variable('UNIQUEID'),
            'dnid': caller_id,
            'channel': agi.get_variable('CHANNEL'),
            'context': agi.get_variable('CONTEXT'),
            'peer_name' : agi.get_variable('DIALEDPEERNAME'),
            'peer_type' : (agi.get_variable('DIALEDPEERNAME')).split('/')[0],
            'peer_number' : agi.get_variable('DIALEDPEERNUMBER'),
            'answered_time': agi.get_variable('ANSWEREDTIME'),
            'calling_pres': agi.get_variable('CALLINGPRES'),
            'dialed_time' : agi.get_variable('DIALEDTIME'),
            'dial_status' : agi.get_variable('DIALSTATUS'),
            'hangup_cause': agi.get_variable('HANGUPCAUSE'),
            'extension': agi.get_variable('EXTEN'),
            'language': agi.get_variable('LANGUAGE'),
            'meet_me_secs': agi.get_variable('MEETMESECS'),
            'priority': agi.get_variable('PRIORITY'),
            'rdnis' : agi.get_variable('RDNIS'),
            'sip_domain' : agi.get_variable('SIPDOMAIN'),
            'sip_codec' : agi.get_variable('SIP_CODEC'),
            'sip_call_id' : agi.get_variable('SIPCALLID'),
            'sip_user_agent' : agi.get_variable('SIPUSERAGENT'),
            'transfer_capability' : agi.get_variable('TRANSFERCAPABILITY'),
            'txt_cid_name' : agi.get_variable('TXTCIDNAME'),
            'recorded_file' : filename,
            'datetime': timestamp
        }

        asterisk_db.insert_call_details(call_data)
        session['call_log'] = True

    elif node['action'] == 'playback':
        session['trace'].append({
            'action' : node['action'],
            'filename' : node['file']
        })
        node_input = agi.get_option(node['file'], '12345')
    elif node['action'] == 'input':
        if node_input != 0:
            ivr_id = node['ivr_id']
            parent_node_id = node['id']
            session['trace'].append({
                'action': node['action'],
                'ivr_id': ivr_id,
                'parent_node_id': parent_node_id
            })
            start_ivr_interation(ivr_id, parent_node_id, node_input)
        else:
            pass
    else:
        session['trace'].append({
            'action': node['action'],
            'hangup_cause': 0
        })
        agi.hangup()


def initiate_call_handling(ivr_id):
    global session
    agi.answer()
    start_ivr_interation(ivr_id)
    session['trace'].append({
        'action': 'hangup',
        'hangup_cause': 0
    })
    asterisk_db.insert_session(session)
    agi.hangup()


call_details = asterisk_db.get_call_details(caller_id)
ivr_details = asterisk_db.get_ivr_details(call_details['company_id'], timestamp.split(' ')[1])
initiate_call_handling(ivr_details['id'])