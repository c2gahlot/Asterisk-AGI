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

call_details = asterisk_db.get_call_details(caller_id)
print(call_details)
dial_str = 'SIP/shubham'
agi.answer()
result = agi.execute('EXEC DIAL {dial_str}'.format(dial_str=dial_str))
agi.verbose(result, level=4)


