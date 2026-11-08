# Pinos da placa (numeração BCM). É a única fonte de verdade dos pinos.
# Opcional: pigpio para todas as peças, se os servos tremerem. Não é usado no sistema final.
# from gpiozero import Device
# from gpiozero.pins.pigpio import PiGPIOFactory
# Device.pin_factory = PiGPIOFactory()

SERVO_ENTRADA = 13   # J2
SERVO_SAIDA = 26     # J3

US_TRIG = 23         # J4, TRIG
US_ECHO = 24         # J4, ECHO (passa pelo divisor R3/R4)

LED_R, LED_G, LED_B = 4, 17, 27   # D1, ânodo comum: nível baixo acende

BUZZER = 6           # J6, via R6 e transistor Q1
BOTAO = 5            # SW1 (e J8 em paralelo)

POT_CARGA = 12       # carrega o capacitor C1 (via R2)
POT_LE = 25          # lê o tempo de carga (via R1 + potenciômetro)

DHT11 = 22           # J5, DAT
