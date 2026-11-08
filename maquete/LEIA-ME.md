# Maquete do estacionamento: imprimir, cortar, montar e guardar

Versão v5, **feita para cortar com tesoura**. Todas as medidas estão em mm e saem de [gerador/design.py](gerador/design.py). Para ver como fica montada, abra a vista 3D [maquete_3d.html](maquete_3d.html) no navegador (precisa de internet).

**Regra desta versão:** todo corte começa na borda da peça, e nenhum recorte tem menos de 10 mm de largura. Não existem rasgos estreitos. Os encaixes viraram:
- **dobradiças de fita crepe** nos cantos, que dobram planas para guardar;
- **tiras coladas** (guias e travas), em que duas tiras lado a lado fazem o papel do rasgo;
- **carros colados** (caixinhas).

## 1. O que imprimir

Os arquivos estão em [impressao/](impressao/). **Imprima sempre a 100 % ("tamanho real"), sem "ajustar à página".** Em cada folha, meça a régua de 100 mm.

| Arquivo | Papel | Folhas |
|---|---|---|
| [gabaritos_A4.pdf](impressao/gabaritos_A4.pdf) | A4 comum (pode ser preto e branco) | 8 |
| [adesivos_A4.pdf](impressao/adesivos_A4.pdf) | A4 comum, **colorido** | 3 |
| [etiquetas_pimaco6282_teste.pdf](impressao/etiquetas_pimaco6282_teste.pdf) | papel comum tamanho **Carta**, para o teste | 1 |
| [etiquetas_pimaco6282.pdf](impressao/etiquetas_pimaco6282.pdf) | 1 folha **PIMACO 6282** (Carta) | 1 |

**Teste das etiquetas:** imprima o arquivo de teste em papel comum e ponha sobre a folha PIMACO, contra a luz. Se os desenhos caírem dentro das etiquetas, imprima o de verdade na folha PIMACO.

## 2. Material

- **Papelão de 2,5 mm:** as peças usam ~0,23 m² da chapa de 1 × 1 m.
- **EVA preto de 1 mm:** 311 × 200.
- **Etiquetas:** 1 folha PIMACO 6282.
- **Fita crepe:** dobradiças e linhas de acesso dos furos.
- **Colas:** cola branca (EVA, tiras, batentes, carros, braço da cancela) e cola bastão (adesivos de papel).
- **Ferramentas:** tesoura, régua e alfinete (ou a ponta de um compasso).
- **Tubinho do pot:** uma tira de papel sulfite de ~25 × 100 mm.

## 3. Ordem de corte (tudo com tesoura)

**0. Teste (folha 1)**

Num retalho, corte os recortes de teste:
- **servo:** 11 / 11,5 / 12 mm, abertos embaixo. O corpo do servo deve entrar justo; o padrão é 11,5.
- **tubinho:** 9 / 10 / 11 mm, abertos em cima. O padrão é 10.

**1. Piso P1 (folhas 2 e 3)**
1. O retângulo já desenhado (281 × 200) cresce **30 mm para a direita**: o piso fica com 311 × 200.
2. Emende as 2 folhas pelas 3 cruzes, prenda no papelão e corte o contorno. O **recorte do sensor** fica na borda esquerda.
3. Para os **2 furos**:
   1. Corte reto pela **linha de acesso** (tracejado vermelho), da borda da frente até o furo.
   2. Recorte o furo.
   3. Passe fita crepe por baixo da linha de acesso. Depois a tira da calçada, colada por cima, também fecha o corte.

**2. EVA preto (mesmas folhas do piso)**

Corte o contorno, o **recorte da guarita** (linha azul) e o recorte do sensor.

**3. Moldura de 5 cm**
- EF (frente e fundo, ×2): folha 6.
- ES (laterais, ×2): folha 5.
- EM (painel do meio, ×1): folha 6.

Os vãos embaixo são para os cabos.

**4. Guarita**
- Folha 4: painel G1, fundo G2 e laterais G3 (×2).
- Folha 5: telhado G4.

**5. Peças pequenas e tiras**
- Folha 7: totem S1 e S2 (×2), braço da cancela C1 (×2), botão do pot K1 e batentes B1 (×4).
- Tiras de 5 mm:
  - GP (guias, colam em cima do piso): ×4;
  - TP (travas, colam embaixo do piso): ×6;
  - GT (travas, colam embaixo do telhado): ×3.

  A guia da calçada (188,8 mm) está na folha 6; as outras, na folha 7.

**6. Carros (folha 7)**
- 16 laterais CL (50 × 15);
- 16 frente/traseira CF (19 × 15);
- 8 tetos CT (24 × 50).

A folha 8 mostra onde tirar cada peça da chapa e traz a lista completa.

> **Recorte largo** (servo, tubinho, LED, energia, janelas do sensor, vãos da moldura): corte os 2 lados até o fundo e depois o fundo.

> **Tiras de 5 mm:** corte uma tira comprida com 5 mm de largura e depois os pedaços no comprimento.

## 4. Montagem

**Piso**

1. **EVA no piso.** Cole o EVA no piso com cola branca, alinhando as bordas. Seque com um peso.
2. **Travas de baixo (TP).** Vire o piso e cole as 6 travas nos lugares tracejados em marrom do gabarito: 4 por dentro da moldura e 2 dos lados do painel do meio.
   - **Dica:** cole com a moldura e o painel do meio no lugar, usando-os de espaçador.
3. **Grama e etiquetas.**
   - Cole a grama (adesivo) na ilha da esquerda.
   - Cole as etiquetas PIMACO (faixas, setas, ENTRADA/SAÍDA, números) onde o gabarito mostra o código.
   - Dica: com o gabarito por cima, fure os cantos de cada etiqueta com o alfinete e cole ligando os furinhos.

**Moldura (estrutura de 5 cm)**

4. **Monte a moldura.**
   - Junte EF, ES, EF, ES em anel, com fita crepe nas quinas (por fora e por dentro).
   - Feche a última quina com um pedaço de fita.
   - Ponha o painel do meio EM em pé.
   - Desça o piso: as travas TP encaixam por dentro da moldura e dos 2 lados do EM.

**Guarita e servos**

5. **Batentes.** Ponha o Pi (com a placa) no lugar e cole os 4 batentes B1 em volta, com **1 mm de folga**. Tire o Pi e deixe secar.
6. **Guarita em U.** Junte o fundo G2 com as 2 laterais G3 pelas quinas de trás, com fita por fora e por dentro.
7. **Servos e guias.**
   - Ponha os 2 servos em pé no piso, no lugar.
   - Desça o U por cima: os servos entram pelos **recortes de baixo** do fundo, com o eixo para fora.
   - Com o U no lugar, cole as **guias GP**: uma do lado de fora de cada lateral, uma atrás do fundo e a **tira da calçada** na frente.
   - Use a própria parede como espaçador. **Deixe o painel G1 encostado enquanto cola a tira da calçada.**
8. **Cancelas.**
   - Cole as listras (etiqueta) nas 2 faces de cada braço C1.
   - Cole o braço plástico do servo no C1 com cola branca, centro em cima da bolinha ●.
   - Com o servo em 0° (fechada), encaixe o braço **na horizontal**.

**Eletrônica e cabos**

9. **Pi e cabos dos servos.**
   - Ponha o Pi + placa entre os batentes.
   - Ligue os servos: o da entrada no **J2**, o da saída no **J3**, pelo vão atrás da placa.
10. **Sensor.**
    - Monte o totem: S1 + as 2 S2, com fita nas quinas.
    - Ponha o HC-SR04 dentro: os transdutores saem pelas janelas, e os pinos e o conector descem pelo **recorte do sensor**.
    - O cabo vai do **J4**, desce pelo **furo de cabos**, passa por baixo e sai pelo vão da moldura da esquerda. São ~25 cm.
11. **Painel G1.**
    - Enrole a tira de papel no eixo do pot até ~Ø 8,5 e cole a tira nela mesma. **Não cole no eixo.**
    - Cole o botão K1, já com o adesivo, na ponta do tubinho.
    - Ponha o painel de pé atrás da tira da calçada, encostado na frente das laterais. O tubinho passa pelo recorte de cima.
    - Encaixe o tubinho no eixo: o botão, do lado de fora, segura o painel em pé.
    - Incline um pouco o LED para o recorte do LED.
12. **Telhado.** Antes, cole as 3 travas GT por baixo do telhado (lugares tracejados na folha 5). O telhado encaixa no U.
13. **Rede e energia.**
    - O cabo de rede pluga no Pi, desce pelo **furo da rede** e sai pelo vão do fundo da moldura.
    - O micro-USB de energia entra pelo recorte de baixo do painel.

**Carros**

14. Para cada carro, cole os adesivos nas peças. Depois, com o teto CT virado para baixo:
    1. Cole as 2 laterais CL em pé nas bordas compridas.
    2. Cole a frente e a traseira CF entre elas (cola branca).

### Tirar e pôr o painel
1. Puxe o botão: ele sai com o tubinho.
2. Incline o painel para a frente e levante.

Não precisa tirar o telhado. Para pôr de volta, faça o inverso.

## 5. Para a equipe (código)

- **Vagas:** a maquete tem **7 vagas**. No servidor, `MAX_VAGAS = 6` (em `guia_equipe/gerador/trechos/t7_server.js`) passa a **7**.
- **Sensor:**
  - O carro parado na cancela fica a **21 a 25 mm** do sensor.
  - Sem carro, ele vê a parede da guarita a **59 mm**.
  - **Limiar sugerido em `carro_presente()`: 40 mm.**
- **Cancelas:** 0° = fechada, 90° = aberta.

## 6. Desmontar e guardar

1. Tire o telhado, o painel e o U da guarita. O U dobra plano pelas dobradiças.
2. Tire o piso da moldura. Solte a fita da última quina da moldura e dobre em zigue-zague.
3. Monte a pilha:
   - **na pasta:** piso (com EVA, etiquetas, guias e travas colados), moldura dobrada, paredes, telhado e totem. Dá ~2 cm.
   - **num saquinho:** os carros (colados) e a eletrônica (Pi, placa, servos com os braços, sensor e cabos).

A pasta precisa ter pelo menos **315 × 205 mm** por dentro.

## 7. Arquivos e como gerar de novo

| Arquivo | O que faz |
|---|---|
| `gerador/design.py` | Todas as medidas. Também confere se todo recorte é largo o bastante para a tesoura. |
| `gerador/gerar_3d.py` + `modelo_3d.html` | Vista 3D: `maquete_3d.html` |
| `gerador/gerar_gabaritos.py` | `impressao/gabaritos_A4.pdf` |
| `gerador/gerar_adesivos.py` | Etiquetas PIMACO e adesivos A4 |
| `gerador/gerar_planta.py` | Planta cotada: `previas/planta_v5.png` |
| `gerador/conferir.py` | Confere a montagem: nenhuma peça invade outra, e a eletrônica não bate no papelão |
| `gerador/conferir_pdf.py` | Confere os PDFs: tamanho da folha, área imprimível, régua de 100 mm e etiquetas |

Na pasta `gerador/`:

```
python -B design.py
python -B conferir.py
python -B gerar_3d.py ../maquete_3d.html
python -B gerar_planta.py ../previas/planta_v5.png
python -B gerar_gabaritos.py ../impressao
python -B gerar_adesivos.py ../impressao
python -B conferir_pdf.py ../impressao
```
