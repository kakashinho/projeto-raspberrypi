# ⚙️ Sistema final

O código que roda na Raspberry Pi: controle das cancelas, sensores, LED, buzzer, servidor e painel web.

## 📂 Arquivos

| Arquivo | Função |
| :-- | :-- |
| `main.py` | Controle principal: decide quando abrir, fechar e registrar |
| `cancelas.py` | Servos das duas cancelas (PWM) |
| `presenca.py` | Sensor ultrassônico que percebe o carro |
| `manual.py` | Potenciômetro e botão da guarita |
| `sinais.py` | LED RGB e buzzer |
| `ambiente.py` | DHT11 (temperatura e umidade) |
| `pinos.py` | Pinos da placa, em um lugar só |
| `server.js`, `package.json` | Servidor Node.js com o banco SQLite |
| `public/index.html` | Painel web |
| `teste_isolado.py` | Testa uma peça por vez |
| `web.sh` | Liga e desliga o servidor e o painel |
| `*.service` | Serviços para rodar em segundo plano |

## ▶️ Como rodar

```bash
npm install            # só na primeira vez
./web.sh start         # painel em http://raspberrypi.local:3000
python3 -u main.py     # parte física
```

Para testar uma peça sozinha: `python3 teste_isolado.py led` (veja as opções no próprio script). Pare o `main.py` antes.

## 🎛️ Calibrar o potenciômetro

Cada placa tem a sua calibração, por isso o `calibracao_pot.json` **não** vai para o repositório. Para criar o seu, rode:

```bash
python3 manual.py
```

O script pede para girar o potenciômetro até o mínimo e depois até o máximo, e grava o arquivo ao lado do `manual.py`.
