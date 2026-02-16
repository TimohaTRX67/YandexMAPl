import os
import sys
import requests
import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"


class GameView(arcade.Window):
    def __init__(self, width = 1280, height = 720, title = "Arcade Window"):
        super().__init__(width, height, title, center_window=True)
        self.current_position = [37.530887, 55.703118]
        self.speed = 0.0001  # Скорость передвижения карты
        
    def setup(self):
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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.move_map('left')
        if key == arcade.key.D:
            self.move_map('rigth')
        if key == arcade.key.W:
            self.move_map('up')
        if key == arcade.key.S:
            self.move_map('down')
        
    def move_map(self, direction: str) -> None:
        if direction == 'left':
            self.current_position[0] -= self.speed
        if direction == 'right':
            self.current_position[0] += self.speed
        if direction == 'up':
            self.current_position[1] += self.speed
        if direction == 'down':
            self.current_position[1] -= self.speed
        self.get_image()

    def get_image(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={self.current_position[0]},{self.current_position[1]}&spn=0.002,0.002'
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


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    # Удаляем за собой файл с изображением.
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()
