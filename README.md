
# PCp Verification Scripts

Computational certificates for the paper:

**“Unconditional positivity of PCp(X) via a mod-3 gate and a single BV penalty”**  
by Masayuki Aoki

This repository contains Colab-ready / local Python scripts that produce **rigorous** lower bounds for
`PCp(X)` with **safe rounding** and **exact** local factors, plus an exact small-X enumerator.
The outputs are hashed (SHA-256) to enable fully reproducible verification.

---

## Repository layout

```text
pcp-verification/
├── colab/
│   ├── colab_conservative.py   # A=3, C_BV^tot=5.0; certifies X ∈ [80k,90k]
│   ├── colab_optimized.py      # A=3, C_BV^tot=3.0; certifies X ∈ [50k,60k]
│   └── colab_exact_small_X.py  # exact PCp(X) up to 80,000 (FFT enumerator)
├── outputs/
│   ├── conservative/           # logs (.txt/.json) + per-file .sha256
│   ├── optimized/              # logs (.txt/.json) + per-file .sha256
│   └── zeros/                  # logs (.txt/.json) + per-file .sha256
├── SHA256SUMS                  # consolidated hashes for all outputs
└── README.md
````

> **Python**: scripts require **Python 3.11+** (uses `Decimal.ln`).
> **Dependencies**: only the small-X enumerator needs `numpy`. Everything else uses the standard library.

---

## Quick start

### Option A — Google Colab (recommended)

1. Open a new Colab notebook and upload the desired script from `colab/`.
2. Run the cell (no extra pip installs for conservative/optimized scripts).
3. The script prints the certification log **and** writes signed outputs into `outputs/...`
   (you can download those files and commit them to GitHub).

### Option B — Local (Python 3.11+)

```bash
python3 --version      # must be 3.11+
python3 colab/colab_conservative.py
python3 colab/colab_optimized.py
python3 -m pip install numpy && python3 colab/colab_exact_small_X.py
```

---

## What the scripts do

### 1) Conservative certificate (`colab_conservative.py`)

* Parameters: **A=3**, **C_BV^tot=5.0**.
* Computes a sanity breakdown at **X = 100,000** (main term, BV base, scale, BV total, r5).
* Certifies **every even X in [80,000, 90,000]** with `PCp(X) > 0`.
* Spot checks multiple larger values.
* Writes:

  * `outputs/conservative/<timestamp>.txt`
  * `outputs/conservative/<timestamp>.json`
  * and per-file `.sha256`

**Expected excerpt (sanity at X=100,000):**

```
[V(z)]     = 0.12709215626844851509333434628867019830175746359213256045768977507194275635758110
[f(3)]     = 0.8230302166065229129458236
[PCp_lower]= 92.35029396934088685910344563770017148916199830827403343260026727252098387721805
```

### 2) Optimized sensitivity (`colab_optimized.py`)

* Parameters: **A=3**, **C_BV^tot=3.0**.
* Certifies **every even X in [50,000, 60,000]**; spot checks beyond.
* Writes logs under `outputs/optimized/`.

**Expected excerpt (sanity at X=50,000):**

```
PCp_lower(50,000) = 126.96555878...  [OK-cert]
```

### 3) Exact small-X enumerator (`colab_exact_small_X.py`)

* Computes `PCp(X)` exactly via FFT convolution for **X ≤ 80,000**.
* Expected zero-set:
  `Zero-set up to 80,000: [6, 8, 10, 36, 210]`
* Writes logs under `outputs/zeros/`.

> The FFT uses `numpy.fft` in double precision and rounds to nearest.
> For this range the counts are small, and the rounding is exact in practice.
> (This enumerator is **auxiliary** — the main certificates are fully rigorous via `Decimal`.)

---

## Rounding discipline (rigor)

* **Main term**: computed with `Decimal` using **ROUND_FLOOR** (downwards).
* **BV penalty**: computed with `Decimal` using **ROUND_CEILING** (upwards) and aggregated as
  `BV_tot = (1 + V(z)·f(3)) · BV_base`.
* **Local factor** `V(z)`: exact rational product over primes **ℓ ≥ 3** up to `z = floor(sqrt(X))+1`.
  Therefore the printed `PCp_lower` is a **formal lower bound**.

---

## Checksums

Each output has a per-file `.sha256`, and the repo root contains a consolidated **`SHA256SUMS`** for all
`outputs/**/*.txt` and `outputs/**/*.json`:

```bash
# verify all outputs at once
sha256sum -c SHA256SUMS
```

To rebuild `SHA256SUMS` after generating new outputs:

```bash
# Linux/macOS
find outputs -type f \( -name '*.txt' -o -name '*.json' \) -print0 \
| sort -z | xargs -0 sha256sum > SHA256SUMS
```

```powershell
# Windows PowerShell
Get-ChildItem outputs -Recurse -Include *.txt,*.json |
  Sort-Object FullName |
  Get-FileHash -Algorithm SHA256 |
  ForEach-Object {
    "$($_.Hash.ToLower())  $((Resolve-Path $_.Path -Relative) -replace '\\','/')"
  } | Out-File -Encoding ascii SHA256SUMS
```

---

## Expected thresholds (summary)

* **Conservative (A=3, C_BV^tot=5.0)**: certifies all even **X ≥ 80,000** (finite window [80k,90k] checked).
* **Optimized (A=3, C_BV^tot=3.0)**: certifies all even **X ≥ 50,000** (finite window [50k,60k] checked).

---

## Reproducibility checklist

* Python 3.11+
* No third-party deps for conservative/optimized; `numpy` for the exact small-X enumerator
* Run scripts → logs saved under `outputs/...` with `.sha256`
* Verify with `sha256sum -c SHA256SUMS`

---

## Citation

If you use these scripts, please cite the associated paper (preprint/DOI here when available).

```
Aoki, M. Unconditional positivity of PCp(X) via a mod-3 gate and a single BV penalty, 2025.
```

```
