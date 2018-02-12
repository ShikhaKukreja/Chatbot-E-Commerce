import math
class Dataconverter:

    @staticmethod
    def convertIntToBinaryList(var, length):
        """
        Take a decimal value and convert that into binary array in length of "length"
        """
        f = []
        f = bin(var)

        p = f.rsplit('b',2)[1]
        p = p.rjust(int(math.ceil(math.log(length,2))), '0')
        f = map(int,list(p))    
        return f

    @staticmethod
    def convertBinaryListToInt(var):
        """
        Convert Binary string into integer
        """
        f = []
        for value in var[0]:
            if value > 0.9:
                f.append('1')
            elif value < 0.1:
                f.append('0')
            else:
                return -1
        
        p = ''.join(f)
        return int(p,2)