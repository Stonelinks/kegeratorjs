#! /usr/bin/env python3
__author__ = 'nwiles'
import ike

def main():

    ikeInstance = ike.Ike(relayPin=17, flow1Pin=23, flow2Pin=24)
    ikeInstance.run()

if __name__ == "__main__":
    main()
