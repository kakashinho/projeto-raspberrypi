# -*- coding: utf-8 -*-
"""Maquete do estacionamento: fonte única de medidas (tudo em mm). Versão v5.

Referencial da maquete, visto de cima:
  X  da esquerda para a direita (0 a PISO_W), olhando de quem está na frente
  Y  da frente (0: lado de quem olha e de onde chegam os carros) para o fundo (PISO_D)
  Z  para cima, a partir da face de cima do papelão do piso (a mesa fica em -ELEV_TOTAL)

Referencial do conjunto Pi + placa (u, v), igual ao prompt_maquete.md, seção 4.1:
  u  ao longo do comprimento, 0 na borda da placa do lado da coluna 1 (balanço)
  v  na largura, 0 na borda da placa do lado da fileira A (GPIO); +v = lado do micro-USB
Na maquete: u cresce para +X e +v aponta para a FRENTE (-Y), para o painel ficar
virado para quem opera a maquete.

Respostas do usuário (2026-11-05): 7 vagas; papelão 1 m x 1 m; EVA 1 mm; impressão colorida em
papel comum + cola bastão; rede por CABO; tudo de papelão; piso de 311 x 200; cola branca;
etiquetas PIMACO 6282; papelão de ~2,5 mm (o rasgo de 2,8 do corpo de prova ficou folgado).

Revisão v5 (2026-11-06): o usuário corta com TESOURA. Regra: todo corte começa na borda da peça
e nenhum recorte tem menos de 8 mm de largura. Por isso:
  - nada de rasgos de encaixe: cantos com dobradiça de fita crepe (dobram planos);
  - onde uma peça precisa ficar presa, duas tiras coladas formam o "rasgo" (guias e travas);
  - piso sem rasgos: os 2 furos têm uma linha de acesso a partir da borda;
  - carros são caixinhas coladas (vão num saquinho).
"""

# ------------------------------------------------------------------ materiais
T = 2.5              # papelão
EVA = 1.0            # EVA
FAIXA = 4.0          # largura das faixas brancas (etiqueta)
CHAPA = (1000.0, 1000.0)   # papelão disponível
GUIA_W = 5.0         # largura das tiras coladas (guias no piso, travas no telhado e embaixo do piso)
RECORTE_MIN = 8.0    # recorte mais estreito que a tesoura faz bem

# ------------------------------------------------------------------ piso
PISO_W, PISO_D = 311.0, 200.0
FRENTE = 6.0         # calçada da frente: recebe a tira-guia do painel

# ------------------------------------------------------------------ carro e vagas
# Carro: caixinha colada de 5 retângulos (2 laterais, frente, traseira e teto).
CARRO_L = 50.0                   # comprimento (as laterais)
CARRO_W = 24.0                   # largura (face de fora das laterais)
CARRO_PAREDE_H = 15.0            # altura das laterais, da frente e da traseira
CARRO_H = CARRO_PAREDE_H + T     # altura total, com o teto
CARRO_W_TOTAL = CARRO_W
VAGA_PASSO = 36.0                # de faixa a faixa (centro a centro)
VAGA_FUNDO = CARRO_L + 10.0
N_VAGAS = 7
N_CARROS = 8                     # 7 para lotar + 1 barrado na entrada

# ------------------------------------------------------------------ Pi + placa (u, v)
# Copiado de kicad_hat/gerador/design.py (só leitura), conferido por script em 2026-11-05.
ENV_U, ENV_V = 122.3, 63.53          # envelope medido: 121 x 63
PLACA = (0.0, 0.0, 100.0, 50.0)      # u0, v0, u1, v1
PI = (35.28, 7.53, 120.28, 63.53)    # placa do Pi 3 (85 x 56)
PI_USB_ETH_U = 122.3                 # USB/Ethernet saem até aqui
PI_FUROS = [(38.8, 11.0), (96.8, 11.0), (38.8, 60.0), (96.8, 60.0)]
SD = (32.5, 30.0, 35.28, 41.0)       # cartão microSD, por baixo do Pi
MICRO_USB_U = 45.9                   # energia, na borda v = 63,5
PECAS = {                            # centro aproximado (u, v)
    "RV1": (15.71, 30.08),           # potenciômetro: eixo aponta para +v
    "D1": (55.08, 22.46),            # LED RGB
    "SW1": (72.86, 22.46),
    "J4": (33.49, 33.89),            # HC-SR04
    "J2": (84.29, 37.70),            # servo 1, entrada
    "J3": (89.37, 37.70),            # servo 2, saída
    "J7": (13.17, 9.76),             # não usado
    "C2": (43.65, 37.70),
}
# Pi 3: a tomada de rede fica centrada a 10,25 mm da borda do micro-USB, com 16 mm de largura
REDE_V = (ENV_V - 10.25 - 8.0, ENV_V - 10.25 + 8.0)
REDE_PLUGUE = 30.0                   # plugue + capa, rígidos, a partir da face da tomada

# Alturas medidas pelo usuário com a placa no Pi, tudo sobre a mesa (2026-11-05).
# Dentro da guarita o Pi apoia direto no papelão (sem EVA), então valem a partir de Z = 0.
PI_Z0 = 2.0                          # face de baixo do Pi (pinos soldados por baixo), estimada
PLACA_TOPO_Z = 15.0                  # medido
POT_EIXO_Z = 48.0                    # medido: centro do eixo
POT_PONTA_V = 52.0                   # medido: a ponta passa 2 mm da borda da placa (v = 50)
POT_CORPO_D = 16.0                   # estimado (pot comum de 16 mm)
POT_EIXO_D = 6.0
LED_TOPO_Z = PLACA_TOPO_Z + 32.0     # medido: 32 mm acima da placa
DUPONT_TOPO_Z = PLACA_TOPO_Z + 23.0  # conectores plugados em J2/J3/J4 (estimado)

# ------------------------------------------------------------------ servo SG90
SERVO_FURO = (11.5, 22.5)            # medido pelo usuário
SERVO_CORPO = (12.2, 22.5, 22.7)     # largura, comprimento, altura (típico, p/ folgas)
SERVO_ABA = 4.85                     # quanto cada aba passa do corpo
SERVO_EIXO_PONTA = 5.9               # distância do eixo até a ponta do corpo
SERVO_ABAIXO_ABA = 15.9              # corpo abaixo das abas (fica dentro da guarita)
SERVO_ACIMA_ABA = 6.8                # corpo + engrenagem acima das abas (fica fora)
SERVO_CABO = 250.0

# ------------------------------------------------------------------ HC-SR04
US_PLACA = (45.0, 20.0, 1.6)
US_TRANSDUTOR_D, US_TRANSDUTOR_SAI = 16.0, 12.0
US_TRANSDUTOR_PASSO = 27.0           # centro a centro
US_DIST_MIN = 21.0                   # carro ENCOSTADO no lado do sensor (o módulo lê de 20 mm)
US_CABO = 400.0                      # usuário: "tem mais de 40 cm"

# ------------------------------------------------------------------ layout em X
FAIXA_ENTRADA = 38.0
FAIXA_SAIDA = 38.0
GUARITA_FOLGA_SERVO = 1.5            # parede da ponta até o servo
GUARITA_FOLGA_PLACA = 2.8            # servo até a placa
GUARITA_FOLGA_REDE = 45.0            # face da tomada de rede até a parede da direita
GUARITA_FOLGA_FRENTE = 4.5           # Pi até o painel: cabe o batente (1 de folga + 3) + 0,5
GUARITA_FOLGA_FUNDO = 3.0            # placa até a parede do fundo (onde vão os servos)
GUARITA_H = 62.0                     # esconde o corpo do pot (topo em 56 mm)
PAINEL_H = GUARITA_H - 0.5           # o painel fica 0,5 abaixo do telhado: sai inclinando para a frente
SEM_EVA = GUIA_W + 0.5               # volta em torno da guarita sem EVA (onde ficam as guias)

US_X_COSTAS = 5.0                    # costas da placa do sensor (o conector fica atrás)
US_X_FACE = US_X_COSTAS + US_PLACA[2] + US_TRANSDUTOR_SAI   # frente dos transdutores
ENTRADA_X0 = US_X_FACE + US_DIST_MIN                        # borda esquerda da faixa de entrada
GUARITA_X0 = ENTRADA_X0 + FAIXA_ENTRADA                     # face de fora da parede esquerda

SERVO_E_X0 = GUARITA_X0 + T + GUARITA_FOLGA_SERVO           # servo da entrada
PLACA_X0 = SERVO_E_X0 + SERVO_CORPO[0] + GUARITA_FOLGA_PLACA  # u = 0


def X(u):
    return PLACA_X0 + u


GUARITA_X1 = X(PI_USB_ETH_U) + GUARITA_FOLGA_REDE + T       # face de fora da parede direita
SERVO_S_X0 = GUARITA_X1 - T - GUARITA_FOLGA_SERVO - SERVO_CORPO[0]   # servo da saída
SAIDA_X0, SAIDA_X1 = GUARITA_X1, GUARITA_X1 + FAIXA_SAIDA

# ------------------------------------------------------------------ layout em Y
GUARITA_Y0 = FRENTE                                          # face de fora do painel


def Y(v):
    return GUARITA_Y0 + T + GUARITA_FOLGA_FRENTE + (ENV_V - v)


GUARITA_Y1 = Y(-GUARITA_FOLGA_FUNDO) + T                     # face de fora da parede do fundo
VAGAS_Y0 = PISO_D - VAGA_FUNDO
CORREDOR = VAGAS_Y0 - GUARITA_Y1
VAGAS_W = N_VAGAS * VAGA_PASSO + FAIXA
VAGAS_X0 = (PISO_W - VAGAS_W) / 2

# ------------------------------------------------------------------ cancelas
# Servo deitado na parede do fundo: corpo dentro, eixo para fora (+Y), aba de baixo
# apoiada no piso. O braço é uma tira de papelão presa no braço plástico do servo.
CANCELA_Y = GUARITA_Y1 + SERVO_ACIMA_ABA + 1.5 + T / 2       # plano do meio do braço
CANCELA_Z = SERVO_ABA + SERVO_EIXO_PONTA                     # altura do eixo acima do papelão
CANCELA_E_X = SERVO_E_X0 + SERVO_CORPO[0] / 2
CANCELA_S_X = SERVO_S_X0 + SERVO_CORPO[0] / 2
BRACO_W = 8.0
BRACO_ATRAS = 6.0                                            # parte do braço atrás do eixo
BRACO_E = CANCELA_E_X - (ENTRADA_X0 - 1.0)                   # do eixo até a ponta
BRACO_S = (SAIDA_X1 + 1.0) - CANCELA_S_X
SERVO_RECORTE_Z = SERVO_ABA + SERVO_FURO[1]                  # recorte aberto embaixo na parede do fundo

# ------------------------------------------------------------------ sensor
CARRO_ESPERA_Y1 = CANCELA_Y - T / 2 - 3.0                    # carro parado na cancela
CARRO_ESPERA_Y0 = CARRO_ESPERA_Y1 - CARRO_L
US_Y = (CARRO_ESPERA_Y0 + CARRO_ESPERA_Y1) / 2
US_Z = US_PLACA[1] / 2                                       # centro dos transdutores
# totem: frente (S1) com 2 janelas abertas embaixo + 2 laterais (S2) presas com dobradiça de fita
TOTEM_H = 26.0
TOTEM_FOLGA_LADO = 3.0                                       # ponta do sensor até a lateral
TOTEM_L = US_PLACA[0] + 2 * (TOTEM_FOLGA_LADO + T)           # comprimento da frente
TOTEM_X0 = US_X_COSTAS + US_PLACA[2]                         # face de trás da frente do totem
TOTEM_FUNDO_X = 1.5                                          # laterais começam aqui
US_JANELA = 17.0
# recorte do sensor: aberto na borda esquerda do piso (os pinos e o conector descem por ele)
US_RASGO = (0.0, US_Y - 7.0, US_X_COSTAS + 1.0, US_Y + 7.0)
ILHA_Y1 = max(GUARITA_Y1, US_Y + TOTEM_L / 2 + 2.0)          # a ilha cobre o totem inteiro

# ------------------------------------------------------------------ furos no piso
# furo de cabos: sob o balanço da placa, ao lado do Pi (não bloqueia o cartão SD).
FURO_CABOS = (X(4.0), Y(54.0), X(30.0), Y(30.0))            # x0, y0, x1, y1
# furo da rede: canto da frente-direita da guarita; folgado para o plugue passar com a capa
FURO_REDE = (X(PI_USB_ETH_U) + 15.0, GUARITA_Y0 + T + 2.0, GUARITA_X1 - T - 2.0, GUARITA_Y0 + T + 30.0)


def fendas_acesso():
    """Linha reta da borda da frente até cada furo: a tesoura entra por ela (fica escondida)."""
    out = []
    for f in (FURO_CABOS, FURO_REDE):
        x = (f[0] + f[2]) / 2
        out.append((x, 0.0, x, f[1]))
    return out


# ------------------------------------------------------------------ painel (parede da frente)
POT_TUBO_D = 8.5                     # tubinho de papel enrolado no eixo (Ø externo)
POT_TUBO_Y = (0.6 + T, Y(POT_PONTA_V) + 8.0)   # colado atrás do botão até 8 mm por cima do eixo
POT_BOTAO = 16.0                     # botão de papelão (octógono)
# recortes abertos em cima (tesoura): o tubinho e o LED
POT_RECORTE = (X(PECAS["RV1"][0]) - 5.0, POT_EIXO_Z - POT_TUBO_D / 2 - 0.5, X(PECAS["RV1"][0]) + 5.0)
LED_RECORTE = (X(PECAS["D1"][0]) - 6.0, LED_TOPO_Z - 10.0, X(PECAS["D1"][0]) + 6.0)
LED_JANELA = (LED_RECORTE[0], LED_RECORTE[1], LED_RECORTE[2], LED_TOPO_Z)   # parte que aparece no adesivo
ENERGIA_RASGO = (X(MICRO_USB_U) - 6.0, 0.0, X(MICRO_USB_U) + 6.0, 12.0)    # aberto embaixo

# ------------------------------------------------------------------ elevação: moldura de 4 painéis
# Frente, direita, fundo e esquerda unidos por dobradiças de fita (3 cantos; o 4º fecha com um
# pedaço de fita na montagem). Um painel solto no meio segura o piso embaixo da guarita.
ELEV_H = 50.0 - T                    # + o piso = 5 cm (usuário, v2)
ELEV_TOTAL = ELEV_H + T
MOLD_X = (16.0, PISO_W - 16.0)       # faces de fora da moldura (o painel da frente cabe numa A4)
MOLD_Y = (10.0, PISO_D - 10.0)
MOLD_MEIO_X = 175.0                  # painel do meio (centro)
ELEV_ARCO = (40.0, 20.0)             # vão embaixo para os cabos (largura, altura)


def arcos():
    """Vãos embaixo dos painéis da moldura: {painel: [centro ao longo do painel, em X ou Y]}."""
    rede = (FURO_REDE[0] + FURO_REDE[2]) / 2 + 4
    # pares iguais (frente = fundo, esquerda = direita): o mesmo gabarito serve para os dois
    return {"frente": [rede], "fundo": [rede], "esquerda": [US_Y], "direita": [US_Y],
            "meio": [(MOLD_Y[0] + MOLD_Y[1]) / 2]}


# ------------------------------------------------------------------ tiras coladas
def guias_piso():
    """Tiras coladas EM CIMA do piso (x0, y0, x1, y1, nome). Prendem as paredes da guarita.

    Cole usando a própria parede como espaçador: assim a folga sai certa com qualquer papelão."""
    g = GUIA_W
    gx0, gx1, gy0, gy1 = GUARITA_X0, GUARITA_X1, GUARITA_Y0, GUARITA_Y1
    return [
        (gx0, 0.5, gx1, gy0 - 0.1, "calçada (guia do painel)"),
        (gx0 - 0.1 - g, gy0 + T + 8, gx0 - 0.1, gy1 - 8, "guia lateral esquerda"),
        (gx1 + 0.1, gy0 + T + 8, gx1 + 0.1 + g, gy1 - 8, "guia lateral direita"),
        (gx0 + 30, gy1 + 0.1, gx1 - 30, gy1 + 0.1 + g, "guia do fundo"),
    ]


def travas_piso():
    """Tiras coladas EMBAIXO do piso (x0, y0, x1, y1, nome): encostam por dentro da moldura e dos
    dois lados do painel do meio, para o piso não escorregar."""
    g = GUIA_W
    mx0, mx1 = MOLD_X
    my0, my1 = MOLD_Y
    m = MOLD_MEIO_X
    return [
        (125.0, my0 + T + 0.2, 160.0, my0 + T + 0.2 + g, "trava da frente"),
        (125.0, my1 - T - 0.2 - g, 160.0, my1 - T - 0.2, "trava do fundo"),
        (mx0 + T + 0.2, 120.0, mx0 + T + 0.2 + g, 160.0, "trava da esquerda"),
        (mx1 - T - 0.2 - g, 120.0, mx1 - T - 0.2, 160.0, "trava da direita"),
        (m - T / 2 - 0.1 - g, 70.0, m - T / 2 - 0.1, 130.0, "trava do meio (esq.)"),
        (m + T / 2 + 0.1, 70.0, m + T / 2 + 0.1 + g, 130.0, "trava do meio (dir.)"),
    ]


def travas_telhado():
    """Tiras coladas EMBAIXO do telhado, por dentro das paredes laterais e do fundo."""
    g = GUIA_W
    gx0, gx1, gy0, gy1 = GUARITA_X0, GUARITA_X1, GUARITA_Y0, GUARITA_Y1
    return [
        (gx0 + T + 0.1, gy0 + T + 10, gx0 + T + 0.1 + g, gy1 - T - 10, "trava esquerda"),
        (gx1 - T - 0.1 - g, gy0 + T + 10, gx1 - T - 0.1, gy1 - T - 10, "trava direita"),
        (gx0 + T + 20, gy1 - T - 0.1 - g, gx1 - T - 20, gy1 - T - 0.1, "trava do fundo"),
    ]


# ------------------------------------------------------------------ etiquetas PIMACO 6282
# Folha Carta 215,9 x 279,4; 2 colunas x 7 linhas; etiqueta 101,6 x 33,9; margem de cima 21,2,
# lateral 4,0 (igual a kicad_hat/gerador/exportar.py).
PIMACO = {"modelo": "6282", "folha": (215.9, 279.4), "etiqueta": (101.6, 33.9), "colunas": 2, "linhas": 7,
          "margem_sup": 21.2, "margem_lat": 4.0}
ETIQ_T = 0.15                        # espessura da etiqueta (para o 3D)


def seta_pts(x, y, ang, comp, larg):
    """Contorno de uma seta pintada no piso (ang em graus: 0 = +X, 90 = +Y)."""
    import math
    r = math.radians(ang)
    ux, uy = math.cos(r), math.sin(r)
    nx, ny = -uy, ux
    h, c = comp * 0.45, larg * 0.32
    pts = [(-comp / 2, -c), (comp / 2 - h, -c), (comp / 2 - h, -larg / 2), (comp / 2, 0),
           (comp / 2 - h, larg / 2), (comp / 2 - h, c), (-comp / 2, c)]
    return [(round(x + px * ux + py * nx, 2), round(y + px * uy + py * ny, 2)) for px, py in pts]


ESCRITA = (30.0, 6.0)                # ENTRADA / SAÍDA: etiqueta preta com letra branca
NUMERO = 8.0                         # número da vaga: quadrado preto com número branco


def marcas_piso():
    """Marcas do piso em etiqueta PIMACO: [(código, tipo, dados)].

    faixa: (x0, y0, x1, y1) branca | seta: [(x, y)...] branca | escrita: (texto, x0, y0, x1, y1)
    numero: (n, x0, y0, x1, y1). C1 e C2 vão em cima da tira da calçada.
    """
    F = FAIXA
    out = [("M1", "faixa", (ENTRADA_X0 - F, 0.0, ENTRADA_X0, ILHA_Y1)),
           ("M2", "faixa", (SAIDA_X1, 0.0, SAIDA_X1 + F, GUARITA_Y1))]
    x0, x1 = VAGAS_X0, VAGAS_X0 + VAGAS_W
    for i in range(3):                                   # linha do fundo em 3 pedaços
        out.append((f"F{i + 1}", "faixa", (x0 + i * (x1 - x0) / 3, PISO_D - 2 - F, x0 + (i + 1) * (x1 - x0) / 3, PISO_D - 2)))
    for k in range(N_VAGAS + 1):
        x = VAGAS_X0 + k * VAGA_PASSO
        out.append((f"V{k + 1}", "faixa", (x, VAGAS_Y0, x + F, PISO_D - 2 - F)))
    cal = guias_piso()[0]
    meio = (cal[0] + cal[2]) / 2                         # calçada em 2 pedaços, em cima da tira
    out.append(("C1", "faixa", (cal[0], cal[1], meio, cal[3])))
    out.append(("C2", "faixa", (meio, cal[1], cal[2], cal[3])))
    yc = (GUARITA_Y1 + SEM_EVA + VAGAS_Y0) / 2
    out.append(("A1", "seta", seta_pts(PISO_W * 0.42, yc, 0, 18, 8)))
    out.append(("A2", "seta", seta_pts(PISO_W * 0.62, yc, 0, 18, 8)))
    out.append(("A3", "seta", seta_pts(ENTRADA_X0 + (FAIXA_ENTRADA - SEM_EVA) / 2, 17, 90, 14, 7)))
    out.append(("A4", "seta", seta_pts(SAIDA_X0 + SEM_EVA + (FAIXA_SAIDA - SEM_EVA) / 2, 17, -90, 14, 7)))
    ew, eh = ESCRITA
    for cod, txt, cx in (("T1", "ENTRADA", ENTRADA_X0 + (FAIXA_ENTRADA - SEM_EVA) / 2),
                         ("T2", "SAÍDA", SAIDA_X0 + SEM_EVA + (FAIXA_SAIDA - SEM_EVA) / 2)):
        out.append((cod, "escrita", (txt, cx - ew / 2, 1.5, cx + ew / 2, 1.5 + eh)))
    for k in range(N_VAGAS):
        cx = VAGAS_X0 + F / 2 + (k + 0.5) * VAGA_PASSO
        out.append((f"N{k + 1}", "numero", (k + 1, cx - NUMERO / 2, VAGAS_Y0 - 2 - NUMERO, cx + NUMERO / 2, VAGAS_Y0 - 2)))
    return out


# ------------------------------------------------------------------ pasta
PASTA = (240.0, 330.0, 30.0)         # pasta com elástico (interno) e lombada
PILHA_BASE = 3 * T                   # piso + o que fica colado em cima (guias, batentes) + travas de baixo


def empilhar(itens, largura=PISO_W, fundo=PISO_D):
    """Empilha peças soltas em camadas do tamanho do piso (prateleiras simples).

    itens: [(chave, w, h)]. Devolve ([(chave, x, y, w, h, camada, girou)], número de camadas).
    """
    lista = []
    for chave, w, h in itens:
        girou = w < h
        lista.append((chave, max(w, h), min(w, h), girou))
    lista.sort(key=lambda it: (-it[2], -it[1]))
    folga = 2.0
    camadas = []          # cada camada: prateleiras [y, altura, x_livre]
    saida = []
    for chave, w, h, girou in lista:
        posto = False
        for ci, prats in enumerate(camadas):
            for p in prats:
                if p[2] + w <= largura and h <= p[1]:
                    saida.append((chave, p[2], p[0], w, h, ci, girou))
                    p[2] += w + folga
                    posto = True
                    break
            if posto:
                break
            y_livre = prats[-1][0] + prats[-1][1] + folga
            if y_livre + h <= fundo:
                prats.append([y_livre, h, w + folga])
                saida.append((chave, 0.0, y_livre, w, h, ci, girou))
                posto = True
                break
        if not posto:
            camadas.append([[0.0, h, w + folga]])
            saida.append((chave, 0.0, 0.0, w, h, len(camadas) - 1, girou))
    return saida, len(camadas)


def orcamento():
    """Tabela do orçamento de espaço (texto)."""
    linhas = [
        (f"Largura (X), {PISO_W:.0f} mm", None),
        ("  sensor + recuo até a faixa", ENTRADA_X0),
        ("  faixa de entrada", FAIXA_ENTRADA),
        ("  guarita (2 servos + espaço da rede)", GUARITA_X1 - GUARITA_X0),
        ("  faixa de saída", FAIXA_SAIDA),
        ("  sobra", PISO_W - SAIDA_X1),
        (f"Profundidade (Y), {PISO_D:.0f} mm", None),
        ("  calçada da frente", FRENTE),
        ("  guarita", GUARITA_Y1 - GUARITA_Y0),
        ("  corredor", CORREDOR),
        ("  vagas", VAGA_FUNDO),
        (f"Vagas: {N_VAGAS} x {VAGA_PASSO:.0f} mm + faixa", VAGAS_W),
        ("  sobra nas laterais (cada)", VAGAS_X0),
    ]
    out = []
    for nome, val in linhas:
        out.append(nome if val is None else f"{nome:<40s}{val:7.1f}")
    return "\n".join(out)


def sensor():
    """Distâncias do sensor (mm): carro centrado, carro encostado, sem carro."""
    folga = (FAIXA_ENTRADA - SEM_EVA - CARRO_W) / 2
    centro = ENTRADA_X0 + folga - US_X_FACE                 # até a lateral (o feixe pega o meio do carro)
    encostado = ENTRADA_X0 - US_X_FACE                      # carro encostado na faixa
    vazio = GUARITA_X0 - US_X_FACE
    return centro, encostado, vazio


def recortes():
    """Recortes que a tesoura precisa fazer: (nome, largura). Todos abertos numa borda."""
    return [("tubinho do pot (painel)", POT_RECORTE[2] - POT_RECORTE[0]),
            ("LED (painel)", LED_RECORTE[2] - LED_RECORTE[0]),
            ("energia (painel)", ENERGIA_RASGO[2] - ENERGIA_RASGO[0]),
            ("servo (fundo)", SERVO_FURO[0]),
            ("sensor (piso)", US_RASGO[3] - US_RASGO[1]),
            ("janelas do totem", US_JANELA),
            ("arcos da moldura", ELEV_ARCO[0])]


def checar():
    erros = []
    if SAIDA_X1 > PISO_W:
        erros.append(f"faixa de saída passa do piso ({SAIDA_X1:.1f} > {PISO_W})")
    if VAGAS_X0 < 0:
        erros.append("vagas não cabem na largura")
    if CORREDOR < 0.8 * CARRO_L:
        erros.append(f"corredor curto ({CORREDOR:.1f} < 80% do carro)")
    _, encostado, _ = sensor()
    if encostado < 20.5:
        erros.append(f"carro encostado no lado do sensor fica a {encostado:.1f} mm (< 20)")
    if FURO_REDE[2] > GUARITA_X1 - T:
        erros.append("furo da rede passa da parede da direita")
    if FURO_CABOS[2] > X(SD[0]):
        erros.append("furo de cabos bloqueia o cartão SD")
    if POT_EIXO_Z + POT_CORPO_D / 2 > GUARITA_H - 3:
        erros.append("corpo do pot passa da altura da guarita")
    for nome, w in recortes():
        if w < RECORTE_MIN:
            erros.append(f"recorte {nome} estreito demais para tesoura ({w:.1f} < {RECORTE_MIN})")
    for f, n in ((FURO_CABOS, "furo de cabos"), (FURO_REDE, "furo da rede")):
        if f[0] < 1.5 or f[2] > PISO_W - 1.5 or f[3] > PISO_D - 1.5:
            erros.append(f"{n} perto demais da borda do piso")
        for x0, y0, x1, y1, nome in travas_piso():
            if x0 < f[2] and f[0] < x1 and y0 < f[3] and f[1] < y1:
                erros.append(f"{nome} cobre o {n}")
        if f[0] < MOLD_MEIO_X + T < f[2] or f[0] < MOLD_MEIO_X - T < f[2]:
            erros.append(f"painel do meio passa embaixo do {n}")
    for x, _, _, _ in fendas_acesso():
        for x0, y0, x1, y1, nome in travas_piso():
            if x0 - 1 < x < x1 + 1 and y0 < 50:
                erros.append(f"{nome} cruza a linha de acesso de um furo")
    if MOLD_X[1] - MOLD_X[0] > 281.0:
        erros.append("painel da moldura não cabe numa A4")
    if BRACO_S + CANCELA_S_X > PISO_W:
        erros.append("braço da cancela de saída passa do piso")
    if LED_RECORTE[0] < POT_RECORTE[2] + 5:
        erros.append("recortes do pot e do LED muito perto")
    return erros


if __name__ == "__main__":
    print(f"Carro: {CARRO_L:.0f} x {CARRO_W:.0f} x {CARRO_H:.1f} mm (caixinha colada)")
    print(orcamento())
    c, e, v = sensor()
    print(f"Sensor: carro centrado a {c:.1f} mm, encostado a {e:.1f} mm, sem carro (parede da guarita) a {v:.1f} mm")
    print(f"Cancela: eixo a {CANCELA_Z:.2f} mm do papelão; braços {BRACO_E:.1f} (entrada) e {BRACO_S:.1f} (saída)")
    print(f"Furo de cabos: X {FURO_CABOS[0]:.1f}-{FURO_CABOS[2]:.1f}, Y {FURO_CABOS[1]:.1f}-{FURO_CABOS[3]:.1f}")
    print(f"Furo da rede:  X {FURO_REDE[0]:.1f}-{FURO_REDE[2]:.1f}, Y {FURO_REDE[1]:.1f}-{FURO_REDE[3]:.1f}")
    print(f"Pot: eixo a {POT_EIXO_Z} mm; tubinho de {POT_TUBO_Y[1] - POT_TUBO_Y[0]:.1f} mm")
    print("Recortes (largura): " + ", ".join(f"{n} {w:.1f}" for n, w in recortes()))
    print(f"Elevação: {ELEV_TOTAL:.0f} mm; moldura {MOLD_X[1] - MOLD_X[0]:.0f} x {MOLD_Y[1] - MOLD_Y[0]:.0f}")
    erros = checar()
    print("OK" if not erros else "PROBLEMAS: " + "; ".join(erros))
