#!/home/vagrant/codes/Asterisk-AGI/.vagenv/bin/python

import sys
from asterisk.agi import AGI

agi = AGI()

callee = sys.argv[1]


def trigger_call(callee):
    agi.execute('EXEC DIAL {},20,g'.format(callee))
    agi.hangup()

trigger_call(callee)
