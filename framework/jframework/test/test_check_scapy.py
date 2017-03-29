import unittest
import os
from jframework.extras.check_scapy import check



class Test_check_scapy(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_check_scapy, self).__init__(*args, **kwargs)
        try:
            from scapy.all import TCP
            self.exist_scapy = True
        except:
            self.exist_scapy = False

    def setUp(self):
        self.result = check()

    def test_sudo(self):
        if self.exist_scapy:
            if os.getuid() != 0:
                self.assertEquals(self.result,"This task requires root")
            else:
                self.assertNotEqual(self.result, "ok")
        else:
            self.assertEqual(self.result, "It's required install scapy module")