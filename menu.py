from const import *  # Tüm sabitler
from market import Market
import arcade

class Menu:
    def __init__(self, game_instance):
        self.game = game_instance  # YarisOyunu sınıfına referans
        
        # Menü değişkenleri
        self.menu_title = None
        self.start_button = None
        self.exit_button = None
        self.start_rect = None
        self.exit_rect = None
        self.high_score_text = None
        self.menu_background_list = arcade.SpriteList()
        self.menu_button_bg_list = arcade.SpriteList()
        
        # How to play değişkenleri
        self.show_how_to_play = True
        self.how_to_play_close_button = None
        self.how_to_play_close_rect = None
        
        # Market sınıfı referansı
        self.market = Market(self.game)

    def setup_menu(self):
        # Menü arka planı ve buton arka planlarını temizle
        self.menu_button_bg_list.clear()
        arcade.set_background_color(arcade.color.BLACK)
        self.game.game_state = 0

        self.show_how_to_play = True  # Oyun başladığında gösterilsin

        # Menü başlığı ve buton metinleri
        self.menu_title = arcade.Text(SCREEN_TITLE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75,
                                    arcade.color.BLACK, 40, anchor_x="center")
        self.start_button = arcade.Text("Başla", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5,
                                        arcade.color.BLACK, 24, anchor_x="center")
        self.market_button = arcade.Text("Market", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.4,
                                        arcade.color.BLACK, 24, anchor_x="center")
        self.exit_button = arcade.Text("Çıkış", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.3,
                                    arcade.color.BLACK, 24, anchor_x="center")

        # ✅ En yüksek skor metni HER SEFERİNDE yeniden oluşturulmalı
        self.high_score_text = arcade.Text(f"En Yüksek Skor: {self.game.high_score}",
                                        SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2,
                                        arcade.color.BLACK, 18, anchor_x="center")

        # Arka plan sadece bir kere yüklensin
        if not self.menu_background_list:
            background_sprite = arcade.Sprite("assets/images/beyaz_araba_arka_plan.png")
            background_sprite.center_x = SCREEN_WIDTH / 2
            background_sprite.center_y = SCREEN_HEIGHT / 2
            background_sprite.width = SCREEN_WIDTH
            background_sprite.height = SCREEN_HEIGHT
            self.menu_background_list.append(background_sprite)

        # Buton dikdörtgenleri
        buton_genislik = 150
        buton_yukseklik = 50

        self.start_rect = (self.start_button.x - buton_genislik / 2, self.start_button.x + buton_genislik / 2,
                        self.start_button.y - buton_yukseklik / 2, self.start_button.y + buton_yukseklik / 2)
        self.market_rect = (self.market_button.x - buton_genislik / 2, self.market_button.x + buton_genislik / 2,
                            self.market_button.y - buton_yukseklik / 2, self.market_button.y + buton_yukseklik / 2)
        self.exit_rect = (self.exit_button.x - buton_genislik / 2, self.exit_button.x + buton_genislik / 2,
                        self.exit_button.y - buton_yukseklik / 2, self.exit_button.y + buton_yukseklik / 2)

    def setup_market(self):
        # Market sınıfının setup_market metodunu çağır
        self.game.market.setup_market()

    def draw_menu(self):
        self.menu_background_list.draw()

        if not self.show_how_to_play:
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

            self.menu_title.draw()
            self.start_button.draw()
            self.market_button.draw()
            self.exit_button.draw()
            self.high_score_text.draw()

        # Nasıl Oynanır kutusu
        if self.show_how_to_play:
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

            self.how_to_play_close_button = arcade.Text("Kapat", center_x, bottom + 25, arcade.color.RED, 18, anchor_x="center")

            self.how_to_play_close_rect = (
                center_x - 50,
                center_x + 50,
                bottom + 15,
                bottom + 45
            )
            
            self.how_to_play_close_button.draw()
            arcade.draw_lrbt_rectangle_outline(*self.how_to_play_close_rect, arcade.color.RED)

    def draw_market(self):
        # Market sınıfının draw_market metodunu çağır
        self.market.draw_market()

    def handle_menu_click(self, x, y, button, modifiers):
        if self.show_how_to_play and self.how_to_play_close_rect:
            if self.check_button_click(self.how_to_play_close_rect, x, y):
                self.show_how_to_play = False
                return True
                
        if self.game.game_state == 0:  # Ana menü
            if self.check_button_click(self.start_rect, x, y):
                self.game.setup_game()
                return True
            elif self.check_button_click(self.market_rect, x, y):
                self.setup_market()
                return True
            elif self.check_button_click(self.exit_rect, x, y):
                arcade.close_window()
                return True
                
        elif self.game.game_state == 2:  # Market
            # Market sınıfının handle_market_click metodunu çağır
            return self.game.market.handle_market_click(x, y, button, modifiers)
                    
        return False  # Hiçbir buton tıklanmadı

    def check_button_click(self, rect, x, y):
        return rect[0] < x < rect[1] and rect[2] < y < rect[3]

    def update(self, delta_time):
        # Market sınıfının update metodunu çağır
        if self.game.game_state == 2:  # Market durumunda
            self.game.market.update(delta_time)
