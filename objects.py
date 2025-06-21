#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization

import random
import arcade
from save import*

class Batiments():
    def __init__(self) -> None:
        """element comprennant les batiments"""
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.all_batiments = []

    def append(self,batiment) -> None:
        """On ajoute un nouveau batiment"""
        self.all_batiments.append(batiment)
        self.sprite_list.append(batiment.sprite)

    def delete(self,batiment) -> None:
        """On supprime un batiment complétement"""
        self.sprite_list.remove()
        self.all_batiments.pop(batiment)
    
    def update(self,time) -> None:
        """Mise à jour des objets batiments"""
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)
        for batiment in self.all_batiments:
            if batiment.update(time):
                self.all_batiments.remove(batiment)
            else:
                self.sprite_list.append(batiment.sprite)

    def draw(self) -> None:
        """Dessine les batiments"""
        self.sprite_list.draw()

class Batiment():
    def __init__(self,folder,state:int,x:int,y:int) -> None:
        """Creer un object avec un etat de cet object avec sa position"""
        self.folder = folder
        self.state = state
        self.old_state = state
        self.x = x
        self.y = y
        self.time = None
        self.charge()

    def charge(self):
        """on charge l'image qui correspond à l'etat de l'arbre"""
        self.sprite = arcade.Sprite(building_int(self.folder,self.state))
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def update(self,time):
        """On dessine l'element selon son état"""
        if self.state != self.old_state:
            self.charge()
            self.old_state = self.state
        return 0

class Monolythe():
    def __init__(self,folder) -> None:
        """Creer un object avec un etat de cet object avec sa position"""
        self.exist = False
        self.folder = folder
        self.time = None
        self.state = 0
        self.x = 0
        self.y = 0
    
    def create(self,state:int,x:int,y:int) -> None:
        """Crée le monolythe au position x,y"""
        self.folder.settings["point_jobs"] +=1
        self.exist = True
        self.state = state
        self.old_state = state
        self.x = x
        self.y = y
        self.charge()

    def charge(self):
        """on charge l'image qui correspond à l'etat de l'arbre"""
        self.sprite = arcade.Sprite(building_int(self.folder,self.state))
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def draw(self) -> None:
        """Dessine le monolythe"""
        if self.exist:
            self.sprite.draw()

    def update(self,time):
        """On dessine l'element selon son état"""
        if self.exist:
            if self.state != self.old_state:
                self.charge()
                self.old_state = self.state
            else:
                if self.state == 6:
                    if self.time == None:
                        self.time = time
                    else:
                        if self.time + 9 < time:
                            self.state = 5
                            self.time = None
                if self.state ==5:
                    if self.time == None:
                        self.time = time
                    else:
                        if self.time + 9 < time:
                            self.state = 4
                            self.time = None
                if self.state == 4:
                    if self.time == None:
                        self.time = time
                    else:
                        if self.time + 0.1 < time:
                            self.state = 7
                            self.time = None
                if self.state == 7:
                    if self.time == None:
                        self.time = time
                    else:
                        if self.time + 0.1 < time:
                            self.state = 8
                            self.time = None
                if self.state == 8:
                    if self.time == None:
                        self.time = time
                    else:
                        if self.time + 0.1 < time:
                            self.state = 4
                            self.time = None
            return 0

class Forets():
    def __init__(self) -> None:
        """element comprennant la foret"""
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.all_arbre = []

    def ajout_arbre(self,arbre) -> None:
        """On ajoute un nouvel arbre"""
        self.all_arbre.append(arbre)
        self.sprite_list.append(arbre.sprite)

    def delete(self,arbre) -> None:
        """On supprime un arbre complétement"""
        self.sprite_list.remove()
        self.all_arbre.pop(arbre)
    
    def update_foret(self,time) -> None:
        """Mise à jour des objets arbre et sapin"""
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)
        for arbre in self.all_arbre:
            if arbre.update(time):
                self.all_arbre.remove(arbre)
            else:
                self.sprite_list.append(arbre.sprite)

    def draw(self) -> None:
        """Dessine la foret"""
        self.sprite_list.draw()

class Arbre():
    def __init__(self,folder,state:int,x:int,y:int) -> None:
        """Creer un object avec un etat de cet object avec sa position"""
        self.folder = folder
        self.state = state
        self.old_state = state
        self.x = x
        self.y = y
        self.time = None
        self.charge()

    def charge(self):
        """on charge l'image qui correspond à l'etat de l'arbre"""
        self.sprite = arcade.Sprite(tiled_int(self.folder,self.state))
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def update(self,time):
        """On dessine l'element selon son état"""
        if self.state != self.old_state:
            self.charge()
            self.old_state = self.state
        else:
            if self.state == 13:
                if self.time == None:
                    self.time = time
                else:
                    if self.time + 9 < time:
                        if random.randint(0,100) == 1:
                            self.state = random.choice([14,15,16,17])
                            self.time = None
            elif self.state == 14:
                if random.randint(0,10000) == 1:
                    self.state = 16
            elif self.state == 15:
                if random.randint(0,10000) == 1:
                    self.state = 17
            elif self.state == 16:
                if random.randint(0,10000) == 1:
                    self.state = 14
            elif self.state == 17:
                if random.randint(0,10000) == 1:
                    self.state = 15
            elif self.state == 18:#si l'arbre est coupé
                if self.time == None:
                    self.time = time
                else:
                    if self.time + 9 < time:
                        self.state = 19
                        self.time = None
            elif self.state == 19:
                if random.randint(0,100000):
                    self.state = 13
        return 0

class Sapin():
    def __init__(self,folder,state:int,x:int,y:int) -> None:
        """Creer un object avec un etat de cet object avec sa position"""
        self.folder = folder
        self.state = state
        self.old_state = state
        self.x = x
        self.y = y
        self.time = None
        self.charge()
    
    def charge(self):
        """on charge l'image qui correspond à l'etat du sapin"""
        self.sprite = arcade.Sprite(tiled_int(self.folder,self.state))
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def update(self,time):
        """On dessine l'element selon son état"""
        if self.state != self.old_state:
            self.charge()
            self.old_state = self.state
        else:
            if self.state == 20:
                if self.time == None:
                    self.time = time
                else:
                    if self.time + 9 < time:
                        if random.randint(0,100) == 1:
                            self.state = random.choice([21,22])
                            self.time = None

                    elif self.state == 23:#si l'arbre est coupé
                        if self.time == None:
                            self.time = time
                        else:
                            if self.time + 9 < time:
                                self.state = 24
                                self.time = None
                    elif self.state == 24:
                        if random.randint(0,100000):
                            self.state = 20

def tiled_int(folder,nombre) -> str:
    """Prend en parametre un nombre et renvoie l'image
    correspondante dans la bibliotheque du jeu"""
    try:
        return(folder.tiled[nombre])
    except:
        print("erreur,image "+str(nombre)+" non trouvé dans les ressources du jeu")

def building_int(folder,nombre) -> str:
    """Prend en parametre un nombre et renvoie l'image
    correspondante dans la bibliotheque du jeu"""
    try:
        return(folder.building[nombre])
    except:
        print("erreur,image "+str(nombre)+" non trouvé dans les ressources du jeu")

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization