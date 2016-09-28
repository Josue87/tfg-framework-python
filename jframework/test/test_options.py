import unittest, sys
import unittest.mock as mock
import jframework.shell as sh


class TestOptions(unittest.TestCase):

    def setUp(self):
        sh.Shell.initial = mock.Mock()
        self.shell = sh.Shell()
        self.shell.myModule = mock.MagicMock()
        self.shell.completer = mock.MagicMock()


    def test_exec_command(self):
        host = '127.0.0.1'
        new_host = "192.168.0.1"

        self.shell.myModule.get_options = ['ip']
        self.shell.myModule.HOST = host
        self.assertEqual(self.shell.myModule.HOST, host)

        self.shell.myModule.ip = (lambda host: set_ip(self.shell.myModule, host))
        self.shell.exec_command("put ip {}".format(new_host))
        self.assertEqual(self.shell.myModule.HOST, new_host)


    def test_exec_commad2(self):
        self.shell.initial()
        self.assertRaises(Exception, self.shell.exec_command("no exist"))


def set_ip(shell, host):
    shell.HOST = host