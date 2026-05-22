# MomScanner v8.06.2 — Trading Guide & README

**Updated:** 2026-05-22  
**GitHub:** vaultlinkcrypto/MomScanner  
**Deployment:** Single `index.html` → GitHub Pages

---

## What Changed in v8.06.2

**Options spread and OI gates removed from the promotion pipeline.** On 5/22, the `spreadOK` (≤5%) and `oiOK` (≥1000) hard gates blocked 196 of 199 tickers from ever promoting — including the day's biggest movers: NVTS (+19.98%, TrendScore 82), DELL (+16.78%, TS 85), HPQ (+15.26%, TS 87), CRDO (+12.94%, TS 83), and SMCI (+6.34%, TS 86). The root cause: 0DTE option spreads widen through the day from theta decay, eventually exceeding the 5% gate and permanently locking out the ticker. Only 12 tickers promoted all day, and their median candidacy was 31 seconds because spread oscillation around the 5% boundary caused rapid promote/demote cycling.

Options spread and OI are now **display-only indicators**. The colored spread pills in the table tell you at a glance: green (≤10%), yellow (≤25%), red (>25%). You evaluate tradability before entering — the scanner evaluates momentum quality.

### Reading the Spread Pills

| Color | Spread | Meaning |
|-------|--------|---------|
| Green | ≤ 10% | Tight spread — standard trade execution |
| Yellow | 10–25% | Moderate spread — acceptable for momentum trades, factor into sizing |
| Red | > 25% | Wide spread — check the actual bid/ask before entering, or use shares |

Hover over any spread pill to see the exact DTE, bid, and ask values.

---

## What Changed in v8.06.1

The Candle Accumulator scoring engine was completely redesigned based on a 3-day backtest (5/18–5/20) across 240,000+ OHLC minute bars and 1,700+ simulated trades.

**Old system (v8.06):** 7 binary criteria scored per-bar, averaged across a rolling window. Profit factor 0.95 (net loser), 38.7% win rate. Several criteria had zero predictive value.

**New system (v8.06.1):** 7 structural criteria scored per-window as a unit. Profit factor 1.63 at the Early threshold, 2.35 at the high-conviction threshold. 46–55% win rate depending on threshold.

### Criteria That Were Dropped (And Why)

These criteria showed no statistical difference between winning and losing trades:

- **Volume above session average** — delta between winners and losers: 0.000. Volume tells you a ticker is active, but the TrendScore layer already filters for activity. Scoring it again in CA adds noise.
- **VWAP cross event** — delta: -0.002. VWAP *position* matters (are you above or below), but the *moment of crossing* is not predictive. Most crosses revert within 2 bars.
- **Close in upper 25% of bar range** — delta: +0.006. Too strict a threshold. Replaced by "close in upper half" which provides better separation.
- **Green candle (binary)** — delta: +0.012. Too noisy on 1-minute bars where many candles have bodies smaller than the spread. Replaced by "aggressive candle detector" which filters for meaningful body size.
- **Streak bonus (+5/+10 for 3/5 strong bars)** — superseded by the higher-close-streak criterion which captures the same signal more precisely and with graduated scoring.

---

## The 7 Structural Criteria

CA v2 scores the entire 5-bar window as a structural unit. Max score: 18 points. CA% = score ÷ 18 × 100.

### Criterion 1: Higher Close Streak (max 4 points)

**What it measures:** The longest consecutive run of bars where each bar's close is higher than the previous bar's close.

**Why it's #1:** This is the single strongest predictor found in the data. A streak of 1 produced 37% WR, streak of 3 → 51% WR, streak of 4 → 56% WR. Consecutive higher closes represent committed, sustained buying pressure — not just random green candles.

**Scoring:** 1 point per streak bar, capped at 4. A perfect 5-bar window where every bar closes higher than the last scores 4/4.

**Bear mode:** Counts consecutive *lower* closes instead.

### Criterion 2: HH+HL Structure (max 4 points)

**What it measures:** How many bars in the window have *both* a higher high AND either a higher low or a higher close compared to the previous bar.

**Why it matters:** This is the textbook definition of an uptrend at the candle level — each bar is pushing boundaries both above (higher high) and holding ground below (higher low). A bar that makes a higher high but a lower low is a range expansion / volatility event, not necessarily a trend. Requiring both filters for genuine structural advance.

**Scoring:** 1 point per qualifying bar, capped at 4.

**Bear mode:** Counts bars with lower low AND (lower high OR lower close).

### Criterion 3: Window Net Move (max 3 points)

**What it measures:** The total percentage move from the first bar's close to the last bar's close across the window.

**Scoring:**
- > 0.20% net move → 3 points
- > 0.10% net move → 2 points
- > 0.02% net move → 1 point
- ≤ 0.02% → 0 points

**Why tiered:** A 0.02% move over 5 minutes is a drift; 0.20% is a decisive directional push. The tiers let the score distinguish between subtle momentum (the DRIFT trades) and aggressive breakouts.

### Criterion 4: Above VWAP (max 1 point)

**What it measures:** Whether the last bar's close is above (bull) or below (bear) the current VWAP.

**Why only 1 point:** VWAP position matters for institutional flow context, but the backtest showed it's nearly always true when the other criteria are strong (99.2% of entries were above VWAP). It's a binary confirmation gate, not a differentiator.

### Criterion 5: Defensive Structure (max 2 points)

**What it measures:** How many bars in the window made a lower low (bull) or higher high (bear) — these are violations of the trend structure.

**Scoring:**
- 0 violations (perfect defense) → 2 points
- 1 violation → 1 point
- 2+ violations → 0 points

**Why it matters:** Holding lows is a stronger signal than making new highs. A window with 3 higher closes but 2 lower lows is choppy — the price is advancing but on shaky ground. Perfect defense (no lower lows) produced 48.4% WR vs 40.9% for windows with multiple violations.

### Criterion 6: Close in Upper Half (max 2 points)

**What it measures:** How many bars in the window close above the midpoint of their own range (high + low ÷ 2).

**Scoring:**
- ≥ 4 bars closing in upper half → 2 points
- ≥ 3 bars → 1 point
- < 3 bars → 0 points

**Why it matters:** A bar that closes in its upper half means buyers were in control at the end of that minute. When 4+ out of 5 bars close in their upper half, the entire window shows consistent buy-side dominance.

### Criterion 7: Aggressive Green Candle (max 2 points)

**What it measures:** How many bars in the window have a body (|close − open|) ≥ 0.15% of price, in the right direction (green for bull, red for bear).

**Scoring:**
- ≥ 2 aggressive candles → 2 points
- 1 aggressive candle → 1 point
- 0 → 0 points

**Why it matters:** On 1-minute bars, most candles have tiny bodies — many are smaller than the bid-ask spread. A candle with a body ≥ 0.15% of price is a genuine directional move, likely representing institutional-sized buying. The backtest showed 53% WR when at least one aggressive candle appeared in the entry window, vs 43% without.

**Configurable:** The 0.15% threshold is adjustable in Settings → Candle Accumulator → Aggressive Candle Body. Lower it to 0.10% for more sensitivity to subtle moves; raise to 0.20% for higher conviction only.

---

## Signal Levels

### Early Alert (E badge, yellow) — CA% ≥ 55%

The early alert fires when the 3-bar window scores ≥ 55%. This is the "heads up" signal — price structure is turning favorable but hasn't fully confirmed yet.

**What 55% means in practice:** Roughly 10 of 18 points. A typical early signal has a 2-bar higher close streak, 2 HH+HL bars, modest net move, and above VWAP. The window is structurally bullish but hasn't yet built the consecutive strength for confirmation.

**Backtested performance at 55%:** PF 1.63, 46.4% WR, +0.114% avg P&L across 476 trades.

**How to trade it:** Watch the ticker. If it stays on the list and the CA% rises toward 72%+, it's building a confirmed signal. If it drops back below 55%, the structure broke.

### Confirmed Signal (C badge, green) — CA% ≥ 72%

The confirmed signal fires when the 5-bar window scores ≥ 72%. This is the "enter" signal — the window shows strong, consistent bullish structure across all seven criteria.

**What 72% means in practice:** Roughly 13 of 18 points. A typical confirmed signal has a 3+ bar higher close streak, 3+ HH+HL bars, net move > 0.10%, above VWAP, perfect or near-perfect defense, most bars closing in upper half, and at least one aggressive candle.

**Backtested performance at 72%:** PF 1.72, 52.0% WR.

### High Conviction — CA% ≥ 80%

Not a separate badge, but when CA% hits 80%+, the backtest showed PF 2.35 and 55.4% WR. These are the trades where everything aligns: long streaks, perfect structure, aggressive buying, and strong directional net move. They're rarer (~100 signals across 3 days) but have the best edge.

---

## Reading the CA% Column

| Display | Meaning |
|---------|---------|
| `—` | Fewer than 3 sealed bars; still warming up |
| `28%` (red) | Structurally bearish window (for a bull candidate = warning) |
| `44%` (gray) | Neutral / mixed structure |
| `58% E` (yellow + E badge) | Early alert: structure building |
| `72% C` (green + C badge) | Confirmed: strong bullish structure |
| `83% C` (bright green + C badge) | High conviction entry |

**Hover tooltip** shows the per-criterion breakdown: `HC-Streak:3/4 · HH+HL:3/4 · Net:2/3 · VWAP:1/1 · Def:2/2 · Upper:2/2 · Aggr:1/2`

This tells you exactly *what* is strong and *what* is missing. For example, if Defense is 0/2 but everything else is high, the price is advancing but making lower lows — be cautious.

---

## Combining CA% with Other Signals

CA% is one dimension of the MomScanner signal stack. The strongest setups combine multiple layers:

**Ideal entry setup:**
- TrendScore ≥ 65 (confirmed candidate)
- CA% ≥ 72% (C badge — structural confirmation)
- ⭐75+ High Conviction badge (peak score confirms)
- Price above VWAP
- No trailing stop warning

**DRIFT trade setup (subtle moves):**
- TrendScore 65–75 (moderate but sustained)
- CA% 55–72% (E badge — structure building slowly)
- Higher close streak ≥ 3 in tooltip
- Low velocity (< 10 bps/min) — this is NOT a breakout
- Defense 2/2 in tooltip — price holding all lows

**Aggressive breakout setup:**
- TrendScore 75+ or BreakoutScore spike
- CA% 72%+ with Aggr Candle 2/2 in tooltip
- Velocity spike alert firing (≥ 25 bps/min)
- Hot streak banner active (3+ promotions in 30 min)

---

## Settings Reference

All configurable in Settings → v8.06.1 Candle Accumulator:

| Setting | Default | Range | Notes |
|---------|---------|-------|-------|
| Confirmed Window | 5 bars | 3–10 | How many sealed bars to evaluate for C signal |
| Early Alert Window | 3 bars | 2–5 | How many sealed bars for E signal |
| Confirmed Threshold | 72% | 50–95% | Minimum CA% for confirmed signal |
| Early Threshold | 55% | 30–80% | Minimum CA% for early alert |
| Aggressive Candle Body | 0.15% | 0.05–0.50% | Min body size to count as aggressive |
| VWAP Soft Gate | ON | ON/OFF | ON = VWAP is criterion 4 (soft). OFF = legacy hard gate |

### Tuning Recommendations

**If you're getting too many false E signals:** Raise Early Threshold to 60–65%.

**If you're missing DRIFT entries:** Lower Aggressive Candle Body to 0.10%. DRIFT moves have smaller per-bar bodies but sustained streaks.

**If you only want high-conviction entries:** Raise Confirmed Threshold to 80%. Fewer signals but PF 2.35.

**If you trade volatile small-caps (FCEL, CLSK, MARA):** These naturally produce larger candle bodies. You can raise Aggressive Candle Body to 0.25% to filter for truly exceptional buying pressure.

---

## Backtest Results Summary

Tested against 3 trading days (5/18, 5/19, 5/20) covering 237K OHLC bars, 199 tickers, and all market regimes (choppy, low-vol, stock-specific, mixed). Entry: CA% crosses threshold + TrendScore ≥ 65. Exit: 0.5% trailing stop from peak OR TrendScore < 55.

| System | Trades | WR% | Avg P&L | Avg Win | Avg Loss | PF |
|--------|--------|-----|---------|---------|----------|------|
| Old Binary ≥73% | 424 | 38.7% | -0.006% | +0.571% | -0.370% | 0.95 |
| 3-Tier ≥64% (proposed, rejected) | 581 | 36.5% | +0.011% | +0.727% | -0.400% | 1.04 |
| **CA v2 ≥55% (Early)** | **476** | **46.4%** | **+0.114%** | **+0.639%** | **-0.340%** | **1.63** |
| **CA v2 ≥72% (Confirmed)** | **229** | **48.5%** | **+0.124%** | **+0.635%** | **-0.356%** | **1.68** |
| CA v2 ≥80% (High Conviction) | 101 | 55.4% | +0.184% | +0.576% | -0.304% | 2.35 |

### v8.06.2 Gate Removal Simulation (5/22 data)

Simulated 5/22 with spread/OI gates removed: 1,035 trades across 88 tickers (vs 12 with gates on). Net positive with PF 1.14. Top missed opportunities recovered: NVTS +4.70% (entry 9:51), DELL +4.29% (9:36), HPQ +3.35% (9:38), QCOM +3.26% (10:20), ARM +2.94% (10:25). Per-ticker net P&L leaders: NVTS +8.05%, QCOM +5.40%, CRDO +5.04%, HPQ +4.88%, DELL +4.86%.

---

## Architecture Notes (for development)

- **Single-file app:** Everything lives in `index.html`. No build step, no dependencies beyond Google Fonts (JetBrains Mono, Syne).
- **Deployment:** Push to GitHub Pages at `vaultlinkcrypto.github.io/MomScanner/`.
- **CA bar buffer:** Per-ticker ring buffer of 60 sealed 1-minute bars (`d._caBars`). Bars are sealed when the minute-epoch changes.
- **Scoring function:** `scoreWindow(windowBars)` returns `{score, max, detail}`. The `detail` object contains per-criterion scores for the tooltip.
- **Session protection:** Never close MomScanner mid-session. Use the End Session button. The CSV logger and CA bar buffer are in-memory only.
- **Settings persistence:** CA settings stored in `ms_v805_settings` localStorage key (shared with the v8.05 trade management settings).
- **TOS links:** All external links use `target="_blank"` and protocol-relative URLs.
