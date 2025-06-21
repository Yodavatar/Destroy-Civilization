#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization

import random
import arcade
import os

class Space_latent():
    def __init__(self,x,y) -> None:
        """Créer un espace composés de y*x celulles
        chaque une composées d'une valeur entre 1 et 20"""
        self.x = x-1
        self.y = y-1
        self.tab = []
        for i in range(y):
            self.tab.append([])
            for j in range(x):
                self.tab[i].append([])
                self.tab[i][j].append(random.randint(1,20))

    def case_exterieur(self,x:int,y:int) -> list:
        """Renvoie la liste des positions des bordures
        d'une case passée en paramètre"""
        impossible = []
        if x == 0: #Bordure à gauche
            impossible.append(3)
        if y == 0: #Bordure en haut
            impossible.append(0)
        if x == self.x: #Bordure à droite
            impossible.append(1)
        if y == self.y: #Bordure en bas
            impossible.append(2)
        return impossible

    def case_interne(self,x:int,y:int) -> list:
        """Renvoie les directions autour d'une case
        qui est cible un case ne touchant pas les bords"""
        possible = [0,1,2,3]
        for i in self.case_exterieur(x,y):
            possible.remove(i)
        return possible

    def sum_case(self,x:int,y:int) -> int:
        """Fait la somme des nombres des cases autour disponibles"""
        possible = self.case_interne(x,y)
        liste = [self.tab[y][x][0]]
        if 0 in possible:
            liste.append(self.tab[y-1][x][0])
        if 1 in possible:
            liste.append(self.tab[y][x+1][0])
        if 2 in possible:
            liste.append(self.tab[y+1][x][0])
        if 3 in possible:
            liste.append(self.tab[y][x-1][0])
        return sum(liste)/(len(possible)+1)

    def zonage(self) -> list:
        """Fait évoluer l'espace pour qu'il soit
        le plus réaliste possible en utilisant formant des
        groupes de cases de meme famille"""
        tab_pass = self.tab.copy()
        for i in range(self.y+1):
            for j in range(self.x+1):
                tab_pass[i][j][0] = self.sum_case(j,i)
        return tab_pass

    def __str__(self) -> str:
        """Renvoie l'espace sous forme de matrice de nombres"""
        all ="\n"
        for i in range(self.y+1):
            for j in range(self.x+1):
                all += str(round(self.tab[i][j][0]))+","
            all += "\n"
        return all

class World():
    def __init__(self,folder) -> None:
        """transforme l'espace latent en espace de cellules individuelles"""
        self.x = int
        self.y = int
        self.folder = folder

    def create_world(self,y=10,x=10) -> None:
        """Crée 3 cartes dans la class en matrice de nombre
        self.map -> carte du jeu, le sol, l'eau, le desert
        self.forest -> carte ou les arbres et sapins peuvent pousser
        self.field -> carte ou les champs peuvent pousser
        """
        self.y,self.x = y,x

        """Espace principale"""
        self.map = Space_latent(y,x)
        for _ in range(10):
            self.map.zonage()
        self.cases_map,self.waters = self.transform_map()
        self.sprites_map = self.sprite_map(self.cases_map)
        self.sprites_waters = self.sprite_map(self.waters)
        
        """Espace de forets"""
        self.forest = Space_latent(y,x)
        for _ in range(10):
            self.forest.zonage()
        self.cases_forest,self.foret = self.transform_forest()
        self.sprites_forest = self.sprite_map(self.cases_forest)

        """Espace de l'agriculture"""
        self.field = Space_latent(y,x)
        for _ in range(10):
            self.field.zonage()
        self.cases_field = self.transform_field()
        self.sprites_field = self.sprite_map(self.cases_field)

    def load_world(self) -> None:
        """on charge la carte d'une partie sauvegardée"""
        self.y,self.x = self.folder.coord
        self.cases_map = self.folder.cases_map
        self.waters = self.folder.waters
        self.cases_forest = self.folder.cases_forest
        self.cases_field = self.folder.cases_field

        self.sprites_map = self.sprite_map(self.folder.cases_map)
        self.sprites_waters = self.sprite_map(self.folder.waters)
        self.sprites_forest = self.sprite_map(self.folder.cases_forest)
        self.sprites_field = self.sprite_map(self.folder.cases_field)

    def create_none_space(self,x,y) -> list:
        """crée un espace vide constitué de x ligne et y colonne"""
        self.new_world = []
        for i in range(y):
            self.new_world.append([])
            for j in range(x):
                self.new_world[i].append(0)
        return self.new_world

    def transform_map(self) -> tuple:
        """change les cases de la carte par un nombre
        representant une image"""
        new_space = self.create_none_space(self.y,self.x)
        waters = self.create_none_space(self.y,self.x)
        nbrligne = 0
        for ligne in self.map.tab:
            nbrcolonne = 0
            for case in ligne:
                if case[0] < 9:#sable
                    new_space[nbrligne][nbrcolonne] = random.choice([9,10,11,12])
                elif case[0] > 11.5:#eau
                    new_space[nbrligne][nbrcolonne] = random.choice([5,6,7,8])
                    waters[nbrligne][nbrcolonne] = 5
                elif case[0] > 11:#sable
                    new_space[nbrligne][nbrcolonne] = random.choice([9,10,11,12])
                else:#herbe
                    new_space[nbrligne][nbrcolonne] = random.choice([1,2,3,4])
                nbrcolonne +=1
            nbrligne +=1
        return new_space,waters

    def transform_forest(self) -> tuple:
        """change la matrice du filtre de la foret par une matrice de nombre
        representant une image, renvoie également une deuxième matrice d'image
        avec les arbres uniquement dans la carte géneré au debut du jeu."""
        filtre_foret = self.create_none_space(self.y,self.x)
        foret = self.create_none_space(self.y,self.x)
        nbrligne = 0
        for ligne in self.forest.tab:
            nbrcolonne = 0
            for case in ligne:
                if case[0] < 10:#arbres
                    if self.cases_map[nbrligne][nbrcolonne] not in [5,6,7,8,9,10,11,12]:
                        filtre_foret[nbrligne][nbrcolonne] = 14
                        if random.randint(0,3) in [0,1,2]:#foret de la carte
                            foret[nbrligne][nbrcolonne] = random.choice([13,14,15,16,17])
                    else:
                        filtre_foret[nbrligne][nbrcolonne] = 28
                elif case[0] > 11:#sapins
                    if self.cases_map[nbrligne][nbrcolonne] not in [5,6,7,8,9,10,11,12]:
                        filtre_foret[nbrligne][nbrcolonne] = 21
                        if random.randint(0,3) in [0,1,2]:#foret de la carte
                            foret[nbrligne][nbrcolonne] = random.choice([20,21,22])
                    else:
                        filtre_foret[nbrligne][nbrcolonne] = 28
                else:#pas de foret
                    filtre_foret[nbrligne][nbrcolonne] = 28
                nbrcolonne +=1
            nbrligne +=1
        return filtre_foret,foret

    def transform_field(self) -> list:
        """change les cases du filtre des champs par un nombre
        representant une image"""
        new_space = self.create_none_space(self.y,self.x)
        nbrligne = 0
        for ligne in self.field.tab:
            nbrcolonne = 0
            for case in ligne:
                if case[0] < 10.5:#agriculture
                    if self.cases_map[nbrligne][nbrcolonne] not in [5,6,7,8,9,10,11,12,13]:
                        new_space[nbrligne][nbrcolonne] = 27
                    else:
                        new_space[nbrligne][nbrcolonne] = 28
                else:#pas d'agriculture
                    new_space[nbrligne][nbrcolonne] = 28
                nbrcolonne +=1
            nbrligne +=1
        return new_space

    def bibliotheques_images(self,nombre) -> str:
        """Prend en parametre un nombre et renvoie l'image correspondante"""
        try:
            return(self.folder.tiled[nombre])
        except:
            print("erreur,image "+str(nombre)+" non trouvé dans les ressources du jeu")

    def sprite_map(self,cases) -> list:
        """Forme la matrice d'image representant la carte du jeu"""
        new_space = self.create_none_space(self.y,self.x)
        nbrligne = 0
        for ligne in cases:
            nbrcolonne = 0
            for case in ligne:
                if type(case) == int and case != 0:
                    road = self.bibliotheques_images(case)
                    new_space[nbrligne][nbrcolonne] = arcade.Sprite(road)
                nbrcolonne +=1
            nbrligne +=1
        return new_space

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization