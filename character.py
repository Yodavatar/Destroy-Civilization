#Coding : utf-8
#Coding by ROBERT Sacha
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization

import time
import arcade
import random
import numpy as np

class Residents():
    def __init__(self,folder,world,monolythe,affichage) -> None:
        """cette class contients tout les personnages et gere 
        les metiers et les evenements independants"""
        self.width,self.height = world.y,world.x
        self.folder = folder
        self.world = world
        self.monolythe = monolythe
        self.affichage = affichage
        self.residents = []
        self.targets = {}
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)

    def ajoute_perso(self,x,y,job="chomeur",old_job="chomeur",health=100,action=0,target_x=None,target_y=None) -> None:
        """Ajoute un nouveau personnage"""
        barbare = Barbare(self.width,self.height,x,y,job,old_job,self.monolythe,self.world,health,action,target_x,target_y)
        self.residents.append(barbare)
        for button in self.affichage.buttons:
            if button["name"] == job:
                button["variable"] +=1

    def change_job(self,remove_job,new_job) -> None:
        """Change un personnage de metier"""
        done = False
        for i in range(len(self.residents)):
            if done is not True:
                if self.residents[i].job == remove_job:
                    self.residents[i].job = new_job
                    self.residents[i].action = 0
                    done = True

    def draw(self) -> None:
        """Dessine chacun des personnages"""
        self.sprite_list.draw()

    def update(self,barrier,time,foret,batiment) -> None:
        """Met à jour tous les personnages"""
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)
        for resident in self.residents:
            if resident.update(barrier,time,foret,self.folder,batiment,self.targets):#si le personnage meurt
                self.residents.remove(resident)
                for button in self.affichage.buttons:
                    if button["name"] == resident.job:
                        button["variable"] -=1
            else:#s'il est en vie alors on ajoute le sprite
                self.sprite_list.append(resident.sprite)
        for cle,valeur in list(self.targets.items()):
            if valeur + 20 < time:
                del self.targets[cle]

class Barbare():
    def __init__(self,width,height,x:int,y:int,job:str,old_job,monolythe,world,health,action,target_x,target_y) -> None:
        """habitant possede un certain nombre de caracteristique unique"""
        self.job = job
        self.old_job = old_job
        self.health = health
        self.sprites = []
        self.paths = ["main_up","main_down","main_right","main_left"]
        for path in self.paths:
            self.sprites.append(arcade.Sprite("assets/sprites/personnage/"+path+".png"))
        self.sprite = arcade.Sprite("assets/sprites/personnage/main_down.png")
        self.sprite.center_x = int(x)
        self.sprite.center_y = int(y)
        self.x = int(x)
        self.y = int(y)
        self.width = height#inversion
        self.height = width#inversion
        self.monolythe = monolythe
        self.world = world
        self.action = action
        self.target_x = target_x
        self.target_y = target_y
        self.time = None
        self.path = []

    def coord_random(self,center_coord) -> int:
        """Renvoie une coordonnée aléatoire"""
        lg = random.randint(50,100)
        if random.randint(0,1) == 1:
            return random.randint(center_coord-lg,center_coord)
        return random.randint(center_coord,center_coord+lg)

    def place_random(self) -> None:
        """renvoie un couple de coordonnée aléatoire sur la carte"""
        self.target_x,self.target_y = (self.coord_random(self.monolythe.x),self.coord_random(self.monolythe.y))

    def target_object(self,wall,target) -> None:
        """initialise le tableau des coordonnées par lequel doit passer le personnage"""
        start = time.time()
        wall = arcade.AStarBarrierList(self.sprite,wall,32,0,self.width*32,0,self.height*32)
        
        print(f"Time elapsed: {time.time() - start}")
        
        self.path = arcade.astar_calculate_path(target,self.sprite.position,wall,diagonal_movement=True)
        if self.path == None:
            self.path = []
            self.target_x,self.target_y = self.sprite.center_x,self.sprite.center_y
        else:
            self.target_x,self.target_y = self.path.pop()
        
    def trouver_object_proche(self,objects,state=[],targets=[]) -> object:
        """Renvoie l'object le plus proche du point (x, y) parmi une liste d'objects"""
        start = time.time()
        mini = float("inf")
        return_object = None
        for object in objects:
            if object.state in state and object not in targets:
                dist = distance_euclidienne(self.x, self.y,object.x, object.y)
                if dist < mini:
                    mini = dist
                    return_object = object
        
        print(f"Time elapsed: {time.time() - start}")

        return return_object

    def continue_walk(self) -> bool:
        """continue le chemin enprunté,renvoie vrai si le chemin est terminé"""
        if len(self.path) != 0:
            self.target_x,self.target_y = self.path.pop()
        else:
            return True
        return False
    
    def found_target(self,wall,time,foret,folder,batiments,targets) -> None:
        """Choisit la prochaine cible"""
        if self.job == "chomeur":
            if self.action == 1:
                self.action = 0
            self.place_random()
        elif self.job == "cueilleur":
            if self.action >= 3:
                self.action = -1
                self.time = None
            elif self.action == 0:#on cherche le fruit le plus proche
                arbre = self.trouver_object_proche(foret.all_arbre,[16,17],targets)
                targets[arbre] = time
                if arbre != None:
                    self.target_object(wall,(arbre.x,arbre.y))
                else:
                    self.place_random()
            elif self.action == 1:#on attend 5 sec
                self.action -= 1
                if self.time == None:
                    self.time = time
                else:
                    if self.time + 5 < time:#on enleve le fruit de l'arbre
                        arbre = None
                        for i in foret.all_arbre:
                            if self.sprite.collides_with_sprite(i.sprite):
                                arbre = i
                        if arbre != None:
                            if arbre.state == 16:
                                arbre.state = 14
                                folder.ressources["nourriture"] += 1
                                folder.settings["point_jobs"] +=1
                            elif arbre.state == 17:
                                arbre.state = 15
                                folder.ressources["nourriture"] += 1
                                folder.settings["point_jobs"] +=1
                        self.action +=1
            if self.action == 2:#on envoie le personnage au monolythe
                self.target_object(wall,(self.monolythe.x,self.monolythe.y))
        elif self.job == "bucheron":
            if self.action >= 3:
                self.action = -1
                self.time = None
            elif self.action == 0:#on cherche l'arbre le plus proche
                arbre = self.trouver_object_proche(foret.all_arbre,[14,15,21,22],targets)
                targets[arbre] = time
                if arbre != None:
                    self.target_object(wall,(arbre.x,arbre.y))
                else:
                    self.place_random()
            elif self.action == 1:#on attend 5 sec
                self.action -= 1
                if self.time == None:
                    self.time = time
                else:
                    if self.time + 5 < time:#on coupe l'arbre
                        arbre = None
                        for i in foret.all_arbre:
                            if self.sprite.collides_with_sprite(i.sprite):
                                arbre = i
                        if arbre != None:
                            if arbre.state in [14,15]:
                                arbre.state = 18
                                folder.ressources["buche"] += 1
                                folder.settings["point_jobs"] +=1
                            elif arbre.state in [21,22]:
                                arbre.state = 23
                                folder.ressources["buche"] += 1
                                folder.settings["point_jobs"] +=1
                        self.action +=1
            elif self.action == 2:#on envoie le personnage au monolythe
                self.target_object(wall,(self.monolythe.x,self.monolythe.y))
        elif self.job == "constructeur":
            if self.action >= 4:
                self.action = -1
                self.time = None
            if self.action == 0:#on cherche le batiment en construction le plus proche
                batiment = self.trouver_object_proche(batiments.all_batiments,[3,11,14,17,20,23],targets)
                targets[batiment] = time
                if batiment != None:
                    self.target_object(wall,(batiment.x,batiment.y))
                else:
                    self.place_random()
                    self.action -=1
            if self.action == 1:#on attend 5 sec
                self.action -= 1
                if self.time == None:
                    self.time = time
                else:
                    if self.time + 5 < time:#on construit la 1e partie
                        batiment = None
                        for i in batiments.all_batiments:
                            if self.sprite.collides_with_sprite(i.sprite):
                                batiment = i
                        if batiment != None:
                            if batiment.state == 3:
                                batiment.state = 2
                            if batiment.state == 11:
                                batiment.state = 10
                            if batiment.state == 14:
                                batiment.state = 13
                            if batiment.state == 17:
                                batiment.state = 16
                            if batiment.state == 20:
                                batiment.state = 19
                            if batiment.state == 23:
                                batiment.state = 22
                        self.action +=1
                        self.time = None
            if self.action == 2:#on attend 5 sec
                self.action -= 1
                if self.time == None:
                    self.time = time
                else:
                    if self.time + 5 < time:#on construit la 2e partie
                        batiment = None
                        for i in batiments.all_batiments:
                            if self.sprite.collides_with_sprite(i.sprite):
                                batiment = i
                        if batiment != None:
                            if batiment.state == 2:
                                batiment.state = 1
                            if batiment.state == 10:
                                batiment.state = 9
                            if batiment.state == 13:
                                batiment.state = 12
                            if batiment.state == 16:
                                batiment.state = 15
                            if batiment.state == 19:
                                batiment.state = 18
                            if batiment.state == 22:
                                batiment.state = 21
                        self.action +=1
                        folder.settings["point_batiment"] +=1
            if self.action == 3:#on envoie le personnage au monolythe
                self.target_object(wall,(self.monolythe.x,self.monolythe.y))
            
    def update(self,wall,time,foret,folder,batiment,targets) -> bool:
        """Met à jour le personnage et renvoie si il meurt"""
        if self.target_x == None:
            self.found_target(wall,time,foret,folder,batiment,targets)
        else:
            if self.target_x -2 < self.x <self.target_x +2 and self.target_y -2 < self.y < self.target_y+2:
                self.x,self.y = self.target_x,self.target_y
                if self.continue_walk():
                    if self.job == self.old_job:
                        self.action +=1
                        self.found_target(wall,time,foret,folder,batiment,targets)
                    else:
                        self.old_job = self.job
                        self.action = 0
                        self.time = None
                        self.found_target(wall,time,foret,folder,batiment,targets)
            #on bouge le personnage
            if self.target_y > 1 + self.y:#le personnage monte
                self.y +=1
                self.sprite = self.sprites[0]
            elif self.target_y < self.y:#le personnage descend
                self.y -=1
                self.sprite = self.sprites[1]
            if self.target_x > 1 + self.x:#le personnage va à droite
                self.x +=1
                self.sprite = self.sprites[2]
            elif self.target_x < self.x:#le personnage va à gauche
                self.x -=1
                self.sprite = self.sprites[3]
            self.sprite.center_x = self.x
            self.sprite.center_y = self.y

        if self.health <=0:
            return True
        return False

class Ennemys():
    def __init__(self) -> None:
        #pas encore implémanter
        pass

class Enemy():
    def __init__(self) -> None:
        #pas encore implémanter
        pass


def distance_euclidienne(x1, y1, x2, y2) -> float:
    """Calcule la distance euclidienne entre deux points 1 et 2"""
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization