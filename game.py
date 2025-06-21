#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization

import arcade
import os
from save import*
from monde import*
from affichage import*
from music import*
from objects import*

class Game(arcade.Window):
    def __init__(self) -> None:
        """Fenetre du jeu"""
        super().__init__(title="Destroy-Civilization",fullscreen=True)
        self.set_update_rate(1/60)
        arcade.schedule(self.on_time, 1)#horloge du jeu
        arcade.schedule(self.update_in_game,1/10)#réactions des éléments
        arcade.schedule(self.update_character,1/30)#vitesse des personnages
        arcade.set_background_color((0,0,0))

        #initialisations des touches
        self.UP = False
        self.DOWN = False
        self.RIGHT = False
        self.LEFT = False
        self.MOUSE_ON = False

        #variables utiles
        self.VIEW_SPEED = 10
        self.STATE_GAME = -1
        self.delta_time = 1

        #souris
        self.mouse = arcade.Sprite("assets/sprites/symboles/mouse.png")
        self.set_mouse_visible(False)

        #intro du jeu
        self.music = Music("studio-quaerite")
     
    def init_home(self) -> None:
        """Initialise les élements pour l'écran principale"""
        #music
        self.music = Music("retrowave")
        #on cherche les parties disponibles
        self.liste_parties = []
        for element in os.listdir("data/"):
            if os.path.isdir(os.path.join("data/", element)):
                self.liste_parties.append(element)
        if len(self.liste_parties) == 0:
            self.home_refuse = True
            self.home_raison = "Aucunne sauvegarde"
        else:
            self.home_refuse = False
        #colors
        self.color_fond = (107,114,142)
        self.clic = (80,87,122)
        self.not_clic = (64,66,88)
        self.color_separe = (71,78,104)
        arcade.set_background_color((6, 35, 42))

        #sauvegardes
        self.num_buttons = 4
        self.button_states = [False] * self.num_buttons
        self.total_button_width = 0

        #variables utiles
        self.shift_pressed = False
        self.home = -1
        self.text = ""

        #rectangle de saisie
        self.rect_width = self.width / 3
        self.rectangle_height = self.height * 10 / 100
        self.center_y = self.height * 20 / 100 - self.rectangle_height / 2

        #rectangle de validation à droite
        self.rect_width_2 = self.width / 4
        self.center_x_2 = 8 * self.width / 10

        #rectangle d'action à gauche
        self.rect_width_3 = self.width / 4
        self.center_x_3 = 2 * self.width / 10

    def load_game(self,name) -> None:
        """Charge le jeu à partir d'une sauvegarde"""
        self.folder = Folder(name)
        self.world = World(self.folder)
        self.world.load_world()
        self.time = self.folder.settings["time"]
        self.affichage = Affichage(self.folder,self.world,self.width,self.height,False)
        self.music.stop()
        self.music = Music("perfect-beauty")

    def new_game(self,name) -> None:
        """Initialise le carte du jeu"""
        self.folder = Folder(name,new=True)
        self.world = World(self.folder)
        self.world.create_world(50,75)
        self.time = self.folder.settings["time"]
        self.affichage = Affichage(self.folder,self.world,self.width,self.height,True)
        self.music.stop()
        self.music = Music("perfect-beauty")
        self.folder.SAVE(self.world,self.affichage.batiments,self.affichage.foret,self.affichage.character,self.affichage.monolythe,self.time)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        """on verifie si les coordonnées de la souris sont à l'intérieur de la fenêtre"""
        if 0 <= x <= self.width and 0 <= y <= self.height:
            self.MOUSE_ON = True
            self.mouse.center_x = x
            self.mouse.center_y = y
        else:
            self.MOUSE_ON = False
        
        if self.STATE_GAME == 0:
            RECTANGLE_WIDTH = 200
            RECTANGLE_HEIGHT = 100
            INNER_RECTANGLE_MARGIN = 10
            for i in range(self.num_buttons):
                x_min = self.width // 2 - self.total_button_width // 2 + i * (RECTANGLE_WIDTH + INNER_RECTANGLE_MARGIN * 2)
                x_max = x_min + RECTANGLE_WIDTH
                y_min = self.height // 2 - RECTANGLE_HEIGHT // 2
                y_max = y_min + RECTANGLE_HEIGHT
                if x_min < x < x_max and y_min < y < y_max:
                    self.button_states[i] = True
                else:
                    self.button_states[i] = False

        if self.STATE_GAME == 1:
            self.affichage.on_mouse_motion(x,y,dx,dy)

    def mouse_on_case(self) -> tuple:
        """Renvoie les coordonnées sur lequel se trouve la souris"""
        #on ajuste les coordonées de la souris en fonction de la position de la caméra
        adjusted_x = self.mouse.center_x + self.affichage.camera_world.position[0]
        adjusted_y = self.mouse.center_y + self.affichage.camera_world.position[1]
        return(adjusted_x,adjusted_y)

    def on_mouse_press(self, x: int, y: int, symbol: int, modifiers: int) -> None:
        """Recuperation des clics de souris"""
        if self.STATE_GAME == 0:
            RECTANGLE_WIDTH = 200
            RECTANGLE_HEIGHT = 100
            INNER_RECTANGLE_MARGIN = 10
            for i in range(self.num_buttons):
                x_min = self.width // 2 - self.total_button_width // 2 + i * (RECTANGLE_WIDTH + INNER_RECTANGLE_MARGIN * 2)
                x_max = x_min + RECTANGLE_WIDTH
                y_min = self.height // 2 - RECTANGLE_HEIGHT // 2
                y_max = y_min + RECTANGLE_HEIGHT
                if x_min < x < x_max and y_min < y < y_max:
                    if i == 0:
                        if self.home == 0:
                            self.home = -1
                        else:
                            if len(self.liste_parties) == 0:
                                self.home_refuse = True
                                self.home_raison = "Aucune sauvegarde"
                            else:
                                self.home_refuse = False
                                self.text = self.liste_parties[0]
                                self.partie_chose = 0
                            self.home = 0
                    if i == 1:
                        if self.home == 1:
                            self.home = -1
                        else:
                            if len(self.liste_parties) == 0:
                                self.home_refuse = True
                                self.home_raison = "Aucune sauvegarde"
                            else:
                                self.home_refuse = False
                                self.text = self.liste_parties[0]
                                self.text_action = "Supprimer"
                                self.partie_chose = 0
                            self.home = 1
                    if i == 2:
                        if self.home == 2:
                            self.home = -1
                        else:
                            self.text = "nouvellepartie"
                            self.home = 2
                    if i == 3:
                        arcade.window_commands.close_window()
            
            if not self.home_refuse:
                if self.home == 0:
                    if (self.center_x_2 - self.rect_width_2 / 2 <= x <= self.center_x_2 + self.rect_width_2 / 2 and self.center_y - self.rectangle_height / 2 <= y <= self.center_y + self.rectangle_height / 2):
                        self.load_game(self.liste_parties[self.partie_chose])
                        self.STATE_GAME = 1
                    
                    elif (self.center_x_3 - self.rect_width_3 / 2 <= x <= self.center_x_3 + self.rect_width_3 / 2 and self.center_y - self.rectangle_height / 2 <= y <= self.center_y + self.rectangle_height / 2):
                        nbr = len(self.liste_parties)
                        if self.partie_chose == nbr - 1:
                            self.partie_chose = 0
                        else:
                            self.partie_chose +=1
                        self.text = self.liste_parties[self.partie_chose]

                if self.home == 1:
                    if (self.center_x_3 - self.rect_width_3 / 2 <= x <= self.center_x_3 + self.rect_width_3 / 2 and self.center_y - self.rectangle_height / 2 <= y <= self.center_y + self.rectangle_height / 2):
                        nbr = len(self.liste_parties)
                        if self.partie_chose == nbr - 1:
                            self.partie_chose = 0
                        else:
                            self.partie_chose +=1
                        self.text = self.liste_parties[self.partie_chose]

                    elif (self.center_x_2 - self.rect_width_2 / 2 <= x <= self.center_x_2 + self.rect_width_2 / 2 and self.center_y - self.rectangle_height / 2 <= y <= self.center_y + self.rectangle_height / 2):
                        if self.text_action == "Supprimer":
                            Folder.del_sauvegarde(name=self.text)
                            self.liste_parties = []
                            for element in os.listdir("data/"):
                                if os.path.isdir(os.path.join("data/", element)):
                                    self.liste_parties.append(element)
                            self.home = -1
                        else:
                            Folder.renommer_sauv(self.liste_parties[self.partie_chose],self.text)
                            self.liste_parties = []
                            for element in os.listdir("data/"):
                                if os.path.isdir(os.path.join("data/", element)):
                                    self.liste_parties.append(element)

            if self.home == 2:
                if (self.center_x_2 - self.rect_width_2 / 2 <= x <= self.center_x_2 + self.rect_width_2 / 2 and self.center_y - self.rectangle_height / 2 <= y <= self.center_y + self.rectangle_height / 2):
                    self.new_game(self.text)
                    self.STATE_GAME = 1

        elif self.STATE_GAME == 1:
            x2,y2 = self.mouse_on_case()
            var = self.affichage.on_mouse_press(x,y,x2,y2,symbol)
            if var == 1:
                self.folder.SAVE(self.world,self.affichage.batiments,self.affichage.foret,self.affichage.character,self.affichage.monolythe,self.time)
            elif var == 2:
                self.folder.SAVE(self.world,self.affichage.batiments,self.affichage.foret,self.affichage.character,self.affichage.monolythe,self.time)
                self.init_home()
                self.STATE_GAME = 0

    def on_key_press(self, symbol,modif) -> None:
        """Verification des touches pressées"""
        if symbol == arcade.key.ESCAPE:
            arcade.window_commands.close_window()

        if self.STATE_GAME == 0 and self.home in [0,1,2]:#ecran d'accueil
            if symbol == arcade.key.BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            elif symbol == arcade.key.LSHIFT or symbol == arcade.key.RSHIFT:
                self.shift_pressed = True
            elif self.is_letter_or_digit(symbol) and len(self.text) < 15:#nombres de caractères limite 
                if self.shift_pressed:
                    self.text += chr(symbol).upper()
                    self.shift_pressed = False
                else:
                    self.text += chr(symbol)

        if self.STATE_GAME == 1:#à l'interieur du jeu
            if symbol == arcade.MOUSE_BUTTON_RIGHT:
                self.affichage.MODE_POSITION = False
            elif symbol == arcade.key.UP:
                self.UP = True
            elif symbol == arcade.key.DOWN:
                self.DOWN = True
            elif symbol == arcade.key.LEFT:
                self.LEFT = True
            elif symbol == arcade.key.RIGHT:
                self.RIGHT = True
            elif symbol == arcade.key.S:
                self.folder.SAVE(self.world,self.affichage.batiments,self.affichage.foret,self.affichage.character,self.affichage.monolythe,self.time)
            elif symbol == arcade.key.TAB:
                if self.affichage.filtre == 2:
                    self.affichage.filtre = 0
                else:
                    self.affichage.filtre +=1

    def on_key_release(self, symbol,modif) -> None:
        """Verification des touches non pressées"""
        if symbol == arcade.key.UP:
            self.UP = False
        if symbol == arcade.key.DOWN:
            self.DOWN = False
        if symbol == arcade.key.LEFT:
            self.LEFT = False
        if symbol == arcade.key.RIGHT:
            self.RIGHT = False
        if symbol == arcade.key.LSHIFT or symbol == arcade.key.RSHIFT:
            self.shift_pressed = False

    def is_letter_or_digit(self, key):
        """Renvoie si la touche appuyé peut etre ajouté à la zone de saisie"""
        if 65 <= key <= 90:  # Lettres majuscules
            return True
        elif 97 <= key <= 122:  # Lettres minuscules
            return True
        elif 48 <= key <= 57:  # Chiffres
            return True
        else:
            return False

    def home_draw(self) -> None:
        """On dessine l'ecran d'accueil"""
        RECTANGLE_WIDTH = 200
        RECTANGLE_HEIGHT = 100
        INNER_RECTANGLE_MARGIN = 10
        BUTTON_MARGIN = 50

        arcade.draw_text("Bienvenue",self.width // 2,self.height*0.9,color=self.color_fond,font_size=36,anchor_x="center",anchor_y="center",bold=True,italic=True)

        arcade.draw_rectangle_filled(self.width // 2,self.height // 2,self.width,RECTANGLE_HEIGHT + BUTTON_MARGIN * 2,self.color_separe)
        menu2_width = self.width - INNER_RECTANGLE_MARGIN * 2
        menu2_height = RECTANGLE_HEIGHT + BUTTON_MARGIN - INNER_RECTANGLE_MARGIN * 2
        arcade.draw_rectangle_filled(self.width // 2,self.height // 2,menu2_width,menu2_height,self.color_fond)
        
        self.total_button_width = RECTANGLE_WIDTH * self.num_buttons + INNER_RECTANGLE_MARGIN * 2 * (self.num_buttons - 1)
        start_x = self.width // 2 - self.total_button_width // 2 + RECTANGLE_WIDTH // 2
        
        button_texts = ["Continuer", "Modifier", "Nouveau", "Quitter"]
        for i in range(self.num_buttons):
            x = start_x + i * (RECTANGLE_WIDTH + INNER_RECTANGLE_MARGIN * 2)
            y = self.height // 2
            color = self.not_clic if self.button_states[i] else self.clic
            arcade.draw_rectangle_filled(x,y,RECTANGLE_WIDTH,RECTANGLE_HEIGHT,color)
            arcade.draw_text(button_texts[i],x,y,self.color_separe,font_size=21,anchor_x="center",anchor_y="center",bold=True)

        if self.home == 0:#on dessine si le bouton continuer est appuyé
            if not self.home_refuse:
                arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width, self.rectangle_height, (71, 78, 104))
                arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width - 20, self.rectangle_height - 20, (80, 87, 122))

                arcade.draw_rectangle_filled(self.center_x_2, self.center_y, self.rect_width_2, self.rectangle_height, (71, 78, 104))
                arcade.draw_rectangle_filled(self.center_x_2, self.center_y, self.rect_width_2 - 20, self.rectangle_height - 20, (80, 87, 122))

                arcade.draw_rectangle_filled(self.center_x_3, self.center_y, self.rect_width_3, self.rectangle_height, (71, 78, 104))
                arcade.draw_rectangle_filled(self.center_x_3, self.center_y, self.rect_width_3 - 20, self.rectangle_height - 20, (80, 87, 122)) 

                arcade.draw_text("Continue la partie", self.center_x_2, self.center_y, (64, 66, 88), 26, anchor_x="center", anchor_y="center")
                arcade.draw_text(self.liste_parties[self.partie_chose],self.width / 2, self.center_y,(6, 35, 42), 30, anchor_x="center", anchor_y="center")
                arcade.draw_text("Suivant",self.center_x_3, self.center_y,(6, 35, 42), 30, anchor_x="center", anchor_y="center")
            else:
                arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width, self.rectangle_height, (71, 78, 104))
                arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width - 20, self.rectangle_height - 20, (80, 87, 122))
                arcade.draw_text(self.home_raison,self.width / 2, self.center_y,(6, 35, 42), 30, anchor_x="center", anchor_y="center")            

        if self.home == 1:#on dessine si le bouton modifier est appuyé
            if not self.home_refuse:
                arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width, self.rectangle_height, (71, 78, 104))
                arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width - 20, self.rectangle_height - 20, (80, 87, 122))

                arcade.draw_rectangle_filled(self.center_x_2, self.center_y, self.rect_width_2, self.rectangle_height, (71, 78, 104))
                arcade.draw_rectangle_filled(self.center_x_2, self.center_y, self.rect_width_2 - 20, self.rectangle_height - 20, (80, 87, 122))

                arcade.draw_rectangle_filled(self.center_x_3, self.center_y, self.rect_width_3, self.rectangle_height, (71, 78, 104))
                arcade.draw_rectangle_filled(self.center_x_3, self.center_y, self.rect_width_3 - 20, self.rectangle_height - 20, (80, 87, 122)) 

                arcade.draw_text("Suivant",self.center_x_3, self.center_y,(6, 35, 42), 30, anchor_x="center", anchor_y="center")
                arcade.draw_text(self.text,self.width / 2, self.center_y,(6, 35, 42), 30, anchor_x="center", anchor_y="center")            
                if self.liste_parties[self.partie_chose] == self.text:
                    self.text_action = "Supprimer"
                else:
                    self.text_action = "Renommer"
                arcade.draw_text(self.text_action, self.center_x_2, self.center_y, (64, 66, 88), 26, anchor_x="center", anchor_y="center")

            else:
                arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width, self.rectangle_height, (71, 78, 104))
                arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width - 20, self.rectangle_height - 20, (80, 87, 122))
                arcade.draw_text(self.home_raison,self.width / 2, self.center_y,(6, 35, 42), 30, anchor_x="center", anchor_y="center")            


        if self.home == 2:#on dessine si le bouton nouvelle partie est appuyé
            arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width, self.rectangle_height, (71, 78, 104))
            arcade.draw_rectangle_filled(self.width / 2, self.center_y, self.rect_width - 20, self.rectangle_height - 20, (80, 87, 122))

            arcade.draw_rectangle_filled(self.center_x_2, self.center_y, self.rect_width_2, self.rectangle_height, (71, 78, 104))
            arcade.draw_rectangle_filled(self.center_x_2, self.center_y, self.rect_width_2 - 20, self.rectangle_height - 20, (80, 87, 122))

            arcade.draw_text("Crée une partie", self.center_x_2, self.center_y, (64, 66, 88), 26, anchor_x="center", anchor_y="center")
            arcade.draw_text(self.text,self.width / 2, self.center_y,(6, 35, 42), 30, anchor_x="center", anchor_y="center")

    def on_draw(self) -> None:
        """On dessine l'écran de l'application"""
        self.clear()
        if self.STATE_GAME == -1:#on dessine l'intro
            if 8 <self.music.position() or self.music.position()==0.0:
                arcade.draw_circle_filled(self.width/2, self.height/2, self.circle_radius, arcade.color.WHITE)
                arcade.draw_text("Studio-Quaerite", self.width/2, self.height/2,color=arcade.color.BLACK,font_size=45, anchor_x="center",bold=True,italic=True)
            else:
                arcade.draw_text("Studio-Quaerite", self.width/2, self.height/2,color=arcade.color.WHITE,font_size=45, anchor_x="center",bold=True,italic=True)
        if self.STATE_GAME == 0:#on dessine le menu principale
            self.home_draw()
        if self.STATE_GAME == 1:#dans le cas ou le jeu se joue
            if self.affichage.filtre == 0:#carte principale
                x,y = self.mouse_on_case()
                self.affichage.draw_carte(x,y)
            elif self.affichage.filtre == 1:#foret uniquement
                self.affichage.draw_foret()
            else:#champ uniquement
                self.affichage.draw_agriculture()
            self.affichage.affiche_gui(1/self.delta_time,self.time)

        if self.MOUSE_ON:
            if self.STATE_GAME != 1:
                self.mouse.draw()
            else:
                if not self.affichage.MODE_POSITION:
                    self.mouse.draw()

    def on_update(self, delta_time) -> None:
        """mise a jour du jeu"""
        if self.STATE_GAME == -1:
            self.circle_radius = (int(self.music.position()*1000)-8000) * self.width/200
            if self.music.position() == 0.0:
                self.STATE_GAME = 0
                self.init_home()

        if self.STATE_GAME == 1:
            if not self.affichage.PAUSE:
                if self.UP and not self.DOWN:
                    self.affichage.point_of_view.center_y  += self.VIEW_SPEED
                elif self.DOWN and not self.UP:
                    self.affichage.point_of_view.center_y -= self.VIEW_SPEED
                if self.LEFT and not self.RIGHT:
                    self.affichage.point_of_view.center_x -= self.VIEW_SPEED
                elif self.RIGHT and not self.LEFT:
                    self.affichage.point_of_view.center_x += self.VIEW_SPEED
                self.delta_time = delta_time
        
    def update_character(self,delta_time) -> None:
        """30 mises à jour/sec pour la vitesse des personnages"""
        if self.STATE_GAME == 1:
            if not self.affichage.PAUSE:
                self.affichage.update_character(self.time)

    def update_in_game(self,delta_time) -> None:
        """10 mises à jour/sec des composants du jeu"""
        self.set_mouse_visible(False)
        if self.STATE_GAME == 0:
            self.music.continue_()
        if self.STATE_GAME == 1:
            if not self.affichage.PAUSE:
                self.affichage.update(self.time)
                self.music.continue_()

    def on_time(self,other) -> None:
        """calcule du temps in game pour calculer les décades"""
        if self.STATE_GAME == 1:
            if not self.affichage.PAUSE:
                self.time +=1

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization