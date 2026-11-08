# Maquete do estacionamento: projeto (v5, para cortar com tesoura)

Resumo das decisões e dos números. Os links:
- montagem passo a passo: [LEIA-ME.md](LEIA-ME.md);
- vista 3D: [maquete_3d.html](maquete_3d.html);
- planta cotada: [previas/planta_v5.png](previas/planta_v5.png);
- arquivos para imprimir: [impressao/](impressao/).

## Histórico de pedidos

| Versão | Pedido | Como ficou |
|---|---|---|
| v1 | Rede por cabo; +30 mm no piso | Piso de 311 × 200, com um furo para o cabo de rede dentro da guarita. |
| v1 | Tudo de papelão, sem palito | Braço da cancela de papelão, colado no braço plástico do servo. |
| v2 | Estrutura menor que 5 cm | Elevação de 5 cm. |
| v2 | Carros menores e mais bonitos | Carro caixa fechado de 50 × 24 × 17,5. |
| v2 | Faixas, escritas e listras em etiqueta | PIMACO 6282, a mesma da placa. |
| v2/v3 | Painel fácil de tirar, sem tirar o telhado | O painel fica solto e sai inclinando para a frente. |
| v4 | Rasgo de 2,8 folgado | Papelão de 2,5 mm. |
| **v5** | **Só tesoura; não alcança rasgos de 3 mm** | **Nenhum rasgo estreito, nenhum furo fechado nas paredes, todo corte começa na borda.** |

**Como a v5 troca cada encaixe:**

| Antes (rasgos) | Agora (tesoura) |
|---|---|
| Grade de travessas em meia-madeira | **Moldura de 4 painéis** com dobradiças de fita (dobra em zigue-zague) + 1 painel solto no meio |
| Abas das travessas em rasgos do piso | **Travas TP** coladas embaixo do piso, por dentro da moldura |
| Abas das paredes em rasgos do piso | **Guias GP** coladas no piso, em volta da guarita (a da frente é a calçada) |
| Paredes encaixadas nos cantos e no telhado | Fundo + laterais em **U com dobradiças de fita**; telhado liso com **travas GT** coladas por baixo |
| Painel preso no telhado | Painel de pé entre a calçada e as laterais, seguro pelo **botão do pot** |
| Furo do tubinho e janela do LED | **Recortes abertos em cima** (10 e 12 mm) |
| Furos dos servos | **Recortes abertos embaixo** (11,5 mm) |
| Rasgos do totem | Totem com **dobradiças de fita** |
| Carro com abas e janelas | **Caixinha colada** de 5 retângulos (vai num saquinho) |
| Furos no meio do piso | **Linha de acesso** reta a partir da borda (fechada depois com fita e com a tira da calçada); o do sensor virou recorte na borda |

## Números principais

| Item | Valor |
|---|---|
| Piso | 311 × 200; elevação de 5 cm (moldura de 279 × 180 × 47,5) |
| Guarita | 188,8 × 76 × 62 (painel com 61,5) |
| Faixas de entrada e saída | 38 cada (com uma volta de 5,5 sem EVA em torno da guarita) |
| Corredor | 58 |
| Vagas | 7 de 36 × 60 |
| Carro | 50 × 24 × 17,5 (colado) |
| Sensor | carro a 21 a 25 mm, sem carro a 59 mm. **Limiar: 40 mm** |
| Recortes (largura) | tubinho 10, LED 12, energia 12, servo 11,5, sensor 14, janelas do totem 17, vãos da moldura 40 |
| Furos no piso | cabos 26 × 24 e rede 28 × 28, ambos com linha de acesso |
| Tiras de 5 mm | GP ×4 (em cima do piso), TP ×6 (embaixo do piso), GT ×3 (embaixo do telhado) |
| Papelão | 2,5 mm; ~0,23 m² da chapa de 1 m² |
| Guardar | pasta com ~2 cm (piso + peças planas); carros e eletrônica num saquinho |

## Como o projeto é conferido (`gerador/`)

- `design.py`: todo recorte tem pelo menos 8 mm de largura. As travas não cobrem furos nem linhas de acesso, e o painel da moldura cabe numa A4.
- `conferir.py`: monta as 75 peças em 3D e confirma que nenhuma invade outra. Também confirma que a eletrônica e os plugues não batem no papelão.
- `conferir_pdf.py`: folhas no tamanho certo, nada a menos de 5 mm da borda, régua de 100 mm em todas as folhas A4 e desenhos dentro das etiquetas PIMACO.
