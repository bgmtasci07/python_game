import arcade 
from const import *

class GameDrawer:
    def __init__(self, game_instance):
        self.game = game_instance 
    def draw_game(self):
        """Oyun ekranını çizer"""
        self.game.seritler.draw()
        self.game.engeller.draw()
        self.game.araba_list.draw()
        self.game.canlar.draw()

        arcade.draw_text(f"Skor: {int(self.game.skor)}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18)
        arcade.draw_text(f"Coin: {self.game.coins}", 10, SCREEN_HEIGHT - 60, arcade.color.YELLOW, 18)
        arcade.draw_text(f"Can: {self.game.can}", 10, SCREEN_HEIGHT - 90, arcade.color.RED, 18)

    def draw_game_over(self):
        arcade.draw_text("OYUN BİTTİ!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                        arcade.color.RED, 40, anchor_x="center")
        arcade.draw_text("R tuşuna basarak yeniden başlat!",
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                        arcade.color.WHITE, 20, anchor_x="center")


    def draw_menu(self):
        """Ana menüyü çizer"""
        self.game.menu.menu_background_list.draw()

        if not self.game.menu.show_how_to_play:
            arcade.draw_lrbt_rectangle_filled(
                SCREEN_WIDTH / 2 - 100, SCREEN_WIDTH / 2 + 100,
                SCREEN_HEIGHT * 0.5 - 25, SCREEN_HEIGHT * 0.5 + 25,
                (255, 255, 255, 100)
            )
            arcade.draw_lrbt_rectangle_filled(
                SCREEN_WIDTH / 2 - 100, SCREEN_WIDTH / 2 + 100,
                SCREEN_HEIGHT * 0.4 - 25, SCREEN_HEIGHT * 0.4 + 25,
                (255, 255, 255, 100)
            )
            arcade.draw_lrbt_rectangle_filled(
                SCREEN_WIDTH / 2 - 100, SCREEN_WIDTH / 2 + 100,
                SCREEN_HEIGHT * 0.3 - 25, SCREEN_HEIGHT * 0.3 + 25,
                (255, 255, 255, 100)
            )
            arcade.draw_lrbt_rectangle_filled(
                SCREEN_WIDTH / 2 - 125, SCREEN_WIDTH / 2 + 125,
                SCREEN_HEIGHT * 0.2 - 20, SCREEN_HEIGHT * 0.2 + 20,
                (255, 255, 255, 100)
            )

            self.game.menu.menu_title.draw()
            self.game.menu.start_button.draw()
            self.game.menu.market_button.draw()
            self.game.menu.exit_button.draw()
            self.game.menu.high_score_text.draw()

        
    def draw_market(self):
        self.game.market.draw_market()
