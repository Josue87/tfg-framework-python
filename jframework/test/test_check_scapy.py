import unittest
import os
from jframework.extras.check_scapy import check



class test_check_scapy(unittest.TestCase):

    def setUp(self):
        self.result = check()

    def test_sudo(self):
        if os.getuid() != 0:
            self.assertEquals(self.result,"This task requires root")
        else:
            self.assertNotEqual(self.result, "ok")

    def test_scapy(self):
        try:
            from scapy.all import TCP
            self.assertNotEqual(self.result, "It's required install scapy module")
        except:
            self.assertEqual(self.result, "It's required install scapy module")

