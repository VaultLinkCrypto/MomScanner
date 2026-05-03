# MomScanner v8

ThinkorSwim deep-links on every ticker symbol, a new Velocity column with cents-per-minute price tracking, per-layer threshold sliders that finally do something, an upgraded regime detector, and a velocity-gated Pre-Promotion Watch. Builds on v7.2 with five additions targeting the three root-cause problems found in the May 1 session logs: late promotions on dead moves, regime misclassification on stock-specific days, and the orphaned score-weight panel.

**Live URL:** https://vaultlinkcrypto.github.io/MomScanner/

## What's new in v8

- **ThinkorSwim deep-links** — every ticker symbol in every table (Watching, Candidates, Near-Miss, History, Transition Log) is now a clickable link. Click a ticker, a new Chrome tab opens with `https://trade.thinkorswim.com/trade?symbol=TICKER`. Saves typing into TOS. **MomScanner stays untouched on its original tab so session data and CSV logging are never interrupted.**
- **Velocity column (Vel)** — shows price velocity in cents-per-minute over the last 60 seconds. Green when above the configured gate, red when below the negative gate, gray when flat. Hover for the exact gate threshold scaled to that ticker's price. Visible on every ticker in the Watching table.
- **Velocity gate as 4th promotion check** — score above threshold + RVol ≥ 1.5x + spread/OI/direction OK is no longer enough. Velocity must also exceed a percentage-of-price threshold at the moment of promotion. Default: 0.03%/min (3¢/min on a $100 stock, 6¢/min on $200, 1.5¢/min on $50). Configurable in Settings. Tickers with high score but stalled price are blocked from promotion or shown in the Near-Miss panel with a "Stale momentum" tag.
- **Velocity-gated Pre-Promotion Watch** — the pulsing ↑ icon now requires three conditions instead of two: (1) Trend or Breakout ≥ 60, (2) Pressure crossed 60 in last 90s, AND (3) price is moving AND still accelerating (current velocity ≥ prior velocity in magnitude). Filters false early alerts on stalled prices.
- **Per-Layer Threshold sliders** — the orphaned v6 score-weight sliders are replaced with real per-layer controls. Direct sliders for Trend / Breakout / Pressure score thresholds, minimum streaks, and minimum qualifying cycles, plus the velocity gate. Real v7 sub-component naming. The manual override finally works.
- **Improved regime detector** — adds two dimensions beyond SPY-only volume: (a) aggregate ticker flip count (catches stock-specific chop even when SPY is calm), (b) "stock-specific" classification when SPY is flat but individual tickers are moving 3%+ intraday (the May 1 INTC scenario). New regimes: low-vol, **stock-specific**, choppy, trending-bull, trending-bear, mixed.

## What carried over from v7.2

- Audio alarms (Bell / Chime / Alert / Tick + custom MP3/WAV upload, volume, cooldown)
- Pre-Promotion Watch ↑ icon (now velocity-gated)
- Near-Miss panel (collapsible, sortable, with new "Stale momentum" block tag)

## What carried over from v7.1

- Three-layer architecture (Trend / Breakout / Pressure)
- Intraday %Chg column and Gap-relationship icon
- VWAP tracking per ticker
- L1-friendly OFI proxies
- High-contrast accessibility theme with adjustable font size
- Pattern-based trading guide with five named patterns

## What carried over from v5/v6/v7

- Bulletproof persistence
- Time-of-day adaptive tuning
- SPY-driven regime indicator (now upgraded — see above)
- Don't-Trade warning banner
- Momentum-type classifier
- End-of-session summary report
- All CSV exports (active + transitions, both now include velocity column)

---

## Part 1 — ThinkorSwim deep-links (v8)

### Why this matters

You always have ThinkorSwim running on the same Chrome browser as MomScanner. When a candidate appears, you need to look at the chart in TOS — and typing the ticker into TOS's search bar takes 5-10 seconds, which can be the difference between a clean entry and a chase.

Now you click the ticker symbol in MomScanner. Done.

### How it works

Every ticker symbol in every table is wrapped in a link to `https://trade.thinkorswim.com/trade?symbol=TICKER`. Clicking opens that URL in a **new Chrome tab** (`target="_blank"`). The MomScanner tab stays open and active — your session data, transition log, and CSV logging are completely uninterrupted.

If you click NOK, then TSLA, then NVDA, you'll accumulate three TOS tabs. Close them as you finish reviewing each chart. MomScanner is always on Tab 1.

### Where it works

- Main Watching table — every ticker
- Trend / Breakout / Pressure Candidates sections — every ticker
- Near-Miss panel — every ticker
- Session Log (transitions) — every ticker
- History Archive — every ticker

### Visual cue

Ticker symbols have a subtle dotted underline on hover and turn yellow (accent color) so you can see they're interactive without it being visually noisy.

---

## Part 2 — Velocity column (v8)

### Why this matters

The May 1 session showed the central problem: by the time a ticker promoted to candidate (after 8/10 cycles + minimum streak), the actual price move was often already over. INTC promoted at 15:15 with score 73 and +6.88% intraday — but at the moment of promotion, INTC was no longer moving. It then churned bull/bear/watch for three hours between $99.04-$99.57. The score said "candidate." The price said "nothing's happening."

Score doesn't measure whether price is still moving right now. Velocity does.

### What the column shows

The **Vel** column (between RVol and Trend) shows price velocity in **cents per minute** over the last 60 seconds. Color-coded:

- **Green (vel-strong)** — velocity is above the configured gate in the up direction. Price is rising at a tradable rate.
- **Red (vel-weak)** — velocity is below the negative gate. Price is falling at a tradable rate.
- **Gray (vel-flat)** — velocity is between the gates. Price is essentially still.
- **Em-dash (—)** — not enough samples yet (need ≥20 seconds of data).

Hover the value for the exact gate threshold for that ticker (e.g. "+5.2¢/min over last 60s · gate ±3.0¢/min (0.03% of $100.00)").

### How velocity is computed

Per ticker, MomScanner maintains a 90-second rolling buffer of `{timestamp, price}` samples. Velocity is the slope of price over the most recent ~60-second span, expressed in cents per minute. Signed: positive means price is going up, negative means price is going down.

### Why cents per minute, not percentage

A 0.05¢/min velocity has very different meaning on a $10 stock vs a $200 stock. Showing cents in the column is human-readable — "INTC is moving 4 cents per minute" is intuitive. For the gating threshold, however, a single cents value would be wrong (3¢/min is huge on a $5 stock and tiny on a $300 stock). So the **gate** is configured as a percentage of price and **scaled per ticker** at evaluation time.

### Default gate setting

**0.03% of price per minute**. This translates to:
- $20 stock → 0.6¢/min
- $50 stock → 1.5¢/min
- $100 stock → 3.0¢/min
- $200 stock → 6.0¢/min
- $400 stock → 12.0¢/min

A stock moving 0.03% per minute is moving 1.8% per hour, which is enough to make an OTM option worth holding. Below that, the move is too slow to capture given option time decay.

Adjust the gate in **Settings → Layer Thresholds & Timing → Min Velocity at Promotion**. Slider range is 0% to 0.20%. Set to 0 to disable the velocity gate entirely.

### Velocity gate behavior by layer

The Pressure layer is allowed half the gate threshold because it's the fastest-firing layer (30s-5min horizon) and fast moves don't always have time to accumulate sustained velocity. Trend and Breakout use the full gate.

---

## Part 3 — Per-Layer Threshold sliders (v8)

### What was wrong before

The Settings panel had five sliders labeled Volume Pressure, Relative Volume, Price vs EMA, Volatility Exp., and Options Activity. These were holdovers from v6's single-score architecture. In v7+, the scoring engine is three independent layers — those sliders affected nothing. They were orphaned.

### What's there now

The sliders are replaced with real per-layer controls. Three groups of three sliders each (one per layer) plus a global velocity gate slider:

#### TREND LAYER (slow · 30 min – hours · VWAP-anchored)
- **Trend Score Threshold** (50-90, default 65) — minimum trend score to qualify
- **Trend Min Streak** (30-300s, default 120s) — must hold qualification for this many seconds
- **Trend Min Qualifying Cycles** (3-15, default 6) — must qualify in this many of the last N polling cycles

#### BREAKOUT LAYER (medium · 5–30 min · range expansion)
- **Breakout Score Threshold** (50-95, default 70)
- **Breakout Min Streak** (10-180s, default 30s)
- **Breakout Min Qualifying Cycles** (3-12, default 5)

#### PRESSURE LAYER (fast · 30s–5 min · OFI proxies)
- **Pressure Score Threshold** (55-95, default 72)
- **Pressure Min Streak** (5-120s, default 15s)
- **Pressure Min Qualifying Cycles** (2-10, default 4)

#### VELOCITY GATE (v8 · all layers)
- **Min Velocity at Promotion (% of price/min)** (0-0.20%, default 0.03%)

### Tuning guidance

**To get more candidates** — lower thresholds, lower min-streak. You'll see more transitions, more flips, more noise.

**To get cleaner candidates** — raise thresholds, raise min-streak. Fewer candidates, longer-held positions, fewer flips.

**To catch fast moves earlier** — drop Pressure min-streak to 5-10 seconds and Pressure threshold to 70. Trade-off: more false positives.

**To filter dead moves** — raise the velocity gate from 0.03% to 0.05% or 0.10%. The May 1 INTC promotion would have been blocked at 0.03% (it had near-zero velocity).

### Save and reset

Click **Save Layer Thresholds** to apply. Click **Reset Defaults** to restore the values listed above.

---

## Part 4 — Velocity-Gated Pre-Promotion Watch (v8)

### What changed

In v7.2, the pulsing ↑ icon required two conditions:
1. Trend OR Breakout score ≥ 60 (slow layer building)
2. Pressure crossed ≥ 60 in last 90 seconds (fast layer firing)

In v8, a third condition is added:
3. Price is moving (|velocity| ≥ half the velocity gate) AND still accelerating (|current velocity| ≥ |prior velocity|)

### Why

In v7.2, the ↑ icon could fire when scores were rising but price had already stalled. The icon was supposed to be a 30-90 second early warning of an imminent promotion. If price wasn't actually moving, that warning was hollow.

The v8 logic asks: is this ticker actually heating up, or is the score lagging?

The **half-gate** for pre-promote (vs full-gate for actual promotion) is intentional — pre-promote is an early-warning indicator, so it fires earlier in the move when velocity is still building.

### What you'll see

- ↑ icon appears next to a ticker symbol in the Watching table
- Pulses in accent yellow color
- Hover for tooltip: "Heating up: Pressure crossed 60 Xs ago, slow layer building, price moving and accelerating"
- Disappears when conditions no longer met (typically because the ticker promoted, or velocity stalled, or pressure dropped)

The optional softer audio alarm (in Settings) fires once per ticker on the first detection of pre-promote state.

---

## Part 5 — Improved regime detector (v8)

### What was wrong before

The May 1 session classified 1,415 transitions as `low-vol`, only 36 as `choppy`. But the session was behaviorally choppy — INTC had 48 transitions and 20 flips. The detector was looking at SPY only. SPY was indeed flat. But individual tickers were moving 5%+. The "low-vol" label was misleading, and worse, the close-window stability override that activates on low-vol days was tightening thresholds when they should have been loosened.

### What changed

The detector now looks at three dimensions:

1. **SPY price action** (existing) — net move, range, direction-flip count over 30 minutes
2. **SPY range** — high-low vs price (proxy for ATR)
3. **Ticker-level chop** — average flip count across all tracked tickers (excluding SPY)
4. **Ticker-level movers** — count of tickers with |intraday %Chg| ≥ 3%

### New regime states

| Regime | Trigger | Meaning |
|---|---|---|
| **trending-bull** | SPY net up ≥ 0.6%, low flips | Confirmed market-wide rally |
| **trending-bear** | SPY net down ≥ 0.6%, low flips | Confirmed market-wide selloff |
| **choppy** | High aggregate ticker flips OR SPY flip rate high | Indecision everywhere — tighten stability filters |
| **low-vol** | SPY flat AND no big movers | Boring tape, nothing's happening |
| **stock-specific** | SPY flat BUT 2+ tickers moving 3%+ | The May 1 scenario — focus on individual ticker signals |
| **mixed** | None of the above | Unclear, default neutral handling |
| **unknown** | < 6 SPY samples yet | Warmup |

### What "stock-specific" looks like

You'll see the regime banner read **"Regime: Stock-Specific (SPY flat, tickers moving)"**. The detail line will say "SPY is flat but individual tickers are moving 3%+ — focus on ticker-level signals, not market direction."

This is a permission slip: don't wait for SPY to confirm. The setup is in the individual stocks today.

---

## Part 6 — Set up the GitHub repository

### Important: keeping older versions accessible

You can save older versions as `index_V7.1.html`, `index_V7.2.html`, etc. in your repo. With GitHub Pages, you can access each independently:

- `https://vaultlinkcrypto.github.io/MomScanner/` → loads `index.html` (now v8)
- `https://vaultlinkcrypto.github.io/MomScanner/index_V7.2.html` → loads v7.2 (if saved)

All versions share the same localStorage origin, which means your settings, history, and tickers carry across all of them. If you want truly isolated state between versions, run them in different browsers.

### 6.1 — Updating from v7.2 to v8

1. Go to https://github.com/vaultlinkcrypto/MomScanner
2. Click `index.html` → click the pencil (edit) icon
3. **Ctrl+A** to select all → **Delete** → paste new v8 code
4. Click **Commit changes**
5. Wait 30-60 seconds, then on the live page hit **Ctrl+Shift+R** (hard refresh)
6. **Open Settings → Audio Alarms → click ▶ Test once.** This unlocks the audio system for the session.

All your v7.2 settings, tickers, history, and transitions carry over via localStorage.

### 6.2 — Verifying the upgrade worked

After hard refresh:
- Header should read **"MOMENTUM TERMINAL v8"**
- Settings drawer should have a new **"Layer Thresholds & Timing (v8)"** section replacing the old "Score Weights" panel
- Main table should show a new **"Vel"** column between RVol and Trend
- Click any ticker symbol — a new Chrome tab should open with that ticker loaded in ThinkorSwim
- Regime banner may show new states like **"Stock-Specific"** depending on market conditions

### 6.3 — If something breaks

If the Vel column shows "—" for all tickers for more than a minute after market open, the price velocity buffer hasn't accumulated enough samples. Wait another 30 seconds.

If the layer threshold sliders don't save, check the browser console for localStorage quota errors. Clear old session summaries via DevTools if needed.

If TOS deep-links don't open new tabs, check Chrome's popup blocker — `trade.thinkorswim.com` should be allowed by default since the click is a direct user gesture.

---

## Part 7 — Daily trading routine for v8

### Pre-market

1. Open MomScanner in Chrome (Tab 1).
2. Open ThinkorSwim in the same browser window (any tab number — TOS will reuse the most recent matching tab).
3. **Open settings → Audio Alarms → click ▶ Test** to unlock audio for the session.
4. Verify Layer Thresholds & Timing settings are at the values you want for today.
5. Run thinkorswim scan, get list of symbols. Don't paste yet.

### 9:30 AM

Paste tickers including SPY into MomScanner. Audio is already unlocked. Velocity buffer starts filling immediately.

### Throughout the session

- When you hear the alarm, look at MomScanner. A new candidate just appeared in one of the three layer Candidates sections. Click the ticker symbol — TOS opens in a new tab with the chart loaded. Review the chart, place the trade if the pattern matches.
- When you see a pulsing ↑ icon next to a ticker in Watching, the ticker is heating up AND moving AND accelerating. Pre-position your trade if you trust the setup.
- Watch the Vel column. If the green/red coloring is dropping out (turning gray) on your held positions, the move is fading — consider exiting.
- During slow periods, expand the Near-Miss panel to see what's moving in the broader market. The "Stale momentum" tag specifically flags tickers with strong scores but dead price action.

### Reading the regime banner

- **Trending-bull / trending-bear** → trust market direction, take more trades
- **Choppy** → fewer high-conviction setups, sit out marginal candidates
- **Low-vol** → consider sitting out entirely
- **Stock-specific** → focus on individual signals, ignore SPY
- **Mixed / unknown** → default approach

### 4:00 PM session close

Click **Session Summary** to generate the end-of-day report. Click **Export CSV** for the active candidates snapshot. Click **Export Transitions CSV** for the full session log including velocity values at each transition.

**Do not close the MomScanner browser tab during the session.** CSV logging happens in real time via localStorage. Closing the tab before exporting will not lose data (localStorage persists), but if you need the CSVs, export before closing.

---

## Part 8 — Reading the three layer scores (carried from v7.1, refined in v8)

### The five trade patterns

These patterns reliably produce profitable trades. v8 doesn't change pattern logic — but the velocity gate now ensures that promotion happens while price is still moving, so the patterns are more actionable.

| Trend | Brkout | Press | Type | Pattern | Hold time | Target |
|---|---|---|---|---|---|---|
| 80+ | 55-70 | 70+ | DRIFT | Strong Sustained Trend | 30+ min | 50-100% |
| 80+ | 40-55 | 60-70 | DRIFT | Quick Subtle Move | 15-25 min | 25-40% |
| 50-65 | 50-65 | 75+ | THRUST/REVR | Pressure Spike Bounce | 5-10 min | 15-25% |
| 55-75 | 75+ | 65+ | DRIFT | Fresh Breakout | 15-30 min | 30-50% |
| Any <70 | Any <70 | Any <70 | — | Don't Trade | — | — |

### Trade entry checklist (12 items, expanded for v8)

1. ✅ Audio alarm fired (you heard the new candidate)
2. ✅ Pattern matched from the cheat sheet
3. ✅ Streak shows minimum sustained time (1+ min for slow patterns, 30+ sec for Pressure)
4. ✅ Flips < 4 (no warning icon next to ticker)
5. ✅ Spread% ≤ 5%
6. ✅ VWAP relationship matches your direction
7. ✅ Gap icon supports the direction
8. ✅ Don't-Trade banner is NOT showing
9. ✅ Type tag visible and matches pattern
10. ✅ Pre-Promotion ↑ was visible 30-60 seconds before promotion (confirmation that the move was real)
11. ✅ **(NEW v8) Vel column is green for bullish trade or red for bearish trade — confirms price is still moving**
12. ✅ **(NEW v8) Regime is not stock-specific OR you've verified the underlying ticker is one of the actual movers**

If all check, click the ticker symbol to open TOS, verify the chart, place the trade.

---

## Part 9 — Settings reference

### Data Source
Tradier or Schwab keys, callback URL, environment selection.

### Options Liquidity Filter
Penny Pilot toggle, max spread %, min OI, max DTE, options check interval.

### Layer Thresholds & Timing (v8) — REPLACES v6 Score Weights
- Trend / Breakout / Pressure each have: score threshold, min streak, min qualifying cycles
- Velocity gate (% of price/min) — global, applies to all layers
- Save / Reset Defaults buttons

### Audio Alarms (v7.2)
Enable, Pre-Promote secondary alarm, Sound choice (4 built-in + custom), Test button, Volume, Cooldown.

### Accessibility (v7)
Theme picker (4 options), Base font size slider (11-22px), live preview, save.

### Time-of-Day Tuning (v5)
Toggle. Adapts thresholds across the three time windows.

### Stability Filter (v4)
Window, Min Qual, Min Streak, Flip Warn (legacy controls — still active for the composite single-score path; v7+ layer paths use the new Layer Thresholds panel).

### Behavior
Smoothing Lag, High Threshold, Low Threshold, Min Refresh.

---

## Part 10 — Troubleshooting

**Vel column shows "—" for all tickers:** The velocity buffer needs ≥20 seconds of price samples before computing. Wait. If it stays at "—" after 60 seconds, the feed isn't returning fresh prices — check the feed status pill in the header.

**Vel column shows numbers but they're all gray:** Velocity is below the gate threshold for those tickers' prices. Either the market is genuinely slow, or your gate is set too high. Lower the **Min Velocity at Promotion** slider in Settings.

**Velocity gate is blocking everything:** Set the gate to 0 in Settings → Layer Thresholds & Timing to disable it temporarily. Verify candidates start appearing again. Then raise the gate gradually until you find the level that filters dead moves without blocking real ones.

**Clicking a ticker symbol does nothing:** Check Chrome's popup blocker. The click is a direct user gesture so it should always succeed, but extreme privacy extensions (uBlock Origin, Privacy Badger) can interfere. Whitelist `trade.thinkorswim.com` if needed.

**Clicking a ticker reloads MomScanner:** Should never happen — every link uses `target="_blank"`. If it does, screenshot the URL bar after the broken navigation and report it via thumbs-down on a Claude conversation.

**Pre-Promotion ↑ icon never appears:** Pre-Promote requires four conditions now: Trend or Breakout ≥ 60, Pressure crossed 60 in last 90s, |velocity| above half-gate, and velocity accelerating. On low-vol days where Pressure stays neutral or velocity is dead, this combination won't occur. Normal.

**Regime always says "low-vol" even when tickers are moving:** Check that you have at least 4 non-SPY tickers in the active scan. The "stock-specific" detection requires 2+ tickers with ≥3% intraday move out of a population of 4+. With fewer tickers, the detector falls back to SPY-only logic.

**Settings panel missing the v8 Layer Thresholds section:** Hard refresh with Ctrl+Shift+R. If still missing, view-source on the live page and verify `lyTrendThresh` appears in the HTML — if not, the GitHub commit didn't propagate yet.

**Code update not showing:** GitHub Pages caches 30-60 seconds. Hard refresh with Ctrl+Shift+R.

**Audio alarm doesn't play when a candidate promotes:** Click the ▶ Test button in Settings → Audio Alarms. Browser policy requires a user gesture before audio can play. After Test plays once, alarms will fire automatically for the rest of the session.

**Custom sound won't upload:** File must be ≤ 1MB and MP3 or WAV format. If your file is too large, trim it to under 3 seconds using any audio editor (Audacity is free).

**Near-Miss panel always empty:** No tickers have score ≥70 with options-gate failures or velocity issues. On low-vol or low-volume sessions this is normal.

---

## Part 11 — Data safety

All API keys, sound files (as base64 data URLs), trading data — stored in browser localStorage only. Never transmitted except directly to Tradier/Schwab API endpoints. Repository contains no keys.

The audio file you upload stays in your browser. If you clear site data, your custom sound is also cleared and you'll need to re-upload it.

**MomScanner must remain open during the trading session.** All session data — transitions log, active candidates, velocity history, layer stability windows — is held in browser memory and periodically saved to localStorage. Closing the tab mid-session is safe (data persists), but any active CSV export must be completed before closing the tab.

ThinkorSwim deep-links open in **new tabs** (`target="_blank"`) precisely so MomScanner is never accidentally replaced. Click as many ticker symbols as you want. Tab 1 stays MomScanner.

---

## Part 12 — Roadmap

Pending features for future versions:

1. **Alpaca L2 integration** — true Order Flow Imbalance with real bid/ask classification (replaces L1 OFI proxies for the Pressure layer).
2. **Schwab token auto-refresh.**
3. **Multiple custom sounds** — assign different sounds per layer (e.g., Bell for Trend, Chime for Breakout, Tick for Pressure).
4. **Browser desktop notifications** — system tray alerts when MomScanner tab is in the background.
5. **Spread trend indicator** — widening vs tightening over last 5 minutes.
6. **Multi-day summary archive browser.**
7. **Auto-export at 4:00 PM** — automatic CSV + PDF.
8. **Per-ticker notes** — annotation field.
9. **Backtest mode** — replay sessions from CSVs (would let us validate v8 velocity gate against May 1 data).
10. **Voice narration option** — short spoken phrase like "INTC, Trend, Bull" instead of a sound effect.
11. **Configurable broker links** — choose between TOS, TradingView, Webull, etc. for ticker click destination.
12. **Velocity sparkline column** — tiny chart of velocity over last 5 minutes alongside the cents/min number.
