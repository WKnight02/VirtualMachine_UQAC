from project.modules.interfaces import *
from multiprocessing import Process

root = Interface()
root2 = ControlerInterface()
root2.title("Controler")
root.title("Editor")
root2.mainloop()
