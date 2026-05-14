# MomScanner v8.04 — Trade Entry & Exit Guide
## OTM Options Strategy on Layer Signals

*This guide is based on analysis of your 5/1, 5/12, and 5/13 session data. All references to scores, velocities, and thresholds reflect v8.04 defaults. This is not financial advice — it is a framework for how to interpret MomScanner signals for your specific OTM options strategy.*

---

## How to Read the Velocity Column (v8.04.1)

The Vel column now shows two numbers side by side:

**+0.06% +135.5¢** — percentage per minute first (normalized), cents per minute second (raw).

The percentage is what matters for decision-making. It normalizes velocity across all price levels, so you can compare a $13 stock directly against a $220 stock. The cents/min is there for reference only — do not let a large cents number influence your entry if the percentage is small.

| Velocity %/min | Meaning | Action |
|---|---|---|
| < 0.01% | Flat / stalled | Do NOT enter |
| 0.01% – 0.03% | Gentle drift | Enter only on Trend layer with confirmed candidacy |
| 0.03% – 0.06% | Moderate move | Enter on Trend or Breakout |
| 0.06% – 0.10% | Strong move | Enter on any layer with confirmation |
| > 0.10% | Spike / extreme | Caution — may be too late, watch for reversal |

---

## TREND Layer Trades (DRIFT)

**What it detects:** Slow, sustained price movement in one direction over 30 minutes to hours. Price staying consistently above or below VWAP. The most reliable signal for your OTM options strategy.

**Ideal regime:** Low-vol, stock-specific.

### Entry Checklist

1. Trend score ≥ 65 (confirmed tier promoted, green C badge showing)
2. Price above VWAP (for calls) or below VWAP (for puts) — check the VWAP% column
3. Arrow direction matches: up arrow for calls, down arrow for puts
4. Options spread ≤ 5% (green in Spread column)
5. Candidacy age > 2 minutes — do NOT enter on the first second of promotion. Wait for the ticker to hold candidate status. If it flickers out in 30 seconds, it wasn't real
6. Velocity %/min is positive (for calls) — even small positive like +0.01% is fine for DRIFT. DRIFT trades do NOT need high velocity. That's the whole point
7. No flip warning (!) next to the ticker name

### Entry Timing

Buy OTM call (or put) when the ticker has been in confirmed Trend candidacy for at least 2 minutes and the move is still developing. For 0-DTE or 1-DTE options, the earlier in the day you enter the better — time decay accelerates dramatically after 2 PM.

Ideal entry window: 9:45 AM – 11:30 AM (after the opening chaos settles, before midday doldrums).

### Avoid Entry When

- Trend score is above threshold but ticker keeps flickering in and out of candidacy (even with v8.04 fixes, some tickers are genuinely indecisive)
- Flip count > 6 — this ticker has been noisy all day
- Regime is "choppy" — everything is unreliable in chop
- VWAP% is near zero (±0.1%) — price is sitting right on VWAP with no directional conviction
- The ticker already moved 5%+ intraday and Trend score is declining — you're late

### Exit Rules

| Condition | Action |
|---|---|
| Option up 15-30% from entry | Take profit. Your NFLX 5/12 trade hit +15% and you sold — that was correct |
| Trend state drops from confirmed to watch | Exit immediately — the signal just died |
| Price crosses back through VWAP | Exit. The directional thesis is broken |
| Arrow reverses (up→down or down→up) | Exit |
| 30 minutes pass with no further price progress | Exit. Stalled DRIFT = theta burn |
| Score drops below 60 | Exit even if still in candidacy |
| After 2:30 PM on 0-DTE | Exit. Gamma risk is extreme |

### Risk Sizing

Position size: 1-2 contracts max for 0-DTE. You're buying lottery tickets, not building positions. Your NVDA $237.50c x4 at $0.04 was the right size — total risk $16.

---

## BREAKOUT Layer Trades

**What it detects:** Range expansion — price breaking out of a consolidation range with volume confirmation. Faster than Trend (5-30 minutes), more volatile.

**Ideal regime:** Stock-specific, trending-bull/trending-bear.

### Entry Checklist

1. Breakout score ≥ 70 (confirmed tier)
2. Breakout direction matches your trade direction (breakoutDir up/down)
3. Velocity %/min ≥ 0.03% — breakouts NEED velocity. Unlike DRIFT trades, a breakout with flat velocity is a failed breakout
4. RVol ≥ 1.0x — breakouts without volume are fakeouts
5. Options spread ≤ 5%
6. At least one other layer supporting: Trend ≥ 55 or Pressure ≥ 60

### Entry Timing

Breakouts are time-sensitive. Enter within the first 2-3 minutes of confirmed Breakout promotion. If you wait 5+ minutes, the initial thrust is usually spent. The premium has already repriced.

Best windows: 9:35 – 10:15 AM (opening breakouts), 2:00 – 3:00 PM (power-hour breakouts).

### Avoid Entry When

- Breakout score is high but velocity is flat or negative — the breakout failed
- The stock is on the Most-Flipped list from the session summary — it's been unreliable all day
- Spread > 5% — you'll lose the profit on the bid-ask round trip
- RVol < 1.0x — no volume behind the breakout, likely to fade

### Exit Rules

| Condition | Action |
|---|---|
| Option up 20-50% from entry | Take profit. Breakout premiums spike fast and fade fast |
| Velocity drops to 0 or reverses within 5 minutes of entry | Exit immediately — failed breakout |
| Breakout state drops from confirmed to watch | Exit |
| 10 minutes pass with no follow-through | Exit. Breakouts that stall usually reverse |
| Price retraces back into the prior consolidation range | Exit. The breakout failed |

### Risk Sizing

Same as Trend: 1-2 contracts max. Breakouts are higher-reward but also higher-failure-rate than DRIFT trades.

---

## PRESSURE Layer Trades

**What it detects:** Short-term order flow imbalance using OFI (order flow imbalance) proxies — bid-ask positioning, volume-weighted tick direction, cluster analysis. Fastest signal (30 seconds to 5 minutes).

**Ideal regime:** Stock-specific (the Pressure layer works best when individual tickers are moving independently of the market).

### Entry Checklist

1. Pressure score ≥ 72 (confirmed tier)
2. Tick direction matches trade direction (avg tick sign > 0.15 for calls)
3. Velocity %/min ≥ 0.03% — Pressure signals with flat velocity are stale
4. Pressure score is NOT sitting at exactly 50 — if Pressure has been at 50 for the last hour, the OFI proxies are stale and the signal is unreliable (this is Bug 3 from the analysis — the Pressure flatline issue)
5. Ideally confirmed by at least one other layer: Trend ≥ 60 or Breakout ≥ 55

### Entry Timing

Pressure is the fastest signal — you have a very narrow window. Enter within 60 seconds of confirmed Pressure promotion or don't enter at all. The signal degrades quickly.

Best windows: 9:30 – 10:30 AM (when OFI data is richest due to high volume), 3:00 – 3:45 PM (closing volume surge).

### IMPORTANT: Pressure is unreliable during midday

From the 5/12 and 5/13 data, 54.7% of afternoon bars have Pressure = exactly 50. The OFI proxies go stale during low-volume midday hours (11:30 AM – 2:00 PM). Do NOT take Pressure-only trades during this window. If Pressure fires during midday, it must be confirmed by Trend or Breakout to be actionable.

### Avoid Entry When

- Pressure = 50 has been flat for 30+ minutes — stale data
- It's between 11:30 AM and 2:00 PM and no other layer confirms
- RVol < 0.8x — not enough tick data for reliable OFI
- You can't fill the order within 60 seconds of the alert

### Exit Rules

| Condition | Action |
|---|---|
| Option up 10-25% from entry | Take profit immediately. Pressure trades are hit-and-run |
| Pressure state drops to watch | Exit. No delay, no second-guessing |
| 3 minutes pass with no price movement | Exit. Pressure signals that don't convert quickly are dead |
| Tick direction reverses | Exit |

### Risk Sizing

1 contract only. Pressure is the least reliable standalone layer. It's best used as confirmation for a Trend or Breakout trade, not as a primary signal.

---

## Multi-Layer Confirmation (Highest Conviction)

The strongest signals are when multiple layers agree. Here's the hierarchy:

| Layers Agreeing | Conviction | Action |
|---|---|---|
| Trend C + Breakout C | Very high | Full size (2 contracts), wider profit target (30-50%) |
| Trend C + Pressure C | High | Standard size, standard targets |
| Trend E + Breakout E | Moderate | Watch for confirmation upgrade, enter on first C badge |
| Single layer C only | Lower | Reduce size, tighter stops |
| Single layer E only | Low | Do NOT enter. Wait for confirmation |
| No layers active | None | Do NOT enter under any circumstances |

*(C = Confirmed tier, E = Early tier)*

The Early tier (yellow E badge) is a heads-up, NOT an entry signal. It tells you to watch this ticker closely and be ready. Enter only when at least one layer shows Confirmed (green C badge).

---

## What to Watch After v8.04 Bug Fixes

The candidacy stability fixes in v8.04 will change the scanner's behavior significantly. Expect:

- Longer candidacy durations (target: 5-30 minutes average, not 1 minute)
- More tickers reaching Confirmed tier (the velocity gate was blocking most Trend promotions)
- FCEL-type low-RVol tickers now visible (RVol floor lowered from 1.5x to 0.3x for Trend)
- Potentially more false positives in the first few sessions — if candidacies are too loose, tighten the RVol floor slider back up

Monitor the session summary stats after each session. If avg candidacy is 20+ minutes and promotions are in the 50-100 range (not 500+), the fixes are working correctly. If promotions are still 500+, the streak counter may need further adjustment.

---

## Quick Reference Card

**Before any trade, check ALL of these:**
1. Is there at least one Confirmed (C) badge? → If no, don't trade
2. Is the velocity %/min positive and meaningful? → If flat, don't trade (exception: DRIFT at 0.01%)
3. Is the options spread ≤ 5%? → If not, the bid-ask will eat your profit
4. Is this ticker on the Most-Flipped / flip warning list? → If yes, it's unreliable today
5. Is the regime "choppy"? → If yes, reduce conviction on everything
6. Have you already taken 3+ trades today? → Stop. Overtrading is the biggest edge killer
