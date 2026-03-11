import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Кольори цифр
NUMBER_COLORS = {
    1: "blue",
    2: "green",
    3: "red",
    4: "purple",
    5: "orange",
    6: "cyan",
    7: "black",
    8: "gray"
}


class Minesweeper(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Сапер")
        self.geometry("420x520")

        self.size = 8
        self.mines_count = 10

        self.create_menu()
        self.start_game()

    # --- Меню складності ---
    def create_menu(self):

        top = ctk.CTkFrame(self)
        top.pack(pady=5)

        self.diff_menu = ctk.CTkOptionMenu(
            top,
            values=["Легка", "Середня", "Складна"],
            command=self.change_difficulty
        )
        self.diff_menu.set("Легка")
        self.diff_menu.pack(side="left", padx=5)

        restart = ctk.CTkButton(top, text="Рестарт", command=self.start_game)
        restart.pack(side="left", padx=5)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack()

    # --- Вибір складності ---
    def change_difficulty(self, choice):

        if choice == "Легка":
            self.size = 8
            self.mines_count = 10
        elif choice == "Середня":
            self.size = 10
            self.mines_count = 20
        else:
            self.size = 12
            self.mines_count = 35

        self.start_game()

    # --- Початок гри ---
    def start_game(self):

        if hasattr(self, "field_frame"):
            self.field_frame.destroy()

        self.buttons = []
        self.mines = set()
        self.opened = set()
        self.flags = set()

        self.field_frame = ctk.CTkFrame(self)
        self.field_frame.pack(pady=10)

        self.create_field()
        self.place_mines()
        self.status.configure(text="")

    # --- Поле ---
    def create_field(self):

        for r in range(self.size):
            row_buttons = []
            for c in range(self.size):

                btn = ctk.CTkButton(
                    self.field_frame,
                    width=35,
                    height=35,
                    text=""
                )
                btn.grid(row=r, column=c, padx=1, pady=1)

                btn.bind("<Button-1>", lambda e, row=r, col=c: self.left_click(row, col))
                btn.bind("<Button-3>", lambda e, row=r, col=c: self.right_click(row, col))

                row_buttons.append(btn)

            self.buttons.append(row_buttons)

    # --- Розставлення мін ---
    def place_mines(self):
        while len(self.mines) < self.mines_count:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            self.mines.add((r, c))

    # --- Підрахунок мін ---
    def count_mines(self, row, col):

        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r, c) in self.mines:
                    count += 1
        return count

    # --- ЛКМ ---
    def left_click(self, row, col):

        if (row, col) in self.flags or (row, col) in self.opened:
            return

        btn = self.buttons[row][col]

        if (row, col) in self.mines:
            btn.configure(text="💣")
            self.game_over(False)
            return

        self.open_cell(row, col)

        if len(self.opened) == self.size * self.size - self.mines_count:
            self.game_over(True)

    # --- ПКМ (прапорець) ---
    def right_click(self, row, col):

        if (row, col) in self.opened:
            return

        btn = self.buttons[row][col]

        if (row, col) in self.flags:
            self.flags.remove((row, col))
            btn.configure(text="")
        else:
            self.flags.add((row, col))
            btn.configure(text="🚩")

    # --- Відкриття клітин ---
    def open_cell(self, row, col):

        if (row, col) in self.opened:
            return

        btn = self.buttons[row][col]
        count = self.count_mines(row, col)

        # Відкрита клітинка стає білою
        btn.configure(
            text=str(count) if count > 0 else "",

            fg_color="#d9d9d9",  # фон клітинки білий
            text_color=("black") # колір цифри
        )

        self.opened.add((row, col))

        # Якщо поруч немає мін, відкриваємо сусідні клітинки
        if count == 0:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.size and 0 <= c < self.size:
                        self.open_cell(r, c)

    # --- Кінець гри ---
    def game_over(self, win):

        for r, c in self.mines:
            self.buttons[r][c].configure(text="💣")

        text = "🎉 Ти виграв!" if win else "💀 Ти програв!"

        # Розміщення по конкретних координатах
        self.status.place(
            x=950,  # відстань від лівого краю
            y=700,  # відстань від верхнього краю
            anchor="center"
        )

        self.status.configure(
            text=text,
            font=("Arial", 30, "bold"),
            text_color="white"
        )

        for row in self.buttons:
            for btn in row:
                btn.configure(state="disabled")


if __name__ == "__main__":
    game = Minesweeper()
    game.mainloop()