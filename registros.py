def verificar(numero):
    infile = open('registros.txt', 'r')
    for line in infile:
        if line[:-1] == numero:
            infile.close()
            return True
    
    infile.close()
    return False
