import os
import sys
import requests
import arcade

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"
MIN = 0.0005
MAX = 0.05
ZOOMIN = 0.5
ZOOMOUT = 2.0


class GameView(arcade.Window):
    def __init__(self, width = 1280, height = 720, title = "Arcade Window"):
        super().__init__(width, height, title, center_window=True)
        self.current_position = [37.530887, 55.703118]
        self.speed = 0.0001  # Скорость передвижения карты
        self.spn = [0.002, 0.002]  # Маштаб
        
        self.timer = 0
        
    def setup(self):
        self.get_image()

    def on_update(self, delta_time):
        self.timer += delta_time
        if self.timer >= 1:
            self.get_image()
            self.timer = 0

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                (self.width - self.background.width) // 2,
                (self.height - self.background.height) // 2,
                self.background.width,
                self.background.height
            ),
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.move_map('left')
        if key == arcade.key.D:
            self.move_map('rigth')
        if key == arcade.key.W:
            self.move_map('up')
        if key == arcade.key.S:
            self.move_map('down')
        # self.get_image()
        
    def move_map(self, direction: str) -> None:
        if direction == 'left':
            self.current_position[0] -= self.speed
        if direction == 'right':
            self.current_position[0] += self.speed
        if direction == 'up':
            self.current_position[1] += self.speed
        if direction == 'down':
            self.current_position[1] -= self.speed

    def get_image(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f"ll={self.current_position[0]},{self.current_position[1]}&spn={self.spn[0]},{self.spn[1]}"
        # Готовим запрос.

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)

    def adjust_zoom(self, factor):
        new_spn_x = self.spn[0] * factor
        new_spn_y = self.spn[1] * factor
        xx = max(MIN, min(MAX, new_spn_x))
        yy = max(MIN, min(MAX, new_spn_y))

        self.spn[0] = xx
        self.spn[1] = yy
        self.get_image()

    def on_key_press(self, key, k):
        if key == arcade.key.P:
            self.adjust_zoom(ZOOMIN)
        elif key == arcade.key.O:
            self.adjust_zoom(ZOOMOUT)


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()
