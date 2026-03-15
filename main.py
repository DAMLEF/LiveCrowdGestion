# Bibliothèques
import tkinter

from engine import *
# ----------- #

# Creation of the app motor
E = Engine()


# Creation of the Tkinter app for file gestion
root = tkinter.Tk()
root.withdraw()

# Launch of the app main loop
E.app_loop()

pygame.quit()

