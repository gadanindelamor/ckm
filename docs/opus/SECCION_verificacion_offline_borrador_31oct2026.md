# Sección nueva para el paper — la verificación del instrumento sin vivo (borrador para incorporar) — 31 oct 2026 (Opus 5.5)

> **Qué es** (delamor, 31 oct): *"le falta al paper una sección entera dedicada a los tests NO en vivo… los que realmente verifican y varían valores de variables. Todo el set, la suite de tests, con los drivers también… no generan REGs y demuestran la rigurosidad del testeo y los resultados correctos… IAP tiene su espacio, y como tal no va a hablar del instrumento, ni es reproducible. Luego de esa sección o dentro de ella, también van Findings y las verificaciones… hacelo aparte, luego lo incorporamos."*
>
> **Dónde iría:** como sección propia, antes de la serie IAP (§6), porque es reproducible y la serie IAP no; o como §5.4. Lo decide delamor al incorporarla a la v36 (se agrega, no reemplaza nada).
>
> **Cómo se armó, y su sesgo (declarado, por la regla del 31 oct):**
> - El inventario sale de los **nombres** de los 50 archivos de `tests/`, de la **primera línea de su docstring** y de **contar con grep** las funciones `test_`, los `parametrize` y los `xfail`. **No se leyeron las aserciones.** La columna "qué verifica" dice lo que dice el docstring, que puede divergir del código: es la falla que nombró delamor el 31 oct.
> - Los resultados de la suite (910 ítems, 903 pasan, 7 fallas esperadas, 0 fallas) son los que reportó Code el 29 oct (BANDEJA, 22:33 y 23:08 UTC). Opus no corrió nada.
> - Los drivers y lo que verifican salen de los reportes de Code de los textos 14, 20 y 21, tal como Code los reportó.
>
> **Pendiente, para Code (Codespace), si se quiere el respaldo exacto:**
> - `pytest --collect-only -q` en serie, para tener la lista de los 910 ítems y su reparto por grupo;
> - el detalle de los 7 xfail (cuáles son, uno por uno).
> Con eso, la tabla de §V.1 pasa de *"funciones `test_`"* a *"ítems recolectados"*.

---

## V. Verification of the Instrument (offline)

The live series of §6 test the instrument in a channel with language models: they are not reproducible, and they are reported as observations. This section reports the opposite kind of evidence. It is deterministic, runs without network access or language models, and anyone with the repository can re-run it. It has two parts: the test suite, which fixes what each component must do and fails when it does not, and the verification drivers, which measure properties of the instrument against exact references.

### V.1 The test suite

The suite lives in `tests/` and runs serially (`tests/run_tests.sh`). It does not write in the repository's state directory (`tests/conftest.py`). Last full run (29 Oct 2026, twice, at the start and at the end of a session): **910 items collected, 903 passed, 7 expected failures, 0 failures**. The 910 items come from 812 test functions in 50 files; 33 of the functions are parametrized over several values. Three parametrized tests use the W of the last live run when it is present, so the number of collected items can vary by three (910 before attempt 5, 913 after it).

| part of the instrument | files | test functions | what the tests verify (from their headers) |
|---|---:|---:|---|
| landscape and estimator (`landscape_engine`) | 6 | 62 | orbits by phase (`pares_por_orbita`); the distance to the basin frontier d(σ); N_eff and frontier logic; the presence theorem (no negative W, so 0 frustrated triangles and T(W) = 0, with presence alone); node selection against relaxation; a check that orientability is not signed balance |
| calibration (`calibrate`) | 4 | 34 | the mechanism and its three states; the reuse of N_eff at λ = 0; the origin W calibrated and registered; the threshold that COCO receives |
| COCO | 5 | 64 | COCO itself; its rebirth with each cycle; its own `Δ_r_compresiones`; that the corpus service no longer owns it; that no device receives a β |
| Monitor and rebuild | 6 | 125 | the Monitor services; that Monitor opens the cycles; invalidation of Δ_r; the rebuild criteria and their connection; that rebuild consults the W version; absence and orbit in the panel |
| configuration and sampling (`CKMlandscapeConfig`) | 3 | 57 | the configuration and its cycles; one place for n_runs and seed for the three cases; the configuration in each run |
| text producer (extraction of W) | 8 | 88 | the analyzer reproduces scikit-learn bit for bit; the node extractor and its corrections; the declared extraction as executable data; a failed extraction does not erase; accumulate and evaluate take one branch; the two measurements on the repository corpora |
| CKM TRUST rule | 3 | 64 | the rule as a single engine; the local criterion and node selection as instances of it |
| trace (signature, versions, judge) | 3 | 25 | Firma_CKM; W versions with the corpus service; the Gatekeeper's θ_W |
| IAP channel and devices | 12 | 293 | the channel clock; the continuous ODA loop; the local criterion of devices; the design of series 2 checked without network; state directories and persistence; the providers registry; the fixes measured in live runs; empty generations; that no prompt reaches a model in Spanish |
| **total** | **50** | **812** | |

**Values are varied, not fixed.** Parametrized tests run the same assertion over several inputs: the analyzer against scikit-learn over several texts and settings (4 parametrizations); node selection against relaxation (3); the presence theorem (3); the reuse of N_eff at λ = 0 over synthetic W of N = 12 and N = 20, plus the W of the last live run when present (3); the Gatekeeper's θ_W (4).

**Known defects are kept visible.** The 7 expected failures are strict (`xfail(strict=True)`): if the behavior they describe changes, the suite fails. They come from two files, and the reason is written in the marker:
- **A nested bigram drags its unigram:** if both are nodes, they co-occur in every text that contains the bigram, so W is positive by construction, not by the field.
- **An empty corpus loses keys:** with an empty or blank corpus, `accumulate` returns 3 keys instead of 5, so whoever reads the frontier record cannot tell "no corpus" from "no tie".
- **Orientability is not signed balance:** `check_orientability` does not receive W and filters W > θ, so the sign never reaches it; it measures simplicial orientability.
A fourth defect of the same file, silent truncation of non-NFC text, was fixed on 13 Oct, and its expected failure became a test that asserts the fix.

### V.2 Verification drivers

The drivers in `experiments/` measure properties of the instrument against exact references, with internal controls declared in each script.

| driver | what it verifies | reference or control |
|---|---|---|
| exact enumeration (§4.3.1) | N_eff against the exact basin volumes of all 2^20 states, three N = 20 corpora | full enumeration, uniform measure |
| `piso_del_colapso.py` | the N_eff of the collapsed landscape, F(N), in closed form | enumeration of all 2^N states, N up to 21, no discrepancy |
| `simpson_en_las_curvas.py` | the plug-in bias of N_eff and the interval of the margin | Simpson's unbiased estimator and the delta method |
| `margen_exacto_14W.py` | the exact margin of the 14 calibrated W; the float64 tie | enumeration checked against `relax_orbit`, 500 of 500 states per W; W rebuilt and checked by its hash |
| `simetria_neff_dos.py` | the bound N_eff ≥ 1/(κ² + (1 − κ)²/2) and the parity of n_runs | all W with entries in {−1, 0, +1} for N = 2–5; the sharper form against F(N), to 10⁻¹⁵; the simulated distribution against the instrument's real sampling at N = 20 and 21 |
| `torsion_lo_que_queda_afuera.py` | which pairs enter Δ_r over an orbit | the collapsed landscape with even N (4–20); the 14 W by class of orbit |
| `driver_cpe_rango_neff.py` and `cpe_0e042ac_vs_head.py` | the stability of N_eff under seed and extraction parameters | re-run unchanged at the commit of the original run, and at the current extraction |

### V.3 Findings of the verification

What these verifications establish, each in the section where the paper uses it:
- **The estimator.** N_eff errs by at most 0.6% against exact enumeration, where orbit counts err by up to 28% (§4.3.1).
- **The collapsed landscape.** Its N_eff has a closed form, F(N), exact up to N = 21 (§6.4).
- **A lower bound.** Under the sampling measure, orbits come in conjugate pairs of equal mass, so N_eff ≥ 2 when the self-conjugate mass κ ≤ 2/3. The bound is tight and its condition is exact: 769 W with N_eff < 2 were found, all with κ > 2/3 (§4.3.1).
- **Parity.** With odd N, the plug-in for the collapsed landscape reaches 2 only with even n_runs (§4.3.1).
- **Calibration, exactly.** None of the 14 W calibrated in attempts 2–4 separates by its exact margin. Of the two W of attempt 5, one does: +0.4915 exact, +0.506 sampled (§6.4).
- **The tie in float64.** In 13–22% of the states of those W, an exact h = 0 is computed as ±10⁻¹⁷. No sign of a margin changes, and no orbit of period greater than 2 appears (§4.1.2).
- **Stability.** The figures of §4.3.2 are reproduced at the commit of their original run, and differ with the current extraction (§4.3.2).
- **Torsion.** In a self-conjugate orbit, torsion is exactly the set of pairs with both nodes on the same side. In the live runs it was 0 (§4.2.2).
- **Presence alone.** No negative weight, so 0 frustrated triangles and T(W) = 0: a theorem, with its test (`tests/test_teorema_presencia.py`).
- **The analyzer** reproduces scikit-learn bit for bit (`tests/test_analizador_S0.py`).

### V.4 Limits
- A test verifies what its author encoded. The headers summarized in V.1 can diverge from the code they describe, and the summary here was made from those headers, not from the assertions.
- The suite was run in one environment, a GitHub Codespace.
- The tests of the IAP case folder (`iap_chatroom/tests/`, 34 files) are classified as process, not as the suite, and are not counted here.
- Exact references exist only up to N ≈ 21. Above that, every sampled quantity lacks an exact check (§4.3.1).
