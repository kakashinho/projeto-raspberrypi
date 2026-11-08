# manual.py (esqueleto: você completa os TODO)
# medir() é a função do calibracao_pot2.py: copie-a para cá.
import json
import os

# o arquivo fica ao lado deste módulo, de onde quer que o programa seja chamado
ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibracao_pot.json")   # {"min": ms, "max": ms}


def calibrar():
    # TODO 1: peça "gire para o MÍNIMO", meça com medir(); depois o mesmo para o MÁXIMO
    # TODO 2: grave os dois valores em ARQ com json.dump
    pass


def posicao_pot():
    """Devolve 0 a 100, ou None se a leitura falhou."""
    # TODO 3: leia a calibração de ARQ. Se o arquivo não existir, devolva None.
    #         (calibrar() usa input(), e o serviço do sistema não tem teclado: não a chame aqui)
    # TODO 4: meça o tempo atual com medir()
    # TODO 5: converta para 0..100 com (t - min) / (max - min) * 100
    #         e limite o resultado entre 0 e 100
    pass


if __name__ == "__main__":
    calibrar()          # calibre à mão: python3 manual.py
