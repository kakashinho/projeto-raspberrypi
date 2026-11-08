from gpiozero import DistanceSensor, RGBLED

from time import sleep
 
# Sensor ultrassônico

sensor = DistanceSensor(

    echo=23,

    trigger=24,

    max_distance=2

)
 
# LED RGB: pinos vermelho, verde e azul

rgb = RGBLED(

    red=2,

    green=3,

    blue=4,

    active_high=True

)
 
while True:

    distancia = sensor.distance  # Distância em metros
 
    print(f"Distância: {distancia:.2f} m")
 
    if distancia < 0.20:

        # Menos de 20 cm: vermelho

        rgb.color = (1, 0, 0)

        print("PERIGO: VERMELHO")
 
    elif distancia < 0.50:

        # De 20 cm até menos de 50 cm: amarelo

        rgb.color = (1, 1, 0)

        print("ATENÇÃO: AMARELO")
 
    elif distancia < 1.00:

        # De 50 cm até menos de 1 m: verde

        rgb.color = (0, 1, 0)

        print("SEGURO: VERDE")
 
    else:

        # A partir de 1 m: azul

        rgb.color = (0, 0, 1)

        print("LONGE: AZUL")
 
    sleep(0.5)

 
