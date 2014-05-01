#coding = utf-8
import socket
import threading
import Queue

msg_queue = Queue.Queue()
client_dict = {}

class Client(threading.Thread):
    
    def __init__(self, conn):
        self.conn = conn
        threading.Thread.__init__(self)

    def run(self):
        global msg_queue, client_dict
        while True:
            data = self.conn.recv(65535)
            try:
                if data[0] == '/':
                    client_dict[data[1:]] = self.conn
                else:
                    msg_queue.put(data)
            except Exception, error:
                print error
                break


class Msg_Consumer(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global msg_queue, client_dict
        while True:
            data = msg_queue.get()
            try:
                try:
                    suid, duid, content = data.split(',')
                    print suid, duid, content
                    client_dict[duid].send(','.join([suid, content]))
                except Exception, error:
                    suid, content = data.split(',')
                    self.send_all(suid, data)
            except Exception, error:
                print error
                break

    def send_all(self, suid, data):
        for uid, client in client_dict.items():
            if uid != suid:
                client.send(data.strip())


HOST = '127.0.0.1'
PORT = 38557

if __name__ == '__main__':
    my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_server.bind((HOST, PORT))
    my_server.listen(3)
    msg_consumer = Msg_Consumer()
    msg_consumer.start()
    while True:
        conn, client_addr = my_server.accept()
        conn.send('succeed')
        client = Client(conn)
        client.start()
    conn.close()
