#! /usr/bin/env python3
__author__ = 'nwiles'
import ike

def main():

    ikeInstance = ike.Ike(relayPin=17, flow1Pin=27, flow2Pin=22)
    ikeInstance.run()

if __name__ == "__main__":
    main()
