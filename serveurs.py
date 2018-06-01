import sys
import socket
import time

HOTE = "127.0.0.1"
PORT = 8000

    # ----------------------------------- #

def serveurUDP_simple():

    fin = False

    caseTab = [ False, False, False, False, False, False, False, False, False ]
    signeTab = [ '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
    signej1 = "o"
    signej2 = "x"

    nomCases = [ 'case1_1', 'case1_2', 'case1_3', 'case2_1', 'case2_2', 'case2_3', 'case3_1', 'case3_2', 'case3_3' ]

            # ----------------- Connexion ----------------- #

    # Création du socket du serveur
    mySocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            # AF_INET : famille d'adresse, ici d'adresses Internet
            # SOCK_DGRAM : type de socket ( mode datagramme ) => UDP

    mySocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
            # ... pour pouvoir réutiliser aussitôt le port
            # ( ex : quand on ferme puis relance le serveur )

    try :
        mySocket.bind( ( HOTE, PORT ) )
    except socket.error():
        print( "La création du serveur a échouée." )
        sys.exit()

        # ----------------- Attente joueurs  ----------------- #

    pseudoJ1, adresseClient1 = mySocket.recvfrom(1024)
    mySocket.sendto( bytes('En attente d\'un autre joueur', 'utf-8'), adresseClient1 )
    pseudoJ2, adresseClient2 = mySocket.recvfrom(1024)
    mySocket.sendto( bytes('', 'utf-8'), adresseClient2 )

    mySocket.sendto( pseudoJ2, adresseClient1 )
    mySocket.sendto( pseudoJ1, adresseClient2 )

    time.sleep(0.5)
    mySocket.sendto( bytes( 'OK', 'utf-8' ), adresseClient1 )
    mySocket.sendto( bytes( 'STOP', 'utf-8' ), adresseClient2 )

    while 1:

        # ----------------- Joueur 1  ----------------- #

        tour = 1

        msgServeur = jeu( mySocket, caseTab, signeTab, tour, nomCases, signej1, adresseClient2 )


        # ----------------- Joueur 2  ----------------- #

        tour = 2

        msgServeur =  jeu( mySocket, caseTab, signeTab, tour, nomCases, signej2, adresseClient1 )


def jeu( mySocket, caseTab, signeTab, tour, nomCases, signe, adresseAdversaire ):

    pointi, adresseClient = mySocket.recvfrom(1024)
    pointj, adresseClient = mySocket.recvfrom(1024)

    case = 'case%s_%s' % ( pointi.decode('utf-8'), pointj.decode('utf-8') )

    caseLibre = recherche_case( case, caseTab, signeTab, tour, nomCases )
    fin = partie_finit( signeTab, signe );

    time.sleep(0.5)
    mySocket.sendto( bytes(str(caseLibre), 'utf-8'), adresseClient )

    if fin != 1 :
        fin = checkEgalite( fin, signeTab )

    mySocket.sendto( bytes(str(fin), 'utf-8'), adresseClient )

    if caseLibre == True :
        mySocket.sendto( bytes(str(fin), 'utf-8'), adresseAdversaire )

        if fin :
            print( "Fin de la partie." )
            mySocket.close()
            sys.exit()

        time.sleep(0.5)
        mySocket.sendto( bytes( 'STOP', 'utf-8' ), adresseClient )
        mySocket.sendto( bytes( 'OK', 'utf-8' ), adresseAdversaire )

    else :

        caseLibre = jeu( mySocket, caseTab, signeTab, tour, nomCases, signe, adresseAdversaire )

    return caseLibre

def checkEgalite( fin, signeTab ) :
    i = 0
    while i < len(signeTab) :
        if signeTab[i] != 'o' and signeTab[i] != 'x' :
            return fin
        i += 1
    return 2

def recherche_case( case, caseTab, signeTab, tour, nomCases ) :
    i = 0
    while i < len(caseTab) :
        if case == nomCases[i] :
            if caseTab[i] :
                return False
            else :
                if tour == 1 :
                    signeTab[i] = "o"
                else :
                    signeTab[i] = "x"
                caseTab[i] = True
                return True
        i += 1

def partie_finit( signeTab, signe ) :

    gagne1 = signeTab[0] == signe and signeTab[1] == signe and signeTab[2] == signe
    gagne2 = signeTab[3] == signe and signeTab[4] == signe and signeTab[5] == signe
    gagne3 = signeTab[6] == signe and signeTab[7] == signe and signeTab[8] == signe
    gagne4 = signeTab[0] == signe and signeTab[3] == signe and signeTab[6] == signe
    gagne5 = signeTab[1] == signe and signeTab[4] == signe and signeTab[7] == signe
    gagne6 = signeTab[2] == signe and signeTab[5] == signe and signeTab[8] == signe
    gagne7 = signeTab[0] == signe and signeTab[4] == signe and signeTab[8] == signe
    gagne8 = signeTab[6] == signe and signeTab[4] == signe and signeTab[2] == signe

    gagneTab = [ gagne1, gagne2, gagne3, gagne4, gagne5, gagne6, gagne7, gagne8 ]

    for gagne in gagneTab :
        if gagne :
            return 1

    return 0

if __name__ == "__main__":
    serveurUDP_simple()