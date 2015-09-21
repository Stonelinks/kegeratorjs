__author__ = 'nwiles'
import math

def volumes(temp_C, pressure_PA):
    return (pressure_PA*0.000145037738 + 14.695)*(0.0181 + 0.090115*math.exp( (32-(temp_C*9/5.0+32))/43.11) ) - 0.00334