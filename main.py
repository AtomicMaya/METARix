# Crée par METARix_Team (Nicolas B., Lucas G.)
# METARix : Version 2.0
# coding=<utf-8>

""" Import des modules nécessaires """

from tkinter import *                   # Module 'natif'
from tkinter import messagebox
from tkinter import font
from utils import *               # Module crée en annexe

""" Cette fonction démarre l'application quand le programme est initié
nativement (et non pas importé) """

def Start_IU() :                        # Génère et maintient la fênetre
    global root                         # Permet l'accès externe à la fonction
    root = Tk()                         # Fenêtre 'racine' (root en anglais)
    root.geometry("1200x731+91+6")
    root.title("METARix 2.0")
    root.resizable(width = 0, height = 0)   # Fixe les dimensions de la fenêtre
    root.wm_iconbitmap('./Ressources/METARix_Ico.ico')
    root.config(bg = "#ffffff")
    __init__(root)
    print('Test : Démarrage')
    root.mainloop()

""" Cette fonction détruit la fenêtre principale ainsi que les fenêtres
secondaires dans le cas ou elles sont ouvertes """

def Quit_IU() :
    root.destroy()
    try :               # Détruit les fenêtre annexes si ouvertes.
        Fen.destroy()
    except :
        pass
    try :
        Log_Window.destroy()
    except :
        pass
    try :
        Email_Window.destroy()
    except :
        pass

""" Cette fonction contient toutes les fonctions de l'application liées au GUI """

def __init__(master) :

    """ Cette fonction, appelée quand l'utilisateur appuie sur le bouton 'B_Connexion',
    vérifie externement si le nom d'utilisateur et le mot de passe figurent dans le
    fichier texte correspondant """

    def Verif_Cred() :
        global N_Util, M_Passe
        N_Util = str(E_Identifiant.get())
        M_Passe = str(E_MotdePasse.get())      # Stockage des entrées
        Verif = Verif_Cred_2(N_Util, M_Passe)   # Vérification des entrées
        Vider_E(E_Identifiant)        ;  Vider_E(E_MotdePasse)
        print('Test : N_Util : ', N_Util, ' , M_Passe : ', M_Passe, ' Verif : ', Verif)

        if Verif == True :                     # Si l'identifiant et le mot de passe sont corrects.
            Message = 'Bienvenue ' + N_Util
            B_Connexion.place_forget()
            B_Deconnexion.place(relx = 0.1, rely = 0.7, height = 25, width = 150)
            B_Deconnexion.config(state = NORMAL)
            L_Bienvenue.config(text = Message, font = _font13)
            L_Bienvenue.place(relx = 0.05, rely = 0.20, relwidth = 0.9)
            print('Test 2 : Passage Vérification')
            Pop_Root()
            Log(2, '', N_Util)

        else :                                  # Dans le cas inverse: Affichage d'une fenêtre d'erreur
            messagebox.showinfo('Attention !', 'Le Nom d\'Utilisateur ou le Mot de Passe est faux. Accès Refusé')
            print('Test 2 : Echec Vérification')

    """ Cette fonction fait disparaître les Widgets de la zone de connexion et
    fait apparaître la fenêtre principale """

    def Pop_Root() :
        Widgets=[L_Identifiant, L_MotdePasse, E_Identifiant, E_MotdePasse]

        for Widget in range (len(Widgets)) : # Cache les widgets.
            Widgets[Widget].place_forget()
        F_Root_2.place(relx = 0.0, rely = 0.0, relheight = 1, relwidth = 1)
        print('Test : Pop_Root Initié')

    """ Cette fonction est appelée quand l'utilisateur appuie sur 'B_Deconnexion'
    et fait disparaître la fenêtre principale et fait apparaître les Widgets de
    la zone de connexion """

    def Deconnexion() : # Cache la fenêtre principale, la réinitialise et fait apparaître les éléments de connexion.
        B_Connexion.place(relx = 0.1, rely = 0.7, height = 25, width = 150)
        B_Connexion.config(state = NORMAL)
        B_Deconnexion.config(state = DISABLED)
        B_Deconnexion.place_forget()

        L_Bienvenue.place_forget()
        L_Identifiant.place(relx = 0.03, rely = 0.05, height = 20, width = 110)
        L_MotdePasse.place(relx = 0.03, rely = 0.29, height = 20, width = 110)

        E_Identifiant.place(relx = 0.43, rely = 0.05, relheight = 0.19, relwidth = 0.53)
        E_MotdePasse.place(relx = 0.43, rely = 0.29, relheight = 0.19, relwidth = 0.53)

        F_Root_2.place_forget()
        F_Root_Reinitialisation()
        Log(3, '', N_Util)
        print('Test : Deconnexion Initiée')

    """ Cette fonction est appelée quand l'utilisateur appuei sur 'B_Choix_1'. Elle
    configure la fenêtre principale de sorte à minimiser l'impact visuel des
    Widgets non utilisés """

    def Itin_Type_1() :
        E_Choix_1.config(state = NORMAL)
        E_Choix_2.config(state = DISABLED)

        B_Choix_2.config(state = DISABLED)
        B_Valider.config(state = NORMAL)

        C_Resultat_2.config(bg = _bgcolor)
        C_Piste_2.config(bg = _bgcolor)
        print('Test : Itin_Type_1 Initié')

    """ Cette fonction est appelée quand l'utilisateur appuei sur 'B_Choix_2'.
    Elle configure la fenêtre principale pour qur tout les widgets soient utilisés """

    def Itin_Type_2() :
        E_Choix_1.config(state = NORMAL)
        E_Choix_2.config(state = NORMAL)

        B_Choix_1.config(state = DISABLED)
        B_Valider.config(state = NORMAL)

        C_Resultat_2.config(bg = 'white')
        C_Piste_2.config(bg = 'white')
        print('Test : Itin_Type_2 Initié')


    """ Cette fonction est appelée automatiquement pour vider les champs de saisie de texte """

    def Vider_E(master) :
        master.delete(0, 'end')
        print('Test : Contenu de ', master, ' Supprimé')

    """ Cette fonction permet d'afficher une liste extraite d'un fichier texte contenant tout
    les OACI de France (+ Genève) diffusant un METAR """

    def List_OACI() :
        F_Branch.place(relx = 0.75, rely = 0.14, relheight = 0.86, relwidth = 0.25)
        B_Acces_OACI.config(state = DISABLED)
        B_Cacher_Branch.place(relx = 0.25, rely = 0.95, height = 25, width = 150)

        C_Branch = Canvas(F_Branch_2, bg = 'blue', relief = SUNKEN)
        C_Branch.config(width = 275, height = 500, scrollregion = (0, 0, 300, 2010), highlightthickness = 0)

        Scroll = Scrollbar(F_Branch_2)           # Barre de défilement verticale
        Scroll.config(command = C_Branch.yview)

        C_Branch.config(yscrollcommand = Scroll.set)
        Scroll.pack(side = RIGHT, fill = Y)
        C_Branch.pack(side = LEFT, expand = YES, fill = BOTH)

        File = open('./Ressources/OACISource/OACIList.txt', 'r')     # Fichier avec la liste des OACI selon le département
        L_File = File.readlines()     ;    File.close()

        for Ligne in range (len(L_File)) :
            C_Branch.create_text(10, 20 + (Ligne * 20), text = L_File[Ligne], fill = 'beige', anchor = 'w')
        print('Test : Liste OACI Initiée')

    """ Cette fonction réinitilise tout les widgets de la fenêtre principale """

    def F_Root_Reinitialisation() :
        Vider_E(E_Choix_1)          ; Vider_E(E_Choix_2)
        E_Choix_1.config(state = DISABLED)     ; E_Choix_2.config(state = DISABLED)
        B_Choix_1.config(state = NORMAL)       ; B_Choix_2.config(state = NORMAL)
        B_Acces_OACI.config(state = NORMAL)

        C_Resultat_1.delete(ALL)     ; C_Resultat_2.delete(ALL) # Vide les 'canvas'
        C_Piste_1.delete(ALL)        ; C_Piste_2.delete(ALL)
        C_Resultat_2.config(bg = _bgcolor)        ; C_Piste_2.config(bg = _bgcolor)
        F_Branch.place_forget()
        B_VAC_1.config(state = DISABLED)     ; B_VAC_2.config(state = DISABLED)
        B_Email_1.config(state = DISABLED)     ; B_Email_2.config(state = DISABLED); B_Email_Double.config(state = DISABLED)
        print('Test : Réinitialisation Frame Principale')

    """ Extrait le METAR de ses champs de saisie et vérifie sa syntaxe . Ensuite
     il lance le processus d'acquisition et de traduction du METAR. Finalement,
     il affiche le METAR traduit et des informations secondaires dans l'interface utilisateur """

    def Reception_METAR() :
        Condition = None
        C_Resultat_1.delete(ALL)  ; C_Resultat_2.delete(ALL)
        C_Piste_1.delete(ALL)        ; C_Piste_2.delete(ALL)
        global OACI1, OACI2
        OACI1 = str(str(E_Choix_1.get())).upper()
        OACI2 = str(str(E_Choix_2.get())).upper()

        if OACI1 == '' or len(OACI1) != 4 : # Si le premier OACI est du mauvais format.
            messagebox.showinfo('Erreur', 'Une erreur s\'est produite à l\'acquisition des informations !\nVerifier que : \n - Les informations données sont éligibles (Code OACI uniquement). \n - Que votre connexion Internet soit stable.')
            Vider_E(E_Choix_1)  ; Vider_E(E_Choix_2)

        elif len(OACI1) == 4 :
            METAR1 = Get_METAR(OACI1) # Demande l'acquisition du METAR
            Log(1, OACI1, N_Util)

            if len(METAR1)>2 : # Si l'acquisition n'a pas échoué.
                T_1 = 'METAR interpreté pour ' + OACI1 + ' :'   ; T_2 = ''
                METAR_Trad(METAR1) # Demande la traduction du METAR
                Nom_Fichier = './Ressources/METAR_Decode/' + OACI1 + ' - METAR Decode.txt' # Ouvre le fichier contenant le METAR traduit
                File = open(Nom_Fichier, 'r')
                METAR_Trad_1 = File.readlines()   ; File.close()
                Condition = True
                B_VAC_1.config(state = NORMAL) ; B_Email_1.config(state = NORMAL)

                File_2 = open('./Ressources/Vent/' + METAR1[0] + ' - Angle du vent.txt', 'r')
                try : # Voit si l'angle est 'VRB' (pas un int)
                    Angle = int(File_2.readline())
                except :
                    Angle = 0
                Message_1 = Pistes_Decollage(OACI1, Angle)

            else :
                T_1 = 'Erreur d\'acquisition du METAR :'
                T_2 = 'NameError / IoError : Veullez vérifier votre connexion Internet !'
                B_VAC_1.config(state = DISABLED)  ; B_Email_1.config(state = DISABLED)

            C_Resultat_1.create_text(5, 20, text = T_1, anchor = 'w')
            C_Resultat_1.create_text(5, 40, text = T_2, anchor = 'w')

            if Condition == True :
                for Element in range (len(METAR1)) :
                    C_Resultat_1.create_text(5, 60 + (Element * 20), text = METAR_Trad_1[Element], anchor = 'w')
                Condition = None
                C_Piste_1.create_text(5, 15, text = Message_1, anchor = 'w')
            print('Test : OACI1 : ', OACI1, ' , METAR : ', METAR_Trad_1[0], '...')

        if OACI2 != '' : # Si le second OACI à été demandé.
            if OACI2 == '' or len(OACI2) != 4 : # Si le second OACI est du mauvais format
                messagebox.showinfo('Erreur', 'Une erreur s\'est produite à l\'acquisition des informations !\nVerifier que les informations données sont éligibles (Code OACI uniquement).')
                Vider_E(E_Choix_1)  ; Vider_E(E_Choix_2)       # Vide les 'entry'

            elif len(OACI2) == 4 :
                Log(1, OACI2, N_Util)
                METAR2 = Get_METAR(OACI2) # Demande l'acquisition du METAR

                if len(METAR2)>2 :
                    T_3 = 'METAR interpreté pour ' + OACI2 + ' :'    ; T_4 = ''
                    METAR_Trad(METAR2) # Traduit le METAR.
                    Nom_Fichier2 = './Ressources/METAR_Decode/' + OACI2 + ' - METAR Decode.txt'
                    File_2 = open(Nom_Fichier2, 'r')
                    METAR_Trad_2 = File_2.readlines()   ;   File_2.close()
                    Condition = True
                    B_VAC_2.config(state = NORMAL) ; B_Email_2.config(state = NORMAL); B_Email_Double.config(state = NORMAL)

                    File_3 = open('./Ressources/Vent/' + METAR2[0] + ' - Angle du vent.txt', 'r')
                    try :
                        Angle = int(File_3.readline())
                    except :
                        Angle = 0
                    Message_2 = Pistes_Decollage(OACI2, Angle)

                else :
                    T_3 = 'Erreur d\'acquisition du METAR : '
                    T_4 = 'NameError / IoError : Veullez vérifier votre connexion Internet !'
                    B_VAC_2.config(state=DISABLED)  ;  B_Email_2.config(state = DISABLED); B_Email_Double.config(state = DISABLED)

                C_Resultat_2.create_text(5, 20, text = T_3, anchor = 'w')
                C_Resultat_2.create_text(5, 40, text = T_4, anchor = 'w')

            if Condition == True :
                for Element_2 in range (len(METAR2)) :
                    C_Resultat_2.create_text(5, 60 + (Element_2 * 20), text = METAR_Trad_2[Element_2], anchor = 'w')
                Condition = None
                C_Piste_2.create_text(5, 15, text = Message_2, anchor = 'w')
            print('Test : OACI2 : ', OACI2, ' , METAR : ', METAR_Trad_2[0], '...')

    """ Cette fonction cache la fenêtre annexe """

    def F_Branch_Exit():
        F_Branch.place_forget()
        B_Acces_OACI.config(state = NORMAL)
        print('Test : Sortie Liste OACI Initiée')

    """ Cette fonction affiche la carte VAC de la première localité recherché """

    def VAC_1():
        File = open('./Ressources/Vent/' + OACI1 + ' - Angle du vent.txt', 'r')
        L_File = File.readlines()    ;   File.close()

        if len(L_File) > 0 and L_File[0] != 'VRB' :
            Alpha = int(L_File[0])
            Acces_VAC(OACI1, Alpha)

        else :
            Acces_VAC(OACI1)
        print('Test : VAC_1 Initié')

    """ Cette fonction affiche la carte VAC de la seconde localité recherchée """

    def VAC_2():
        File_2 = open('./Ressources/Vent/' + OACI2 + ' - Angle du vent.txt', 'r')
        L_File_2 = File_2.readlines()       ;   File_2.close()

        if len(L_File_2) > 0 and L_File_2[0] != 'VRB' :
            Alpha = int(L_File_2[0])
            Acces_VAC(OACI2, Alpha)

        else :
            Acces_VAC(OACI2)
        print('Test : VAC_2 Initié')

    """ Cette fonction configure une fenêtre secondaire affichant la carte VAC """

    def Acces_VAC(OACI_T, Alpha=0) :
        Fen = Toplevel(master = None)
        Fen.geometry('600x600')
        Fen.title('Carte VAC : ' + str(OACI_T))
        Fen.resizable(width = 0, height = 0)
        Add_Window(Fen, OACI_T, Alpha)
        print('Test : Acces_VAC Initiée')
        Fen.mainloop()

    """ Ces fonctions donnent les informations à une autre fonction pour envoyer le METAR par Email  """

    def Email_1() :
        Email_Send(OACI1, 1)
        Log(4, OACI1, N_Util)
        print('Test : Email_1 Initié')

    def Email_2() :
        Email_Send(OACI2, 1)
        Log(4, OACI2, N_Util)
        print('Test : Email_2 Initié')

    def Email_Double() :
        Email_Send(OACI1, 2, OACI2)
        Log(4, OACI1, N_Util) ; Log(4, OACI2, N_Util)
        print('Test : Email_Double Initié')


    """ Configuration des fontes et des couleurs fréquement utilisées """

    _bgcolor = '#efefef'
    _font11 = font.Font(family = 'Courier New', size = 10, weight = 'normal')
    _font12 = font.Font(family = 'Courier New', size = 10, weight = 'bold')
    _font13 = font.Font(family = 'Segoe UI', size = 12, weight = 'bold')

    """ Configuration initiale de tous les widgets """

    F_Logo = Frame(master)
    F_Logo.place(relx = 0, rely = 0, height = 50, relwidth = 0.75)
    F_Logo.config(relief = GROOVE, borderwidth = '2', bg = 'white', width = 900)

    L_Logo = Label(F_Logo)
    L_Logo.place(relx = 0.0, rely = 0.0, height = 50, width = 900)
    L_Logo.config(bg = _bgcolor, text = 'Label')
    F_Logo._img1 = PhotoImage(file = "./Ressources/METARix_Logo.gif")
    L_Logo.config(image = F_Logo._img1)

    F_Connexion = Frame(master)
    F_Connexion.place(relx = 0.75, rely = 0.0, relheight = 0.14, relwidth = 0.25)
    F_Connexion.config(relief = GROOVE, borderwidth = '2', bg = _bgcolor, highlightbackground = "#d9d9d9", width = 300)

    L_Identifiant = Label(F_Connexion)
    L_Identifiant.place(relx = 0.03, rely = 0.05, height = 20, width = 110)
    L_Identifiant.config(bg = _bgcolor, text = 'Identifiant')

    L_MotdePasse = Label(F_Connexion)
    L_MotdePasse.place(relx = 0.03, rely = 0.29, height = 20, width = 110)
    L_MotdePasse.config(bg = _bgcolor, highlightbackground = "#d9d9d9", text = 'Mot de Passe')

    E_Identifiant = Entry(F_Connexion)
    E_Identifiant.place(relx = 0.43, rely = 0.05, relheight = 0.19, relwidth = 0.53)
    E_Identifiant.config(bg = 'white', font = _font11)

    E_MotdePasse = Entry(F_Connexion)
    E_MotdePasse.place(relx = 0.43, rely = 0.29, relheight = 0.19, relwidth = 0.53)
    E_MotdePasse.config(bg = 'white', font = _font11, show = '*')

    B_Connexion = Button(F_Connexion)
    B_Connexion.place(relx = 0.1, rely = 0.7, height = 25, width = 150)
    B_Connexion.config(bg = 'green', text = 'Connexion', command = Verif_Cred)

    B_Deconnexion = Button(F_Connexion)
    B_Deconnexion.place_forget()
    B_Deconnexion.config(bg = 'red', text = 'Déconnexion', state = DISABLED, command = Deconnexion)

    B_Quitter = Button(F_Connexion)
    B_Quitter.place(relx = 0.67, rely = 0.7, height = 25, width = 90)
    B_Quitter.config(bg = 'red', text = 'Quitter', command = Quit_IU, font = _font12)

    L_Bienvenue = Label(F_Connexion)
    L_Bienvenue.place_forget()
    L_Bienvenue.config(bg = _bgcolor)

    F_Root = Frame(master)
    F_Root.place(relx = 0, rely = 0.07, relheight = 0.93, relwidth = 0.75)
    F_Root.config(relief = GROOVE, bg = 'white', borderwidth = '1')

    F_Root_2 = Frame(F_Root)
    F_Root_2.place_forget()
    F_Root_2.config(relief = GROOVE, borderwidth = '2', bg = _bgcolor)

    L_Choix = Label(F_Root_2)
    L_Choix.place(relx = 0.01, rely = 0.01, height = 25, width = 183)
    L_Choix.config(bg = _bgcolor, text = 'CHOISIR UN TYPE D\'ITINERAIRE :')

    L_Choix_1 = Label(F_Root_2)
    L_Choix_1.place(relx = 0.06, rely = 0.07, height = 25, width = 200)
    L_Choix_1.config(bg = _bgcolor, text = 'DEPART :')

    L_Choix_2 = Label(F_Root_2)
    L_Choix_2.place(relx = 0.06, rely = 0.12, height = 25, width = 200)
    L_Choix_2.config(bg = _bgcolor, text = 'DESTINATION :')

    E_Choix_1 = Entry(F_Root_2)
    E_Choix_1.place(relx = 0.33, rely = 0.07, relheight = 0.04, relwidth = 0.22)
    E_Choix_1.config(bg = 'white', font = _font11, state = DISABLED)

    E_Choix_2 = Entry(F_Root_2)
    E_Choix_2.place(relx = 0.33, rely = 0.12, relheight = 0.04, relwidth = 0.22)
    E_Choix_2.config(bg = 'white', font = _font11, state = DISABLED)

    B_Choix_1 = Button(F_Root_2)
    B_Choix_1.place(relx = 0.44, rely = 0.01, height = 25, width = 200)
    B_Choix_1.config(bg = _bgcolor, text = 'Tour de Piste', command = Itin_Type_1)

    B_Choix_2 = Button(F_Root_2)
    B_Choix_2.place(relx = 0.72, rely = 0.01, height = 25, width = 200)
    B_Choix_2.config(bg = _bgcolor, text = 'Navigation', command = Itin_Type_2)

    B_Acces_OACI = Button(F_Root_2)
    B_Acces_OACI.place(relx = 0.72, rely = 0.09, height = 25, width = 200)
    B_Acces_OACI.config(bg = '#00FFFF', text = 'Liste de données OACI', command = List_OACI)

    B_Valider = Button(F_Root_2)
    B_Valider.place(relx = 0.32, rely = 0.18, height = 25, width = 100)
    B_Valider.config(bg = 'green', text = 'Valider', command = Reception_METAR, state = DISABLED)

    B_Historique = Button (F_Root_2)
    B_Historique.place(relx = 0.60, rely = 0.18, height = 25, width = 100)
    B_Historique.config(bg = 'purple', text = 'Historique', command = Log_Get)

    C_Resultat_1 = Canvas(F_Root_2)
    C_Resultat_1.place(relx = 0, rely = 0.23, relheight = 0.55, relwidth = 0.49)
    C_Resultat_1.config(bg = 'white', borderwidth = '1' , relief = RIDGE)

    C_Resultat_2 = Canvas(F_Root_2)
    C_Resultat_2.place(relx = 0.5, rely = 0.23, relheight = 0.55, relwidth = 0.49)
    C_Resultat_2.config(bg = _bgcolor, borderwidth = '1' , relief = RIDGE)

    C_Piste_1 = Canvas(F_Root_2)
    C_Piste_1.place(relx = 0, rely = 0.79, relheight = 0.05, relwidth = 0.49)
    C_Piste_1.config(bg = 'white', borderwidth = '1' , relief = RIDGE)

    C_Piste_2 = Canvas(F_Root_2)
    C_Piste_2.place(relx = 0.5, rely = 0.79, relheight = 0.05, relwidth = 0.49)
    C_Piste_2.config(bg = _bgcolor, borderwidth = '1' , relief = RIDGE)

    B_VAC_1 = Button(F_Root_2)
    B_VAC_1.place(relx = 0.15, rely = 0.85, height = 25, width = 150)
    B_VAC_1.config(bg = _bgcolor, text = 'Carte VAC 1', command = VAC_1, state = DISABLED)

    B_VAC_2 = Button(F_Root_2)
    B_VAC_2.place(relx = 0.65, rely = 0.85, height = 25, width = 150)
    B_VAC_2.config(bg = _bgcolor, text = 'Carte VAC 2', state = DISABLED, command = VAC_2)

    B_Email_1 = Button(F_Root_2)
    B_Email_1.place(relx = 0.13, rely = 0.90, height = 25, width = 175)
    B_Email_1.config(bg = 'yellow', text = 'Envoyer ce METAR par Mail', state = DISABLED, command = Email_1)

    B_Email_2 = Button(F_Root_2)
    B_Email_2.place(relx = 0.63, rely = 0.90, height = 25, width = 175)
    B_Email_2.config(bg = 'yellow', text = 'Envoyer ce METAR par Mail', state = DISABLED, command = Email_2)

    B_Email_Double = Button(F_Root_2)
    B_Email_Double.place(relx = 0.38, rely = 0.90, height = 25, width = 175)
    B_Email_Double.config(bg = 'yellow', text = 'Envoyer ces METAR par Mail', state = DISABLED, command = Email_Double)

    B_Reinitialisation = Button(F_Root_2)
    B_Reinitialisation.place(relx = 0.37, rely = 0.95, height = 25, width = 200)
    B_Reinitialisation.config(bg = 'orange', text = 'Rafraîchir', command = F_Root_Reinitialisation)

    F_Branch = Frame(master)
    F_Branch.place_forget()
    F_Branch.config(relief = GROOVE, borderwidth = '2')

    F_Branch_2 = Frame(F_Branch)
    F_Branch_2.place(relx = 0, rely = 0, relheight = 0.93, relwidth = 1)

    B_Cacher_Branch = Button(F_Branch)
    B_Cacher_Branch.place_forget()
    B_Cacher_Branch.config(bg = 'red', text = 'Fermer', command = F_Branch_Exit)

""" Initialisation du programme """

if __name__ == '__main__':
    Start_IU()
