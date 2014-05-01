#coding = utf-8

import socket
import threading
import time

global UID

HOST = '127.0.0.1'
PORT = 38557
UID = ''
SUCCESS = 'succeed'

class Receive(threading.Thread):
    global UID
    def __init__(self, conn):
        self.conn = conn
        self.is_receiving = True
        threading.Thread.__init__(self)

    def run(self):
        while self.is_receiving:
            try:
                server_msg = self.conn.recv(65535)
                if not len(server_msg):
                    break
                print ''
                print server_msg
            except Exception, error:
                print error
                break


def regist_uid(client, uid):
    try:
        regist_data = '/%s' % uid
        client.send(regist_data)
        recv_data = client.recv(65535)
        print recv_data
        if recv_data == SUCCESS:
            return True
        else:
            return False
    except Exception, error:
        print error
        return False


if __name__ == '__main__':
    while True:
        uid = raw_input('please enter your username:')
        try:
            my_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_client.connect((HOST, PORT))
            if regist_uid(my_client, uid):
                UID = uid
                break
        except Exception, error:
            print error
            print 'regist failed, try another username'
        else:
            print 'login succeed, you can start chatting now'
            print 'format: DEST_ID, content\n'
    receive = Receive(my_client)
    receive.start()

    while True:
        try:
            data = raw_input('[%s]' %UID)
            if data.strip() == '':
                continue
            elif data == 'exit':
                break
            send_data = ','.join([UID, data])
            my_client.send(send_data)
            print data
        except Exception, error:
            print error
    my_client.shutdown(socket.SHUT_WR)
    my_client.close()

