#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization

import arcade
from objects import*
from character import*

class Affichage():  
    def __init__(self,folder,world,width,height,new) -> None :
        #variables generiques
        self.world = world
        self.folder = folder
        self.width = width
        self.height = height

        #variables si le zoom est disponible ( en pixels)
        self.zoom = 32
        self.origine_x = 0
        self.origine_y = 0
        self.zoom_min = 2
        self.zoom_max = 256

        #valeurs principales
        self.margin_camera = self.height-100
        self.SPRITE_SCALING = 0.5
        self.VIEWPORT_MARGIN = 100
        self.CAMERA_SPEED = 0.05
        self.MODE_POSITION = False

        #cameras
        self.camera_world = arcade.Camera(self.width, self.height)
        self.camera_gui = arcade.Camera(self.width, self.height)

        #vues du jeu (1=monde,2=foret,3=agriculture)
        self.view_left = 0
        self.view_bottom = 0
        self.filtre = 0

        #setup du jeu
        self.setup_gui()
        self.setup_game(new)

    def draw_building(self,x,y) -> None:
        """Dessine le batiment qui à été choisit dans le menu de construction"""
        pos = self.position_building(x,y)
        self.batiment_chose.center_x = pos[0]
        self.batiment_chose.center_y = pos[1]
        self.batiment_chose.draw()

    def position_building(self,x,y) -> tuple:
        """Renvoie la position des batiments"""
        if self.methode_construction == 2:
            return([((x//32)*32)+16,((y//32)*32)+16])
        else:
            return([((x//32)*32),((y//32)*32)])

    def choose_building(self,batiment:int) -> None:
        """choisir un batiment à afficher"""
        self.name_building = batiment
        self.batiment_chose = arcade.Sprite("assets/sprites/building/"+batiment+".png")
        if batiment in ["monolythe","cabane_grande","grange_grande","mine","foresterie"] :#batiment 2*2
            self.methode_construction = 2
        else:#batiment 1*1
            self.methode_construction = 1
        self.MODE_POSITION = True
    
    def verif_lay_building(self,x,y) -> bool:
        """on verifie que le batiment peut etre posé au coordonnée"""
        liste = arcade.check_for_collision_with_list(self.batiment_chose,self.waters)
        liste2 = arcade.check_for_collision_with_list(self.batiment_chose,self.foret.sprite_list)
        liste3 = arcade.check_for_collision_with_list(self.batiment_chose,self.batiments.sprite_list)
        collision_monolythe = False
        if self.monolythe.exist:
            collision_monolythe = arcade.check_for_collision(self.batiment_chose,self.monolythe.sprite)
        return len(liste) == 0 and len(liste2)==0 and len(liste3)==0 and collision_monolythe == False
         
    def lay_building(self,x,y) -> None:
        """le batiment selectionné est posé"""
        if self.verif_lay_building(x,y):
            if self.name_building == "monolythe":
                pos = self.position_building(x,y)
                self.monolythe.create(6,pos[0],pos[1])
                for _ in range(3):#nombre de personnage au debut du jeu
                    self.character.ajoute_perso(x,y)
            else:
                pos = self.position_building(x,y)
                state = self.folder.building_inverse[self.name_building+"3"]
                self.batiments.append(Batiment(self.folder,state,pos[0],pos[1]))
            
    def setup_game(self,new) -> None:
        """Initialise les éléments in-game
        de l'affichage"""
        self.create_map_view(new)
        self.create_forest_view()
        self.create_field_view()

        self.batiments = Batiments()
        if not new:
            for batiment in self.folder.all_batiments:
                self.batiments.append(Batiment(self.folder,batiment[0],batiment[1],batiment[2]))
        self.monolythe = Monolythe(self.folder)
        if not new:
            self.monolythe.exist = self.folder.monolythe[0]
            self.monolythe.state = self.folder.monolythe[1]
            self.monolythe.old_state = self.folder.monolythe[1]
            self.monolythe.x = self.folder.monolythe[2]
            self.monolythe.y = self.folder.monolythe[3]
            self.monolythe.charge()
        self.character = Residents(self.folder,self.world,self.monolythe,self)
        if not new:
            for character in self.folder.characters:
                self.character.ajoute_perso(character[3],character[4],character[0],character[1],character[2],character[5],character[6],character[7])

        #creer un point de vision pour l'affichage de la carte
        self.point_of_view = arcade.Sprite("assets/sprites/tiled/pixel.png")
        self.point_of_view.center_x = self.width/2
        self.point_of_view.center_y = self.width/2

        #on cree la mur d'eau que les personnages ne pourront pas passer
        self.barrier = arcade.SpriteList(use_spatial_hash=True)
        for ligne in self.world.waters:
            for case in ligne:
                if type(case) != int:
                    self.barrier.append(case)
    
    def setup_gui(self) -> None:
        """Initialise les élements utiles pour le gui"""
        #le setup pour le jeu en action
        self.buttons = [
            {"image": arcade.load_texture("assets/sprites/symboles/cueilleur.png"), "variable": 0, "name": "cueilleur", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/bucheron.png"), "variable": 0, "name": "bucheron", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/mineur.png"), "variable": 0, "name": "mineur", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/constructeur.png"), "variable": 0, "name": "constructeur", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/chercheur.png"), "variable": 0, "name": "chercheur", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/agriculteur.png"), "variable": 0, "name": "agriculteur", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/pecheur.png"), "variable": 0, "name": "pecheur", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/lancier.png"), "variable": 0, "name": "lancier", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/archer.png"), "variable": 0, "name": "archer", "visible": True},
            {"image": arcade.load_texture("assets/sprites/symboles/chomeur.png"), "variable": 0, "name": "chomeur", "visible": True}
        ]
        for job in self.folder.jobs:
            for i in self.buttons:
                if job == i["name"]:
                    i["visible"] = self.folder.jobs[job]
        self.button_positions = self.calculate_button_positions(self.buttons)

        #on ajoute les positions des rectangles
        self.rect_black = [self.width / 2, self.height / 2,self.width * 0.8,self.height * 0.8]
        self.rect_white = [self.width / 2, self.height / 2,self.width * 0.8-40,self.height * 0.8-40]
        self.rect_almond = [self.width / 2, self.height/2+self.rect_white[3]/2-52/2,self.rect_white[2],52]       
        self.start_x = self.width / 2 - self.rect_almond[2] / 2
        self.start_y = self.rect_almond[1]

        #categorie de la page d'amelioration
        self.button_paths = ["technologie","capacite","retour"]
        self.categories = []
        self.categorie_value = 1
        for categorie in self.button_paths:
            image = arcade.Sprite("assets/sprites/symboles/"+categorie+".png")
            self.categories.append(image)
            image.center_x = self.start_x
            image.center_y = self.start_y
        
        total_buttons_width = sum([image.width for image in self.categories])
        spacing = (self.rect_almond[2] - total_buttons_width) / (len(self.categories) + 1)
        for i, image in enumerate(self.categories):
            image.center_x = self.start_x + (32 / 2) + spacing * (i + 1) + sum([self.categories[j].width for j in range(i)])
            image.center_y = self.start_y

        #images de l'arbre d'amelioration des metiers
        self.jobs = ["cueilleur","bucheron","constructeur","chercheur","mineur","agriculteur","pecheur","lancier","archer"]
        self.upgrades_not_done = []
        self.upgrades_done = []
        self.information_jobs = -1
        for job in self.jobs:
            self.upgrades_not_done.append(arcade.Sprite("assets/sprites/symboles/"+job+"_none.png"))
            self.upgrades_done.append(arcade.Sprite("assets/sprites/symboles/"+job+".png"))
        self.positions_jobs = self.images_position(self.upgrades_done,[1, 2, 2, 2, 1, 1])
        for i in range(len(self.jobs)):
            x,y=self.positions_jobs[i]
            self.upgrades_done[i].center_x = x
            self.upgrades_done[i].center_y = y
            self.upgrades_not_done[i].center_x = x
            self.upgrades_not_done[i].center_y = y

        #images de l'arbre d'amelioration des batiments
        self.building = ["monolythe","cabane","foresterie","grange","cabane_grande","grange_grande","mine"]
        self.building_not_done = [None]
        self.information_building = -1
        self.building_done = [arcade.Sprite("assets/sprites/building/monolythe.png")]
        for i in range(1,len(self.building)):
            self.building_not_done.append(arcade.Sprite("assets/sprites/building/"+self.building[i]+"_none.png"))
            self.building_done.append(arcade.Sprite("assets/sprites/building/"+self.building[i]+".png"))
        self.positions_building = self.images_position(self.building_done,[1,1,1,2,2])
        
        for i in range(len(self.building)):
            x,y=self.positions_building[i]
            self.building_done[i].center_x = x
            self.building_done[i].center_y = y
            if i != 0:
                self.building_not_done[i].center_x = x
                self.building_not_done[i].center_y = y
        
        #page d'information des ellements
        self.rect_info1 = [self.rect_white[0]+self.rect_white[2]/5,self.rect_white[1],self.rect_white[2]/2,self.rect_white[3]/2]
        self.rect_info2 = [self.rect_info1[0],self.rect_info1[1],self.rect_info1[2]-10,self.rect_info1[3]-10]

        #boutons vers l'arbre d'amelioration
        self.button_upgrade_on = arcade.Sprite("assets/sprites/symboles/amelioration_dispo.png")
        self.button_upgrade_off = arcade.Sprite("assets/sprites/symboles/amelioration_indispo.png")
        self.button_upgrade_on.left = 0
        self.button_upgrade_off.left = 0
        self.button_upgrade_on.top = self.height - 32
        self.button_upgrade_off.top = self.height - 32
        self.AMELIORATION = False
        
        #boutons vers le menu construction
        self.button_building = arcade.Sprite("assets/sprites/building/building.png")
        self.button_building.left = 0
        self.button_building.top = self.height - 64
        self.BUILDING = False

        #boutons vers la PAUSE
        self.button_pause = arcade.Sprite("assets/sprites/symboles/pause.png")
        self.button_play = arcade.Sprite("assets/sprites/symboles/play.png")
        self.button_pause.left = 0
        self.button_play.left = 0
        self.button_pause.top = self.height - 96
        self.button_play.top = self.height - 96
        self.PAUSE = False

        #boutons parcours affichage
        self.button_fleche = arcade.Sprite("assets/sprites/symboles/fleche.png")
        self.button_fleche.left = 0
        self.button_fleche.top = self.height - 128

        #boutons sauvegarde
        self.button_save = arcade.Sprite("assets/sprites/symboles/save.png")
        self.button_save.left = 0
        self.button_save.top = self.height - 160

        #boutons sauvegarde
        self.button_house = arcade.Sprite("assets/sprites/symboles/house.png")
        self.button_house.left = 0
        self.button_house.top = self.height - 192

        #setup de informations du jeu en haut
        self.sprite_nourriture = arcade.load_texture("assets/sprites/symboles/nourriture.png")
        self.sprite_buche = arcade.load_texture("assets/sprites/symboles/buche.png")
        self.sprite_roche = arcade.load_texture("assets/sprites/symboles/roche.png")

        #variables utiles
        self.rectangle_width = self.width // 2
        self.almond_color = (255, 179, 143)#(233, 150, 122)beaucoup plus foncé
        self.image_width = 32
        self.total_image_width = 3 * self.image_width
        self.total_spacing = self.rectangle_width - self.total_image_width
        self.spacing_between_images = self.total_spacing // 4
        self.image_y = self.height - 16

    def images_position(self,tab,ensemble) -> None:
        """Calcule les positions des images des jobs en fonction de leurs deverouillages"""
        start_x = self.width / 2 - 0.4 * self.width / 2
        start_y = self.height / 2 + 0.4 * self.height / 2
        positions = []
        vertical_positions = [-50, -100, -150, -200, -250, -300]
        index = 0
        for group_index, num_images in enumerate(ensemble):
            for _ in range(num_images):
                x = start_x + (tab[index].width / 2) + (tab[index].width * _)
                y = start_y + vertical_positions[group_index]
                positions.append([x, y])
                index += 1
        return positions

    def calculate_button_positions(self,tab) -> list:
        """On calcule la position des boutons selon le nombre de metier debloqué"""
        visible_buttons = [button for button in tab if button["visible"]]
        num_buttons = len(visible_buttons)
        button_positions = []
        for i in range(num_buttons):
            button_positions.append(((2*i + 1) * self.width // (2*num_buttons), 15))
        return button_positions

    def create_map_view(self,new) -> None:
        """créer la carte principale"""
        self.map_list = arcade.SpriteList(use_spatial_hash=True)
        j = -1
        for ligne in self.world.sprites_map:
            j+=1
            i=-1
            for sprite in ligne:
                i+=1
                if type(sprite) == arcade.Sprite:
                    sprite.center_x = self.origine_x+j*self.zoom
                    sprite.center_y = self.origine_y+i*self.zoom
                    self.map_list.append(sprite)
        self.foret = Forets()
        if new:
            #on créer la foret de depart
            j = -1
            for ligne in self.world.foret:
                j+=1
                i=-1
                for case in ligne:
                    i+=1
                    if type(case) == int:
                        x = self.origine_x+j*self.zoom
                        y = self.origine_y+i*self.zoom
                        if case in [13,14,15,16,17]:
                            self.foret.ajout_arbre(Arbre(self.folder,case,x,y))
                        elif case in [20,21,22]:
                            self.foret.ajout_arbre(Sapin(self.folder,case,x,y))
        else:
            for arbre in self.folder.forets:
                if arbre[0] in [13,14,15,16,17,18,19]:
                    self.foret.ajout_arbre(Arbre(self.folder,arbre[0],arbre[1],arbre[2]))
                elif arbre[0] in [20,21,22,23,24]:
                    self.foret.ajout_arbre(Sapin(self.folder,arbre[0],arbre[1],arbre[2]))

        self.waters = arcade.SpriteList(use_spatial_hash=True)
        j = -1
        for ligne in self.world.sprites_waters:
            j+=1
            i=-1
            for sprite in ligne:
                i+=1
                if type(sprite) == arcade.Sprite:
                    sprite.center_x = self.origine_x+j*self.zoom
                    sprite.center_y = self.origine_y+i*self.zoom
                    self.waters.append(sprite)

    def create_forest_view(self) -> None:
        """affiche le filtre de la foret"""
        self.forest_list = arcade.SpriteList(use_spatial_hash=True)
        j=-1
        for ligne in self.world.sprites_forest:
            j+=1
            i= -1
            for sprite in ligne:
                i += 1
                if type(sprite) == arcade.Sprite:
                    sprite.center_x = self.origine_x+j*self.zoom
                    sprite.center_y = self.origine_y+i*self.zoom
                    self.forest_list.append(sprite)

    def create_field_view(self) -> None:
        """affiche le filtre de l'agriculture"""
        self.field_list = arcade.SpriteList(use_spatial_hash=True)
        j = -1
        for ligne in self.world.sprites_field:
            j += 1
            i =- 1
            for sprite in ligne:
                i += 1
                if type(sprite) == arcade.Sprite:
                    sprite.center_x = self.origine_x+j*self.zoom
                    sprite.center_y = self.origine_y+i*self.zoom
                    self.field_list.append(sprite)

    def scroll_to_view(self) -> None:
        """Fait un petit effet sur la camera"""
        # Scroll left
        left_boundary = self.view_left + self.margin_camera
        if self.point_of_view.left < left_boundary:
            self.view_left -= left_boundary - self.point_of_view.left

        # Scroll right
        right_boundary = self.view_left + self.width - self.margin_camera
        if self.point_of_view.right > right_boundary:
            self.view_left += self.point_of_view.right - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.height - self.margin_camera
        if self.point_of_view.top > top_boundary:
            self.view_bottom += self.point_of_view.top - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + self.margin_camera
        if self.point_of_view.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.point_of_view.bottom

        # Scroll to the proper location
        position = self.view_left, self.view_bottom
        self.camera_world.move_to(position, self.CAMERA_SPEED)

    def affiche_gui(self,fps,time) -> None:
        """affiche les boutons et toutes les interfaces in-game"""
        self.camera_gui.use()
        if self.AMELIORATION:#gui des ameliorations
            arcade.draw_rectangle_filled(self.rect_black[0],self.rect_black[1],self.rect_black[2],self.rect_black[3],arcade.color.BLACK)
            arcade.draw_rectangle_filled(self.rect_white[0],self.rect_white[1],self.rect_white[2],self.rect_white[3],arcade.color.WHITE)
            arcade.draw_rectangle_filled(self.rect_almond[0],self.rect_almond[1],self.rect_almond[2],self.rect_almond[3],arcade.color.ALMOND)
            for i, image in enumerate(self.categories):#affichage des catégories d'améliorations
                image.draw()

            if self.categorie_value == 1:#affichage de l'arbre des batiments
                arcade.draw_line(self.positions_building[0][0], self.positions_building[0][1],self.positions_building[1][0], self.positions_building[1][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_building[1][0], self.positions_building[1][1],self.positions_building[2][0], self.positions_building[2][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_building[2][0], self.positions_building[2][1],self.positions_building[3][0], self.positions_building[3][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_building[2][0], self.positions_building[2][1],self.positions_building[4][0], self.positions_building[4][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_building[3][0], self.positions_building[3][1],self.positions_building[5][0], self.positions_building[5][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_building[4][0], self.positions_building[4][1],self.positions_building[6][0], self.positions_building[6][1], arcade.color.BLACK, 1)
                
                arcade.draw_text(str(self.folder.settings["point_batiment"])+" point(s)",self.rect_white[0]+self.rect_white[2]/3,self.rect_white[1]+self.rect_white[3]/2-self.rect_almond[3]-50,arcade.color.YELLOW_ORANGE,25)
                
                for i in range(len(self.building)):
                    if self.folder.batiments[self.building[i]]:#si le metier est deja deverouillé
                        self.building_done[i].draw()
                        if self.information_building == i:
                            arcade.draw_rectangle_filled(self.rect_info1[0],self.rect_info1[1],self.rect_info1[2],self.rect_info1[3],arcade.color.BLACK)
                            arcade.draw_rectangle_filled(self.rect_info2[0],self.rect_info2[1],self.rect_info2[2],self.rect_info2[3],arcade.color.WHITE)
                            arcade.draw_text(self.building[i] + " : déverouiller.",self.rect_info2[0]-self.rect_info2[2]/2,self.rect_info2[1]+self.rect_info2[3]/2,arcade.color.BLACK,20,anchor_x="left",anchor_y="top",bold=True,italic=True)

                    else:#si le metier n'est pas deverouillé
                        self.building_not_done[i].draw()
                        if self.information_building == i:
                            arcade.draw_rectangle_filled(self.rect_info1[0],self.rect_info1[1],self.rect_info1[2],self.rect_info1[3],arcade.color.BLACK)
                            arcade.draw_rectangle_filled(self.rect_info2[0],self.rect_info2[1],self.rect_info2[2],self.rect_info2[3],arcade.color.WHITE)
                            arcade.draw_text(self.building[i] + " -> " + str(self.folder.data[self.building[i]])+" point(s)",self.rect_info2[0]-self.rect_info2[2]/2,self.rect_info2[1]+self.rect_info2[3]/2,arcade.color.BLACK,20,anchor_x="left",anchor_y="top",bold=True,italic=True)

                
            if self.categorie_value == 2:#affichage de l'arbre metiers
                arcade.draw_line(self.positions_jobs[0][0], self.positions_jobs[0][1],self.positions_jobs[1][0], self.positions_jobs[1][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_jobs[0][0], self.positions_jobs[0][1],self.positions_jobs[2][0], self.positions_jobs[2][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_jobs[1][0], self.positions_jobs[1][1],self.positions_jobs[3][0], self.positions_jobs[3][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_jobs[2][0], self.positions_jobs[2][1],self.positions_jobs[4][0], self.positions_jobs[4][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_jobs[3][0], self.positions_jobs[3][1],self.positions_jobs[5][0], self.positions_jobs[5][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_jobs[4][0], self.positions_jobs[4][1],self.positions_jobs[6][0], self.positions_jobs[6][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_jobs[5][0], self.positions_jobs[5][1],self.positions_jobs[7][0], self.positions_jobs[7][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_jobs[6][0], self.positions_jobs[6][1],self.positions_jobs[7][0], self.positions_jobs[7][1], arcade.color.BLACK, 1)
                arcade.draw_line(self.positions_jobs[7][0], self.positions_jobs[7][1],self.positions_jobs[8][0], self.positions_jobs[8][1], arcade.color.BLACK, 1)
            
                arcade.draw_text(str(self.folder.settings["point_jobs"])+" point(s)",self.rect_white[0]+self.rect_white[2]/3,self.rect_white[1]+self.rect_white[3]/2-self.rect_almond[3]-50,arcade.color.YELLOW_ORANGE,25)
                
                for i in range(len(self.jobs)):
                    if self.folder.jobs[self.jobs[i]]:#si le metier est deja deverouillé
                        self.upgrades_done[i].draw()
                        if self.information_jobs == i:
                            arcade.draw_rectangle_filled(self.rect_info1[0],self.rect_info1[1],self.rect_info1[2],self.rect_info1[3],arcade.color.BLACK)
                            arcade.draw_rectangle_filled(self.rect_info2[0],self.rect_info2[1],self.rect_info2[2],self.rect_info2[3],arcade.color.WHITE)                    
                            arcade.draw_text(self.jobs[i] + " : déverouiller.",self.rect_info2[0]-self.rect_info2[2]/2,self.rect_info2[1]+self.rect_info2[3]/2,arcade.color.BLACK,25,anchor_y="top",bold=True,italic=True)

                    else:#si le metier n'est pas disponible
                        self.upgrades_not_done[i].draw()
                        if self.information_jobs == i:
                            arcade.draw_rectangle_filled(self.rect_info1[0],self.rect_info1[1],self.rect_info1[2],self.rect_info1[3],arcade.color.BLACK)
                            arcade.draw_rectangle_filled(self.rect_info2[0],self.rect_info2[1],self.rect_info2[2],self.rect_info2[3],arcade.color.WHITE)                    
                            arcade.draw_text(self.jobs[i] + " -> " + str(self.folder.data[self.jobs[i]])+" point(s)",self.rect_info2[0]-self.rect_info2[2]/2,self.rect_info2[1]+self.rect_info2[3]/2,arcade.color.BLACK,25,anchor_y="top",bold=True,italic=True)
        if self.BUILDING:#gui des batiments
            arcade.draw_rectangle_filled(self.rect_black[0],self.rect_black[1],self.rect_black[2],self.rect_black[3],arcade.color.BLACK)
            arcade.draw_rectangle_filled(self.rect_white[0],self.rect_white[1],self.rect_white[2],self.rect_white[3],arcade.color.WHITE)
            arcade.draw_rectangle_filled(self.rect_almond[0],self.rect_almond[1],self.rect_almond[2],self.rect_almond[3],arcade.color.ALMOND)
            self.categories[2].draw()
            arcade.draw_text("Menu construction",self.rect_almond[0]-self.rect_almond[2]/2,self.rect_almond[1]-self.rect_almond[3]/3,arcade.color.YELLOW_ORANGE,25)

            for i in range(len(self.building)):
                    if self.folder.batiments[self.building[i]]:#si le metier est deja deverouillé
                        self.building_done[i].draw()
                        if self.information_building == i:
                            arcade.draw_rectangle_filled(self.rect_info1[0],self.rect_info1[1],self.rect_info1[2],self.rect_info1[3],arcade.color.BLACK)
                            arcade.draw_rectangle_filled(self.rect_info2[0],self.rect_info2[1],self.rect_info2[2],self.rect_info2[3],arcade.color.WHITE)
                            arcade.draw_text(self.building[i] + " : déverouiller.",self.rect_info2[0]-self.rect_info2[2]/2,self.rect_info2[1]+self.rect_info2[3]/2,arcade.color.BLACK,20,anchor_x="left",anchor_y="top",bold=True,italic=True)

                    else:#si le metier n'est pas deverouillé
                        self.building_not_done[i].draw()
                        if self.information_building == i:
                            arcade.draw_rectangle_filled(self.rect_info1[0],self.rect_info1[1],self.rect_info1[2],self.rect_info1[3],arcade.color.BLACK)
                            arcade.draw_rectangle_filled(self.rect_info2[0],self.rect_info2[1],self.rect_info2[2],self.rect_info2[3],arcade.color.WHITE)
                            arcade.draw_text(self.building[i] + " : vérouillé.",self.rect_info2[0]-self.rect_info2[2]/2,self.rect_info2[1]+self.rect_info2[3]/2,arcade.color.BLACK,20,anchor_x="left",anchor_y="top",bold=True,italic=True)
        if self.PAUSE:#gui de la pause
            self.button_play.draw()
        else:#jeu en action
            if self.folder.settings["point_jobs"] >0 or self.folder.settings["point_batiment"] >0:#si amelioration disponible
                self.button_upgrade_on.draw()
            else:#si aucune amelioration disponible
                self.button_upgrade_off.draw()
            self.button_building.draw()
            self.button_pause.draw()
            self.button_fleche.draw()
            self.button_save.draw()
            self.button_house.draw()

            #le haut du gui
            arcade.draw_rectangle_filled(self.width // 2, self.height - 16, self.width, 32, arcade.color.ALMOND)
            self.image_x = self.width // 4 - self.rectangle_width // 2 + self.spacing_between_images + self.image_width // 2
            arcade.draw_rectangle_filled(self.width // 4, self.height - 16, self.rectangle_width, 32, self.almond_color)
            self.sprite_nourriture.draw_scaled(self.image_x, self.image_y)
            arcade.draw_text(str(self.folder.ressources["nourriture"]), self.image_x + self.image_width + 5, self.image_y, arcade.color.BLACK,bold=True , font_size=12, anchor_x="left", anchor_y="center")
            self.image_x += self.image_width + self.spacing_between_images
            self.sprite_buche.draw_scaled(self.image_x, self.image_y)
            arcade.draw_text(str(self.folder.ressources["buche"]), self.image_x + self.image_width + 5, self.image_y, arcade.color.BLACK,bold=True , font_size=12, anchor_x="left", anchor_y="center")
            self.image_x += self.image_width + self.spacing_between_images
            self.sprite_roche.draw_scaled(self.image_x, self.image_y)
            arcade.draw_text(str(self.folder.ressources["roche"]), self.image_x + self.image_width + 5, self.image_y, arcade.color.BLACK,bold=True , font_size=12, anchor_x="left", anchor_y="center")

            #le bas du gui
            arcade.draw_lrtb_rectangle_filled(0, self.width, 30, 0, arcade.color.ALMOND)
            visible_buttons = [button for button in self.buttons if button["visible"]]
            for button, button_position in zip(visible_buttons, self.button_positions):
                arcade.draw_texture_rectangle(button_position[0], button_position[1],button["image"].width, button["image"].height,button["image"])
                arcade.draw_text(f"{button['variable']}", button_position[0] + button["image"].width / 2 + 10, button_position[1], arcade.color.RED, 16, anchor_y="center")

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        """on verifie si la souris se trouve sur un endroit précis"""
        if self.AMELIORATION:#amelioration
            if self.categorie_value == 1:#si on clic sur les boutons des batiments
                var = False
                for i in range(len(self.building)):
                    if self.building_done[i].center_x - self.building_done[i].width / 2 <= x <= self.building_done[i].center_x + self.building_done[i].width / 2 and self.building_done[i].center_y - self.building_done[i].height / 2 <= y <= self.building_done[i].center_y + self.building_done[i].height / 2:
                        self.information_building = i
                        var = True
                if not var:
                    self.information_building = -1

            elif self.categorie_value == 2:#si on clic sur les boutons des metiers
                var = False
                for i in range(len(self.jobs)):
                    if self.upgrades_done[i].center_x - self.upgrades_done[i].width / 2 <= x <= self.upgrades_done[i].center_x + self.upgrades_done[i].width / 2 and self.upgrades_done[i].center_y - self.upgrades_done[i].height / 2 <= y <= self.upgrades_done[i].center_y + self.upgrades_done[i].height / 2:
                        self.information_jobs = i
                        var = True
                if not var:
                    self.information_jobs = -1
        if self.BUILDING:#menu construction
            var = False
            for i in range(len(self.building)):
                if self.building_done[i].center_x - self.building_done[i].width / 2 <= x <= self.building_done[i].center_x + self.building_done[i].width / 2 and self.building_done[i].center_y - self.building_done[i].height / 2 <= y <= self.building_done[i].center_y + self.building_done[i].height / 2:
                    self.information_building = i
                    var = True
            if not var:
                self.information_building = -1

    def on_mouse_press(self, x, y,x2,y2, button) -> bool:
        """Verifications des clics de souris dans le jeu, en renvoie si le joueur demande un enregistrement"""
        if self.MODE_POSITION and button == arcade.MOUSE_BUTTON_LEFT:
            self.lay_building(x2,y2)
            self.MODE_POSITION = False
        if self.MODE_POSITION and button == arcade.MOUSE_BUTTON_RIGHT:
            self.MODE_POSITION = False
        if self.AMELIORATION:#dans le menu amelioration
            for i in range(len(self.categories)):#si on clic sur les boutons des categories
                if self.categories[i].center_x - self.categories[i].width / 2 <= x <= self.categories[i].center_x + self.categories[i].width / 2 and self.categories[i].center_y - self.categories[i].height / 2 <= y <= self.categories[i].center_y + self.categories[i].height / 2:
                    if i == 0:
                        self.categorie_value = 1
                    elif i == 1:
                        self.categorie_value = 2
                    elif i == 2:
                        self.categorie_value = 1
                        self.AMELIORATION = False
            if self.categorie_value == 1:#si on clic sur les boutons des batiments on verifie si l'amelioration est debloquable
                for i in range(len(self.building)):
                    if self.building_done[i].center_x - self.building_done[i].width / 2 <= x <= self.building_done[i].center_x + self.building_done[i].width / 2 and self.building_done[i].center_y - self.building_done[i].height / 2 <= y <= self.building_done[i].center_y + self.building_done[i].height / 2:
                        if self.building[i] == "cabane" and self.folder.batiments[self.building[i]] == False:
                            if self.folder.settings["point_batiment"] >= self.folder.data[self.building[i]]:
                                self.folder.settings["point_batiment"] -= self.folder.data[self.building[i]]
                                self.folder.batiments[self.building[i]] = True
                        if self.building[i] == "cabane_grande" and self.folder.batiments[self.building[i]] == False:
                            if self.folder.settings["point_batiment"] >= self.folder.data[self.building[i]]:
                                self.folder.settings["point_batiment"] -= self.folder.data[self.building[i]]
                                self.folder.batiments[self.building[i]] = True
                        if self.building[i] == "grange" and self.folder.batiments[self.building[i]] == False:
                            if self.folder.settings["point_batiment"] >= self.folder.data[self.building[i]]:
                                self.folder.settings["point_batiment"] -= self.folder.data[self.building[i]]
                                self.folder.batiments[self.building[i]] = True
                        if self.building[i] == "grange_grande" and self.folder.batiments[self.building[i]] == False:
                            if self.folder.settings["point_batiment"] >= self.folder.data[self.building[i]]:
                                self.folder.settings["point_batiment"] -= self.folder.data[self.building[i]]
                                self.folder.batiments[self.building[i]] = True
                        if self.building[i] == "foresterie" and self.folder.batiments[self.building[i]] == False:
                            if self.folder.settings["point_batiment"] >= self.folder.data[self.building[i]]:
                                self.folder.settings["point_batiment"] -= self.folder.data[self.building[i]]
                                self.folder.batiments[self.building[i]] = True
                        if self.building[i] == "mine" and self.folder.batiments[self.building[i]] == False:
                            if self.folder.settings["point_batiment"] >= self.folder.data[self.building[i]]:
                                self.folder.settings["point_batiment"] -= self.folder.data[self.building[i]]
                                self.folder.batiments[self.building[i]] = True

            if self.categorie_value == 2:#si on clic sur les boutons des metiers on verifie si l'amelioration est debloquable
                for i in range(len(self.jobs)):
                    if self.upgrades_done[i].center_x - self.upgrades_done[i].width / 2 <= x <= self.upgrades_done[i].center_x + self.upgrades_done[i].width / 2 and self.upgrades_done[i].center_y - self.upgrades_done[i].height / 2 <= y <= self.upgrades_done[i].center_y + self.upgrades_done[i].height / 2:
                        
                        if self.jobs[i] == "cueilleur":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]]:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)

                        if self.jobs[i] == "bucheron":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]] and self.folder.jobs["cueilleur"] == True:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)
                        
                        if self.jobs[i] == "constructeur":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]] and self.folder.jobs["cueilleur"] == True:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.settings["point_batiment"] +=1
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)
                        
                        if self.jobs[i] == "chercheur":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]] and self.folder.jobs["bucheron"] == True:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)

                        if self.jobs[i] == "mineur":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]] and self.folder.jobs["constructeur"] == True:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)

                        if self.jobs[i] == "agriculteur":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]] and self.folder.jobs["chercheur"] == True:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)

                        if self.jobs[i] == "pecheur":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]] and self.folder.jobs["mineur"] == True:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)

                        if self.jobs[i] == "lancier":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]] and self.folder.jobs["agriculteur"] == True and self.folder.jobs["pecheur"] == True:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)

                        if self.jobs[i] == "archer":
                            if self.folder.settings["point_jobs"] >= self.folder.data[self.jobs[i]] and self.folder.jobs["lancier"] == True:
                                for button in self.buttons:
                                    if button["name"] == self.jobs[i]:
                                        if button["visible"] == False:
                                            button["visible"] = True
                                            self.folder.settings["point_jobs"] -= self.folder.data[self.jobs[i]]
                                            self.folder.jobs[self.jobs[i]] = True
                                            self.button_positions = self.calculate_button_positions(self.buttons)
        elif self.BUILDING:#dans le menu construction
            image = self.categories[2]
            if image.center_x - image.width / 2 <= x <= image.center_x + image.width / 2 and image.center_y - image.height / 2 <= y <= image.center_y + image.height / 2:
                self.BUILDING = False
            if self.categorie_value == 1:#si on clic sur les boutons des batiments
                for i in range(len(self.building)):
                    if self.building_done[i].center_x - self.building_done[i].width / 2 <= x <= self.building_done[i].center_x + self.building_done[i].width / 2 and self.building_done[i].center_y - self.building_done[i].height / 2 <= y <= self.building_done[i].center_y + self.building_done[i].height / 2:
                        if self.folder.batiments[self.building[i]]:
                            if i == 0:
                                if self.monolythe.exist == False:
                                    self.BUILDING = False
                                    self.choose_building("monolythe")
                            else:
                                self.BUILDING = False
                                self.choose_building(self.building[i])
        elif self.PAUSE:#dans le menu pause
            if (self.button_pause.left <= x <= self.button_pause.right and self.button_pause.bottom <= y <= self.button_pause.top):
                self.PAUSE = False
        else:#dans le jeu
            if (self.button_upgrade_off.left <= x <= self.button_upgrade_off.right and self.button_upgrade_off.bottom <= y <= self.button_upgrade_off.top):
                self.AMELIORATION = True
            elif (self.button_building.left <= x <= self.button_building.right and self.button_building.bottom <= y <= self.button_building.top):
                self.BUILDING = True
            elif (self.button_pause.left <= x <= self.button_pause.right and self.button_pause.bottom <= y <= self.button_pause.top):
                self.PAUSE = True
            elif (self.button_fleche.left <= x <= self.button_fleche.right and self.button_fleche.bottom <= y <= self.button_fleche.top):
                if self.folder.settings["affiche_parcours"] == False:
                    self.folder.settings["affiche_parcours"] = True
                else:
                    self.folder.settings["affiche_parcours"] = False
            elif (self.button_save.left <= x <= self.button_save.right and self.button_save.bottom <= y <= self.button_save.top):
                return 1
            elif (self.button_house.left <= x <= self.button_house.right and self.button_house.bottom <= y <= self.button_house.top):
                return 2
            elif button == arcade.MOUSE_BUTTON_RIGHT:#bar des metiers
                for button, button_position in zip(self.buttons, self.button_positions):
                    if button["visible"] and button["name"] != "chomeur":
                        if (button_position[0] - button["image"].width / 2 < x < button_position[0] + button["image"].width / 2 and button_position[1] - button["image"].height / 2 < y < button_position[1] + button["image"].height / 2):
                            if button["variable"] > 0:
                                button["variable"] -= 1
                                self.buttons[-1]["variable"] += 1
                                self.character.change_job(button["name"],"chomeur")
            
            elif button == arcade.MOUSE_BUTTON_LEFT:#bar des metiers
                for button, button_position in zip(self.buttons, self.button_positions):
                    if button["visible"] and button["name"] != "chomeur":
                        if (button_position[0] - button["image"].width / 2 < x < button_position[0] + button["image"].width / 2 and button_position[1] - button["image"].height / 2 < y < button_position[1] + button["image"].height / 2):
                            if self.buttons[-1]["variable"] > 0:
                                button["variable"] += 1
                                self.buttons[-1]["variable"] -= 1
                                self.character.change_job("chomeur",button["name"])
        return 0
   
    def draw_carte(self,x,y) -> None:
        """Dessine la carte principale"""
        self.camera_world.use()
        self.map_list.draw()
        self.foret.draw()
        self.batiments.draw()
        self.monolythe.draw()
        self.character.draw()
        if self.folder.settings["affiche_parcours"]:
            for i in self.character.residents:
                if i.job != "chomeur":
                    arcade.draw_line_strip(i.path, arcade.color.BLUE, 2)
        if self.MODE_POSITION:
            self.camera_world.use()
            self.draw_building(x,y)

    def draw_foret(self) -> None:
        """Dessine le filtre des forets du jeu"""
        self.camera_world.use()
        self.forest_list.draw()
    
    def draw_agriculture(self) -> None:
        """Dessine le filtre de l'agriculture du jeu"""
        self.camera_world.use()
        self.field_list.draw()

    def update_character(self,time) -> None:
        """30 mises à jour/sec pour la vitesse des personnages"""
        self.character.update(self.barrier,time,self.foret,self.batiments)

    def update(self,time) -> None:
        """Mise à jour des composantes 10/sec"""
        self.scroll_to_view()
        self.foret.update_foret(time)
        self.monolythe.update(time)
        self.batiments.update(time)

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization