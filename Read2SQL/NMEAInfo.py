

def PrnList(kind):
    GPS = ['GP'+'%.2d'%i for i in range(1,31)]
    BDS = ['GB'+'%.2d'%i for i in range(1,61)]
    GLO = ['GL'+'%.2d'%i for i in range(61,96)]
    GAL = ['GA'+'%.2d'%i for i in range(61,96)]
    print(GPS)
    print('s')