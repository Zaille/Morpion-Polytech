import sys
import socket
import time

HOTE = "127.0.0.1"
PORT = 8000

# ----------------------------------- #

def clientUDP_simple():

    # Création du socket du serveur
    mySocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    # AF_INET : famille d'adresse, ici d'adresses Internet
    # SOCK_DGRAM : type de socket ( mode datagramme ) => UDP

    caseTab = [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ]
    nomCases = [ 'case1_1', 'case1_2', 'case1_3', 'case2_1', 'case2_2', 'case2_3', 'case3_1', 'case3_2', 'case3_3']

    pseudo = input( "Pseudonyme : " )

    mySocket.sendto( bytes( pseudo, 'utf-8' ), ( ( HOTE, PORT ) ) )
    attente, adresseServeur = mySocket.recvfrom(1024)
    print( attente.decode('utf-8') )
    adversaire, adresseServeur = mySocket.recvfrom(1024)

    print( "     1   2   3 \n" \
           "    -----------  j \n" \
           " 1 | %s | %s | %s | \n" % ( caseTab[0], caseTab[1], caseTab[2] ),
           "  |-----------| \n" \
           " 2 | %s | %s | %s | \n" % ( caseTab[3], caseTab[4], caseTab[5] ),
           "  |-----------| \n" \
           " 3 | %s | %s | %s | \n" % ( caseTab[6], caseTab[7], caseTab[8] ),
           "   ----------- \n" \
           "   i \n" \
           "   --------> %s -- VS -- %s <--------\n " % ( pseudo, adversaire.decode('utf-8') ),
           "-------------------------------------------")

    tour, adresseServeur = mySocket.recvfrom(1024)
    message = False
    while tour.decode( 'utf-8' ) != 'OK' :
        if message == False :
            print('C\'est au tour de %s' % ( adversaire.decode('utf-8') ))
            message = True
        tour, adresseServeur = mySocket.recvfrom(1024)

    print('C\'est ton tour : ')

    while 1:

        pointi_j = demande_points()

        pointi = pointi_j[0]
        pointj = pointi_j[2]

        case = 'case%s' % ( pointi_j )

        time.sleep(0.5)
        mySocket.sendto( bytes( str(pointi), 'utf-8' ), ( ( HOTE, PORT ) ) )
        mySocket.sendto( bytes( str(pointj), 'utf-8' ), ( ( HOTE, PORT ) ) )

        boolCase, adresseServeur = mySocket.recvfrom(1024)
        finPartie, adresseServeur = mySocket.recvfrom(1024)

        while boolCase.decode('utf-8') == 'False' :

            print( 'Case occupée, choisir une autre case : ')

            pointi_j = demande_points()

            pointi = pointi_j[0]
            pointj = pointi_j[2]

            case = 'case%s' % ( pointi_j )

            time.sleep(0.5)
            mySocket.sendto( bytes( str(pointi), 'utf-8' ), ( ( HOTE, PORT ) ) )
            mySocket.sendto( bytes( str(pointj), 'utf-8' ), ( ( HOTE, PORT ) ) )

            boolCase, adresseServeur = mySocket.recvfrom(1024)
            finPartie, adresseServeur = mySocket.recvfrom(1024)

        i = 0
        while i < len(nomCases) :
            if case == nomCases[i] and attente.decode('utf-8') == '' :
                caseTab[i] = 'o'
            elif case == nomCases[i] and attente.decode('utf-8') != '' :
                caseTab[i] = 'x'
            i += 1

        print( "     1   2   3 \n" \
               "    -----------  j \n" \
               " 1 | %s | %s | %s | \n" % ( caseTab[0], caseTab[1], caseTab[2] ),
               "  |-----------| \n" \
               " 2 | %s | %s | %s | \n" % ( caseTab[3], caseTab[4], caseTab[5] ),
               "  |-----------| \n" \
               " 3 | %s | %s | %s | \n" % ( caseTab[6], caseTab[7], caseTab[8] ),
               "   ----------- \n" \
               "   i \n" \
               "-------------------------------------------")

        if finPartie.decode('utf-8') == '1' :
            print( 'Tu as gagné !' )
            mySocket.close()
            sys.exit()
        elif finPartie.decode('utf-8') == '2' :
            print( 'Égalité !')
            mySocket.close()
            sys.exit()
        else :
            tour, adresseServeur = mySocket.recvfrom(1024)
            message = False
            while tour.decode( 'utf-8' ) != 'OK' :
                if message == False :
                    print('C\'est au tour de %s' % ( adversaire.decode('utf-8') ))
                    message = True
                finPartie, adresseServeur = mySocket.recvfrom(1024)
                if finPartie.decode('utf-8') == '1' :
                    print( 'Tu as perdu !' )
                    mySocket.close()
                    sys.exit()
                elif finPartie.decode('utf-8') == '2' :
                    print( 'Égalité !')
                    mySocket.close()
                    sys.exit()
                tour, adresseServeur = mySocket.recvfrom(1024)


        print('C\'est ton tour :')


def demande_points():
    i = 0

    while i < 2 :
        n = 0
        while n < 1 or n > 3:
            try:
                if i == 0 :
                    n = int(input( "Case i ? " ))
                    print('-------------------------------------------')
                    pointi = n
                else :
                    n = int(input( "Case j ? " ))
                    print('-------------------------------------------')
                    pointj = n
                if n < 1 or n > 3:
                    print( "Valeur incorrect." )
                    print('-------------------------------------------')
                else :
                    i += 1
            except ValueError:
                print("Entrer un nombre.")
                print('-------------------------------------------')

    result = '%s_%s' % ( pointi, pointj )

    return result

if __name__ == "__main__":
    clientUDP_simple()