

const path = require('path');
const express = require('express');
const Database = require('better-sqlite3');

const MAX_VAGAS = 7;
const PORTA = Number(process.env.PORT) || 3000;
const ARQ_BANCO = process.env.DB_ARQ || path.join(__dirname, 'estacionamento.db');
const VALIDADE_COMANDO_S = 30;
const CONTROLADOR_ONLINE_S = 15;

const db = new Database(ARQ_BANCO);
db.pragma('journal_mode = WAL');
db.exec(`
  CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
  );
  CREATE TABLE IF NOT EXISTS ambiente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura REAL NOT NULL,
    umidade REAL NOT NULL,
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
  );
  CREATE TABLE IF NOT EXISTS comandos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alvo TEXT NOT NULL,
    acao TEXT NOT NULL,
    feito INTEGER NOT NULL DEFAULT 0,         -- 0 pendente, 1 entregue, 2 expirado
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
  );
`);

db.prepare('UPDATE comandos SET feito = 2 WHERE feito = 0').run();
db.prepare("DELETE FROM ambiente WHERE criado_em < datetime('now', 'localtime', '-30 days')").run();

let ultimoSinalControlador = 0;
const controladorOnline = () => Date.now() - ultimoSinalControlador < CONTROLADOR_ONLINE_S * 1000;

const app = express();
app.use(express.json());

app.get('/vendor/chart.umd.js', (req, res) =>
  res.sendFile(path.join(__dirname, 'node_modules', 'chart.js', 'dist', 'chart.umd.js')));
app.use(express.static(path.join(__dirname, 'public')));


app.use('/api/comandos', (req, res, next) => {
  if (req.method === 'POST') {
    console.log(new Date().toLocaleTimeString('pt-BR'), 'POST /api/comandos', JSON.stringify(req.body), 'de', req.ip);
  }
  next();
});

const conta = (tipo) =>
  db.prepare('SELECT COUNT(*) AS n FROM eventos WHERE tipo = ?').get(tipo).n;
const dentro = () => Math.max(0, conta('entrada') - conta('saida'));

app.post('/api/eventos', (req, res) => {
  const { tipo } = req.body || {};
  if (!['entrada', 'saida'].includes(tipo)) {
    return res.status(400).json({ erro: 'tipo inválido (use entrada ou saida)' });
  }
  if (tipo === 'saida' && dentro() === 0) {
    return res.status(409).json({ erro: 'ninguém dentro' });
  }
  db.prepare('INSERT INTO eventos (tipo) VALUES (?)').run(tipo);
  res.status(201).json({ ok: true });
});

app.get('/api/resumo', (req, res) => {

  const dias = [];
  for (let i = 6; i >= 0; i--) {
    dias.push(db.prepare("SELECT date('now', 'localtime', ?) AS d").get(`-${i} days`).d);
  }
  const linhas = db.prepare(
    'SELECT date(criado_em) AS dia, tipo, COUNT(*) AS n FROM eventos WHERE date(criado_em) >= ? GROUP BY dia, tipo'
  ).all(dias[0]);
  const por_dia = dias.map((dia) => ({
    dia,
    entradas: (linhas.find((l) => l.dia === dia && l.tipo === 'entrada') || {}).n || 0,
    saidas: (linhas.find((l) => l.dia === dia && l.tipo === 'saida') || {}).n || 0,
  }));
  res.json({
    entradas: por_dia.reduce((soma, d) => soma + d.entradas, 0),
    saidas: por_dia.reduce((soma, d) => soma + d.saidas, 0),
    dentro: dentro(),
    vagas: MAX_VAGAS,
    por_dia,
    controlador_online: controladorOnline(),
  });
});

app.post('/api/ambiente', (req, res) => {
  const { temperatura, umidade } = req.body || {};
  if (!Number.isFinite(temperatura) || !Number.isFinite(umidade)) {
    return res.status(400).json({ erro: 'temperatura e umidade precisam ser números' });
  }
  db.prepare('INSERT INTO ambiente (temperatura, umidade) VALUES (?, ?)').run(temperatura, umidade);
  res.status(201).json({ ok: true });
});

app.get('/api/ambiente/ultima', (req, res) => {
  const l = db.prepare(
    `SELECT temperatura, umidade, criado_em,
            strftime('%s', 'now', 'localtime') - strftime('%s', criado_em) AS ha_segundos
       FROM ambiente ORDER BY id DESC LIMIT 1`
  ).get();
  if (!l) return res.status(204).end();
  res.json(l);
});


app.post('/api/comandos', (req, res) => {
  const { alvo, acao } = req.body || {};
  if (alvo !== 'saida' || acao !== 'abrir') {
    return res.status(400).json({ erro: 'comando inválido (use alvo "saida" e acao "abrir")' });
  }
  if (!controladorOnline()) {
    return res.status(503).json({ erro: 'o controlador (main.py) não está rodando' });
  }
  if (dentro() === 0) {
    return res.status(409).json({ erro: 'não há carros dentro' });
  }
  if (db.prepare('SELECT 1 FROM comandos WHERE feito = 0').get()) {
    return res.status(200).json({ ok: true, repetido: true });
  }
  db.prepare('INSERT INTO comandos (alvo, acao) VALUES (?, ?)').run(alvo, acao);
  res.status(201).json({ ok: true });
});

app.get('/api/comandos/proximo', (req, res) => {
  ultimoSinalControlador = Date.now();
  db.prepare(
    `UPDATE comandos SET feito = 2 WHERE feito = 0
       AND criado_em < datetime('now', 'localtime', '-${VALIDADE_COMANDO_S} seconds')`
  ).run();
  const c = db.prepare('SELECT id, alvo, acao FROM comandos WHERE feito = 0 ORDER BY id LIMIT 1').get();
  if (!c) return res.status(204).end();
  db.prepare('UPDATE comandos SET feito = 1 WHERE id = ?').run(c.id);
  res.json(c);
});

app.post('/api/controlador/batimento', (req, res) => {
  ultimoSinalControlador = Date.now();
  res.status(204).end();
});


app.use((erro, req, res, next) => {
  if (erro.type === 'entity.parse.failed') return res.status(400).json({ erro: 'JSON inválido' });
  console.error(erro);
  res.status(500).json({ erro: 'erro interno' });
});

app.listen(PORTA, '0.0.0.0', () => console.log(`Servidor em http://0.0.0.0:${PORTA}`));
