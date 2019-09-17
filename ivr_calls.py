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

call_details = asterisk_db.get_call_details(caller_id)

time_now = datetime.datetime.now().time()

extension_plan = asterisk_db.get_extension_plan(call_details['company_id'], context, time_now)

dial_str = 'SIP/shubham'
agi.answer()
result = agi.execute('EXEC DIAL {dial_str}'.format(dial_str=dial_str))
agi.verbose(result, level=4)
agi.hangup()
