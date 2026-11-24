import sqlite3
from tkinter import Tk, messagebox

from view.view import AplicatieAnimale


class Application:
    @classmethod
    def run(cls):
        try:
            aplicatie = AplicatieAnimale()
        except sqlite3.Error as error:
            root = Tk()
            root.withdraw()
            messagebox.showerror("Baza de date", f"Baza de date nu poate fi deschisă: {error}", parent=root)
            root.destroy()
            return
        aplicatie.mainloop()
