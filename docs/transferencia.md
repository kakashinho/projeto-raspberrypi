# Entrega: o que foi entregue e como usar

## O que tem

| Pasta ou arquivo | O que tem |
|---|---|
| `codigo/sistema/` | `main.py`, `cancelas.py`, `presenca.py`, `manual.py`, `sinais.py`, `ambiente.py`, `pinos.py`, `server.js`, `public/`, `estacionamento.service` e `estacionamento-web.service` |
| `codigo/starter/` | Código de partida das 8 tarefas |
| `codigo/exemplos_originais/` | Os 9 scripts do começo do projeto |
| `hardware/` | Projeto KiCad, PDFs de montagem, trilhas em 1:1 e etiqueta Pimaco |
| `docs/` | Lista de materiais e ligações (CSV) |
| `guia/` | O guia da equipe (`index.html`) e o gerador dele |
| `README.md` | Resumo do projeto e comandos |

## Como usar

### Rodar o sistema no Raspberry

```bash
# No Raspberry (uma vez)
sudo apt update && sudo apt install -y python3-gpiozero python3-requests libgpiod2 nodejs npm
pip3 install adafruit-circuitpython-dht

# No seu PC: copiar o sistema (troque pelo IP de hoje)
scp -r codigo/sistema dsm@192.168.0.153:~/codigos/final

# No Raspberry: instalar o servidor e ligar os serviços
cd ~/codigos/final && npm install
sudo cp estacionamento.service estacionamento-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now estacionamento-web estacionamento

# Painel, no navegador do PC ou do celular
#   http://raspberrypi.local:3000
```

### Montar a placa

- Lista de compras: `docs/lista_de_materiais.csv`
- Etiqueta (imprimir a 100%): `hardware/etiquetas_A_B_pimaco6282.pdf`
- Ordem de montagem e testes: seção "Replicar a placa" do guia (`guia/index.html`)

### Testar uma peça

```bash
# pare o sistema antes
sudo systemctl stop estacionamento
python3 codigo/starter/tarefa2_teste_distancia.py
```

### Gerar de novo o guia

```bash
python3 guia/gerador/montar.py
```
