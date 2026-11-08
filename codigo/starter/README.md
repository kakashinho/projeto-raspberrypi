# 🧪 Códigos de partida

Um esqueleto para cada tarefa do projeto. Cada pessoa começa daqui, testa a própria peça e depois entrega o módulo final.

## 📂 Tarefas

| Tarefa | Arquivo de partida | O que fazer |
| :-: | :-- | :-- |
| 1️⃣ Cancelas | `tarefa1_teste_servo.py` | Mover os dois servos |
| 2️⃣ Presença | `tarefa2_teste_distancia.py` | Ler a distância do sensor |
| 3️⃣ Guarita manual | `tarefa3_manual_esqueleto.py` e `tarefa3_teste_botao.py` | Ler o potenciômetro e o botão |
| 4️⃣ Sinalização | `tarefa4_teste_sinais.py` | Acender o LED e tocar o buzzer |
| 5️⃣ Ambiente | `tarefa5_teste_dht11.py` | Ler temperatura e umidade |
| 6️⃣ Lógica | `tarefa6_main_esqueleto.py` | Juntar tudo no `main.py` |
| 7️⃣ Backend | `tarefa7_server.js` | Servidor com a API e o banco |
| 8️⃣ Frontend | `tarefa8_public_index.html` | Painel que mostra os números |

Também tem `pinos.py` (os pinos da placa em um lugar só) e `estacionamento.service` (para rodar o `main.py` em segundo plano).

## ▶️ Como usar

Copie o arquivo da sua tarefa para a Raspberry e rode-o. Os `TODO` dentro dos esqueletos indicam o que falta fazer.

> ⚠️ Estes são os **pontos de partida**. O sistema final, em `codigo/sistema/`, evoluiu a partir deles (por exemplo, o LED passou a usar PWM do RPi.GPIO e o DHT11 passou a usar `libgpiod`). Quando tiver dúvida, compare com o código final.
