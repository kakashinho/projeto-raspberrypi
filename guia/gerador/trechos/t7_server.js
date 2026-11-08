// npm init -y && npm install express better-sqlite3
const express = require('express');
const Database = require('better-sqlite3');

const MAX_VAGAS = 6;                   // fácil de mudar

const db = new Database('estacionamento.db');
db.exec(`
  CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
  )`);

const app = express();
app.use(express.json());
app.use(express.static('public'));     // a página da tarefa 8 fica em public/

const conta = (tipo, filtro = '') =>
  db.prepare(`SELECT COUNT(*) AS n FROM eventos WHERE tipo = ? ${filtro}`).get(tipo).n;
const dentro = () => Math.max(0, conta('entrada') - conta('saida'));

app.post('/api/eventos', (req, res) => {
  const { tipo } = req.body;
  if (!['entrada', 'saida'].includes(tipo)) {
    return res.status(400).json({ erro: 'tipo inválido' });
  }
  if (tipo === 'saida' && dentro() === 0) {
    return res.status(409).json({ erro: 'ninguém dentro' });   // evita "dentro" negativo
  }
  db.prepare('INSERT INTO eventos (tipo) VALUES (?)').run(tipo);
  res.status(201).json({ ok: true });
});

app.get('/api/resumo', (req, res) => {
  const semana = "AND criado_em >= datetime('now', 'localtime', '-7 days')";
  res.json({
    entradas: conta('entrada', semana),
    saidas: conta('saida', semana),
    dentro: dentro(),
    vagas: MAX_VAGAS,
  });
});

app.listen(3000, '0.0.0.0', () => console.log('Servidor em http://0.0.0.0:3000'));
