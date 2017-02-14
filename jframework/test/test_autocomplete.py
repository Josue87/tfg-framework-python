import unittest
import os
import pexpect



class Autocomolete(unittest.TestCase):

    def setUp(self):
        self.path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,  os.pardir,'jf.py'))
        self.shell = pexpect.spawn('python3 {}'.format(self.path))
        self.shell.send('\r\n')

    def tearDown(self):
        self.shell = None

    def test_prompt(self):
        self.shell.send('\r\n')
        self.shell.expect_exact("jf >>", timeout=1)

    def test_complete_load(self):
        self.shell.send("l\t")
        self.shell.expect_exact("jf >> load ", timeout=1)

    def test_tabulator(self):
        self.shell.send("\t\t")
        self.shell.expect("credentials", timeout=1)
        self.shell.expect("exit", timeout=1)
        self.shell.expect("load", timeout=1)
        self.shell.expect("session", timeout=1)
        self.shell.expect("delete_session", timeout=1)
        self.shell.expect("show_sessions", timeout=1)


if __name__ == "__main__":
    unittest.main()