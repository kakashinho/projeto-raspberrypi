# 🔌 Hardware: placa de interface

Projeto da placa que encaixa no Raspberry Pi e reúne os sensores e atuadores do estacionamento. Feita no **KiCad 10**.

## 📂 O que tem aqui

| Arquivo | Para que serve |
| :-- | :-- |
| `placa_interface.kicad_pro` e `.kicad_pcb` | Projeto da placa no KiCad (abra o `.kicad_pro`) |
| `montagem_placa_interface.pdf` | Lado dos componentes, lado do cobre, etiqueta e lista de montagem |
| `trilhas_tamanho_real_A4.pdf` | Trilhas em tamanho real (1:1), para conferir sobre a placa |
| `etiquetas_A_B_pimaco6282.pdf` | Etiquetas para a folha Pimaco 6282 |
| `etiquetas_A_B_folha_cheia.pdf` | Mesmas etiquetas, em folha cheia |
| `etiquetas_teste_papel_comum.pdf` | Teste de impressão em papel comum, antes de gastar a folha |
| `previas/` | Imagens de pré-visualização (montagem, trilhas, etiquetas) |
| `gerador/` | Scripts que geram os arquivos acima |

## 🧭 Pinos principais

As posições dos pinos estão em `gerador/design.py`, que é a **fonte da verdade** da placa. Os pinos usados no software estão em [`codigo/sistema/pinos.py`](../codigo/sistema/pinos.py).

## 🔁 Gerar de novo

Com o KiCad 10 instalado (e o PyMuPDF para os PDFs), rode na pasta `hardware/gerador`:

```bash
"C:\Program Files\KiCad\10.0\bin\python.exe" gerar_placa.py ../
python exportar.py ../
```

A imagem 3D da placa pode ser renderizada com o próprio KiCad, por exemplo:

```bash
kicad-cli pcb render -o previas/placa_3d.png --side top --rotate "-45,0,30" --background transparent placa_interface.kicad_pcb
```

## 🧾 Lista de materiais

A lista completa de componentes está em [`docs/lista_de_materiais.csv`](../docs/lista_de_materiais.csv).
