
import RPi.GPIO as GPIO
import time
import statistics

# =====================================
# CONFIGURAÇÕES
# =====================================
pin_a = 12  # GPIO 12: carrega o capacitor
pin_b = 25  # GPIO 25: detecta a carga

TIMEOUT = 0.5
NUM_LEITURAS = 3
ALPHA = 0.35          # Menor = mais estável, porém mais lento
ZONA_MORTA = 1.0      # Ignora pequenas variações (%)
TEMPO_DESCARGA = 0.05 # 20 ms

# =====================================
# CONFIGURAÇÃO GPIO
# =====================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_a, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# =====================================
# DESCARGA DO CAPACITOR
# =====================================
def discharge():
    GPIO.output(pin_a, GPIO.LOW)
    time.sleep(TEMPO_DESCARGA)


# =====================================
# TEMPO DE CARGA
# =====================================
def charge_time():
    GPIO.output(pin_a, GPIO.HIGH)
    inicio = time.perf_counter()

    while not GPIO.input(pin_b):
        if time.perf_counter() - inicio > TIMEOUT:
            GPIO.output(pin_a, GPIO.LOW)
            return None

    duracao = time.perf_counter() - inicio
    GPIO.output(pin_a, GPIO.LOW)

    return duracao * 1000


# =====================================
# LEITURA DO POTENCIÔMETRO
# =====================================
def analog_read():
    discharge()
    return charge_time()


def medir():
    leituras = []

    for _ in range(NUM_LEITURAS):
        valor = analog_read()

        if valor is not None:
            leituras.append(valor)

        time.sleep(0.005)

    if leituras:
        return statistics.median(leituras)

    return None


# =====================================
# CALIBRAÇÃO E POSIÇÃO ESTIMADA
# =====================================
try:
    print("=" * 40)
    print(" CALIBRACAO DO POTENCIOMETRO")
    print("=" * 40)

    input(
        "\nGire para o MINIMO e pressione ENTER..."
    )

    minimo = medir()

    if minimo is None:
        raise RuntimeError("Falha ao medir o minimo.")

    input(
        "\nGire para o MAXIMO e pressione ENTER..."
    )

    maximo = medir()

    if maximo is None:
        raise RuntimeError("Falha ao medir o maximo.")

    limite_inferior = min(minimo, maximo)
    limite_superior = max(minimo, maximo)
    intervalo = limite_superior - limite_inferior

    if intervalo <= 0:
        raise RuntimeError(
            "Intervalo invalido. Calibre novamente."
        )

    print("\nCalibracao concluida.")
    print("Gire o potenciometro para testar.")
    print("Pressione CTRL+C para terminar.\n")

    valor_filtrado = None
    nivel_exibido = None

    while True:
        valor = medir()

        if valor is None:
            print("Sem leitura")
            time.sleep(0.05)
            continue

        # Converte a medição em posição percentual
        posicao = (
            (valor - limite_inferior) / intervalo
        ) * 100.0

        posicao = max(0.0, min(100.0, posicao))

        # Filtro exponencial
        if valor_filtrado is None:
            valor_filtrado = posicao
        else:
            valor_filtrado = (
                ALPHA * posicao
                + (1.0 - ALPHA) * valor_filtrado
            )

        # Limita a escala de 0 a 100
        valor_filtrado = max(
            0.0, min(100.0, valor_filtrado)
        )

        # Zona morta para reduzir oscilações na exibição
        if nivel_exibido is None:
            nivel_exibido = round(valor_filtrado)
        elif abs(valor_filtrado - nivel_exibido) >= ZONA_MORTA:
            nivel_exibido = round(valor_filtrado)

        print(f"Posicao estimada: {nivel_exibido:3d}/100")

        time.sleep(0.03)

except KeyboardInterrupt:
    print("\nTeste encerrado.")

except RuntimeError as erro:
    print(f"\nErro: {erro}")

finally:
    GPIO.cleanup()
    print("GPIO liberados.")
