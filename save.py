#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization

import os
import json

class Folder:
    def __init__(self,name,new=False) -> None:
        """name est le nom de la sauvegarde,
    
        -si la partie est nouvelle, et si il existe déjà une sauvegarde à son
        nom on détruit les fichiers de ce dossier, si la sauvegarde n'existe pas
        on crée un dossier à son nom;
        
        -si la partie n'est pas nouvelle on verifie son intégrité, puis on lance le jeu
        
        la fonction init renvoie si l'enregistrement à été un echec ou non"""

        self.name = name
        if new:
            if not os.path.exists("data/"+self.name):#si le dossier n'existe pas
                os.makedirs("data/"+self.name)#on crée le dossier
            else:#si le dossier existe, on supprime les fichiers.
                self.clear_dossier(self.name)
            self.new_sauvegarde()
        else:#On verifie l'intégrité de la sauvegarde
            if self.integrite(name):
                self.LOAD()
            else:#on fait une nouvelle sauvegarde si la sauvegarde est corrompue
                print("mauvaise integrité")
                self.clear_dossier(self.name)
                self.new_sauvegarde()
        
        self.tiled_int()
        self.building_int()
        self.data()
    
    def integrite(self,name) -> bool:
        """On verifie l'intégrité de la sauvegarde au chemin name"""
        fichiers = []
        for fichier in os.listdir("data/"+name):
            fichiers.append(fichier)
        for fichier in fichiers:
            if fichier not in ["map.desciv","batiments.desciv","forets.desciv","character.desciv","monolythe.desciv","updates.desciv","settings.desciv","ressources.desciv"]:
                return False
        return True

    @staticmethod
    def renommer_sauv(old_name,new_name) -> bool:
        """On change le nom de la sauvegarde, renvoie si la fonction a été un succes"""
        try:#le dossier a ete renomme 
            os.rename("data/"+old_name,"data/"+new_name)
            return True
        except FileExistsError:#le dossier existe déjà
            return False

    @staticmethod
    def clear_dossier(name) -> None:
        """on clear le dossier"""
        for fichier in os.listdir("data/"+name+"/"):
            os.remove("data/"+name+"/"+fichier)

    @staticmethod
    def del_sauvegarde(name) -> None:
        """on detruit la sauvegarde de chemin path/ + name"""
        for fichier in os.listdir("data/"+name):
            os.remove("data/"+name+"/"+fichier)
        os.rmdir("data/"+name)

    def data(self) -> None:
        """recupere des données sur le jeu en general"""
        fichier = open("assets/data.txt","r")
        value = 0
        self.data = {}
        for ligne in fichier:
            value += 1
            if "\n" in ligne:
                liste = ligne[0:-1].split(",")
                if len(liste) == 2:
                    self.data[liste[0]] = int(liste[1])
        fichier.close()

    def tiled_int(self) -> None:
        """class qui relie un nombre avec une tuile"""
        fichier = open("assets/sprites/tiled.txt","r")
        value = 0
        self.tiled = {}
        for i in fichier:
            value += 1
            try:
                self.tiled[value] = 'assets/sprites/tiled/'+i[0:-1]+'.png'
            except:
                self.tiled[value] = i[0:-1]+".png"
        fichier.close()
    
    def building_int(self) -> None:
        """class qui relie un nombre avec un batiment"""
        fichier = open("assets/sprites/building.txt","r")
        value = 0
        self.building = {}
        self.building_inverse = {}
        for i in fichier:
            value += 1
            try:
                self.building[value] = 'assets/sprites/building/'+i[0:-1]+'.png'
                self.building_inverse[i[0:-1]] = value
            except:
                self.building[value] = i[0:-1]+".png"
                self.building_inverse[i] = value

    def SAVE(self,world,batiments,foret,characters,monolythe,time) -> None:
        """sauvegarde le jeu"""
        self.save_map(world)
        self.save_batiments(batiments)
        self.save_forets(foret)
        self.save_characters(characters)
        self.save_monolythe(monolythe)
        self.save_upgraded()
        self.save_settings(time)
        self.save_ressources()

    def save_map(self,world) -> None:
        """Sauvegarde les cartes de départs dans un fichier"""
        fichier = open("data/"+self.name+"/map.desciv","w+")
        for ligne in world.cases_map:
            all = ""
            for case in ligne:
                all += str(case) +","
            fichier.write(all[0:-1]+"\n")
        fichier.write(";\n")
        for ligne in world.cases_forest:
            all = ""
            for case in ligne:
                all += str(case) + ","
            fichier.write(all[0:-1]+"\n")
        fichier.write(";\n")
        for ligne in world.cases_field:
            all = ""
            for case in ligne:
                all += str(case) + ","
            fichier.write(all[0:-1]+"\n")
        fichier.write(";")
        fichier.close()

    def save_batiments(self,batiments) -> None:
        """Enregistre les batiments dans un fichier"""
        fichier = open("data/"+self.name+"/batiments.desciv","w+")
        for batiment in batiments.all_batiments:
            all = str(batiment.state)+","+str(int(batiment.x))+","+str(int(batiment.y))
            fichier.write(all+"\n")
        fichier.close()

    def save_forets(self,forets) -> None:
        """Enregistre les arbres de la foret dans un fichier"""
        fichier = open("data/"+self.name+"/forets.desciv","w+")
        for arbre in forets.all_arbre:
            all = str(arbre.state)+","+str(int(arbre.x))+","+str(int(arbre.y))
            fichier.write(all+"\n")
        fichier.close()

    def save_characters(self,characters) -> None:
        """Enregistre les arbres de la foret dans un fichier"""
        fichier = open("data/"+self.name+"/character.desciv","w+")
        for character in characters.residents:
            all = character.job+","+character.old_job+","+str(character.health)+","+str(int(character.x))+","+str(int(character.y))+","+str(character.action)+","+str(character.target_x)+","+str(character.target_y)
            fichier.write(all+"\n")
        fichier.close()

    def save_monolythe(self,monolythe) -> None:
        """Enregistre le statue de la monolythe dans un fichier"""
        fichier = open("data/"+self.name+"/monolythe.desciv","w+")
        fichier.write(str(monolythe.exist)+","+str(monolythe.state)+","+str(int(monolythe.x))+","+str(int(monolythe.y)))
        fichier.close()

    def save_upgraded(self) -> None:
        """Sauvegarde les améliorations, des batiments et des
        métiers deverrouillés"""
        with open("data/"+self.name+"/updates.desciv", 'w+') as fichier:
            json.dump([self.batiments,self.jobs], fichier)

    def save_settings(self,time) -> None:
        """Sauvegarde les paramètres in-game"""
        self.settings["time"] = time
        with open("data/"+self.name+"/settings.desciv", 'w') as fichier:
            json.dump(self.settings, fichier)
    
    def save_ressources(self) -> None:
        """Sauvegarde les ressources in game"""
        with open("data/"+self.name+"/ressources.desciv", 'w') as fichier:
            json.dump(self.ressources, fichier)

    def new_sauvegarde(self) -> None:
        """Crée les variables utiles au jeu"""
        self.settings = {"time":0,"fps":60,"affiche_parcours":False,"point_jobs":0,"point_batiment":0}
        self.jobs = {"cueilleur":False,
                        "bucheron":False,
                        "constructeur":False,
                        "agriculteur":False,
                        "chercheur":False,
                        "pecheur":False,
                        "lancier":False,
                        "archer":False,
                        "mineur":False,
                        "chomeur":True}
        self.batiments = {"monolythe":True,
                          "cabane":False,
                          "cabane_grande":False,
                          "grange":False,
                          "grange_grande":False,
                          "mine":False,
                          "foresterie":False}
        self.ressources = {"nourriture":10,
                           "buche":0,
                           "roche":0}

    def LOAD(self) -> None:
        """Charge toutes les variables du jeu"""
        self.batiments,self.jobs = self.load_upgrade()
        self.settings = self.load_settings()
        self.ressources = self.load_ressources()
        self.monolythe = self.load_monolythe()
        self.cases_map,self.cases_forest,self.cases_field,self.waters,self.coord = self.load_map()
        self.all_batiments = self.load_batiments()
        self.forets = self.load_forets()
        self.characters = self.load_characters()

    def load_map(self) -> list: 
        """renvoie un tuple de 5 élements, 
        4 listes des cartes du jeu
        et 1 tuple de la longueur et largeur de la carte"""
        fichier = open("data/"+self.name+"/map.desciv","r")
        cases_map = []
        cases_forest = []
        cases_field = []
        state = 0
        for ligne in fichier:
            if "\n" in ligne:
                ligne = ligne[0:-1]
                if ligne == ";":
                    state +=1
                else:
                    cases = ligne.split(",")
                    cases = list(map(int, cases))
                    if state == 0:
                        cases_map.append(cases)
                    if state == 1:
                        cases_forest.append(cases)
                    if state == 2:
                        cases_field.append(cases)
        fichier.close()
        waters = []
        for i in range(len(cases_map)):
            waters.append([])
            for j in range(len(cases_map[0])):
                if cases_map[i][j] in [5,6,7,8]:
                    waters[i].append(5)
                else:
                    waters[i].append(0)
        return cases_map,cases_forest,cases_field,waters,(len(cases_map[0]),len(cases_map))

    def load_batiments(self) -> list:
        """renvoie une liste des batiments"""
        fichier = open("data/"+self.name+"/batiments.desciv","r")
        batiments = []
        for ligne in fichier:
            if "\n" in ligne:
                ligne = ligne[0:-1]
                liste = ligne.split(",")
                new_liste = []
                for i in liste:
                    try:
                        new_liste.append(int(i))
                    except:
                        new_liste.append(i)
                batiments.append(new_liste)
        fichier.close()
        return batiments
    
    def load_forets(self) -> list:
        """renvoie une liste des forets"""
        fichier = open("data/"+self.name+"/forets.desciv","r")
        forets = []
        for ligne in fichier:
            if "\n" in ligne:
                ligne = ligne[0:-1]
                liste = list(map(int,ligne.split(",")))
                forets.append(liste)
        fichier.close()
        return forets

    def load_characters(self) -> list:
        """renvoie une liste des characters"""
        fichier = open("data/"+self.name+"/character.desciv","r")
        characters = []
        for ligne in fichier:
            if "\n" in ligne:
                ligne = ligne[0:-1]
                liste = ligne.split(",")
                new_liste = []
                for i in liste:
                    try:
                        new_liste.append(int(i))
                    except:
                        new_liste.append(i)
                characters.append(new_liste)
        fichier.close()
        return characters

    def load_upgrade(self) -> tuple:
        """renvoie un tuple composé de 2 dictionnaires 
        -un dictionnaire des metiers debloqués
        -un dictionnaire des batiments debloqués"""
        with open("data/"+self.name+"/updates.desciv", 'r') as fichier:
            objets = json.load(fichier)
        return objets

    def load_settings(self) -> dict:
        """Renvoie le dictionnaire des parametres d'une sauvegarde"""
        with open("data/"+self.name+"/settings.desciv", 'r') as fichier:
            settings = json.load(fichier)
        return settings
    
    def load_ressources(self) -> dict:
        """Renvoie le dictionnaire des ressources d'une sauvegarde"""
        with open("data/"+self.name+"/ressources.desciv", 'r') as fichier:
            ressources = json.load(fichier)
        return ressources

    def load_monolythe(self) -> list:
        """renvoie une liste des infos sur la monolythe"""
        fichier = open("data/"+self.name+"/monolythe.desciv","r")
        for ligne in fichier:
            liste = ligne.split(",")
        fichier.close()
        liste[0] = (liste[0].lower()=="true")
        for i in range(1,4):
            liste[i] = int(liste[i])
        return liste

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization