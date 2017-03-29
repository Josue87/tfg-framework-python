import unittest
from jframework.modules.scan.synscan import Synscan
from jframework.modules.scan.ackscan import Ackscan


class ScanTest(unittest.TestCase):
    def setUp(self):
        self.syn_scan = Synscan()
        self.ack_scan = Ackscan()

    def test_default_value_syn(self):
        self.assertEqual(self.syn_scan.host, "127.0.0.1")
        self.assertEqual(self.syn_scan.ports_list, [80])

    def test_default_value_ack(self):
        self.assertEqual(self.ack_scan.host, "127.0.0.1")
        self.assertEqual(self.ack_scan.ports_list, [80])
        self.assertIsNotNone(self.ack_scan.ports_list)


if __name__ == '__main__':
    unittest.main()
