import RPi.GPIO as GPIO
import time
import colorsys

# ==========================================
# CONFIGURACAO DOS PINOS (BCM)
# ==========================================
PIN_R = 4
PIN_G = 17
PIN_B = 27
PIN_BOTAO = 5

FREQUENCIA_PWM = 1000

DURACAO_CIRCULO = 60.0
INTERVALO = 0.01
TEMPO_COR_INICIAL = 1.0
TEMPO_BRANCO_INICIAL = 3.0
DEBOUNCE = 0.25

# Fracoes dedicadas aos tons especiais
FRACAO_BRANCO = 0.05
FRACAO_PASTEL = 0.10

# ==========================================
# CONFIGURACAO GPIO
# LED ativo em nivel baixo
# ==========================================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN_R, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PIN_G, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PIN_B, GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(
    PIN_BOTAO,
    GPIO.IN,
    pull_up_down=GPIO.PUD_UP
)

pwm_r = GPIO.PWM(PIN_R, FREQUENCIA_PWM)
pwm_g = GPIO.PWM(PIN_G, FREQUENCIA_PWM)
pwm_b = GPIO.PWM(PIN_B, FREQUENCIA_PWM)

pwms = [pwm_r, pwm_g, pwm_b]
pinos = [PIN_R, PIN_G, PIN_B]
nomes = ["VERMELHO", "VERDE", "AZUL"]

for pwm in pwms:
    pwm.start(0)

# Brilho atual de cada canal, de 0 a 100%
cor_atual = (100.0, 0.0, 0.0)


# ==========================================
# APLICAR COR
# ==========================================
def aplicar_cor(r, g, b):
    global cor_atual

    cor_atual = tuple(
        max(0.0, min(100.0, float(v)))
        for v in (r, g, b)
    )

    # LED ativo em LOW: duty eletrico invertido
    for pwm, brilho in zip(pwms, cor_atual):
        duty_eletrico = 100.0 - brilho
        pwm.ChangeDutyCycle(duty_eletrico)


# ==========================================
# MOSTRAR CONFIGURACAO AO PAUSAR
# ==========================================
def mostrar_configuracao():
    print("\n========== LED RGB PAUSADO ==========")

    for nome, pino, brilho in zip(
        nomes, pinos, cor_atual
    ):
        duty_eletrico = 100.0 - brilho

        print(
            f"{nome:10s} | GPIO {pino:2d} | "
            f"Duty cycle: {duty_eletrico:6.2f}% | "
            f"Brilho: {brilho:6.2f}%"
        )

    print("-------------------------------------")
    print(
        f"RGB atual: ({cor_atual[0]:.1f}%, "
        f"{cor_atual[1]:.1f}%, "
        f"{cor_atual[2]:.1f}%)"
    )
    print("Clique novamente para continuar.")
    print("=====================================\n")


# ==========================================
# HSV PARA RGB
# ==========================================
def hsv_para_rgb(hue, saturacao=1.0, valor=1.0):
    r, g, b = colorsys.hsv_to_rgb(
        hue % 1.0,
        max(0.0, min(1.0, saturacao)),
        max(0.0, min(1.0, valor))
    )

    return r * 100.0, g * 100.0, b * 100.0


# ==========================================
# SEQUENCIA INICIAL
# VERMELHO, VERDE, AZUL E BRANCO
# ==========================================
def mostrar_cores_iniciais():
    cores = [
        ((100, 0, 0), "Vermelho"),
        ((0, 100, 0), "Verde"),
        ((0, 0, 100), "Azul"),
        ((80, 100, 100), "BRANCO")
    ]

    for cor, nome in cores:
        aplicar_cor(*cor)
        print(f"Cor inicial: {nome}")

        inicio_cor = time.monotonic()
        duracao = (
            TEMPO_BRANCO_INICIAL
            if nome == "BRANCO"
            else TEMPO_COR_INICIAL
        )

        while time.monotonic() - inicio_cor < duracao:
            time.sleep(0.005)


# ==========================================
# COR DA ANIMACAO
# ==========================================
def cor_da_animacao(tempo):
    fase = (tempo % DURACAO_CIRCULO) / DURACAO_CIRCULO
    hue = fase

    # Branco no inicio de cada volta
    if fase < FRACAO_BRANCO:
        return (100.0, 100.0, 100.0)

    # Tons pasteis
    if fase < FRACAO_BRANCO + FRACAO_PASTEL:
        return hsv_para_rgb(
            hue,
            saturacao=0.25,
            valor=1.0
        )

    # Circulo cromatico completo
    return hsv_para_rgb(
        hue,
        saturacao=1.0,
        valor=1.0
    )


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================
try:
    print("=====================================")
    print(" LED RGB - CIRCULO CROMATICO")
    print("=====================================")
    print("GPIO 4  = Vermelho")
    print("GPIO 17 = Verde")
    print("GPIO 27 = Azul")
    print("GPIO 5  = Botao ativo em LOW")
    print()
    print("Sequencia: vermelho, verde, azul e branco.")
    print("Branco inicial: 3 segundos.")
    print("Depois: tons pasteis e circulo cromatico.")
    print("Clique: pausar e mostrar duty cycles.")
    print("Clique novamente: continuar.")
    print("CTRL+C: encerrar.")
    print()

    mostrar_cores_iniciais()

    inicio_animacao = time.monotonic()
    tempo_pausado_acumulado = 0.0
    inicio_pausa = None

    pausado = False
    botao_anterior = GPIO.HIGH
    ultimo_clique = 0.0

    while True:
        agora = time.monotonic()
        estado_botao = GPIO.input(PIN_BOTAO)

        # Detecta o pressionamento do botao
        if (
            botao_anterior == GPIO.HIGH
            and estado_botao == GPIO.LOW
            and agora - ultimo_clique >= DEBOUNCE
        ):
            ultimo_clique = agora
            pausado = not pausado

            if pausado:
                inicio_pausa = agora
                mostrar_configuracao()
            else:
                tempo_pausado_acumulado += (
                    agora - inicio_pausa
                )
                inicio_pausa = None
                print("Animacao retomada.\n")

        botao_anterior = estado_botao

        # Atualiza a cor apenas quando nao estiver pausado
        if not pausado:
            tempo_ativo = (
                agora
                - inicio_animacao
                - tempo_pausado_acumulado
            )

            cor = cor_da_animacao(tempo_ativo)
            aplicar_cor(*cor)

        time.sleep(INTERVALO)

except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuario.")

finally:
    # Apaga o LED e libera os GPIOs
    for pwm in pwms:
        pwm.ChangeDutyCycle(0)
        pwm.stop()

    GPIO.cleanup()
    print("GPIO liberados.")

