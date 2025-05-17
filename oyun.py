import arcade
import random
import time
import os
from const import *  # Tüm sabitleri const.py'den içe aktarıyoruz
from menu import Menu  # Menü sınıfını içe aktarıyoruz
from draw import GameDrawer  # Çizim sınıfını içe aktarıyoruz
from market import Market  # Market sınıfını içe aktarıyoruz

class CanPaketi(arcade.Sprite):
    def __init__(self, x, y, hiz):
        super().__init__()
        self.frames = [arcade.load_texture(f"assets/images/horoz_{i}.png") for i in range(3)]
        self.texture_index = 0
        self.texture = self.frames[self.texture_index]
        self.center_x = x
        self.center_y = y
        self.change_y = -hiz * 0.5
        self.animation_timer = 0
        self.scale = 0.3

        self.change_x = random.choice([-1.5, 1.5])  # Sağ-sol hareket

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x

        if self.left <= 0 or self.right >= SCREEN_WIDTH:
            self.change_x *= -1

        self.center_y += self.change_y

    def update_animation(self, delta_time: float = 1/60):
        self.animation_timer += delta_time
        if self.animation_timer > 0.1:
            self.texture_index = (self.texture_index + 1) % len(self.frames)
            self.texture = self.frames[self.texture_index]
            self.animation_timer = 0


class YarisOyunu(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.game_state = 0  # Menüden başlayalım

        self.game_music = None
        self.game_music_player = None
        if os.path.exists("assets/sounds/denizli_turkusu.wav"):
            self.game_music = arcade.load_sound("assets/sounds/denizli_turkusu.wav")
            
        # Menü, çizim ve market sınıflarını oluştur
        self.menu = Menu(self)  # Menü sınıfını oluştur
        self.drawer = GameDrawer(self)  # Çizim sınıfını oluştur
        self.market = Market(self)  # Market sınıfını oluştur


                # diğer tanımlar:
        self.button_background_list = arcade.SpriteList()
        self.menu_title = None
        self.start_button = None
        # Oyun değişkenleri
        self.coins = 500 # Varsayılan başlangıç
        self.high_score = 0 # Varsayılan en yüksek skor
        self.can = 1 # Başlangıç canı

        try:
            with open("save_data.txt", "r") as f:
                lines = f.readlines()
                if len(lines) >= 1:
                    self.coins = int(lines[0].strip())
                if len(lines) >= 2:
                    self.high_score = int(lines[1].strip())
                if len(lines) >= 3:
                    self.purchased_cars = [bool(int(x)) for x in lines[2].strip().split(',')]
                if len(lines) >= 4:
                    self.selected_car_index = int(lines[3].strip())
        except (FileNotFoundError, ValueError, IndexError):
            self.coins = 500
            self.high_score = 0
            self.purchased_cars = [True, False, False, False]  # Default değer
    

        self.skor = 0
        self.hiz = ENGEL_HIZI
        self.son_engel_zamani = 0
        self.son_coin_skoru = 0
        self.son_can_skoru = 0 # Can paketi için skor takibi

        # Seçilen araba ve market
        self.car_options = [arcade.color.BLUE, arcade.color.RED, arcade.color.YELLOW, arcade.color.GREEN, arcade.color.WHITE]  # 5. öğe sadece listeyi uzatsın diye

        self.car_prices = [0, 500, 1000, 5000, 10000]
        self.purchased_cars = [True, False, False, False, False]
        self.selected_car_index = 0

        # Sprite listeleri
        self.araba_list = arcade.SpriteList()
        self.seritler = arcade.SpriteList()
        self.engeller = arcade.SpriteList()
        self.canlar = arcade.SpriteList() # Can paketleri için SpriteList
        self.menu_background_list = arcade.SpriteList() # Menü arka planı için
        self.menu_button_bg_list = arcade.SpriteList() # Menü buton arka planları için

        # Menü - Market için değişkenler
        self.menu_title = None
        self.start_button = None
        self.market_button = None
        self.exit_button = None
        self.start_rect = None
        self.market_rect = None
        self.exit_rect = None
        self.market_title = None
        self.market_cars = arcade.SpriteList()
        self.market_car_rects = []
        self.market_back_button = None
        self.market_back_rect = None
        self.market_car_price_texts = []
        self.market_coin_text = None
        self.insufficient_coins_text = None
        self.show_insufficient_coins_message = False
        self.insufficient_coins_timer = 0.0
        self.pause_continue_button = None
        self.pause_mainmenu_button = None
        self.pause_continue_rect = None
        self.pause_mainmenu_rect = None
        self.show_how_to_play = True
        self.how_to_play_close_button = None
        self.how_to_play_close_rect = None

    

        self.setup_menu()

    def setup_menu(self):
        # Menü kurulumunu menu.py'deki Menu sınıfına devret
        self.menu.setup_menu()


    def setup_market(self):
        # Market kurulumunu menu.py'deki Menu sınıfına devret
        self.menu.setup_market()


    def setup_game(self):
        arcade.set_background_color(arcade.color.DIM_GRAY)
        self.game_state = 1
        
        # Menü müziği varsa durdur
        if hasattr(self, "menu_music_player") and self.menu_music_player:
            self.menu_music_player.delete()

        # Oyun müziğini başlat
        if self.game_music:
            self.game_music_player = self.game_music.play(loop=True)

        self.araba_list.clear()
        self.seritler.clear()
        self.create_lanes()
        self.engeller.clear()
        self.canlar.clear() # Canları temizle

        self.skor = 0
        self.hiz = ENGEL_HIZI
        self.son_engel_zamani = 0
        self.son_coin_skoru = 0 # Coin skorunu sıfırla
        self.son_can_skoru = 0 # Can skorunu sıfırla
        self.can = 1 # Canı 1'e ayarla

        # Araba oluşturma (seçili araca göre)
        araba_yolu_ve_olcek = [
            ("assets/images/beyaz_araba.png", 0.7),
            ("assets/images/kirmizi_araba.png", 0.4),
            ("assets/images/mor_araba.png", 0.4),
            ("assets/images/klasik_araba.png", 0.4)
        ]

        if self.selected_car_index < len(araba_yolu_ve_olcek):
            yol, olcek = araba_yolu_ve_olcek[self.selected_car_index]
            self.araba = arcade.Sprite(yol, scale=olcek)
        else:
            # Eğer resimli olmayan beşinci araba gibi bir şey eklersen burası çalışır
            self.araba = arcade.SpriteSolidColor(40, 60, self.car_options[self.selected_car_index])

        self.araba.center_x = SCREEN_WIDTH / 2
        self.araba.center_y = 100
        self.araba_list.append(self.araba)


    def create_lanes(self):
        """Yol şeritlerini oluşturur"""
        print("create_lanes() fonksiyonu çalıştı")  # Kontrol için

        toplam_birim = SERIT_YUKSEKLIK + SERIT_BOSLUK
        mevcut_y = SCREEN_HEIGHT + SERIT_YUKSEKLIK / 2

        while mevcut_y > -toplam_birim:
            for x in SERIT_X_KONUMLARI:
                serit = arcade.SpriteSolidColor(SERIT_GENISLIK, SERIT_YUKSEKLIK, arcade.color.YELLOW)  # Gerçek sarı
                serit.center_x = x
                serit.center_y = mevcut_y
                serit.change_y = -self.hiz
                self.seritler.append(serit)
            mevcut_y -= toplam_birim
            
    def create_obstacle(self):
        """Rastgele iki farkli engel fotoğrafindan birini seçip engel oluşturur."""
        engel_secenekleri = [
            "assets/images/engel.png",
            "assets/images/engel_duba.png"
        ]
        secilen_engel = random.choice(engel_secenekleri)

        engel = arcade.Sprite(secilen_engel, scale=0.4)  # Gerekirse scale'ı ayarlayabilirsin
        engel.center_x = random.choice(ENGEL_KONUMLARI)
        engel.center_y = SCREEN_HEIGHT + 30
        engel.change_y = -self.hiz
        self.engeller.append(engel)

    def create_can(self):
        """Can paketi (horoz) oluşturur"""
        x = random.choice(ENGEL_KONUMLARI)
        y = SCREEN_HEIGHT + 30
        can_paketi = CanPaketi(x, y, self.hiz)
        self.canlar.append(can_paketi)
        
    def on_draw(self):
        self.clear()

        # Çizim işlemlerini draw.py'deki GameDrawer sınıfına devret
        if self.game_state == 0:  # Menü
            self.drawer.draw_menu()
        elif self.game_state == 2:  # Market
            self.drawer.draw_market()
        elif self.game_state == 1:  # Oyun
            self.drawer.draw_game()
        elif self.game_state == 3:  # Oyun Bitti
            self.drawer.draw_game_over()
        elif self.game_state == 4:  # Duraklatıldı
            self.drawer.draw_pause_menu()



    def on_update(self, delta_time):
        # Menü ve market durumlarında menü güncellemelerini çağır
        if self.game_state in [0, 2]:
            self.menu.update(delta_time)

        # Sadece oyun durumunda oyun güncellemelerini yap
        elif self.game_state == 1:
            self.araba.update()
            self.seritler.update()
            self.engeller.update()
            self.canlar.update()

            self.son_engel_zamani += delta_time
            if self.son_engel_zamani > 1.0:
                self.create_obstacle()
                self.son_engel_zamani = 0

            # Şeritleri tekrar konumlandır (sonsuz yol efekti)
            for serit in self.seritler:
                if serit.center_y < -SERIT_YUKSEKLIK / 2:
                    serit.center_y = SCREEN_HEIGHT + SERIT_YUKSEKLIK

            # Ekrandan çıkan engelleri sil, skor ve hızı güncelle
            for engel in list(self.engeller):
                if engel.top < 0:
                    puan_artisi = int((self.hiz / ENGEL_HIZI) * 10)
                    self.skor += max(1, puan_artisi)
                    self.hiz = min(self.hiz + HIZ_ARTIS, 12)  # Maksimum hız = 12

                    # Yeni hızları uygula
                    for serit in self.seritler:
                        serit.change_y = -self.hiz
                    for e in self.engeller:
                        e.change_y = -self.hiz
                    for c in self.canlar:
                        c.change_y = -self.hiz

                    engel.remove_from_sprite_lists()

            # Ekrandan çıkan horozları sil
            for can_paketi in list(self.canlar):
                if can_paketi.top < 0:
                    can_paketi.remove_from_sprite_lists()

            # Araba - engel çarpışması
            if self.can > 0:
                engel_carpismalari = arcade.check_for_collision_with_list(self.araba, self.engeller)
                for engel in engel_carpismalari:
                    engel.remove_from_sprite_lists()
                    self.can -= 1
                    if self.can <= 0:
                        if self.skor > self.high_score:
                            self.high_score = int(self.skor)
                            print("YENİ HIGH SCORE:", self.high_score)

                        if self.game_music_player:
                            try:
                                self.game_music_player.pause()
                            except AttributeError:
                                pass
                            self.game_music_player = None

                        self.game_state = 3
                        if hasattr(self, "game_music_player") and self.game_music_player:
                            self.game_music_player.delete()
                        break  # Oyun bitti, diğer kontrolleri yapma

            # Araba - horoz çarpışması (can toplama)
            if self.can > 0:
                can_toplamalar = arcade.check_for_collision_with_list(self.araba, self.canlar)
                for can_paketi in can_toplamalar:
                    can_paketi.remove_from_sprite_lists()
                    self.can += 1

            # Coin kazanma (100 skor = 1 coin)
            if self.can > 0:
                new_coin_threshold = int(self.skor) // 100
                if new_coin_threshold > self.son_coin_skoru:
                    self.coins += 1
                    self.son_coin_skoru = new_coin_threshold

            # Horoz oluşturma (200 skor = 1 horoz, max 3 tane ekranda)
            new_can_threshold = int(self.skor) // 200
            if self.can > 0 and new_can_threshold > self.son_can_skoru:
                if len(self.canlar) < 3:
                    self.create_can()
                self.son_can_skoru = new_can_threshold

            self.canlar.update()
            self.canlar.update_animation(delta_time)

    def on_key_press(self, key, modifiers):
        """Tuş basıldığında çağrılır"""
        if self.game_state == 1:  # Oyun durumunda
            if key == arcade.key.LEFT:
                self.araba.change_x = -self.hiz * 1.2
            elif key == arcade.key.RIGHT:
                self.araba.change_x = self.hiz * 1.2
            elif key == arcade.key.ESCAPE:
                self.game_state = 4  # Oyun -> duraklat
                if self.game_music_player:
                    try:
                        self.game_music_player.pause()
                    except Exception:
                        pass

        elif self.game_state == 4 and key == arcade.key.ESCAPE:
            self.game_state = 1  # Duraklatma -> devam
            if self.game_music_player:
                try:
                    self.game_music_player.play()
                except Exception:
                    pass

        elif self.game_state == 0 and key == arcade.key.ESCAPE:
            self.close()  # Menüdeyken çık

        elif self.game_state == 3 and key == arcade.key.R:
            if self.skor > self.high_score:
                self.high_score = int(self.skor)
            self.setup_menu()
            self.game_state = 0

    def on_key_release(self, key, modifiers):
        """Tuş bırakıldığında çağrılır"""
        if self.game_state == 1:  # Oyun durumunda
            if key in (arcade.key.LEFT, arcade.key.RIGHT):
                self.araba.change_x = 0
                
    def on_mouse_press(self, x, y, button, modifiers):
        # Menü ve market tıklamalarını menu.py'deki Menu sınıfına devret
        if self.game_state in [0, 2]:  # Menü veya Market durumunda
            if self.menu.handle_menu_click(x, y, button, modifiers):
                return  # Menü tıklaması işlendiyse fonksiyondan çık
                
        # Duraklatma menüsü için mevcut kodu koru
        elif self.game_state == 4:
            if self.check_button_click(self.pause_continue_rect, x, y):
                self.game_state = 1  # Devam et
                if self.game_music_player:
                    try:
                        self.game_music_player.play()
                    except Exception:
                        pass
            elif self.check_button_click(self.pause_mainmenu_rect, x, y):
                self.setup_menu()

    def check_button_click(self, rect, x, y):
        return rect[0] < x < rect[1] and rect[2] < y < rect[3]

    def on_close(self):
        if self.skor > self.high_score:
            self.high_score = int(self.skor)

        try:
            with open("save_data.txt", "w") as f:
                f.write(f"{self.coins}\n")
                f.write(f"{self.high_score}\n")
                f.write(','.join(['1' if x else '0' for x in self.purchased_cars]) + "\n")
                f.write(f"{self.selected_car_index}\n")  # Seçilen araba indexini kaydet
        except Exception as e:
            print(f"Kaydetme hatası: {e}")

        # Menü müziğini durdur
        if hasattr(self, "menu_music_player") and self.menu_music_player:
            self.menu_music_player.delete()

        # Oyun müziğini durdur
        if hasattr(self, "game_music_player") and self.game_music_player:
            self.game_music_player.delete()
        super().on_close()
        

