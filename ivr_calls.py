#!/home/vagrant/code/Asterisk-AGI/.vagenv/bin/python

import sys
import asterisk_db
from asterisk.agi import AGI

agi = AGI()

unique_id = sys.argv[1]
caller_id = sys.argv[2]
context = sys.argv[3]
extension = sys.argv[4]
timestamp = sys.argv[5]
node_id = None
node_input = None


def start_ivr_interation(ivr_id):
    agi.verbose('IVR ID : {}'.format(ivr_id), level=4)
    nodes = asterisk_db.get_nodes(ivr_id)
    for node in nodes:
        command_handler(node)


def command_handler(node):
    global node_id, node_input

    node_id = node['id']
    if node['action'] == 'dial':
        agi.execute('EXEC DIAL {}'.format(node['user']))
    elif node['action'] == 'playback':
        node_input = agi.get_option(node['file'], '12345')
    elif node['action'] == 'input':
        if node_input is not None:
            ivr_details = asterisk_db.get_ivr_id_from_input(node_id, node_input)
            start_ivr_interation(ivr_details['ivr_id'])
        else:
            pass
    elif node['action'] == 'hangup':
        agi.hangup()
    else:
        agi.hangup()


call_details = asterisk_db.get_call_details(caller_id)

time_now = timestamp.split(' ')[1]

ivr_details = asterisk_db.get_ivr_details(call_details['company_id'], time_now)

agi.answer()

start_ivr_interation(ivr_details['id'])

agi.hangup()
