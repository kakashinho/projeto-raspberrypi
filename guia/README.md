# 📘 Guia da equipe

Passo a passo de cada uma das oito tarefas do projeto, com figuras, códigos de partida e a lista do que cada pessoa entrega.

## 📂 O que tem aqui

| Arquivo | Para que serve |
| :-- | :-- |
| `index.html` | O guia em página web. Abra no navegador |
| `guia_equipe.pdf` | A mesma versão em PDF, para imprimir ou enviar |
| `gerador/` | Código que monta o `index.html` a partir do texto e dos desenhos |

## 🌐 Como ler

Abra o `index.html` no navegador. No topo há a lista das tarefas; clique numa para ver o passo a passo.

## 🔁 Gerar de novo o `index.html`

Só precisa de Python 3. Rode na pasta `guia/gerador`:

```bash
python3 montar.py
```

O script escreve o `index.html` na pasta `guia/`. O texto das tarefas fica em `gerador/pagina.html`, e os trechos de código, em `gerador/trechos/`.

## 🖨️ Gerar o PDF

Abra o `index.html` no Chrome ou no Edge, use **Imprimir** e escolha **Salvar como PDF**. Antes de imprimir, os blocos recolhidos precisam estar abertos, senão o PDF sai com partes escondidas.
