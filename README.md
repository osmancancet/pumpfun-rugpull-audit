# Seen creators, settled labels: a leakage-aware audit of early rug-pull prediction for Solana pump.fun memecoins

Code, per-run results, figures and manuscript source for the paper by Osman Can Çetlenbik
(Manisa Celal Bayar University).

| Folder | Contents |
|---|---|
| `code/` | Pipeline (`run_all.sh`), unit and synthetic tests, configuration; see `code/README.md` for setup and run order |
| `results/` | Outputs of the full run used in the paper; `results/key_numbers.md` lists every number the manuscript cites with its source file |
| `figures/` | Figures 1–5 (PNG and PDF) |
| `manuscript/` | Manuscript source (Markdown) and highlights |

Data: loopholetape, *pump.fun launches with outcomes* (2026), Hugging Face, CC BY 4.0,
revision `022649eb0504005be0ae34833d224341777355be`. The data are not redistributed here; `code/README.md` gives the
download command. A full run takes about 40 minutes on a laptop (Apple M-series, 8 cores).

Licence: MIT (code). The dataset keeps its own CC BY 4.0 licence.
