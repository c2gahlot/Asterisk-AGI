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

parent_node_id = 0
node_input = 0


def start_ivr_interation(ivr_id, parent_node_id=0, last_input=0):
    nodes = asterisk_db.get_nodes(ivr_id, parent_node_id, last_input)
    for node in nodes:
        command_handler(node)


def command_handler(node):
    global node_id, node_input

    if node['action'] == 'dial':
        agi.execute('EXEC DIAL {}'.format(node['user']))
    elif node['action'] == 'playback':
        node_input = agi.get_option(node['file'], '12345')
    elif node['action'] == 'input':
        if node_input != 0:
            ivr_id = node['ivr_id']
            parent_node_id = node['id']
            start_ivr_interation(ivr_id, parent_node_id, node_input)
        else:
            pass
    elif node['action'] == 'hangup':
        agi.hangup()
    else:
        agi.hangup()


def initiate_call_handling(ivr_id):
    agi.answer()
    start_ivr_interation(ivr_id)
    agi.hangup()


call_details = asterisk_db.get_call_details(caller_id)
ivr_details = asterisk_db.get_ivr_details(call_details['company_id'], timestamp.split(' ')[1])
initiate_call_handling(ivr_details['id'])