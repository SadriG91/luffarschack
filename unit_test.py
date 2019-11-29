import unittest
import socket

class Test_server (unittest.TestCase):

    host = '127.0.0.1'
    port = 62222

    def test_server1(self):
        """
        Testar servern
        """
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))
        msg = "{}-{}".format(1, "X")
        conn.send(msg.encode())
        rec = conn.recv(1024).decode()
        conn.close()
        self.assertEqual(msg, rec[::-1])


if __name__ == '__main__':
    unittest.main()