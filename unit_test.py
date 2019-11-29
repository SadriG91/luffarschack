import unittest
import socket
# from unittest.mock import Mock
# mock = Mock()


class Test_server (unittest.TestCase):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 62222

    def setUp(self):
        print("Start testing")

    def tearDown(self):
        print("Finish testing")

    def test_port(self):
        self.assertEqual(self.port, 62222)
        print("Port is ready")

    def test_connection(self):
        self.sock.connect((self.host, self.port))
        self.assertTrue(True)
        print("Client is connected")
        
    def test_sending(self):
        msg = "{}-{}".format(1, "X").encode()
        self.sock.send(msg)
        print("Sending complete")

    # def test_server1(self):
    #     """
    #     Testar servern
    #     """
        
    #     #conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    #     
    #     #input()
    #     #rec = conn.recv(1024).decode()
    #     conn.close()
    #     #self.assertEqual(msg, rec[::-1])


if __name__ == '__main__':
    unittest.main()