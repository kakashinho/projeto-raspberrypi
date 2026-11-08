from gpiozero import Button
from signal import pause

botao = Button(5)          # pull-up interno: solto = 1, apertado = 0

botao.when_pressed = lambda: print("apertou")
botao.when_released = lambda: print("soltou")

pause()
