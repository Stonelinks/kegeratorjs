import ike
import socket

pi_hostname = 'ike'
ike.Ike(relayPin=17, flow1Pin=23, flow2Pin=24, mock=socket.gethostname() == pi_hostname).run()
