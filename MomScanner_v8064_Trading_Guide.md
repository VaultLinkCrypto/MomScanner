# MomScanner v8.06.4 — Trading Guide & README

**Updated:** 2026-05-26  
**GitHub:** vaultlinkcrypto/MomScanner  
**Deployment:** Single `index.html` → GitHub Pages  
**Includes:** v8.06.1 (CA v2), v8.06.2 (Gate Removal), v8.06.3 (VWAP Velocity), v8.06.4 (OHLC Fix + Exclude)

---

## What's New in v8.06.4

### OHLC Accuracy Fix

On 5/26, 62.7% of all OHLC bars were completely flat (Open = High = Low = Close). With 199 tickers polled in chunks of 40 at a computed refresh interval of 10 seconds (Math.ceil(199/20)), most tickers received only 1 `d.last` snapshot per minute — producing a point-in-time reading instead of a true candle.

Three improvements now produce realistic OHLC bars even with 1-2 ticks per minute:

**1. Bid/Ask Range Estimation** — Every poll, the L1 bid and ask are used to widen the bar's range. At any moment, the true last-trade price sits between bid and ask. So bid becomes a valid low estimate and ask a valid high estimate. This is applied on every tick, including the bar's first tick, ensuring that even single-tick bars have a realistic range instead of a flat line.

**2. Feed Session High/Low Delta Tracking** — Tradier and Schwab return the session-high and session-low with every quote. If the session-high increased between two consecutive polls, a new intraday high was printed between those polls — even though `d.last` might not have reflected the extreme. The new session-high is captured as the bar's high. Same logic for session-low decreases.

**3. First-Tick Range** — Bid/ask are applied immediately when the bar opens, so the opening bar already has a high (ask) and low (bid) instead of four identical values.

### Why the Transition Log Shows Alerts Before the OHLC Log

The transition log records the exact moment a state change occurs (e.g., `10:28:12` when SMCI promoted to bull). The OHLC log records state at the moment the bar seals (start of the next minute). If SMCI promoted at 10:28:12 and demoted at 10:28:42, the bar sealing at 10:29:00 records `TrendState=watch` because that's the state at seal time. The 30-second promotion was real but too short to appear in minute-resolution OHLC data. This is expected behavior — the transition log is the authoritative record for promotion/demotion events, while the OHLC log captures minute-level snapshots for candle analysis.

### Ticker Exclude List

New input field below the ticker bar. Type ticker symbols to exclude (e.g., SOXL, TQQQ, ARKK, UVXY) and click Save. Excluded tickers are hidden from the candidates table and skipped when adding new tickers via Add to Scan. The list persists in localStorage across sessions.

Excluded tickers still receive data in the background — no mid-session removal, which protects OHLC logging integrity. They simply don't appear in the visible table, reducing visual noise from leveraged ETFs and other non-interest tickers.

---

## What's New in v8.06.3: VWAP Velocity Monitor

A new VWAP extension velocity tracker that classifies each ticker into one of three states — displayed as color-coded badges in the VWAP column. Backtested across 5 trading days (5/18–5/22), 400K bars, 193 unique tickers.

### The Three VWAP States

**↗ EXTENDING (blue badge)**

VWAP velocity > +0.03%/min while price is above VWAP. Price is actively pulling away from VWAP upward. Momentum is live — this is a valid entry zone if you're not already overextended. Backtested: 55.4% WR at 5 minutes.

**R REVERTING (green badge) — Best Entry Signal**

Price velocity is positive (current tick rising) BUT VWAP velocity is negative (< -0.03%/min, extension shrinking), and price is still above VWAP. This is the pullback buy: price pushed, pulled back toward VWAP, and is now bouncing. Backtested: 63.3% WR at 5 minutes, 63.3% at 10 minutes, PF 2.30. This was the single strongest entry signal found across all features tested. Over 5 days, REVERT entries produced 1,340 trades with +0.136% avg return, PF 1.80, and +409.8% total gross gains.

**! OVEREXTENDED (red badge) — Caution**

VWAP extension exceeds 1.5% (the P90 threshold across all observations). Mean reversion risk is high. At TrendScore 85+, the OVEREXTENDED state produced only a 30.2% WR — the worst bucket in the entire dataset. Don't chase. Wait for the pullback (REVERT badge to appear).

### How VWAP Velocity Is Computed

```
VWAP Extension = (Close - VWAP) / VWAP × 100    →  how far from VWAP in %
VWAP Velocity  = (Extension_now - Extension_3min_ago) / 3   →  %pts/min
```

The 3-minute lookback smooths out single-bar noise while staying responsive to real directional changes. This runs on the same VWAP data already computed from price and volume snapshots every poll cycle.

### Reading the VWAP Column

The VWAP column now shows two elements:

1. **Extension percentage** (existing): `+0.45%` means price is 0.45% above VWAP
2. **State badge** (new in v8.06.3): appears to the right of the extension

| Display | Meaning |
|---------|---------|
| `+0.45%` | Above VWAP, no active velocity state (neutral) |
| `+0.32% ↗` | Above VWAP + EXTENDING (blue — momentum live) |
| `+0.58% R` | Above VWAP + REVERTING (green — pullback buy, best entry) |
| `+1.72% !` | Above VWAP + OVEREXTENDED (red — don't chase) |

Hover over any badge for a tooltip with the exact VWAP velocity in %/min.

---

## Combining VWAP State with CA% and TrendScore

### The Ideal Entry (REVERT + CA Confirmed)

The strongest entries combine all three systems:

- TrendScore ≥ 65 (confirmed candidate)
- CA% ≥ 72% (C badge — structural candle confirmation)
- VWAP State = REVERTING (R badge — pullback buy)
- Price above VWAP

This combination captures entries where the trend is confirmed (TrendScore), the candle structure is building (CA v2), and you're buying the pullback rather than chasing (VWAP REVERT). The REVERT badge means price just made a push, pulled back toward VWAP, and the current tick is rising — you're entering at the moment of the bounce.

### The DRIFT Trade Setup

For the subtle "3% in 3 hours" moves:

- TrendScore 65–75 (moderate but sustained)
- CA% 55–72% (E badge — structure building slowly)
- VWAP State = EXTENDING or REVERTING (↗ or R)
- VWAP extension < 1.0%
- Low velocity (< 10 bps/min)

DRIFT moves show repeated EXTENDING → REVERTING cycles as price climbs in small steps. Each REVERT is a potential add-on entry.

### The Aggressive Breakout Setup

- TrendScore 75+ or BreakoutScore spike
- CA% ≥ 72% with Aggr Candle 2/2
- VWAP State = EXTENDING (↗)
- Velocity spike alert firing
- VWAP extension 0.3%–1.0% (strong but not overextended)

### When NOT to Enter

- VWAP State = OVEREXTENDED (!) at any TrendScore — wait for pullback
- EXTENDING + extension > 1.5% — you're late
- REVERTING but TrendScore < 55 — the trend may be breaking

---

## What Changed in v8.06.2: Options Gate Removal

Removed `spreadOK` (≤5%) and `oiOK` (≥1000) as hard promotion gates. On 5/22, these blocked 196 of 199 tickers from promoting — including SMCI (+6.34%, TS 85.6), DELL (+16.78%), HPQ (+15.26%), NVTS (+19.98%). Root cause: 0DTE theta decay widened ATM spreads past the 5% gate, permanently locking out tickers. Options spread and OI are now display-only indicators shown as colored pills.

### Spread Pills

| Color | Spread | Meaning |
|-------|--------|---------|
| Green | ≤ 10% | Standard trade execution |
| Yellow | 10–25% | Factor into sizing |
| Red | > 25% | Check bid/ask before entering |

---

## What Changed in v8.06.1: Candle Accumulator v2

Complete redesign of the CA scoring engine. 7 structural criteria totaling 18 max points, scored per-window (not per-bar). PF 1.63 at 55% threshold, PF 2.35 at 80%.

### The 7 Criteria

| # | Criterion | Max | What It Measures |
|---|-----------|-----|-----------------|
| 1 | Higher Close Streak | 4 | Consecutive bars closing higher (strongest single predictor; streak 4 = 56% WR) |
| 2 | HH+HL Structure | 4 | Bars with higher high AND (higher low or higher close) |
| 3 | Window Net Move | 3 | Total % move across 5-bar window (tiered: >0.02/0.10/0.20%) |
| 4 | Above VWAP | 1 | Binary confirmation |
| 5 | Defensive Structure | 2 | No lower lows (0 violations = 2pts, 1 = 1pt) |
| 6 | Close in Upper Half | 2 | Bars closing above midpoint of range |
| 7 | Aggressive Green Candle | 2 | Bars with body ≥ 0.15% of price |

### Signal Levels

| Signal | Threshold | Backtested |
|--------|-----------|------------|
| Early (E, yellow) | CA% ≥ 55% | PF 1.63, 46.4% WR |
| Confirmed (C, green) | CA% ≥ 72% | PF 1.72, 52.0% WR |
| High Conviction | CA% ≥ 80% | PF 2.35, 55.4% WR |

Hover over any CA% value to see the per-criterion breakdown: `HC-Streak:3/4 · HH+HL:3/4 · Net:2/3 · VWAP:1/1 · Def:2/2 · Upper:2/2 · Aggr:1/2`

---

## Settings Reference

All configurable in Settings panel.

### v8.06.3 VWAP Velocity Monitor

| Setting | Default | Range | Notes |
|---------|---------|-------|-------|
| Velocity Lookback | 3 min | 1–10 | How far back to measure extension change |
| Extending Threshold | 0.03 %/min | 0.01–0.20 | VWAP vel above this = EXTENDING badge |
| Reverting Threshold | -0.03 %/min | -0.01 to -0.20 | VWAP vel below this (with price up) = REVERTING badge |
| Overextended Limit | 1.50% | 0.50–3.00 | Extension above this = OVEREXTENDED warning |

### v8.06.1 Candle Accumulator v2

| Setting | Default | Range | Notes |
|---------|---------|-------|-------|
| Confirmed Window | 5 bars | 3–10 | Bars for C signal |
| Early Alert Window | 3 bars | 2–5 | Bars for E signal |
| Confirmed Threshold | 72% | 50–95% | Min CA% for confirmed |
| Early Threshold | 55% | 30–80% | Min CA% for early alert |
| Aggressive Candle Body | 0.15% | 0.05–0.50% | Min body for aggressive candle |
| VWAP Soft Gate | ON | ON/OFF | ON = VWAP in CA scoring. OFF = legacy hard gate |

### Tuning Tips

- **Missing DRIFT entries?** Lower Aggressive Candle Body to 0.10% and Reverting Threshold to -0.02.
- **Too many false entries?** Raise Confirmed Threshold to 80% and Reverting Threshold to -0.05.
- **Volatile small-caps (FCEL, CLSK, MARA)?** Raise Aggressive Candle Body to 0.25% and Overextended Limit to 2.0%.
- **Want only REVERT entries?** Watch for the green R badge before entering. Ignore entries where only ↗ appears.

---

## OHLC Export Columns (v8.06.3)

The per-minute OHLC CSV now includes 28 columns:

| Column | Type | New? | Description |
|--------|------|------|-------------|
| Timestamp | ISO | | Bar timestamp |
| Ticker | str | | Symbol |
| Open/High/Low/Close | float | | OHLC prices |
| Volume | int | | Cumulative session volume |
| VolumeDelta | int | | Volume change this bar |
| VWAP | float | | Session VWAP |
| PctChg | float | | Day % change |
| IntradayPctChg | float | | Intraday % change |
| Bid/Ask | float | | L1 quotes |
| SpreadPct | float | | Bid-ask spread as % |
| RelVol | float | | Relative volume |
| PriceVelocity | float | | Price vel in ¢/min |
| TrendScore | float | | L1 trend score |
| BreakoutScore | float | | L2 breakout score |
| PressureScore | float | | L3 pressure score |
| TrendState | str | | bull/bear/watch |
| BreakoutState | str | | bull/bear/watch |
| PressureState | str | | bull/bear/watch |
| MomentumType | str | | drift/thrust/reversal |
| Regime | str | | Market regime |
| TickCount | int | | Ticks in this bar |
| **VWAPExt** | **float** | **✓** | **VWAP extension (% from VWAP)** |
| **VWAPVel** | **float** | **✓** | **VWAP velocity (%pts/min)** |
| **VWAPState** | **str** | **✓** | **extending/reverting/overext/neutral** |

---

## Backtest Results Summary

### CA v2 Scoring (3 days: 5/18–5/20)

| System | Trades | WR% | PF |
|--------|--------|-----|-----|
| Old Binary CA ≥73% | 424 | 38.7% | 0.95 |
| CA v2 ≥55% (Early) | 476 | 46.4% | 1.63 |
| CA v2 ≥72% (Confirmed) | 229 | 48.5% | 1.68 |
| CA v2 ≥80% (High Conviction) | 101 | 55.4% | 2.35 |

### VWAP REVERT Signal (5 days: 5/18–5/22)

| Day | Trades | WR% | Avg P&L | PF |
|-----|--------|-----|---------|-----|
| 5/18 | 244 | 38.9% | +0.033% | 1.17 |
| 5/19 | 201 | 42.8% | +0.090% | 1.54 |
| 5/20 | 350 | 54.6% | +0.240% | 2.80 |
| 5/21 | 301 | 44.2% | +0.151% | 1.87 |
| 5/22 | 244 | 36.9% | +0.108% | 1.55 |
| **Total** | **1,340** | **44.4%** | **+0.136%** | **1.80** |

**Top tickers by net P&L (REVERT signal, 5 days):** ARM +11.80%, APLD +9.57%, DELL +8.28%, SWKS +8.14%, GTLB +7.21%, CIFR +6.16%, DAL +5.93%, QCOM +5.49%, IBM +5.18%, F +5.13%.

---

## Architecture Notes

- **Single-file app:** Everything in `index.html`, no build step.
- **VWAP velocity data flow:** `updateVWAP(d)` → `updateVWAPVelocity(d)` → renders in VWAP cell → logged in OHLC export.
- **Ring buffer:** `d._vwapExtHistory` holds last 5 minutes of extension readings for velocity calculation.
- **State stored per-ticker:** `d._vwapExt`, `d._vwapVel`, `d._vwapAccel`, `d._vwapState`, `d._vwapExtPeak`.
- **Session protection:** Never close MomScanner mid-session. All buffers are in-memory only.
- **Settings persistence:** VWAP velocity settings stored in `ms_v805_settings` localStorage key alongside CA and trade management settings.
