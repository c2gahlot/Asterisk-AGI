import random
import unittest
import datetime
import asterisk_db


class AsteriskDBTest(unittest.TestCase):

    def test_get_call_details(self):
        cases = [{'sample_id': 100}]
        case = cases[0]
        call_details = asterisk_db.get_call_details(case['sample_id'])
        call_details_keys = call_details.keys()
        self.assertIn('dnid', call_details_keys)
        self.assertIn('company_id', call_details_keys)
        self.assertIn('company_name', call_details_keys)
        self.assertIsInstance(call_details['dnid'], str)
        self.assertIsInstance(call_details['company_id'], int)
        self.assertIsInstance(call_details['company_name'], str)

    def test_get_ivr_details(self):
        cases = [{'company_id': 1, 'timestamp': '04:00:00'}]
        case = cases[0]
        ivr_details = asterisk_db.get_ivr_details(case['company_id'], case['timestamp'])
        ivr_details_keys = ivr_details.keys()
        self.assertIn('id', ivr_details_keys)
        self.assertIn('context', ivr_details_keys)
        self.assertIn('company_id', ivr_details_keys)
        self.assertIn('name', ivr_details_keys)
        self.assertIn('start_time', ivr_details_keys)
        self.assertIn('end_time', ivr_details_keys)
        self.assertIsInstance(ivr_details['id'], int)
        self.assertIsInstance(ivr_details['context'], str)
        self.assertIsInstance(ivr_details['company_id'], int)
        self.assertIsInstance(ivr_details['name'], str),
        self.assertIsInstance(ivr_details['start_time'], datetime.timedelta)
        self.assertIsInstance(ivr_details['end_time'], datetime.timedelta)

    def test_get_nodes(self):
        cases = [{'ivr_id': 1, 'parent_node_id': 2, 'last_input': 2}]
        case = cases[0]
        nodes = asterisk_db.get_nodes(case['ivr_id'], case['parent_node_id'], case['last_input'])
        node = nodes[0]
        node_keys = node.keys()
        self.assertIsInstance(nodes, list)
        self.assertIn('id', node_keys)
        self.assertIn('ivr_id', node_keys)
        self.assertIn('parent_node_id', node_keys)
        self.assertIn('last_input', node_keys)
        self.assertIn('node_name', node_keys)
        self.assertIn('action', node_keys)
        self.assertIn('file', node_keys)
        self.assertIn('users_tag', node_keys)
        self.assertIsInstance(node['id'], int)
        self.assertIsInstance(node['ivr_id'], int)
        self.assertIsInstance(node['parent_node_id'], int)
        self.assertIsInstance(node['last_input'], int)
        self.assertIsInstance(node['node_name'], str)
        self.assertIsInstance(node['action'], str)
        self.assertIsInstance(node['file'], str)

    def test_insert_call_details(self):
        cases = [{
            'unique_id': random.randrange(1000000000, 9999999999),
            'dnid': '100',
            'channel': 'SIP/agi-user-00000009',
            'context': 'incoming',
            'peer_name': 'SIP/shubham-0000000b',
            'peer_type': 'SIP',
            'peer_number': 'shubham',
            'answered_time': '21',
            'calling_pres': '0',
            'dialed_time': '22',
            'dial_status': 'ANSWER',
            'hangup_cause': '16',
            'extension': '100',
            'language': '',
            'meet_me_secs': '',
            'priority': '1',
            'rdnis': '',
            'sip_domain': '192.168.10.11',
            'sip_codec': '',
            'sip_call_id': 'HzEK.JxxsSTzgu.jgdTxmCuqVqaaigXA',
            'sip_user_agent': '',
            'transfer_capability': '',
            'txt_cid_name': '',
            'recorded_file': '/home/vagrant/code/Asterisk-AGI/storage/recordings/sales_department 2019-09-19 04:46:22.965164.wav',
            'datetime': '2019-09-19 04:46:09'
        }]
        case = cases[0]
        self.assertRaises(Exception, asterisk_db.insert_call_details(case))

    def test_insert_session(self):
        cases = [{
            'unique_id': random.randrange(1000000000, 9999999999),
            'dnid': '100',
            'context': 'incoming',
            'extension': '100',
            'timestamp': '2019-09-19 04:46:09',
            'call_log': False,
            'trace': [
                {
                    'action': 'playback',
                    'filename': '/home/vagrant/code/Asterisk-AGI/storage/audios/welcome'
                },
                {
                    'action': 'input',
                    'ivr_id': 1,
                    'parent_node_id': 2
                },
                {
                    'action': 'playback',
                    'filename': '/home/vagrant/code/Asterisk-AGI/storage/audios/redirect_sales'
                },
                {
                    'action': 'dial',
                    'agent_string': 'SIP/sales&SIP/shubham'
                },
                {
                    'action': 'hangup',
                    'hangup_cause': 0
                }
            ]
        }]
        case = cases[0]
        self.assertRaises(Exception, asterisk_db.insert_session(case))

if __name__ == '__main__':
    unittest.main()
