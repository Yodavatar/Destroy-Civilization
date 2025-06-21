#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization

import arcade

class Music():
    def __init__(self,name:str) -> None:
        self.song = arcade.load_sound("assets/songs/"+name+".ogg")
        self.player = arcade.play_sound(self.song)
    
    def continue_(self) -> None:
        """Verifie si la musique est terminé et rejoue la musique"""
        if self.is_finished():
            self.replay()

    def replay(self) -> None:
        """Rejoue la musique depuis le début"""
        arcade.stop_sound(self.player)
        self.player = arcade.play_sound(self.song)

    def position(self) -> arcade.Sound:
        """renvoie la position de la musique"""
        return self.song.get_stream_position(self.player)
    
    def length(self) -> float:
        """Renvoie la longueur de la musique"""
        return self.song.get_length()
    
    def is_finished(self) -> bool:
        """Vérifie si la musique est terminée"""
        return self.position() == 0.0
        return self.position() >= self.length()#ne fonctionne pas car je verifie uniquement 10/sec

    def stop(self) -> None:
        """Stop une musique, ou continue la musique si elle est déja arretée"""
        if self.song.is_playing(self.player):
            self.song.stop(self.player)
        else:
            self.song.play()

    def max_volume(self) -> None:
        """Met le volume au maximum"""
        self.song.set_volume(1,self.player)

    def min_volume(self) -> None:
        """Met le volume au minimum"""
        self.song.set_volume(0,self.player)

    def augmente_volume(self,song,aug:int) -> None:
        """Augmente le volume de aug avec 1 comme maximum"""
        volume = song.volume
        if volume + aug >= 1:
            self.max_volume(song)
        else:
            song.set_volume(volume + aug)

    def diminue_volume(self,song,dim:int) -> None:
        """Diminue le volume de dim avec 0 comme minimum"""
        volume = song.volume
        if volume - dim <= 0:
            self.min_volume(song)
        else:
            song.set_volume(volume - dim)

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Game : Destroy-Civilization