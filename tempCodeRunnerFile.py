f key == arcade.key.T:
            if self.theme == "light":
                self.theme = "dark"
            else:
                self.theme = "light"

            print(f"Текущая тема: {self.theme}")
            self.get_image()