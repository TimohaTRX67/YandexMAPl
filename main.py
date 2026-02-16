import os
import sys
import requests
import arcade
import arcade.gui as gui

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"
MIN = 0.0005
MAX = 1
ZOOMIN = 0.5
ZOOMOUT = 2.0


class GameView(arcade.Window):
    def __init__(self, width = 1280, height = 720, title = "Arcade Window"):
        super().__init__(width, height, title, center_window=True)
        self.current_position = [37.530887, 55.703118]
        self.speed = 0.0005  # Скорость передвижения карты
        self.spn = [0.002, 0.002]  # Маштаб
        
        self.timer = 0
        self.theme = "light"
        self.ui_manager = gui.UIManager()
        self.search_input = None
        self.search_button = None
        
    def setup(self):
        self.setup_ui()
        self.get_image()

    def setup_ui(self):
        self.ui_manager.enable()
        self.ui_manager.clear()

        input_height = 32
        input_width = 360
        padding = 10

        self.search_input = gui.UIInputText(
            x=padding,
            y=self.height - input_height - padding,
            width=input_width,
            height=input_height,
            text=""
        )
        self.search_button = gui.UIFlatButton(
            text="Искать",
            x=padding + input_width + 10,
            y=self.height - input_height - padding,
            width=100,
            height=input_height
        )
        self.search_button.on_click = self.find_coords

        self.ui_manager.add(self.search_input)
        self.ui_manager.add(self.search_button)

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
        self.ui_manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.T:
            if self.theme == "light":
                self.theme = "dark"
            else:
                self.theme = "light"

            print(f"Текущая тема: {self.theme}")
            self.get_image()
        if key == arcade.key.A:
            self.move_map('left')
        if key == arcade.key.D:
            self.move_map('right')
        if key == arcade.key.W:
            self.move_map('up')
        if key == arcade.key.S:
            self.move_map('down')
        if key == arcade.key.P:
            self.zoom(ZOOMIN)
        if key == arcade.key.O:
            self.zoom(ZOOMOUT)
        
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
        ll_spn = f"ll={self.current_position[0]},{self.current_position[1]}&spn={self.spn[0]},{self.spn[1]}"

        theme_param = f"&theme={self.theme}"

        map_request = f"{server_address}{ll_spn}&apikey={api_key}{theme_param}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
            
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)

    def zoom(self, k):
        new_spn_x = self.spn[0] * k
        new_spn_y = self.spn[1] * k
        xx = max(MIN, min(MAX, new_spn_x))
        yy = max(MIN, min(MAX, new_spn_y))

        self.spn[0] = xx
        self.spn[1] = yy
        self.get_image()

    def find_coords(self, event) -> None:
        """ Ищем координаты запроса """
        geocode = self.search_input.text
        server_address = 'http://geocode-maps.yandex.ru/1.x/?'
        api_key = '8013b162-6b42-4997-9691-77b7074026e0'
        geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'
        response = requests.get(geocoder_request)
        json_response = response.json()
        
        data = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        # data = list(map(lambda x: float(str(x)), data.split(data)))
        if response:
            # Запрос успешно выполнен, печатаем полученные данные.
            print(data)
        else:
            # Произошла ошибка выполнения запроса. Обрабатываем http-статус.
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()
