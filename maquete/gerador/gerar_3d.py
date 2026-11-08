# -*- coding: utf-8 -*-
"""Gera a vista 3D interativa da maquete: um único HTML com three.js (vem da CDN).

Uso:  python -B gerar_3d.py ../maquete_3d.html
Todas as medidas vêm de design.py. Cada peça de papelão é um contorno 2D extrudado
com a espessura do papelão (design.T), o mesmo que vira gabarito; o "modo pasta" deita essas
mesmas peças numa pilha.
"""
import json
import math
import sys

import design as d

T = d.T
W, D = d.PISO_W, d.PISO_D
X, Y = d.X, d.Y

ITENS, CABOS, ROTULOS, PIVOS = [], [], [], {}

PAPELAO = "#b9b3a6"
FACHADA = "#efe5cb"
TELHADO = "#8d939c"
EVA_PRETO = "#232327"
EVA_BRANCO = "#f3f3f0"
GRAMA = "#5f9c4a"
TOTEM = "#e7c35a"
PI_VERDE = "#1f7a40"
HAT = "#f5f5f0"
PRATA = "#c4c9d0"
PRETO = "#202020"
SERVO_AZUL = "#2f5fd8"
SENSOR_AZUL = "#1d4fa8"
LARANJA = "#e8892b"


# ---------------------------------------------------------------- primitivas
def ret(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def tira(comp, alt, cima=(), baixo=()):
    """Contorno de uma tira 0..comp x 0..alt. cima/baixo: (a0, a1, prof); prof > 0 corta
    para dentro (rasgo ou vão), prof < 0 sai para fora (aba)."""
    pts = [[0, 0]]
    for a0, a1, p in sorted(baixo):
        pts += [[a0, 0], [a0, p], [a1, p], [a1, 0]]
    pts += [[comp, 0], [comp, alt]]
    for a0, a1, p in sorted(cima, reverse=True):
        pts += [[a1, alt], [a1, alt - p], [a0, alt - p], [a0, alt]]
    pts += [[0, alt]]
    return pts


def placa(cod, plano, origem, contorno, furos=(), cor=PAPELAO, grupo="piso", unid=None,
          explode=(0, 0, 0), t=T, nome="", tex=None):
    """plano 'xy': (a, b) = (X, Y), espessura para +Z; 'xz': (X, Z), espessura +Y;
    'yz': (Y, Z), espessura +X. origem = canto (a = 0, b = 0, espessura = 0).
    tex: nome de um adesivo (ver adesivos_3d) que vai na face de fora da peça."""
    ITENS.append({"k": "placa", "cod": cod, "pl": plano, "o": list(origem), "c": contorno,
                  "f": list(furos), "t": t, "cor": cor, "g": grupo, "u": unid,
                  "e": list(explode), "n": nome, "tex": tex})


def caixa(grupo, cor, a, b, unid=None, explode=(0, 0, 0), op=1.0, nome=""):
    ITENS.append({"k": "caixa", "g": grupo, "cor": cor, "a": list(a), "b": list(b), "u": unid,
                  "e": list(explode), "op": op, "n": nome})


def cil(grupo, cor, eixo, p0, comp, r, unid=None, explode=(0, 0, 0), op=1.0, nome=""):
    """Cilindro com eixo 'x', 'y' ou 'z' começando em p0 e crescendo +comp."""
    ITENS.append({"k": "cil", "g": grupo, "cor": cor, "ax": eixo, "p": list(p0), "h": comp, "r": r,
                  "u": unid, "e": list(explode), "op": op, "n": nome})


def cabo(cor, pts, r=1.0):
    CABOS.append({"cor": cor, "pts": pts, "r": r})


def rotulo(texto, p, tam=6.0, fundo=False):
    """fundo=True: o rótulo some atrás das peças (números das vagas)."""
    ROTULOS.append({"t": texto, "p": list(p), "s": tam, "fundo": fundo})


def furo_ret(f, dx=0.0, dy=0.0):
    x0, y0, x1, y1 = f
    return ret(x0 - dx, y0 - dy, x1 - dx, y1 - dy)


# ---------------------------------------------------------------- piso e EVA
def com_recorte_sensor(x1, y1):
    """Retângulo 0..x1 x 0..y1 com o recorte do sensor aberto na borda esquerda."""
    _, ry0, rx1, ry1 = d.US_RASGO
    return [[0, 0], [x1, 0], [x1, y1], [0, y1], [0, ry1], [rx1, ry1], [rx1, ry0], [0, ry0]]


def piso():
    c = com_recorte_sensor(W, D)
    placa("P1", "xy", (0, 0, -T), c, [furo_ret(d.FURO_CABOS), furo_ret(d.FURO_REDE)], nome="Piso")
    # EVA preto: tudo, menos a guarita e a volta dela (onde ficam as guias)
    s_ = d.SEM_EVA
    gx0, gx1, gy1 = d.GUARITA_X0 - s_, d.GUARITA_X1 + s_, d.GUARITA_Y1 + s_
    _, ry0, rx1, ry1 = d.US_RASGO
    placa("EVA", "xy", (0, 0, 0), [[0, 0], [gx0, 0], [gx0, gy1], [gx1, gy1], [gx1, 0], [W, 0], [W, D], [0, D],
                                   [0, ry1], [rx1, ry1], [rx1, ry0], [0, ry0]],
          cor=EVA_PRETO, t=d.EVA, nome="EVA preto")
    # ilha de grama (papel impresso colado no EVA)
    placa(None, "xy", (0, 0, d.EVA), com_recorte_sensor(d.ENTRADA_X0 - d.FAIXA, d.ILHA_Y1), cor=GRAMA, t=0.3,
          tex="grama")
    # tiras coladas: guias em cima do piso (prendem a guarita) e travas embaixo (prendem na moldura)
    for x0, y0, x1, y1, nome in d.guias_piso():
        placa("GP", "xy", (0, 0, 0), ret(x0, y0, x1, y1), cor="#9c8f78", nome="Guia: " + nome)
    for x0, y0, x1, y1, nome in d.travas_piso():
        placa("TP", "xy", (0, 0, -2 * T), ret(x0, y0, x1, y1), cor="#9c8f78", grupo="estrutura",
              nome="Trava do piso: " + nome)
    # marcas em etiqueta PIMACO (a calçada vai em cima da tira da calçada)
    et = d.ETIQ_T
    for cod, tipo, dado in d.marcas_piso():
        z = T if cod in ("C1", "C2") else d.EVA
        if tipo == "faixa":
            placa(None, "xy", (0, 0, z), ret(*dado), cor=EVA_BRANCO, t=et, tex=cod)
        elif tipo == "seta":
            placa(None, "xy", (0, 0, z), [list(p) for p in dado], cor=EVA_BRANCO, t=et, tex=cod)
        else:
            placa(None, "xy", (0, 0, z), ret(*dado[1:]), cor="#111111", t=et, tex=cod)
            texto = dado[0] if tipo == "escrita" else str(dado[0])
            cx, cy = (dado[1] + dado[3]) / 2, (dado[2] + dado[4]) / 2
            rotulo(texto, (cx, cy, z + 0.5), 4.0 if tipo == "escrita" else 6.0, fundo=True)
    # batentes do Pi: cantoneiras em L coladas no papelão, 1 mm fora do contorno do Pi
    px0, px1 = X(d.PI[0]), X(d.PI[2])
    py0, py1 = Y(d.PI[3]), Y(d.PI[1])
    for cx, cy, sx, sy in [(px0, py0, 1, 1), (px1, py0, -1, 1), (px0, py1, 1, -1), (px1, py1, -1, -1)]:
        g, L, w = 1.0, 6.0, 3.0
        bx, by = cx - sx * g, cy - sy * g
        loc = [(0, 0), (L, 0), (L, -w), (-w, -w), (-w, L), (0, L)]
        placa("B1", "xy", (0, 0, 0), [[bx + sx * a, by + sy * b] for a, b in loc], cor="#8a6a45",
              nome="Batente do Pi (colado)")


# ---------------------------------------------------------------- elevação
def painel_moldura(comp, centros, a0):
    """Contorno de um painel da moldura: retângulo com os vãos de cabo embaixo."""
    aw, ah = d.ELEV_ARCO
    return tira(comp, d.ELEV_H, (), [(c - a0 - aw / 2, c - a0 + aw / 2, ah) for c in centros])


def elevacao():
    z0 = -d.ELEV_TOTAL
    mx0, mx1 = d.MOLD_X
    my0, my1 = d.MOLD_Y
    arcos = d.arcos()
    ex = (0, 0, -40)
    # frente e fundo: o comprimento todo; laterais entre eles (dobradiças de fita nos cantos)
    placa("EF", "xz", (mx0, my0, z0), painel_moldura(mx1 - mx0, arcos["frente"], mx0), grupo="estrutura",
          explode=ex, nome="Moldura: frente / fundo")
    placa("EF", "xz", (mx0, my1 - T, z0), painel_moldura(mx1 - mx0, arcos["fundo"], mx0), grupo="estrutura",
          explode=ex, nome="Moldura: frente / fundo")
    for x, lado in ((mx0, "esquerda"), (mx1 - T, "direita")):
        placa("ES", "yz", (x, my0 + T, z0), painel_moldura(my1 - my0 - 2 * T, arcos[lado], my0 + T),
              grupo="estrutura", explode=ex, nome="Moldura: lateral")
    placa("EM", "yz", (d.MOLD_MEIO_X - T / 2, my0 + T + 0.5, z0),
          painel_moldura(my1 - my0 - 2 * T - 1.0, arcos["meio"], my0 + T + 0.5), grupo="estrutura", explode=ex,
          nome="Moldura: painel do meio")


# ---------------------------------------------------------------- guarita
def guarita():
    gx0, gx1, gy0, gy1, H = d.GUARITA_X0, d.GUARITA_X1, d.GUARITA_Y0, d.GUARITA_Y1, d.GUARITA_H
    gx, gy = gx1 - gx0, gy1 - gy0
    # painel (frente): recortes abertos em cima (tubinho e LED) e embaixo (energia)
    p0, pz, p1 = d.POT_RECORTE
    l0, lz, l1 = d.LED_RECORTE
    e0, _, e1, ez = d.ENERGIA_RASGO
    Hp = d.PAINEL_H
    cima = [(p0 - gx0, p1 - gx0, Hp - pz), (l0 - gx0, l1 - gx0, Hp - lz)]
    placa("G1", "xz", (gx0, gy0, 0), tira(gx, Hp, cima, [(e0 - gx0, e1 - gx0, ez)]), cor=FACHADA, grupo="painel",
          explode=(0, -40, 0), nome="Parede da frente (painel)", tex="painel")
    # fundo: recortes abertos embaixo para os servos
    baixo = []
    for sx0 in (d.SERVO_E_X0, d.SERVO_S_X0):
        cx = sx0 + d.SERVO_CORPO[0] / 2 - gx0
        baixo.append((cx - d.SERVO_FURO[0] / 2, cx + d.SERVO_FURO[0] / 2, d.SERVO_RECORTE_Z))
    placa("G2", "xz", (gx0, gy1 - T, 0), tira(gx, H, (), baixo), cor=FACHADA, grupo="paredes",
          explode=(0, 40, 0), nome="Parede do fundo", tex="fundo")
    gl = gy - 2 * T                                  # laterais: entre o painel e o fundo
    for x, ex, tex in ((gx0, -40, "lado_porta"), (gx1 - T, 40, "lado_janela")):
        placa("G3", "yz", (x, gy0 + T, 0), ret(0, 0, gl, H), cor=FACHADA, grupo="paredes",
              explode=(ex, 0, 0), nome="Parede lateral", tex=tex)
    # telhado: retângulo liso + travas coladas por baixo (por dentro das laterais e do fundo)
    o = 3.0
    placa("G4", "xy", (gx0 - o, gy0 - o, H), ret(0, 0, gx + 2 * o, gy + 2 * o), cor=TELHADO,
          grupo="telhado", explode=(0, 0, 70), nome="Telhado", tex="telhado")
    for x0, y0, x1, y1, nome in d.travas_telhado():
        placa("GT", "xy", (0, 0, H - T), ret(x0, y0, x1, y1), cor="#6d737b", grupo="telhado",
              explode=(0, 0, 70), nome="Trava do telhado: " + nome)
    rotulo("PAINEL: botão do pot + LED", ((gx0 + gx1) / 2 - 20, gy0 - 6, H + 14))
    rotulo("GUARITA", ((gx0 + gx1) / 2 + 40, gy0 + 30, H + 22), 7)


# ---------------------------------------------------------------- eletrônica
def eletronica():
    g = "eletronica"
    z_pi = d.PI_Z0
    z_hat0 = d.PLACA_TOPO_Z - 1.6
    # Pi 3
    caixa(g, PI_VERDE, (X(d.PI[0]), Y(d.PI[3]), z_pi), (X(d.PI[2]), Y(d.PI[1]), z_pi + 1.6))
    zt = z_pi + 1.6
    ue = d.PI_USB_ETH_U
    caixa(g, PRATA, (X(ue) - 21, Y(d.REDE_V[1]), zt), (X(ue), Y(d.REDE_V[0]), zt + 13.5))     # rede
    for vc in (63.53 - 29.0, 63.53 - 47.0):                                                    # USB
        caixa(g, PRATA, (X(ue) - 17.5, Y(vc + 6.6), zt), (X(ue), Y(vc - 6.6), zt + 15.6))
    caixa(g, PRATA, (X(d.MICRO_USB_U) - 4, Y(63.53) - 0.5, zt), (X(d.MICRO_USB_U) + 4, Y(63.53) + 5, zt + 3))
    caixa(g, PRATA, (X(67.3) - 7.5, Y(63.53), zt), (X(67.3) + 7.5, Y(63.53) + 11, zt + 6.5))   # HDMI
    # barra de pinos que levanta a placa
    caixa(g, PRETO, (X(42.4), Y(13.5), zt), (X(93.2), Y(8.5), z_hat0))
    # placa de interface
    caixa(g, HAT, (X(0), Y(50), z_hat0), (X(100), Y(0), d.PLACA_TOPO_Z))
    # adesivo da placa: o desenho da própria placa (render do KiCad), colado por cima da caixa
    ITENS.append({"k": "plano", "g": g, "tex": "interface", "p": [X(50), Y(25), d.PLACA_TOPO_Z + 0.1],
                  "w": 100.0, "h": 50.0, "u": None, "e": [0, 0, 0], "n": "Adesivo da placa"})
    # etiqueta A PIMACO por cima do desenho: a metade de cima da placa (y do KiCad de 100 a 133,9 mm)
    ITENS.append({"k": "plano", "g": g, "tex": "etiqueta_A", "p": [X(50), Y(16.95), d.PLACA_TOPO_Z + 0.2],
                  "w": 100.0, "h": 33.9, "u": None, "e": [0, 0, 0], "n": "Etiqueta A PIMACO"})
    zh = d.PLACA_TOPO_Z
    # potenciômetro (pernas compridas, eixo para a frente)
    pu, pv = d.PECAS["RV1"]
    for du in (-5.08, 0, 5.08):
        caixa(g, PRATA, (X(pu + du) - 0.4, Y(pv) - 0.4, zh), (X(pu + du) + 0.4, Y(pv) + 0.4, d.POT_EIXO_Z - 6))
    cil(g, "#c9a24a", "y", (X(pu), Y(pv + 7), d.POT_EIXO_Z), 9.0, d.POT_CORPO_D / 2)
    cil(g, "#d8b860", "y", (X(pu), Y(pv + 14), d.POT_EIXO_Z), 7.0, 3.5)
    cil(g, PRATA, "y", (X(pu), Y(d.POT_PONTA_V), d.POT_EIXO_Z), Y(pv + 14) - Y(d.POT_PONTA_V), d.POT_EIXO_D / 2)
    # extensor: tubinho de papel + botão de papelão (K1)
    ty0, ty1 = d.POT_TUBO_Y
    cil(g, "#fbf7ea", "y", (X(pu), ty0, d.POT_EIXO_Z), ty1 - ty0, d.POT_TUBO_D / 2)
    b = d.POT_BOTAO
    c = b * 0.29
    octo = [[c, 0], [b - c, 0], [b, c], [b, b - c], [b - c, b], [c, b], [0, b - c], [0, c]]
    placa("K1", "xz", (X(pu) - b / 2, ty0 - T, d.POT_EIXO_Z - b / 2), octo, cor="#d23c3c",
          grupo=g, nome="Botão do pot", tex="botao")
    # LED RGB (pernas compridas), botão, buzzer, capacitor, conectores dupont
    lu, lv = d.PECAS["D1"]
    for du in (-1.9, -0.6, 0.6, 1.9):
        caixa(g, PRATA, (X(lu + du) - 0.25, Y(lv) - 0.25, zh), (X(lu + du) + 0.25, Y(lv) + 0.25, d.LED_TOPO_Z - 8))
    cil(g, "#22dd44", "z", (X(lu), Y(lv), d.LED_TOPO_Z - 8.6), 8.6, 2.5, nome="LED")
    su, sv = d.PECAS["SW1"]
    caixa(g, PRETO, (X(su) - 3, Y(sv) - 3, zh), (X(su) + 3, Y(sv) + 3, zh + 5))
    cil(g, PRETO, "z", (X(64.0), Y(35.0), zh), 9.0, 6.0)
    cil(g, "#2b4fa0", "z", (X(d.PECAS["C2"][0]), Y(d.PECAS["C2"][1]), zh), 13.0, 5.0)
    caixa(g, "#3d7fd1", (X(66.5) - 6, Y(26), zh), (X(66.5) + 6, Y(19), zh + 20))            # DHT11
    for ref, n in (("J2", 3), ("J3", 3), ("J4", 4)):
        u, v = d.PECAS[ref]
        meia = n * 2.54 / 2
        caixa(g, PRETO, (X(u) - 1.3, Y(v + meia), zh), (X(u) + 1.3, Y(v - meia), d.DUPONT_TOPO_Z))
    # servos: corpo dentro, aba apoiada no piso, engrenagem e eixo do lado de fora
    gy1 = d.GUARITA_Y1
    for sx0, cor in ((d.SERVO_E_X0, SERVO_AZUL), (d.SERVO_S_X0, "#2a2a2a")):
        cx = sx0 + d.SERVO_CORPO[0] / 2
        x0, x1 = cx - d.SERVO_FURO[0] / 2, cx + d.SERVO_FURO[0] / 2
        z0, z1 = d.SERVO_ABA, d.SERVO_RECORTE_Z
        caixa(g, cor, (x0, gy1 - T - d.SERVO_ABAIXO_ABA, z0), (x1, gy1 + 2.0, z1))
        caixa(g, cor, (x0, gy1 - T - 2.5, 0.0), (x1, gy1 - T, z1 + d.SERVO_ABA))
        cil(g, cor, "y", (cx, gy1 + 2.0, d.CANCELA_Z), 2.0, 5.5)
        cil(g, "#f0f0f0", "y", (cx, gy1 + 4.0, d.CANCELA_Z), 2.8, 2.4)
    # sensor HC-SR04 em pé, pinos para baixo pelo rasgo
    z = d.EVA
    caixa(g, SENSOR_AZUL, (d.US_X_COSTAS, d.US_Y - 22.5, z), (d.US_X_COSTAS + 1.6, d.US_Y + 22.5, z + 20))
    for s in (-1, 1):
        cil(g, PRATA, "x", (d.US_X_COSTAS + 1.6, d.US_Y + s * d.US_TRANSDUTOR_PASSO / 2, z + d.US_Z),
            d.US_TRANSDUTOR_SAI, d.US_TRANSDUTOR_D / 2)
    caixa(g, PRETO, (d.US_X_COSTAS - 2.5, d.US_Y - 5.1, -14.0), (d.US_X_COSTAS, d.US_Y + 5.1, z + 2.5))


def totem():
    z = d.EVA
    L1, H = d.TOTEM_L, d.TOTEM_H
    y0 = d.US_Y - L1 / 2
    J = d.US_JANELA
    # frente: 2 janelas abertas embaixo para os transdutores
    baixo = [(L1 / 2 + s * d.US_TRANSDUTOR_PASSO / 2 - J / 2, L1 / 2 + s * d.US_TRANSDUTOR_PASSO / 2 + J / 2,
              d.US_Z + J / 2) for s in (-1, 1)]
    placa("S1", "yz", (d.TOTEM_X0, y0, z), tira(L1, H, (), baixo), cor=TOTEM, grupo="paredes",
          explode=(0, 0, 40), nome="Totem, frente", tex="totem")
    # laterais: atrás da frente, nas pontas (dobradiça de fita na quina)
    comp = d.TOTEM_X0 - d.TOTEM_FUNDO_X
    for yy in (y0, y0 + L1 - T):
        placa("S2", "xz", (d.TOTEM_FUNDO_X, yy, z), ret(0, 0, comp, H), cor=TOTEM, grupo="paredes",
              explode=(0, 0, 55), nome="Totem, lado")
    rotulo("SENSOR (totem)", (12, d.US_Y, 52))


# ---------------------------------------------------------------- cancelas
def cancelas():
    for unid, cx, comp, sinal in (("bracoE", d.CANCELA_E_X, d.BRACO_E, -1), ("bracoS", d.CANCELA_S_X, d.BRACO_S, 1)):
        PIVOS[unid] = [cx, d.CANCELA_Y, d.CANCELA_Z, sinal]
        total = comp + d.BRACO_ATRAS
        x0 = cx - comp if sinal < 0 else cx - d.BRACO_ATRAS
        y0 = d.CANCELA_Y - T / 2
        z0 = d.CANCELA_Z - d.BRACO_W / 2
        placa("C1", "xz", (x0, y0, z0), ret(0, 0, total, d.BRACO_W), cor="#f6f6f6", grupo="cancelas",
              unid=unid, nome="Braço da cancela", tex="braco_E" if sinal < 0 else "braco_S")
        # braço plástico do servo, por trás do papelão
        hx0, hx1 = (cx - 15, cx + 3) if sinal < 0 else (cx - 3, cx + 15)
        caixa("cancelas", "#ffffff", (hx0, d.GUARITA_Y1 + 6.8, d.CANCELA_Z - 2.5), (hx1, y0, d.CANCELA_Z + 2.5),
              unid=unid)
    rotulo("cancela de ENTRADA (servo 1)", (d.CANCELA_E_X - 22, d.CANCELA_Y, 75))
    rotulo("cancela de SAÍDA (servo 2)", (d.CANCELA_S_X + 18, d.CANCELA_Y, 75))


# ---------------------------------------------------------------- carros
CORES = ["#d62828", "#f2b705", "#1f5fbf", "#efefef", "#f07d1a", "#2a9d63", "#7b4fc9", "#9aa3ad"]


def carro(unid, cx, y0, cor):
    """Carro: caixinha colada de 5 retângulos (2 laterais, frente, traseira e teto), frente para +Y."""
    g = "carros"
    L, Wc, Hp = d.CARRO_L, d.CARRO_W, d.CARRO_PAREDE_H
    z = d.EVA
    exl = {-1: (-14, 0, 10), 1: (14, 0, 10)}           # explodida: laterais para fora
    for xf, s in ((cx - Wc / 2, -1), (cx + Wc / 2 - T, 1)):
        placa("CL", "yz", (xf, y0, z), ret(0, 0, L, Hp), cor=cor, grupo=g, unid=unid, explode=exl[s],
              nome="Carro, lateral", tex=f"carro:{cor}:lat")
    Wi = Wc - 2 * T
    exf = {0: (0, -14, 4), 1: (0, 14, 4)}
    for k, yy in enumerate((y0, y0 + L - T)):
        placa("CF", "xz", (cx - Wi / 2, yy, z), ret(0, 0, Wi, Hp), cor=cor, grupo=g, unid=unid, explode=exf[k],
              nome="Carro, frente/traseira", tex=f"carro:{cor}:{'tras' if k == 0 else 'frente'}")
    zt = z + Hp
    ext = (0, 0, 30)
    placa("CT", "xy", (cx - Wc / 2, y0, zt), ret(0, 0, Wc, L), cor=cor, grupo=g, unid=unid, explode=ext,
          nome="Carro, teto", tex=f"carro:{cor}:teto")
    # adesivos (só para ver): janelas e rodas nas laterais, vidros no teto, faróis e lanternas
    vid = "#26303b"
    for xf, s in ((cx - Wc / 2, -1), (cx + Wc / 2, 1)):
        xa, xb = sorted((xf, xf + s * 0.25))
        caixa(g, vid, (xa, y0 + 13, z + 8.5), (xb, y0 + 39, z + 13.5), unid=unid, explode=exl[s])
        for a in (11.0, L - 11.0):
            cil(g, "#151515", "x", (min(xf, xf + s * 0.3), y0 + a, z + 4.2), 0.3, 4.2, unid=unid, explode=exl[s])
            cil(g, "#b9bec6", "x", (min(xf, xf + s * 0.45), y0 + a, z + 4.2), 0.45, 1.8, unid=unid, explode=exl[s])
    zt2 = zt + T
    caixa(g, vid, (cx - Wc / 2 + 2.5, y0 + 31, zt2), (cx + Wc / 2 - 2.5, y0 + 38, zt2 + 0.25), unid=unid, explode=ext)
    caixa(g, vid, (cx - Wc / 2 + 2.5, y0 + 10, zt2), (cx + Wc / 2 - 2.5, y0 + 15, zt2 + 0.25), unid=unid, explode=ext)
    for s in (-1, 1):
        caixa(g, "#fff1a8", (cx + s * 5.5 - 2.5, y0 + L, z + 8), (cx + s * 5.5 + 2.5, y0 + L + 0.3, z + 11), unid=unid,
              explode=exf[1])
        caixa(g, "#e0302a", (cx + s * 5.5 - 2.5, y0 - 0.3, z + 8), (cx + s * 5.5 + 2.5, y0, z + 11), unid=unid,
              explode=exf[0])
    PIVOS.setdefault(unid, [cx, y0 + L / 2, z, 0])


def carros():
    cx = d.ENTRADA_X0 + d.FAIXA_ENTRADA / 2
    carro("espera", cx, d.CARRO_ESPERA_Y0, CORES[0])
    for k in range(d.N_VAGAS):
        x = d.VAGAS_X0 + d.FAIXA / 2 + (k + 0.5) * d.VAGA_PASSO
        carro(f"vaga{k + 1}", x, d.VAGAS_Y0 + 3.0, CORES[1 + k % 7])


# ---------------------------------------------------------------- cabos
def cabos():
    z_d = d.DUPONT_TOPO_Z
    E = d.ELEV_TOTAL
    base = -E + 4
    # sensor: J4 -> por cima da borda da placa -> furo de cabos -> por baixo -> rasgo do sensor
    j4x, j4y = X(d.PECAS["J4"][0]), Y(d.PECAS["J4"][1])
    fx = (d.FURO_CABOS[0] + d.FURO_CABOS[2]) / 2
    cabo("#9a9a9a", [[j4x, j4y, z_d], [j4x - 1, j4y - 8, z_d + 3], [j4x - 4, Y(50) - 1, z_d - 4],
                     [j4x - 7, Y(52), 20], [fx + 6, Y(52) + 1, 6], [fx + 1, Y(52) + 4, -2], [fx - 2, Y(52) + 9, -0.3 * E],
                     [fx - 8, 36, -0.65 * E], [70, d.US_Y - 6, base + 3], [30, d.US_Y - 1, base + 2],
                     [d.MOLD_X[0] + 1, d.US_Y, base + 3], [d.US_X_COSTAS - 1.2, d.US_Y, -0.6 * E],
                     [d.US_X_COSTAS - 1.2, d.US_Y, -14]], 1.3)
    rotulo("cabo do sensor: furo -> por baixo -> totem", (60, 48, -0.45 * E), 6, fundo=True)
    # rede: plugue rígido -> desce pelo furo da rede -> sai pelos fundos
    xe = X(d.PI_USB_ETH_U)
    yr = Y((d.REDE_V[0] + d.REDE_V[1]) / 2)
    zr = d.PI_Z0 + 1.6 + 6.5
    caixa("cabos", "#4f9cf9", (xe, yr - 6, zr - 5.5), (xe + d.REDE_PLUGUE, yr + 6, zr + 5.5))
    fxr = d.arcos()["fundo"][0]
    cabo("#2f80ed", [[xe + d.REDE_PLUGUE - 1, yr, zr], [fxr + 3, yr, zr - 1], [fxr, yr + 1, 1], [fxr, yr + 3, -0.3 * E],
                     [fxr, 45, -0.75 * E], [fxr, 100, base + 2], [fxr, 160, base + 1], [fxr, D + 20, base + 1],
                     [fxr, D + 60, base]], 2.6)
    rotulo("cabo de REDE: desce no furo e sai pelos fundos", (fxr, D + 30, -0.5 * E), 6, fundo=True)
    # energia: plugue micro-USB atravessa o rasgo da parede da frente
    xm = X(d.MICRO_USB_U)
    caixa("cabos", "#2a2a2a", (xm - 4, -14, 3.0), (xm + 4, Y(63.53) - 0.5, 9.5))
    cabo("#1b1b1b", [[xm, -13, 6.2], [xm, -20, 4], [xm, -25, -10], [xm, -24, -0.6 * E], [xm, -22, base],
                     [xm, -60, base - 2]], 1.6)
    rotulo("ENERGIA (micro-USB)", (xm, -30, 22), 6)
    # servos: por dentro da guarita, junto da parede do fundo
    for ref, sx0 in (("J2", d.SERVO_E_X0), ("J3", d.SERVO_S_X0)):
        u, v = d.PECAS[ref]
        x, y = X(u), Y(v)
        cx = sx0 + d.SERVO_CORPO[0] / 2
        yb = (Y(0) + d.GUARITA_Y1 - T) / 2          # vão entre a borda da placa e a parede do fundo
        s = -1 if cx < x else 1
        cabo(LARANJA, [[x, y, z_d], [x + s * 2, y + 10, z_d + 4], [x + s * 6, yb, 30], [x + s * 12, yb, 8],
                       [x + s * 30, yb, 3], [cx - s * 14, yb, 3], [cx - s * 8, 66, 3],
                       [cx, d.GUARITA_Y1 - T - d.SERVO_ABAIXO_ABA - 0.5, d.SERVO_ABA + 3]], 1.1)
    rotulo("furo de cabos", (fx, (d.FURO_CABOS[1] + d.FURO_CABOS[3]) / 2, 28), 6, fundo=True)
    rotulo("furo da rede", (fxr, yr, 30), 6, fundo=True)


# ---------------------------------------------------------------- adesivos como textura
def adesivos_3d():
    """Etiquetas e adesivos (os mesmos desenhos dos PDFs de impressão) como textura, um PNG com transparência
    por peça. Cada PNG cobre o retângulo (x0, y0, w, h) da peça em mm: a textura encaixa no contorno dela."""
    import base64
    import pymupdf
    import gerar_adesivos as ga
    from folha import MM

    saida = {}
    o = 5.0                                   # margem dentro da página, em mm

    def gera(nome, x0, y0, w, h, desenha, espelho=False):
        doc = pymupdf.open()
        F = ga.Folha(doc, w + 2 * o, h + 2 * o)
        desenha(F, o, o)
        F.fim()
        clip = pymupdf.Rect(o * MM, o * MM, (o + w) * MM, (o + h) * MM)
        pix = doc[0].get_pixmap(clip=clip, dpi=150, alpha=True)
        saida[nome] = {"png": base64.b64encode(pix.tobytes("png")).decode("ascii"),
                       "x0": x0, "y0": y0, "w": w, "h": h, "espelho": espelho}

    import os
    png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hardware", "previas",
                       "placa_topo_adesivo.png")
    with open(png, "rb") as f:
        saida["interface"] = {"png": base64.b64encode(f.read()).decode("ascii"),
                              "x0": 0, "y0": 0, "w": 100.0, "h": 50.0, "espelho": False}
    # etiqueta A PIMACO (metade de cima da placa, papel branco com a impressão): arte do User.3 do KiCad
    png_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hardware", "previas",
                         "etiqueta_A_pimaco.png")
    with open(png_a, "rb") as f:
        saida["etiqueta_A"] = {"png": base64.b64encode(f.read()).decode("ascii"),
                               "x0": 0, "y0": 0, "w": 100.0, "h": 33.9, "espelho": False}

    # guarita (paredes, telhado, totem)
    gx = d.GUARITA_X1 - d.GUARITA_X0
    gy = d.GUARITA_Y1 - d.GUARITA_Y0
    gl = gy - 2 * d.T
    gera("painel", 0, 0, gx, d.PAINEL_H, ga.adesivo_painel)
    gera("fundo", 0, 0, gx, d.GUARITA_H, ga.adesivo_fundo, espelho=True)   # colado por fora, visto de trás
    gera("lado_porta", 0, 0, gl, d.GUARITA_H, lambda F, x, y: ga.adesivo_lado(F, x, y, porta=True))
    gera("lado_janela", 0, 0, gl, d.GUARITA_H, lambda F, x, y: ga.adesivo_lado(F, x, y, porta=False))
    gera("totem", 0, 0, d.TOTEM_L, d.TOTEM_H, ga.adesivo_totem)
    gera("telhado", 0, 0, gx + 6, gy + 6, ga.adesivo_telhado)
    gera("botao", 0, 0, d.POT_BOTAO, d.POT_BOTAO, ga.adesivo_botao)
    # ilha de grama e cancelas
    gera("grama", 0, 0, d.ENTRADA_X0 - d.FAIXA, d.ILHA_Y1, ga.adesivo_grama)
    for lado, comp, pivo in (("E", d.BRACO_E, True), ("S", d.BRACO_S, False)):
        total = comp + d.BRACO_ATRAS
        gera(f"braco_{lado}", 0, 0, total, d.BRACO_W,
             lambda F, x, y, t=total, p=pivo: ga.listra_cancela(F, x, y, p, comp=t))
    # carros: teto, laterais, frente e traseira, nas 8 cores
    wi = d.CARRO_W - 2 * d.T
    for k, cor in enumerate(CORES):
        rgb, taxi = ga.hexrgb(cor), k == 1
        gera(f"carro:{cor}:teto", 0, 0, d.CARRO_W, d.CARRO_L,
             lambda F, x, y, c=rgb, t=taxi: ga.carro_teto(F, x, y, c, taxi=t))
        gera(f"carro:{cor}:lat", 0, 0, d.CARRO_L, d.CARRO_PAREDE_H,
             lambda F, x, y, c=rgb: ga.carro_lado(F, x, y, c, False))
        gera(f"carro:{cor}:frente", 0, 0, wi, d.CARRO_PAREDE_H,
             lambda F, x, y, c=rgb: ga.carro_ponta(F, x, y, c, True))
        gera(f"carro:{cor}:tras", 0, 0, wi, d.CARRO_PAREDE_H,
             lambda F, x, y, c=rgb: ga.carro_ponta(F, x, y, c, False))
    # etiquetas PIMACO do piso: faixas e setas brancas, escritas e números pretos
    for cod, tipo, dado in d.marcas_piso():
        if tipo == "faixa":
            x0, y0, x1, y1 = dado
            gera(cod, x0, y0, x1 - x0, y1 - y0,
                 lambda F, x, y, w=x1 - x0, h=y1 - y0: F.ret(x, y, x + w, y + h, cor=None, fill=(1, 1, 1), w=0))
        elif tipo == "seta":
            x0, y0 = min(p[0] for p in dado), min(p[1] for p in dado)
            w, h = max(p[0] for p in dado) - x0, max(p[1] for p in dado) - y0
            gera(cod, x0, y0, w, h,
                 lambda F, x, y, pts=dado, a=x0, b=y0: F.poly([(x + px - a, y + py - b) for px, py in pts],
                                                              None, (1, 1, 1), 0))
        else:
            x0, y0, x1, y1 = dado[1:]
            w, h = x1 - x0, y1 - y0
            if tipo == "escrita":
                gera(cod, x0, y0, w, h,
                     lambda F, x, y, t=dado[0], w=w, h=h: ga.preto_com_texto(F, x, y, w, h, t, 3.6))
            else:
                gera(cod, x0, y0, w, h,
                     lambda F, x, y, t=str(dado[0]), w=w, h=h: ga.preto_com_texto(F, x, y, w, h, t, 5.0))
    return saida


# ---------------------------------------------------------------- pasta
COLADAS = ("P1", "EVA", "B1", "GP", "TP", "GT", "CL", "CF", "CT")   # coladas no piso/telhado ou carros colados


def pasta():
    """Deita cada peça de papelão na pilha (o piso com o EVA e os batentes é a base)."""
    pecas = [(i, it) for i, it in enumerate(ITENS)
             if it["k"] == "placa" and it["cod"] and it["cod"] not in COLADAS]
    lista = []
    for i, it in pecas:
        xs = [p[0] for p in it["c"]]
        ys = [p[1] for p in it["c"]]
        lista.append((i, max(xs) - min(xs), max(ys) - min(ys)))
    saida, n = d.empilhar(lista)
    z_base = d.PILHA_BASE - T
    for i, x, y, w, h, camada, girou in saida:
        it = ITENS[i]
        xs = [p[0] for p in it["c"]]
        ys = [p[1] for p in it["c"]]
        amin, amax, bmin = min(xs), max(xs), min(ys)

        def tr(p):
            a, b = p
            return [round(b - bmin, 3), round(amax - a, 3)] if girou else [round(a - amin, 3), round(b - bmin, 3)]

        c = [tr(p) for p in it["c"]]
        f = []
        for fu in it["f"]:
            if isinstance(fu, dict):
                a, b, r = fu["c"]
                q = tr((a, b))
                f.append({"c": [q[0], q[1], r]})
            else:
                f.append([tr(p) for p in fu])
        it["fl"] = {"o": [round(x, 2), round(y, 2), round(z_base + camada * T, 2)], "c": c, "f": f}
    return n


def main(saida):
    piso()
    elevacao()
    guarita()
    eletronica()
    totem()
    cancelas()
    carros()
    cabos()
    n = pasta()
    c, e, v = d.sensor()
    cena = {
        "piso": [W, D], "itens": ITENS, "cabos": CABOS, "rotulos": ROTULOS, "pivos": PIVOS,
        "elev": d.ELEV_TOTAL,
        "sensor": {"x": d.US_X_FACE, "y": d.US_Y, "z": d.EVA + d.US_Z, "parede": d.GUARITA_X0,
                   "limiar": 40.0, "faixa": [d.ENTRADA_X0, d.GUARITA_X0]},
        "carro": {"L": d.CARRO_L, "W": d.CARRO_W, "espera_y0": d.CARRO_ESPERA_Y0,
                  "corredor_y": (d.GUARITA_Y1 + d.VAGAS_Y0) / 2, "cancela_y": d.CANCELA_Y},
        "pasta": {"camadas": n, "base": d.PILHA_BASE + T, "T": T, "interno": list(d.PASTA)},
        "texto": {"versao": "v5", "sensor": [round(c, 1), round(e, 1), round(v, 1)]},
        "texturas": adesivos_3d(),
    }
    with open("modelo_3d.html", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("/*__CENA__*/null", json.dumps(cena, ensure_ascii=False, separators=(",", ":")))
    with open(saida, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"gerado: {saida}  ({len(ITENS)} itens, {len(CABOS)} cabos, pasta com {n} camadas)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../maquete_3d.html")
