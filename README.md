<a id="topo"></a>

<h1 align="center">🅿️ Estacionamento Inteligente</h1>

<p align="center">
Raspberry Pi, sensores e um painel web para controlar entradas, saídas e vagas.
</p>

<p align="center">
<img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white" alt="Raspberry Pi">
<img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js">
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/KiCad-314CB0?style=for-the-badge&logo=kicad&logoColor=white" alt="KiCad">
</p>

<p align="center">
<img src="docs/projeto_fisico/fotos/07-painel-e-maquete-em-funcionamento.jpeg" width="760" alt="Protótipo funcionando: painel no notebook e maquete">
</p>

<p align="center">
<a href="docs/projeto_fisico/video/demonstracao-projeto-fisico.mp4"><b>▶️ Vídeo</b></a> &nbsp;·&nbsp;
<a href="codigo/sistema/"><b>💻 Código</b></a> &nbsp;·&nbsp;
<a href="guia/guia_equipe.pdf"><b>📘 Guia (PDF)</b></a> &nbsp;·&nbsp;
<a href="maquete/"><b>🧱 Maquete</b></a>
</p>

---

## 🎯 Sobre o projeto

Projeto da atividade **Apresentação do projeto Raspberry**. O caso escolhido é um **estacionamento de supermercado**, em que o que importa é a **saída**: quem sai precisa estar liberado (no protótipo, pelo painel ou pelo potenciômetro da guarita).

| 🚗 Entrada | 🚧 Saída | 🖥️ Painel |
| :-- | :-- | :-- |
| O sensor percebe o carro. Se há vaga, a cancela abre e fecha depois que o carro passa. | O porteiro libera a saída pelo painel ou pela guarita. | Vagas livres, movimento da semana e temperatura do pátio. |

---

## 🧭 Como funciona

```mermaid
flowchart LR
  subgraph S["📡 Sensores"]
    direction TB
    DHT["🌡️ DHT11<br/>temperatura e umidade"]
    US["📏 HC-SR04<br/>presença"]
    POT["🎛️ Potenciômetro e botão<br/>guarita"]
  end

  subgraph R["🍓 Raspberry Pi"]
    direction TB
    MAIN["🧠 main.py<br/>decide e aciona"]
    CANC["🚧 Cancelas, LED e buzzer"]
    NODE["⚙️ Node.js + Express<br/>server.js"]
    DB[("🗄️ SQLite<br/>estacionamento.db")]
    PAINEL["🖥️ Painel web<br/>public/index.html"]
  end

  NAV["💻 Navegador<br/>PC ou celular"]

  DHT --> MAIN
  US --> MAIN
  POT --> MAIN
  MAIN --> CANC
  MAIN -- "API HTTP /api" --> NODE
  NODE <--> DB
  NODE --> PAINEL
  NAV -- "raspberrypi.local:3000" --> PAINEL

  classDef sensor fill:#FFF4D6,stroke:#E0A800,color:#3D2E00
  classDef pi fill:#E3F2FD,stroke:#1E6FD9,color:#0B2E59
  classDef server fill:#E8F5E9,stroke:#2E7D32,color:#123B16
  classDef painel fill:#F3E5F5,stroke:#8E24AA,color:#3A1347
  classDef user fill:#ECEFF1,stroke:#546E7A,color:#263238
  class DHT,US,POT sensor
  class MAIN,CANC pi
  class NODE,DB server
  class PAINEL painel
  class NAV user
  style S fill:#FFFBEA,stroke:#E0A800
  style R fill:#F4F9FF,stroke:#1E6FD9
```

**Em ordem, o que acontece:**

1. 🚗 Um carro chega à entrada e o sensor percebe.
2. 🧠 A Raspberry decide: se há vaga, abre a cancela. Se está lotado, acende o LED vermelho.
3. ⚙️ A Raspberry registra a entrada ou saída no servidor.
4. 🖥️ O painel atualiza as vagas, e a pessoa vê tudo no navegador.

> 🎨 **Cores:** 🟡 sensores · 🔵 Raspberry Pi · 🟢 servidor e banco · 🟣 painel · ⚪ navegador


---

## 👥 Quem fez o quê

| Integrante | Tarefa | Redes |
| :-- | :-- | :-- |
| *Ana Graciano* | 1️⃣ Cancelas | [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Ane-Graciano) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ana-graciano/) |
| *Laís Zanardi* | 2️⃣ Presença | [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/lais-zanardi) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lais-zanardi-inocencio/) |
| *Pedro Nascimento* | 3️⃣ Guarita manual | [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/P3dr0213) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedro-nascimento-87a22937a/) |
| *Lucas Inácio* | 4️⃣ Sinalização | [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Lukitta013) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/luucasinacioo/) |
| *João Moura* | 5️⃣ Ambiente | [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/JoaooMoura) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joaoomoura/) |
| *Gustavo Rosa* | 6️⃣ Lógica | [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/gustasvos) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gustavo-rosa-46a251180/) |
| *João Silva* | 7️⃣ Backend | [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/kakashinho) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joao-vitor-siqueira-a2a2a3227/) |
| *Enzo Gabriel de Paula* | 8️⃣ Frontend | [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/EnzoGabrielCode) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/enzo-gabriel-de-paula-8795a8332/) |

---

## 🔧 Como ficou na prática

Primeiro montamos tudo sobre uma base de papelão, para testar as ligações. Depois veio o protótipo completo, com a maquete e o painel.

<p align="center">
<img src="hardware/previas/placa_3d_sem_fundo.png" width="620" alt="Placa de interface em 3D (KiCad)"><br>
<sub>Placa de interface em 3D, feita no KiCad</sub>
</p>

<details>
<summary><b>📷 Fotos da bancada (antes do protótipo)</b></summary>

<table>
<tr>
<td align="center"><img src="docs/projeto_fisico/fotos/01-visao-geral-pi-servos-sensor.jpeg" width="380" alt="Bancada: Pi, placa, servos e sensor"><br><sub>Pi, placa, servos e sensor</sub></td>
<td align="center"><img src="docs/projeto_fisico/fotos/04-vista-de-cima-placa-servos-sensor.jpeg" width="380" alt="Bancada: vista de cima"><br><sub>Vista de cima</sub></td>
</tr>
<tr>
<td align="center"><img src="docs/projeto_fisico/fotos/05-vista-lateral-placa-servos-sensor.jpeg" width="380" alt="Bancada: vista lateral"><br><sub>Vista lateral</sub></td>
<td align="center"><img src="docs/projeto_fisico/fotos/02-materiais-eva-preto-branco.jpeg" width="380" alt="Materiais: EVA preto e branco"><br><sub>Materiais: EVA preto e branco</sub></td>
</tr>
</table>

</details>

<details>
<summary><b>📷 Fotos do protótipo montado</b></summary>

<table>
<tr>
<td align="center"><img src="docs/projeto_fisico/fotos/08-maquete-detalhe.jpeg" width="380" alt="Detalhe da maquete"><br><sub>Detalhe da maquete</sub></td>
<td align="center"><img src="docs/imagens/painel-web.png" width="380" alt="Painel web"><br><sub>Painel web</sub></td>
</tr>
</table>

</details>

---

## 🧱 Maquete de papelão

Feita só com papelão, EVA e papel impresso. Ela desmonta em peças planas que cabem numa pasta.

<p align="center">
<img src="maquete/previas/vista_3d.png" width="760" alt="Vista 3D da maquete do estacionamento"><br>
<sub>Vista 3D: abra <a href="maquete/maquete_3d.html">maquete_3d.html</a> para girar o modelo</sub>
</p>

- 📖 [Passo a passo para montar](maquete/LEIA-ME.md)
- 🧭 [Proposta e decisões](maquete/FASE1_proposta.md)
- 🖨️ [Arquivos para imprimir](maquete/impressao/)

---

## 🚀 Como rodar no Raspberry

No Raspberry, a partir da pasta `~/codigos/final`:

```bash
npm install            # só na primeira vez
./web.sh start         # painel em http://raspberrypi.local:3000
python3 -u main.py     # parte física (cancelas, LED e buzzer)
```

<details>
<summary><b>🧪 Testar uma peça por vez</b></summary>

```bash
python3 teste_isolado.py led     # também: buzzer, servo_entrada, servo_saida, botao, pot, distancia, dht
```

Pare o `main.py` antes de testar uma peça.

</details>

---

## 📚 Onde ler mais

| Documento | Para que serve |
| :-- | :-- |
| 📘 [Guia da equipe](guia/index.html) | Passo a passo de cada tarefa, com figuras |
| 📕 [Guia em PDF](guia/guia_equipe.pdf) | A mesma versão, para imprimir |
| 📦 [Transferência](docs/transferencia.md) | O que tem no repositório e como usar cada parte |
| 🧾 [Lista de materiais](docs/lista_de_materiais.csv) | Componentes da placa |

---

<details>
<summary><b>🔎 Saiba mais</b></summary>

### Pinos (numeração BCM)

| Peça | GPIO |
| :-- | :-- |
| Servo da entrada / da saída | 13 / 26 |
| Ultrassônico (TRIG / ECHO) | 23 / 24 |
| LED RGB (vermelho / verde / azul) | 4 / 17 / 27 |
| Buzzer | 6 |
| Botão | 5 |
| Potenciômetro (carrega / lê) | 12 / 25 |
| DHT11 | 22 |

### Regras do sistema

| Regra | Valor |
| :-- | :-- |
| Vagas | 7 |
| Carro na entrada | menos de 5 cm, confirmado em duas leituras |
| Tempo para fechar a cancela | 2 s |
| Intervalo mínimo entre entradas | 6 s |
| Leitura de temperatura e umidade | a cada 30 s |

### API (como o painel e a Raspberry conversam)

| O que acontece | Quem faz |
| :-- | :--: |
| Registra uma entrada ou saída | 🧠 Raspberry |
| Recusa saída se não há ninguém dentro | 🧠 Raspberry |
| Mostra vagas e movimento no painel | 🖥️ Painel |
| Guarda temperatura e umidade | 🧠 Raspberry |
| Pede a liberação da saída | 🖥️ Painel |
| Recebe o pedido e abre a cancela | 🧠 Raspberry |

As rotas exatas estão em [`codigo/sistema/server.js`](codigo/sistema/server.js).

### Testes realizados

- ✅ API: contagem de eventos, recusa de saída sem ninguém dentro e comandos antigos.
- ✅ Painel: no computador e em tela de celular.
- ✅ Peças físicas: cada uma testada separadamente.
- ✅ Controle: `main.py` rodado com as peças reais.

### Pastas do repositório

| Pasta | Conteúdo |
| :-- | :-- |
| `codigo/sistema/` | Sistema final |
| `codigo/starter/` | Códigos de partida das 8 tarefas |
| `codigo/exemplos_originais/` | Scripts do começo do projeto |
| `guia/` | Guia da equipe e o gerador dele |
| `hardware/` | Projeto da placa no KiCad |
| `maquete/` | Maquete e o gerador dela |
| `docs/` | Documentação, fotos e vídeo |

</details>

---

<p align="center"><a href="#topo">⬆️ Voltar ao topo</a></p>
