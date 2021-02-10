# Crée par METARix_Team (Nicolas B., Lucas G.)
# METARix : Version 2.0
# coding=<utf-8>

""" Cette fonction compare le Nom d'Utilisateur et le Mot de Passe saisis """

def Verif_Cred_2(NU, MDP) :
    File = open('./Ressources/Login.txt', 'r')          # Fichier où sont stockés les Identifiants et Mots de Passe
    L_File = File.readlines()    ;   File.close()

    for Cred in range (len(L_File)) :
        Objet = L_File[Cred]
        Check_Nom_Util = None       ; Check_Mdp = None
        Separateur = Objet.split()
        Nom_Util = Separateur[0]    ; Mdp=Separateur[1]

        if NU == Nom_Util :                            # Si l'Identifiant correspond à un de ceux du fichier
            Check_Nom_Util = True
        else :
            Check_Nom_Util = False

        if MDP == Mdp :                                # Si le mot de Passe correspond à un de ceux du fichier
            Check_Mdp = True
        else :
            Check_Mdp = False

        if Check_Nom_Util == True and Check_Mdp == True :  # Si les deux sont corrects : Validation et sortie de boucle.
            Check = True
            break
        else :
            Check = False
            continue
    print('Test : Verif 2 Initiée')
    return Check

""" Cette fonction extrait le METAR brut depuis Internet """

def Get_METAR(OACI) :
    # Importation de la fonction 'urlretrieve' du module 'urllib' -> Sert à télécharger un fichier HTML
    from urllib.request import urlretrieve
    from os import remove
    URL = 'http://fr.allmetsat.com/metar-taf/france.php?icao=' + OACI             # URL du site web, avec l'OACI comme suffixe.
    HtmlSource_Filename = './Ressources/Temp/' + OACI + ' - HtmlSource.txt' # Definit le fichier de sauvegarde (format '.txt')

    try :   # Essaye de faire tourner une portion de code sans erreur. Si une erreur apparaît, le programme fait tourner le 'except'
        urlretrieve(URL, HtmlSource_Filename)          # Code pour télécharger le code source HTML sous forme d'un fichier .txt
        HtmlSource = open(HtmlSource_Filename, 'r')    # Ouverture du fichier crée
        List_HTML = HtmlSource.readlines()       # Répartition du contenu du fichier dans une liste
        Len_List = len(List_HTML)
        HtmlSource.close()                             # Ferme le fichier pour réinitialiser le compteur de lignes
        HtmlSource = open(HtmlSource_Filename, 'r')    # Réouvre le fichier
        Extract = 'METAR:</b> ' + OACI                 # Définit l'élément récurrent qui est définissant

        for Sentence in range (Len_List) :         # La boucle trouve la ligne contenant l'élément définissant dans le fichier
            if Extract in List_HTML[Sentence] :
                METAR_Data = List_HTML[Sentence]
                break                                  # Si trouvé : Sort de la boucle

        Tags = ['<h1>', '</h1>', '<p>', '</p>', '<h4>', '</h4>', '<div class="mt">', '<div class="mt2">', '</div>', '<script>', '</script>', '<b>', '</b>', '<br>', '///']    # Une liste des 'tags' retrouvés dans le code HTML.
        for Tag in range (len(Tags)) :                   # Boucle qui enlève les 'tags' de la ligne
            METAR_Data = METAR_Data.replace(Tags[Tag], '')

        List_Data = METAR_Data.split()           # Sépare les éléments de la ligne dans une liste
        Count_Data_Start = 0

        for Object in range (len(List_Data)) :        # Trouve l'élément 'OACI' dans la liste.
            if List_Data[Object] == OACI :
                break
            else :
                Count_Data_Start += 1

        METAR_Data = List_Data[Count_Data_Start::] # Conserve uniquement la liste 'METAR'

    except :
        METAR_Data = ['']

    try :
        remove(HtmlSource_Filename) # Supprime le fichier .txt de l'ordinateur.

    except :
        pass
    print('Test : METAR acquis')
    return METAR_Data

""" Cette fonction donne les coordonnées spécifiques d'un point en fonction de l'angle du vent. """

def Perimeter_Point(Alpha):
    from math import cos, sin, radians

    x1 = round(300+250*cos(radians(Alpha-110)), 0)  # Selon la formule :
    y1 = round(300+250*sin(radians(Alpha-110)), 0)  # x(point)=x(centre)+rayon*cos(Alpha)
    x2 = round(300+250*cos(radians(Alpha+110)), 0)  # y(point)=y(centre)+rayon*sin(Alpha)
    y2 = round(300+250*sin(radians(Alpha+110)), 0)
    xmid = round(300+250*cos(radians(Alpha)), 0)
    ymid = round(300+250*sin(radians(Alpha)), 0)

    return (x1, y1, x2, y2, xmid, ymid)   # Donne un 'tuple' (semi-liste)

""" Cette fonction détermine la piste de décollage optimale selon le vent """

def Pistes_Decollage(OACI_T, VentAngle) :
    Liste = []
    File = open("./Ressources/Liste_Pistes.txt", "r") # Fichier contenant une liste des pistes à chaque aérodrome.
    L_File = File.readlines()     ;    File.close()
    Error_Message = 'Aucune piste viable aux conditions données. Décollage déconseillé.'

    for i in range (len(L_File)) :     # Stocke toutes les orientations des pistes si plusieurs existent.
        if L_File[i][0:4] == OACI_T : # Trouve la ligne
            Index = 0
            Text = str(L_File[i])

            while Index < len(Text) :
                Index = Text.find('Piste_' , Index)

                if Index == -1 :
                    break

                Start = Index + 9
                End = Start + 7
                Liste.append(L_File[i][Start:End]) # Ajoute les angles des pistes dans une liste
                Index += 6

    for k in range (len(Liste)) :
        Liste[k] += '\n'
    Liste = (''.join(Liste)).split()

    for Angle in range (len(Liste)) :
        if int(Liste[Angle]) + 110 > VentAngle and VentAngle > int(Liste[Angle]) - 110  :
            if Angle == 0 :  # 3 pistes bi-directionnelles au maximum dans le fichier.
                P_Out = ''.join(['Utiliser la piste n°', str(1), ' dans la direction ', str(int(Liste[Angle])), '° - ', str(int(Liste[Angle+1])), '°.'])
            if Angle == 1 :
                P_Out = ''.join(['Utiliser la piste n°', str(1), ' dans la direction ', str(int(Liste[Angle])), '° - ', str(int(Liste[Angle-1])), '°.'])
            if Angle == 2 :
                P_Out = ''.join(['Utiliser la piste n°', str(2), ' dans la direction ', str(int(Liste[Angle])), '° - ', str(int(Liste[Angle+1])), '°.'])
            if Angle == 3 :
                P_Out = ''.join(['Utiliser la piste n°', str(2), ' dans la direction ', str(int(Liste[Angle])), '° - ', str(int(Liste[Angle-1])), '°.'])
            if Angle == 4 :
                P_Out = ''.join(['Utiliser la piste n°', str(3), ' dans la direction ', str(int(Liste[Angle])), '° - ', str(int(Liste[Angle+1])), '°.'])
            if Angle == 5 :
                P_Out = ''.join(['Utiliser la piste n°', str(3), ' dans la direction ', str(int(Liste[Angle])), '° - ', str(int(Liste[Angle-1])), '°.'])
            break
        print('Test : Pistes de décollage')
    try :   # Si P_Out à été crée
        return P_Out
    except : # Dans le cas ou aucune piste a étée trouvée
        return Error_Message

""" Cette fonction configure la fenêtre affichant la carte VAC de la localité recherchée """

def Add_Window(master, OACI_T, Alpha) :
    from tkinter import Canvas, PhotoImage, Label
    Nom_Fichier = str('./Ressources/OACISource/' + OACI_T + '.gif')
    AngleduVent = Alpha - 90
    X1, Y1, X2, Y2, XMID, YMID = Perimeter_Point(AngleduVent) # Coordonnées du point. Fractionnage du tuple.

    Essai = True
    C_VAC = Canvas(master, width = 600, height = 600)
    C_VAC.place(relx = 0, rely = 0)

    try :      # Si la carte VAC est dans le fichier de données.
        C_VAC._img_1 = PhotoImage(file = Nom_Fichier)

    except :  # Dans le cas contraire
        C_VAC._img_1 = PhotoImage(file = './Ressources/OACISource/NotFound.gif')
        Essai = False

    C_VAC.create_image(0, 0, image = C_VAC._img_1, anchor = 'nw')
    print('Test : Fenêtre')

    if Essai == True :  # Dessine un cercle montrant la direction du vent.
        C_VAC.create_oval(50, 50, 550, 550, width = 3, outline = '#ffff00')
        C_VAC.create_line(50, 300, 550, 300, fill = '#ffff00', width = 3)
        C_VAC.create_line(300, 50, 300, 550, fill = '#ffff00', width = 3)
        C_VAC.create_line(300, 300, X1, Y1, fill = '#1dff32', width = 3)
        C_VAC.create_line(300, 300, X2, Y2, fill = '#1dff32', width = 3)
        C_VAC.create_line(300, 300, XMID, YMID, fill = 'red', width = 3)

""" Cette fonction effectue la traduction du METAR depuis son stade brut """

def METAR_Trad(METAR) :
    Fichier = open('./Ressources/METAR_Decode/' + METAR[0] + ' - METAR Decode.txt', 'w')
    Fichier_2 = open('./Ressources/Vent/' + METAR[0] + ' - Angle du vent.txt', 'w')

    Texte_Vers_Fichier=''
    Basique = ''  # Fraction des aires de résultat pour conserver l'ordre.
    Phenom = '\n'
    Paliers = '\n'
    Closing = '\n'

    Valeur = 0
    Valeur_2 = 0

    # Liste de tous les phénomènes possibles et traduction
    Phenomenes = ['VC', 'MI', 'PR', 'DR', 'BL', 'FZ', 'RE', 'BC', 'SH', 'TS', 'XX', 'RA', 'SN', 'GR', 'DZ', 'PL', 'GS', 'SG', 'IC', 'UP', 'BR', 'FG', 'HZ', 'FU', 'SA', 'DU', 'VA', 'PO', 'SS', 'DS', 'SQ', 'FC']
    Phenomenes_Trad = ['Au Voisinage', 'Mince', 'Couvrant partiellement l\'aerodrome', 'En chasse bas', 'En chasse eleve', 'Froid Gelant', 'Recent', 'Bancs', 'Averses', 'Orage', 'Violent', 'Pluie', 'Neige', 'Grele', 'Bruine', 'Granules de Glace', 'Neige Roulee', 'Neige en Grains', 'Cristaux de Glace', 'Precipitation Inconnue', 'Brume', 'Brouillard', 'Brume Seche', 'Fumée', 'Sable', 'Poussiere', 'Cendres Volcaniques', 'Poussiere', 'Tempete de Sable', 'Tempete de Poussiere', 'Tornade ou Trombe Marine']
    Excep_List = ['TEMPO', 'OVC', 'NSG'] # Liste de variables similaires aux phénomènes

    for i in range (len(METAR)) :   # Cherche les caractères déterminants du METAR.
        Valeur_2 += 1
        if i == 1 :    # METAR[1] est toujours le temps
            Basique += ''.join(['Heure du relevé : ', str(METAR[i][2:4]), ':', str(METAR[i][4:6]), ' UTC+00']) + '\n'   # Structure polymorphique

        if i<5 and METAR[i][5:] == 'KT' : # Cherche '*****KT'
            Basique += ''.join(['Angle du vent : ', METAR[i][:3], '°'])

            if METAR[i][:3] == 'VRB' :
                Basique += ' (Angle Variable)\n'
            else :
                Basique += '\n'

            Fichier_2.write(str(METAR[i][:3]))
            Fichier_2.close()
            Val = int(METAR[i][3:5])
            Basique += ''.join(['Vitesse du vent : ', str(METAR[i][3:5]), ' Knots, soit : ', str(round(int(METAR[i][3:5])*1.852, 2)), ' km/h']) + '\n'

        if '/' in METAR[i] :   # Cherche '(*)**/(*)**'
            Slash = METAR[i].find('/')
            Temp = METAR[i][:Slash]

            if 'M' in Temp :  # Remplace 'M' par '-'
                Temp = '-' + Temp[1:]
            Basique += ''.join(['Température : ', Temp, '°C']) + '\n'
            PointdeRosee = METAR[i][Slash+1:]

            if 'M' in PointdeRosee :   # Remplace 'M' par '-'
                PointdeRosee = '-' + PointdeRosee[1:]
            Basique += ''.join(['Point de rosée : ', PointdeRosee, '°C']) + '\n'

        if METAR[i][0] == 'Q' :  # Cherche 'Q****'
            Basique += ''.join(['Pression au niveau de la mer : ', METAR[i][1:], ' hPa']) + '\n'

        if METAR[i] == 'BECMG' :  # Cherche 'BECMG'
            Basique += '\nChangements prévus pour bientot' + '\n'

        if i>5 and METAR[i][5:] == 'KT' and Valeur_2 > 4 : # Cherche '*****KT'
            Basique += ''.join(['Angle (vrai) du vent : ', str(METAR[i][:3]), '°']) + '\n'
            Basique += ''.join(['Vitesse (vraie) du vent : ', str(METAR[i][3:5]), ' Knots, soit : ', str(round(int(METAR[i][3:5])*1.852, 2)), ' km/h']) + '\n'

        elif len(METAR[i]) == 7 and METAR[i][3] == 'V' :  # Cherche '***V***'
            Texte_Vers_Fichier += ''.join(['Variation du vent : Entre ', METAR[i][:3], '° et ', METAR[i][4:], '°']) + '\n'

        if METAR[i] == 'CAVOK' : # Cherche 'CAVOK'
            Basique += str(''.join(['Visibilité : Ciel clair et conditions optimales'])) + '\n'

        for k in range (10000) : # Cherche un nombre entre 0 et 9999
            if METAR[i] == str(k) :
                Basique += str(''.join(['Visibilité : ', str(round(k/1000, 0)), ' km'])) + '\n'

        for z in range (len(Phenomenes)) :  # Cherche les phénomènes.
            if Phenomenes[z] in METAR[i] and Valeur_2 > 4 and METAR[i][:3] not in Excep_List and METAR[i] not in Excep_List :
                if '+' in METAR[i] :
                    Phenom += 'Le(s) phénomène(s) ci-dessous sera (seront) d\'intensité forte : ' + '\n'
                if '-' in METAR[i] :
                    Phenom += 'Le(s) phénomène(s) ci-dessous sera (seront) d\'intensité faible : ' + '\n'
                Phenom += 'Phénomène météorologique : ' + str(Phenomenes_Trad[z]) + '\n'

        PAL = ['FEW', 'SCT', 'BKN', 'OVC']
        PAL_2 = ['Ciel eclairci', 'Nuages epars', 'Ciel fragmenté', 'Ciel couvert']
        Link = [' en dessous de ', ' pieds\n(soit ', ' metres d\'altitude)']

        if METAR[i][:3] in PAL : # Cherche 'FEW***' ou 'SCT***', etc.
            if METAR[i][:3] == PAL[0] :
                Value = int(METAR[i][3:6])*100
                Paliers += ''.join(['Palier : ', PAL_2[0], Link[0], str(Value), Link[1], str(round(Value*0.3048, 0)), Link[2]]) + '\n'

            elif METAR[i][:3] == PAL[1] :
                Value = int(METAR[i][3:6])*100
                Paliers += ''.join(['Palier : ', PAL_2[1], Link[0], str(Value), Link[1], str(round(Value*0.3048, 0)), Link[2]]) + '\n'

            elif METAR[i][:3] == PAL[2] :
                Value = int(METAR[i][3:6])*100
                Paliers += ''.join(['Palier : ', PAL_2[2], Link[0], str(Value), Link[1], str(round(Value*0.3048, 0)), Link[2]]) + '\n'

            elif METAR[i][:3] == PAL[3] :
                Value = int(METAR[i][3:6])*100
                Paliers += ''.join(['Palier : ', PAL_2[3], Link[0], str(Value), Link[1], str(round(Value*0.3048, 0)), Link[2]]) + '\n'

        if METAR[i] == 'NSC' : # Cherche 'NSC'
            Paliers += 'Aucun nuage sous 5000 pieds et pas de cumulonimbus (bourgeonnants ou non)' + '\n'

        if METAR[i] == 'NCD' : # Cherche 'NCD'
            Paliers += 'Aucun nuage detecté' + '\n'

        if METAR[i] == 'SKC' :  # Cherche 'SKC'
            Paliers += 'Ciel Clair' + '\n'

        elif METAR[i] == 'NOSIG' :  # Cherche 'NOSIG'
            Closing += 'Aucun changement significatif prevu.'

    print('Test : METAR traduit')

    Texte_Vers_Fichier = str(Basique + Phenom + Paliers + Closing)   # Structure la sortie.
    Fichier.write(Texte_Vers_Fichier) # Exporte vers le fichier texte.
    Fichier.close()

""" Cette fonction génère un historique des actions effectuées par l'utilisateur """

def Log(Comment, OACI = '', N_Util = '') :
    from datetime import datetime # Module en rapport au temps.

    Full_Date = datetime.today() # Donne un string contenant tout les détails de l'heure actuelle.
    # Exemple : 2016-04-04 08:25:16.641000
    Full_Date = str(Full_Date)
    YYYY_MM_DD = Full_Date[:10] # Extrait la date
    YYYY_MM_DD = YYYY_MM_DD.replace('-', '/')
    HH_MM = Full_Date[11:19] # Extrait l'heure

    # Sort différentes remarques dépendant du commentaire fait en appel de fonction.
    if Comment == 1 :
        Input = 'Recherche : ' + OACI

    if Comment == 2 :
        Input = 'Action : Connexion'

    if Comment == 3 :
        Input = 'Action : Deconnexion'

    if Comment == 4 :
        Input = 'Envoi par Email (' + OACI + ')'

    String = [YYYY_MM_DD , '\t', HH_MM , '\t', N_Util, '\t', Input, '\n'] # Arrange la liste de sortie
    String=''.join(String) # Conversion de la liste en string

    File = open('./Ressources/Activity_Log.txt', 'r') # Lit l'historique
    File_L = File.readlines() ; File.close()
    if len(File_L) >= 25 : # Vide l'historique à l'exception des 10 dernières lignes.
        File = open('./Ressources/Activity_Log.txt', 'w')
        Text = ''.join(File_L[15:25])
        File.write(Text)
        File.close()

    File = open('./Ressources/Activity_Log.txt', 'a') # Ouvre l'historique et y ajoute le string.
    File.write(String)
    File.close()

""" Cette fonction ouvre une fenêtre contenant l'historique des actions effectuées """

def Log_Get() :
    from tkinter import Toplevel, Canvas
    File = open('./Ressources/Activity_Log.txt', 'r')
    File_L = File.readlines()

    Log_Window = Toplevel()
    Log_Window.title('Historique')
    Log_Window.geometry('350x500')
    Log_Window.resizable(width = 0, height = 0)
    C_Log = Canvas(Log_Window)
    C_Log.place(x = 0, y = 0, relwidth = 1, relheight = 1)
    C_Log.config(bg = 'white')

    for i in range (len(File_L)) :
        C_Log.create_text(5, (i*20), text = File_L[i], anchor = 'w', fill = 'black')

    print('Test : Affichage Historique')
    Log_Window.mainloop()

""" Cette fonction structure les informations pour permettre leur envoi par email à l'adresse entrée par l'utilisateur """

def Email_Send(OACI_T, Value, OACI_Bis = '') :
    import smtplib  # Module permettant d'accéder à un serveur SMTP.
    from email.mime.multipart import MIMEMultipart # Permet de configurer les champs d'envoi d'un email.
    from email.mime.text import MIMEText # Permet d'ajouter du texte à cet email.
    from tkinter import Toplevel, Button, Entry, font, Label

    """ Cette fonction envoie l'email au travers d'un serveur SMTP """

    def Send_Mail(Recipient, OACI_Mail, Value, OACI_Mail_Bis = '') :
        try : # Si accès Internet disponible.
            Email = MIMEMultipart() # Champs d'envoi.
            Email['From'] = 'metarix.noreply@gmail.com'
            Email['To'] = Recipient
            if Value == 1 :
                Email['Subject'] = 'METARix - EMAIL AUTOMATISE : METAR pour ' + OACI_Mail
                File = open('./Ressources/METAR_Decode/' + OACI_Mail + ' - METAR Decode.txt', 'r')
                L_File = File.readlines() ; File.close()
                message = ''.join(L_File)
                message = message.replace('é', 'e'); message = message.replace('è', 'e'); message = message.replace('ê', 'e'); message = message.replace('à', 'a'); message = message.replace('°C', ' Degres Celcius'); message = message.replace('°', ' Degres')
            if Value == 2 :
                Email['Subject'] = 'METARix - EMAIL AUTOMATISE : METAR pour ' + OACI_Mail + ' et ' + OACI_Mail_Bis
                File = open('./Ressources/METAR_Decode/' + OACI_Mail + ' - METAR Decode.txt', 'r')
                L_File = File.readlines() ; File.close()
                File_Bis = open('./Ressources/METAR_Decode/' + OACI_Mail_Bis + ' - METAR Decode.txt', 'r')
                L_File_Bis = File_Bis.readlines() ; File_Bis.close()
                message_1 = ''.join(L_File)
                message_2 = ''.join(L_File_Bis)
                message_1 = message_1.replace('é', 'e'); message_1 = message_1.replace('è', 'e'); message_1 = message_1.replace('ê', 'e'); message_1 = message_1.replace('à', 'a'); message_1 = message_1.replace('°C', ' Degres Celcius'); message_1 = message_1.replace('°', ' Degres')
                message_2 = message_2.replace('é', 'e'); message_2 = message_2.replace('è', 'e'); message_2 = message_2.replace('ê', 'e'); message_2 = message_2.replace('à', 'a'); message_2 = message_2.replace('°C', ' Degres Celcius'); message_2 = message_2.replace('°', ' Degres')

            # Construit le message.
            if Value == 1 :
                Message = 'METAR pour : ' + OACI_Mail + '\n\n' + message + '\n\nMessage envoye par le logiciel METARix, v.2.0, cree par la METARix_Team.'
            if Value == 2 :
                Message = 'METAR pour : ' + OACI_Mail + '\n\n' + message_1 + '\n\n' + 'METAR pour : ' + OACI_Mail_Bis + '\n\n' + message_2 +'\n\nMessage envoye par le logiciel METARix, v.2.0, cree par la METARix_Team.'

            Email.attach(MIMEText(Message)) # Ajoute le message au email
            Serveur_Gmail = smtplib.SMTP('smtp.gmail.com', 587) # Connecte au serveur SMTP de Gmail, au port 587.
            Serveur_Gmail.ehlo()    # Permet au programme de s'identifier au serveur SMTP.
            Serveur_Gmail.starttls() # Démarre l'encryption de la connection selon le protocole TLS (Transport Layer Security).
            Serveur_Gmail.ehlo() # Le programme doit se réidentifier.
            Serveur_Gmail.login('metarix.noreply@gmail.com', 'OneupfortheTeam') # Paramètres de connexion au compte de l'application.
            Serveur_Gmail.sendmail('metarix.noreply@gmail.com', Recipient, Email.as_string()) # Envoie le mail à la personne choisie.
            Serveur_Gmail.quit() # Ferme la connexion au serveur.
            Email_Window.destroy() # Ferme directement la fênetre.

        except : # Sans Internet
            Email_Window.destroy()

    """ Cette fonction permet à l'utilisateur de confirmer l'adresse email entrée """

    def Confirme() :
        Recipient = str(E_Email.get()) # Insère le texte entré dans une variable.
        if Value == 1 :
            Send_Mail(Recipient, OACI_T, 1)
        if Value == 2 :
            Send_Mail(Recipient, OACI_T, 2, OACI_Bis)
    Email_Window = Toplevel() # Ouvre une nouvelle fenêtre contenant des champs pour entrer une adresse mail.
    Email_Window.geometry('300x100')
    Email_Window.title(OACI_T + ' ' + OACI_Bis + ' : Envoi par Email')

    L_Email = Label(Email_Window)
    L_Email.place(relx = 0.35, rely = 0)
    L_Email.config(text = 'Adresse Mail :')

    E_Email = Entry(Email_Window)
    E_Email.place(relx = 0.1, rely = 0.25, width = 240, height = 25)
    E_Email.config(bg = 'white', font = font.Font(family = 'Consolas', size = 10, weight = 'normal'))

    B_Get = Button(Email_Window)
    B_Get.place(relx = 0.18, rely = 0.65, width = 200, height = 25)
    B_Get.config(bg = 'yellow', text = 'Envoyer à cette adresse mail', command = Confirme)

    print('Test : Envoi du mail')
    Email_Window.mainloop()
