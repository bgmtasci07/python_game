import arcade
from const import *  # Tüm sabitleri const.py'den içe aktarıyoruz

class GameDrawer:
    def __init__(self, game_instance):
        self.game = game_instance  # YarisOyunu sınıfına referans

    def draw_game(self):
        """Oyun ekranını çizer"""
        self.game.seritler.draw()
        self.game.engeller.draw()
        self.game.araba_list.draw()
        self.game.canlar.draw()

        # Skor, coin ve can bilgilerini çiz
        arcade.draw_text(f"Skor: {int(self.game.skor)}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18)
        arcade.draw_text(f"Coin: {self.game.coins}", 10, SCREEN_HEIGHT - 60, arcade.color.YELLOW, 18)
        arcade.draw_text(f"Can: {self.game.can}", 10, SCREEN_HEIGHT - 90, arcade.color.RED, 18)

    def draw_game_over(self):
        """Oyun bitti ekranını çizer"""
        arcade.draw_text("OYUN BİTTİ!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                        arcade.color.RED, 40, anchor_x="center")
        arcade.draw_text("R tuşuna basarak yeniden başlat!",
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                        arcade.color.WHITE, 20, anchor_x="center")

    def draw_pause_menu(self):
        """Duraklatma menüsünü çizer"""
        arcade.draw_text("Duraklatıldı", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6,
                        arcade.color.YELLOW, 40, anchor_x="center")

        self.game.pause_continue_button = arcade.Text("Devam Et", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.45,
                                                arcade.color.WHITE, 24, anchor_x="center")
        self.game.pause_mainmenu_button = arcade.Text("Ana Menü", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.35,
                                                arcade.color.WHITE, 24, anchor_x="center")

        self.game.pause_continue_button.draw()
        self.game.pause_mainmenu_button.draw()

        self.game.pause_continue_rect = (self.game.pause_continue_button.x - 75, self.game.pause_continue_button.x + 75,
                                    self.game.pause_continue_button.y - 20, self.game.pause_continue_button.y + 20)
        self.game.pause_mainmenu_rect = (self.game.pause_mainmenu_button.x - 75, self.game.pause_mainmenu_button.x + 75,
                                    self.game.pause_mainmenu_button.y - 20, self.game.pause_mainmenu_button.y + 20)

        arcade.draw_lrbt_rectangle_filled(*self.game.pause_continue_rect, (255, 255, 255, 80))
        arcade.draw_lrbt_rectangle_filled(*self.game.pause_mainmenu_rect, (255, 255, 255, 80))

    def draw_menu(self):
        """Ana menüyü çizer"""
        self.game.menu.menu_background_list.draw()

        if not self.game.menu.show_how_to_play:
            # Şeffaf buton arkaplanları
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

        # Nasıl Oynanır kutusu
        if self.game.menu.show_how_to_play:
            self.draw_how_to_play()

    def draw_how_to_play(self):
        """Nasıl oynanır ekranını çizer"""
        width, height = 650, 500
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        left = center_x - width / 2
        right = center_x + width / 2
        bottom = center_y - height / 2
        top = center_y + height / 2

        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.WHITE_SMOKE)
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.BLACK, border_width=2)

        info_lines = [
            "NASIL OYNANIR?",
            "",
            "▶ Yön tuşları ile aracınızı şeritler arasında hareket ettirin.",
            "▶ Amacınız: engellere çarpmadan mümkün olduğunca uzun süre ilerlemek.",
            "",
            "🔧 Oyun Mekanikleri:",
            "• Engellere çarpmaktan kaçının. Her çarpma bir can götürür.",
            "• Skorunuz arttıkça oyun daha da hızlanır!",
            "• Her 100 skor için 1 coin kazanırsınız.",
            "• Her 500 skor için ekranda 1 horoz (can paketi) belirir.",
            "• Horozlara çarparsanız +1 can kazanırsınız.",
            "",
            "🛒 Market Bilgisi:",
            "• Ana menüdeki 'Market' bölümünden coin ile yeni arabalar satın alabilirsiniz.",
            "• Satın aldığınız arabaları seçerek kullanabilirsiniz.",
            "",
            "⏸ ESC tuşu ile oyunu duraklatabilir / devam ettirebilirsiniz.",
            "",
            "🚗 İyi oyunlar! Pamukkale Drift keyfini çıkarın!"
        ]

        for i, line in enumerate(info_lines):
            arcade.draw_text(line, center_x, center_y + 220 - i * 20,
                            arcade.color.BLACK, 12, anchor_x="center")

        self.game.menu.how_to_play_close_button = arcade.Text("Kapat", center_x, bottom + 25, arcade.color.RED, 18, anchor_x="center")

        self.game.menu.how_to_play_close_rect = (
            center_x - 50,
            center_x + 50,
            bottom + 15,
            bottom + 45
        )
        
        self.game.menu.how_to_play_close_button.draw()
        arcade.draw_lrbt_rectangle_outline(*self.game.menu.how_to_play_close_rect, arcade.color.RED)

    def draw_market(self):
        """Market ekranını çizer"""
        # Market sınıfının draw_market metodunu çağır
        self.game.market.draw_market()
