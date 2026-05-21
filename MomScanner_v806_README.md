# MomScanner v8.06 — Candle Accumulator
## README & Trading Guide

---

## What's New in v8.06

### The Candle Accumulator (CA% column)

A new column appears between VWAP% and Dir in the main table. It shows a percentage score representing how many of the last 5 minute-bars were bullish (or bearish for PUT candidates).

Each minute bar is scored on 7 criteria:

| # | Bullish Criteria (CALL) | Bearish Criteria (PUT) |
|---|---|---|
| 1 | Close > Open (green candle) | Close < Open (red candle) |
| 2 | Close > Previous Close | Close < Previous Close |
| 3 | Low > Previous Low (higher low) | High < Previous High (lower high) |
| 4 | Close > VWAP | Close < VWAP |
| 5 | Volume above session average | Volume above session average |
| 6 | Close in upper 25% of bar range | Close in lower 25% of bar range |
| 7 | Price crossed UP through VWAP | Price crossed DOWN through VWAP |

**5-bar window** (5 minutes): 5 bars × 7 criteria = 35 points max + up to 10 streak bonus = 45 max. Confirmed signal fires at **73%** of max.

**3-bar window** (3 minutes): Early alert fires at **78%** of max. This is your heads-up — start watching this ticker.

**Streak bonus**: +5 points for 3 consecutive bars scoring 5+/7. +10 for 5 consecutive. This rewards the pattern where price goes up minute after minute without interruption.

### VWAP Soft Gate

VWAP is no longer a hard entry requirement. Previously, price had to be above VWAP for a CALL entry — this blocked entries at the exact moment of VWAP crossover, which is often the best entry point. Now VWAP position is one of 7 candle criteria (soft scoring). If you prefer the old behavior, toggle "VWAP Soft Gate" to OFF in Settings.

### Display

| CA% Value | Color | Meaning |
|---|---|---|
| 73%+ | Green + C badge | Confirmed entry signal — 5 of 5 bars bullish |
| 55-72% | Yellow | Warming up — watch for improvement |
| 40-54% | Gray | Neutral — no signal |
| Below 40% | Red | Bearish minute bars — wrong direction |

**Tooltip** (hover): Shows raw scores for 5-bar and 3-bar windows, session-wide bullish %, and streak length.

---

## HOW TO TRADE WITH v8.06

### Entry Decision — The Triple Check

Before entering any trade, all three must be true:

```
1. TREND SCORE ≥ 70  (Confirmed C badge on Trend layer)
2. CA% ≥ 73%         (Green with C badge — 5 bars of committed buying)
3. NO REGIME WARNING  (Yellow ⚠ bar not showing)
```

If any one is missing, don't trade. If all three are present, check the secondary filters:

- Spread ≤ 5% (green in Spread column)
- Not on Most-Flipped list (no ! warning)
- Time: 10:00 - 11:30 AM preferred (56% of winners enter here)

### What to Watch After Entry

| Signal | What It Means | Action |
|---|---|---|
| CA% stays 70%+ | Buyers still winning each minute | HOLD |
| ⭐75 badge appears | Peak score confirmed at 75+ (81% win rate) | HOLD — you're winning |
| ★85 badge appears | Peak score 85+ (94% win rate) | MAXIMUM HOLD |
| CA% drops to 50-65% | Momentum fading | Watch closely |
| CA% drops below 45% | Sellers taking over | Prepare to exit |
| ⚠ yellow warning | Score declining or near VWAP | Pay attention |
| EXIT red badge | Trailing stop hit or scores collapsed | SELL NOW |

### Exit Decision Tree

```
FIRST 30 MINUTES after entry:
    → HOLD regardless of CA% fluctuations
    → Only exit if all scores drop below 60 (EXIT badge fires)
    → Watch for ⭐ badge — confirms the trade

AFTER 30 MINUTES:
    → Is CA% still 65%+?
        YES → Continue holding, watch trailing stop
        NO  → Is ⭐ badge showing?
            YES → Hold (peak score already confirmed)
            NO  → EXIT (never confirmed, fading)
    
    → EXIT badge showing?
        YES → SELL IMMEDIATELY
    
    → Trailing stop level hit?
        YES → SELL
```

### Reading the CA% Column in Real Time

The CA% updates every time a new minute bar seals. Here's how to read the progression:

**Strong entry setup** (take the trade):
```
09:55  CA: 45%  — nothing happening
09:56  CA: 52%  — warming up
09:57  CA: 64%  — E badge appears (early alert)
09:58  CA: 71%  — almost confirmed
09:59  CA: 78%  C badge — CONFIRMED. Trend also ≥70. ENTER NOW.
```

**Fakeout** (don't trade):
```
10:00  CA: 48%  — flat
10:01  CA: 61%  — spike
10:02  CA: 55%  — dropped back
10:03  CA: 47%  — fading
→ Never reached 73%. No C badge. SKIP.
```

**Exit signal** (sell):
```
10:30  CA: 76%  — strong (you're holding)
10:31  CA: 72%  — slight dip
10:32  CA: 64%  — dropping
10:33  CA: 51%  — sellers winning. ⚠ warning appears.
10:34  CA: 43%  — EXIT badge fires. SELL.
```

### The 3-Minute Early Alert

The early alert (E badge, yellow) fires when 3 consecutive bars score 78%+. This appears 2-3 minutes before the confirmed signal. Use it to:

1. Pull up the options chain for this ticker
2. Check the spread (is it ≤ 5%?)
3. Identify your strike and contract
4. Wait for the C badge to confirm, then buy immediately

Do NOT enter on the E badge alone. It's a heads-up, not an entry signal.

---

## SETTINGS

All v8.06 settings are in **Settings → v8.05 Trade Management** (bottom section).

| Setting | Default | What It Controls |
|---|---|---|
| Confirmed Window | 5 bars | How many minute bars for confirmed signal |
| Early Alert Window | 3 bars | How many minute bars for early alert |
| Confirmed Threshold | 73% | Minimum bullish % for C badge |
| Early Alert Threshold | 78% | Minimum bullish % for E badge |
| Streak Bonus | ON | +5/+10 bonus for consecutive strong bars |
| VWAP Soft Gate | ON | VWAP as scoring criterion vs hard gate |

---

## POSITION SIZING (unchanged)

| Condition | Max Contracts | Max Risk |
|---|---|---|
| Trend C + CA% C + no regime warning, 10-11 AM | 2 | $50 |
| One C badge missing or after 12 PM | 1 | $25 |
| Regime warning showing | 1 (or skip) | $25 |
| After 2:30 PM on 0-DTE | DO NOT TRADE | — |
| Maximum trades per day | 3 | — |

---

## DEPLOYMENT

1. Go to `https://github.com/vaultlinkcrypto/MomScanner`
2. Click `index.html` → pencil icon → Ctrl+A → delete → paste v8.06 code
3. Commit → wait 30-60s → Ctrl+Shift+R
4. Verify: header shows "MOMENTUM TERMINAL v8.06"
5. Verify: CA% column appears between VWAP and Dir
6. Open Settings → verify v8.06 Candle Accumulator sliders visible
7. Open Settings → Audio Alarms → ▶ Test to re-unlock audio
8. Keep Trend slider at 70 (your 5/20 setting)

## VERIFICATION CHECKLIST

- [ ] Header: "MOMENTUM TERMINAL v8.06"
- [ ] Banner: "v8.06 LOADED ✓"
- [ ] CA% column visible between VWAP% and Dir
- [ ] CA% shows percentage with color coding (green/yellow/gray/red)
- [ ] E badge (yellow) appears on 3-bar alert
- [ ] C badge (green) appears on 5-bar confirmed
- [ ] Hover tooltip shows 5-bar, 3-bar, session %, streak info
- [ ] Settings → v8.06 Candle Accumulator section with 6 sliders
- [ ] VWAP Soft Gate toggle works (ON = soft scoring, OFF = hard gate)
- [ ] All v8.05 features still work (trailing stop, badges, exit signals, etc.)
- [ ] OHLC logger, CSV exports, audio alarms all functional

---

## EXPECTED BEHAVIOR ON 05/21

Based on backtesting with CA ≥ 73%:

- **Good day (stock-specific/low-vol regime):** 40-70 candidates, 71%+ win rate, +0.55% avg profit
- **Bad day (mixed/choppy regime):** 20-50 candidates, 36% win rate — the regime warning will tell you to reduce size or skip

The CA% column will be empty for the first 5 minutes after session start (needs 5 sealed bars). First signals typically appear by 9:41-9:45 AM.

Watch for the E badge as your early warning, then wait for C badge to confirm. The combination of Trend ≥ 70 + CA% C badge + no regime warning was the most profitable filter in our backtesting.

---

## CHANGELOG

| Version | Date | Key Change |
|---|---|---|
| v8.06 | 2026-05-20 | Candle Accumulator (CA% column), VWAP soft gate, direction-aware scoring, streak bonus |
| v8.05 | 2026-05-15 | Trailing stop, min hold, HC badge, vel spike, hot streak, regime warn, exit signal |
| v8.04.2 | 2026-05-14 | Velocity gate completion fix |
| v8.04.1 | 2026-05-13 | Velocity display %/min + ¢/min |
| v8.04 | 2026-05-13 | Velocity gate off for Trend, RVol sliders |
| v8.03.1 | 2026-05-08 | Session Protection Suite |
