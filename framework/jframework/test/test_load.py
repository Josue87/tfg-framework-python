import unittest
from jframework.extras.load import loadModule
import sys


class LoadTest(unittest.TestCase):

    def test_load_synscan(self):
        sys.path.append("../modules/scan")
        module = loadModule("scan/synscan")
        self.assertNotEqual(module, None)
        self.assertEqual(module.__class__.__name__, "Synscan")

    def test_load_ftpservice(self):
        sys.path.append("../modules/banner")
        module = loadModule("banner/ftpservice")
        self.assertIsNotNone(module)
        self.assertEqual(module.__class__.__name__, "Ftpservice")
        ftpservice =  __import__("ftpservice")
        self.assertIsInstance(module, ftpservice.Ftpservice)

    def test_load_httpbruteforce(self):
        sys.path.append("../modules/login")
        module = loadModule("login/httpbruteforce")
        self.assertIsNotNone(module)
        self.assertEqual(module.__class__.__name__, "Httpbruteforce")

    def test_load_noexist_module(self):
        sys.path.append("../modules/login")
        module = loadModule("login/noexist")
        self.assertIsNone(module)

if __name__ == '__main__':
    unittest.main()