from tkinter import Tk
from app import AppGUI
from database import Database
from typing import Final

USER: Final = 'user-name'
PASSWORD: Final = 'password'
DSN: Final = '155.158.112.45:1521/oltpstud'

if __name__ == '__main__':
    db = Database(USER, PASSWORD, DSN)
    # Create window object
    root = Tk()
    my_gui = AppGUI(root, db)
    root.mainloop()
