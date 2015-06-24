from ike import Ike
import socket

mock = socket.gethostname() == 'ike'

my_ike = Ike(relayPin=17, flow1Pin=23, flow2Pin=24, mock=mock)
my_ike.run()
