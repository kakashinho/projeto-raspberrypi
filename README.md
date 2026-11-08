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
<img src="docs/projeto_fisico/fotos/07-painel-e-maquete-em-funcionamento.jpeg" width="760" alt="Protótipo funcionando: painel no notebook e maquete"><br>
<sub>Primeiro protótipo</sub>
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

## 👥 Trabalho em equipe

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

<p align="center">
<img src="docs/imagens/fluxo_desenvolvimento.png" width="760" alt="Fluxo de desenvolvimento em 4 etapas: planejamento, placa, guia e código, montagem"><br>
<sub>Fluxo de desenvolvimento, na ordem em que foi feito</sub>
</p>

<p align="center">
<img src="hardware/previas/placa_3d_com_etiqueta.png" width="760" alt="Placa de interface em 3D (KiCad)"><br>
<sub>Placa de interface em 3D, feita no KiCad, com a etiqueta PIMACO</sub>
</p>

<details>
<summary><b>▶️ Ver a placa de outros ângulos</b></summary>

<table align="center">
<tr>
<td align="center"><img src="hardware/previas/kicad_etiqueta/1_topo_reto.png" width="380" alt="Placa vista de cima"><br><sub>Vista de cima</sub></td>
<td align="center"><img src="hardware/previas/kicad_etiqueta/2_inclinada.png" width="380" alt="Placa vista inclinada"><br><sub>Vista inclinada</sub></td>
</tr>
<tr>
<td align="center"><img src="hardware/previas/kicad_etiqueta/3_lado_esquerdo.png" width="380" alt="Placa vista do lado esquerdo"><br><sub>Lado esquerdo</sub></td>
<td align="center"><img src="hardware/previas/kicad_etiqueta/4_lado_direito.png" width="380" alt="Placa vista do lado direito"><br><sub>Lado direito</sub></td>
</tr>
</table>

</details>

<details>
<summary><b>▶️ Antes da montagem: a bancada de testes</b></summary>

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
<summary><b>▶️ Depois da montagem: o protótipo completo</b></summary>

<table>
<tr>
<td align="center"><img src="docs/projeto_fisico/fotos/08-maquete-detalhe.jpeg" width="380" alt="Detalhe da maquete"><br><sub>Detalhe da maquete</sub></td>
<td align="center"><img src="docs/imagens/painel-web.png" width="380" alt="Painel web"><br><sub>Painel web</sub></td>
</tr>
</table>

</details>

---

## 🧱 Projeto de montagem da maquete

O projeto que mostra como montar a maquete. Usa só papelão, EVA e papel impresso, e as peças são planas, para caberem numa pasta.

<p align="center">
<img src="maquete/previas/angulos/1_inicial.png" width="760" alt="Vista geral da maquete do estacionamento"><br>
<sub>Para girar o modelo, abra <a href="maquete/maquete_3d.html">maquete_3d.html</a></sub>
</p>

<details>
<summary><b>🔍 Mais ângulos da maquete</b></summary>

<table align="center">
<tr>
<td align="center"><img src="maquete/previas/angulos/5_lateral_esquerda.png" width="370" alt="Lateral da entrada"><br><sub>Lado da entrada</sub></td>
<td align="center"><img src="maquete/previas/angulos/8_diagonal_traseira.png" width="370" alt="Diagonal por trás"><br><sub>Por trás, em diagonal</sub></td>
</tr>
<tr>
<td align="center"><img src="maquete/previas/angulos/3_frente.png" width="370" alt="Frente da guarita"><br><sub>Frente da guarita</sub></td>
<td align="center"><img src="maquete/previas/angulos/9_painel_perto.png" width="370" alt="Painel de perto"><br><sub>Painel de perto (MANUAL e STATUS)</sub></td>
</tr>
</table>

</details>

- 📖 [Passo a passo para montar](maquete/LEIA-ME.md)
- 🧭 [Proposta e decisões](maquete/FASE1_proposta.md)
- 🖨️ [Arquivos para imprimir](maquete/impressao/)

---

## 🚀 Como rodar o sistema

Os comandos ficam na pasta [`codigo/sistema/`](codigo/sistema/), e rodam na Raspberry Pi com a placa de interface:

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
| 🔌 [Placa de interface](hardware/README.md) | Projeto da placa no KiCad, arquivos e etiquetas |
| 🧪 [Códigos de partida](codigo/starter/README.md) | Um esqueleto por tarefa, para começar |
| ⚙️ [Código final](codigo/sistema/README.md) | O sistema que roda na Raspberry Pi |

---

<details>
<summary><b>🔎 Saiba mais</b></summary>

<p align="center">
<img src="docs/imagens/ilustracao_pinos_gpio.png" width="760" alt="Pinos GPIO usados pela placa, com ilustração de cada componente"><br>
<sub>Pinos GPIO usados pela placa, na numeração BCM</sub>
</p>

<p align="center">
<img src="docs/imagens/saiba_regras.png" width="700" alt="Regras de funcionamento do sistema"><br>
<sub>Regras de funcionamento do sistema</sub>
</p>

<p align="center">
<img src="docs/imagens/saiba_api.png" width="700" alt="Quem faz cada ação no painel e na Raspberry"><br>
<sub>Quem faz cada ação no painel e na Raspberry</sub>
</p>
<p align="center">As rotas exatas estão em <a href="codigo/sistema/server.js"><code>codigo/sistema/server.js</code></a>.</p>


<p align="center">
<img src="docs/imagens/saiba_testes.png" width="700" alt="Testes feitos antes da entrega"><br>
<sub>Testes feitos antes da entrega</sub>
</p>

<p align="center">
<img src="docs/imagens/saiba_pastas.png" width="700" alt="Pastas do repositório e o que cada uma guarda"><br>
<sub>Pastas do repositório: o que cada uma guarda</sub>
</p>

</details>

---

<p align="center"><a href="#topo">⬆️ Voltar ao topo</a></p>
