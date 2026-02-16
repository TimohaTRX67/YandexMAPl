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
    def setup(self):
        self.ll = (37.530887, 55.703118)
        self.spn = [0.002, 0.002]
        self.get_image()

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

    def get_image(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f"ll={self.ll[0]},{self.ll[1]}&spn={self.spn[0]},{self.spn[1]}"

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
        clamped_x = max(MIN, min(MAX, new_spn_x))
        clamped_y = max(MIN, min(MAX, new_spn_y))

        if clamped_x == self.spn[0] and clamped_y == self.spn[1]:
            return

        self.spn[0] = clamped_x
        self.spn[1] = clamped_y
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
