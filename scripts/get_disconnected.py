#!/home/vagrant/codes/Asterisk-AGI/.vagenv/bin/python

import sys, os

channel_name = sys.argv[1]
channel_info = os.system("sudo asterisk -rx 'core show channel {}'".format(channel_name))
channel_info_list = channel_info.splitlines()
data = {}
for line in channel_info_list:
    if ":" in line:
        line = line.strip()
        line = line.split(':')
        if 'level' not in line[0]:
            data[line[0].strip()] = line[1].strip()
        else:
            if 'level' not in data.keys():
                data['level'] = []
            level_number = int(line[0].split(' ')[1]) - 1
            if len(data['level']) <= level_number:
                for i in range((len(data['level']) - level_number)+1):
                    data['level'].append({})
            level_info = line[1].strip().split('=')
            data['level'][level_number][level_info[0]] = level_info[1]

sys.stdout.write(data['level'][-1]['dstchannel'])
sys.stdout.flush()
sys.exit(0)
