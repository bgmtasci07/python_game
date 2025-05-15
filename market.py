import arcade
from const import *

class Market:
    def __init__(self, game_instance):
        self.game = game_instance  
        
        # Market değişkenleri
        self.market_title = None
        self.market_coin_text = None
        self.market_cars = arcade.SpriteList()
        self.market_car_rects = []
        self.market_back_button = None
        self.market_back_rect = None
        self.market_car_price_texts = []
        self.insufficient_coins_text = None
        self.show_insufficient_coins_message = False
        self.insufficient_coins_timer = 0
    
    def setup_market(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.game.game_state = 2

        self.market_title = arcade.Text("Araba Seç", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85,
                                        arcade.color.WHITE, 30, anchor_x="center")

        self.market_coin_text = arcade.Text(f"Coin: {self.game.coins}", SCREEN_WIDTH - 10, SCREEN_HEIGHT - 30,
                                            arcade.color.YELLOW, 18, anchor_x="right")

        self.insufficient_coins_text = arcade.Text("Yetersiz Coin!", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.25,
                                                arcade.color.RED, 20, anchor_x="center")
        self.show_insufficient_coins_message = False

        self.market_cars.clear()
        self.market_car_rects.clear()
        self.market_car_price_texts.clear()

        car_y = SCREEN_HEIGHT / 2
        spacing_x = 160  # veya 180
        start_x = SCREEN_WIDTH / 6

        for i in range(4):
            x = start_x + i * spacing_x

            if i == 0:
                car = arcade.Sprite("assets/images/beyaz_araba.png", scale=0.9)
            elif i == 1:
                car = arcade.Sprite("assets/images/kirmizi_araba.png", scale=0.4)
            elif i == 2:
                car = arcade.Sprite("assets/images/mor_araba.png", scale=0.9)
            elif i == 3:
                car = arcade.Sprite("assets/images/klasik_araba.png", scale=0.7)  

            car.center_x = x
            car.center_y = car_y
            self.market_cars.append(car)

            rect = (x - car.width / 2 - 10, x + car.width / 2 + 10,
                    car_y - car.height / 2 - 10, car_y + car.height / 2 + 10)
            self.market_car_rects.append(rect)

            fiyat_y = SCREEN_HEIGHT * 0.25  

            # Çerçeve boyutu
            kutu_genislik = 80
            kutu_yukseklik = 30
            # Yazıyı oluştur
            price_text = arcade.Text(
                "Ücretsiz" if self.game.car_prices[i] == 0 else f"{self.game.car_prices[i]} Coin",
                x, fiyat_y,
                arcade.color.WHITE, 14, anchor_x="center", anchor_y="center"
            )
            self.market_car_price_texts.append(price_text)

        self.market_back_button = arcade.Text("Geri", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.15,
                                            arcade.color.ORANGE, 24, anchor_x="center")
        self.market_back_rect = (self.market_back_button.x - 60, self.market_back_button.x + 60,
                                self.market_back_button.y - 30, self.market_back_button.y + 30)
    
    def draw_market(self):
        self.market_title.draw()
        self.market_cars.draw()
        self.market_back_button.draw()
        self.market_coin_text.draw()

        fiyat_y = SCREEN_HEIGHT * 0.25
        kutu_genislik = 90
        kutu_yukseklik = 30

        for i, car in enumerate(self.market_cars):
            left = car.center_x - kutu_genislik / 2
            right = car.center_x + kutu_genislik / 2
            bottom = fiyat_y - kutu_yukseklik / 2
            top = fiyat_y + kutu_yukseklik / 2

            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_BLUE_GRAY)
            fiyat_yazi = "Ücretsiz" if self.game.car_prices[i] == 0 else f"{self.game.car_prices[i]} Coin"
            arcade.draw_text(
                fiyat_yazi, car.center_x, fiyat_y,
                arcade.color.WHITE, 14,
                anchor_x="center", anchor_y="center"
            )

        if self.show_insufficient_coins_message:
            self.insufficient_coins_text.draw()

    def handle_market_click(self, x, y, button, modifiers):
        if self.check_button_click(self.market_back_rect, x, y):
            # Ana menüye dön
            self.game.menu.setup_menu()
            return True
            
        for i, rect in enumerate(self.market_car_rects):
            if self.check_button_click(rect, x, y):
                if not self.game.purchased_cars[i]:  
                    if self.game.coins >= self.game.car_prices[i]:
                        self.game.coins -= self.game.car_prices[i]
                        self.game.purchased_cars[i] = True
                        self.game.selected_car_index = i
                        self.market_coin_text.text = f"Coin: {self.game.coins}"
                    else:
                        self.show_insufficient_coins_message = True
                        self.insufficient_coins_timer = 2.0
                else:
                    self.game.selected_car_index = i 
                return True
                
        return False  
    
    def update(self, delta_time):
        if self.show_insufficient_coins_message:
            self.insufficient_coins_timer -= delta_time
            if self.insufficient_coins_timer <= 0:
                self.show_insufficient_coins_message = False
    
    def check_button_click(self, rect, x, y):
        return rect[0] < x < rect[1] and rect[2] < y < rect[3]        
    
    
