# MomScanner v6

Real-time momentum scoring terminal with L1-aware scoring, bulletproof persistence, time-of-day adaptive thresholds, late-day breakout detection, market regime classification, momentum-type tagging, end-of-session reporting, and an explicit "don't trade today" warning system.

## What's new in v6

- **Volume Pressure rewrite** — the VP component no longer relies on the bid/ask position proxy (which was unreliable on L1 due to potentially-stale snapshots). Instead it tracks tick-direction (last price up/down vs previous poll) volume-weighted over a 30-second sliding window. Cleaner and more honest signal on L1 data.
- **Score rebalancing for L1 reality** — default weights re-tuned. Volume Pressure dropped to 10% (was 30%) because L1 makes the proxy noisy. Relative Volume and Price vs EMA boosted to 26% each. Volatility Expansion and Options Activity now 19% each. The 70% of the score that comes from daily-aggregate fields (RV, PE, VE) is the most reliable on L1 and now dominates.
- **Don't-Trade warning banner** — prominent red banner appears when the regime is low-vol or choppy AND no candidate has lasted >30 seconds in the last hour. Tells you explicitly when the market isn't producing tradable setups, instead of leaving you to figure it out from oscillating candidates.
- **Low-vol close-window override** — on low-vol days, the close-window thresholds no longer loosen. Midday-strict thresholds apply throughout the close window because late-day flickers in low-vol environments are even less reliable than usual.
- **Bug fix: momentum type at promotion time** — `updateMomentumType` now runs BEFORE `updateStability` so the type column populates the moment a candidate appears, not after demotion (Monday's session showed types only attached after demotion).
- **Bug fix: breakout detector memory bound** — added a hard cap on the long-window price array to prevent memory bloat over multi-hour sessions.
- **Honesty fixes** — feed label corrected from "Tradier L2" to "Tradier L1". All references in the UI and documentation updated to reflect actual data tier.

## What carried over from v5

- Bulletproof persistence (every poll and transition saves immediately, heartbeat, session detection)
- Time-of-day adaptive tuning
- Acceleration section + consolidation breakout detector
- Market regime indicator
- Momentum-type classifier (DRIFT / THRUST / REVR)
- Flip counter warning icon
- End-of-session summary report

## What carried over from v4 / v3

- Two-stage candidate classification (raw + stability gate)
- Streak column, Flips column, Session Log
- Two-tier layout, action dots, sparklines, confidence fade, slide-out settings
- Penny Pilot whitelist, live options spread/OI columns with auto-hide
- Schwab + Tradier dual-feed support

---

## Part 1 — The L1 Honesty Layer

### Why this matters

In prior conversations I was operating under the (incorrect) assumption that your Tradier feed included Level 2 data. After review of Tradier's actual documentation, your feed is Level 1 only — meaning:

- **Quote snapshots, not streams.** Each `bid`, `ask`, and `last` field is the most recent value at the moment your poll request was answered. The bid and ask may have refreshed at slightly different timestamps than the last trade.
- **No tick-by-tick time-and-sales.** L2 would give you every individual print with a flag indicating whether it hit bid or ask. L1 gives you only daily aggregates.
- **No order book depth.** L2 would include bid/ask sizes at multiple price levels. L1 gives you only top-of-book bid/ask sizes.

### What this changed

The original Volume Pressure component (30% of v5 score) relied on a proxy: "where in the bid-ask spread did the last trade print" — close to ask = buying, close to bid = selling. With L1's potentially-stale bid/ask snapshots, this proxy was producing false direction flips. Monday's session showed the symptom clearly: NVDA at high volume oscillating in/out of candidate status because the VP component was flipping based on quote timing rather than actual market activity.

### What v6 does about it

Two changes implemented as Option A + Option B from our discussion:

**Option A (immediate rebalance):** Default score weights changed.
- Old (v5): VP 30, RV 20, PE 20, VE 15, OA 15
- New (v6): VP 10, RV 26, PE 26, VE 19, OA 19

The 20-point reduction in VP gets distributed: +6 to RV, +6 to PE, +4 to VE, +4 to OA. The two daily-aggregate components (RV and PE) get the largest boost because they're the most reliable on L1.

**Option B (proper rewrite):** The VP component itself was rewritten to no longer use the bid/ask proxy. Instead it uses tick-direction volume weighting:

1. Each poll cycle, compare current `last` to the previous poll's `last`. Sign = +1 (up), -1 (down), 0 (flat).
2. Compute the volume delta since the last poll.
3. Push `{sign, volDelta}` into a rolling 30-second buffer.
4. Sum signed volume across the buffer, divide by total volume, clamp to ±1.
5. Convert to a 0-100 score via `50 + ratio*40`.
6. Blend in 30% direction-arrow signal for continuity.

This relies only on the `last` field (the most reliable L1 data point) and the daily volume counter. No bid/ask timing dependencies.

### What this means for trading

Your scores will be slightly different on the same data than they were in v5, but more accurate. Specifically:
- Stocks with genuine sustained momentum will score similarly to before
- Stocks that were oscillating in v5 due to quote-timing noise will be more stable in v6
- The candidate flip rate should drop noticeably on choppy days

You may want to lower your score threshold from 75 to 73 or 72 to compensate for the slight average-score reduction caused by the lower VP weight. Test for a few sessions before deciding.

---

## Part 2 — The Don't-Trade Warning

### Why this exists

Monday's session produced 17 candidates, none lasting more than 46 seconds, on a low-vol day. The tool was correctly reporting that the market was untradable, but the only signal communicating this was the small "Regime: Low Volatility Drift" text in the corner. Easy to miss.

v6 makes it impossible to miss.

### When it triggers

The warning banner appears when ALL of these conditions are true:
1. Session has been running for at least 60 minutes (so we have enough data to evaluate)
2. Regime is `low-vol` OR `choppy`
3. In the last 60 minutes, NO candidate (across all tickers) lasted ≥30 seconds

OR alternatively:
1. Session running 90+ minutes
2. Regime is `low-vol` or `choppy`
3. ZERO transitions in the last 60 minutes (truly dead market)

### What it looks like

Bright red banner above the table with a pulsing glow effect: "⚠ Today may not be tradable" with a subtitle telling you the specific stats (e.g., "23 transitions in last hour, longest candidacy 11s. Sitting out is a valid choice.").

### What you should do when you see it

The warning is exactly what it says: an opinion that today is unlikely to produce profitable trades for your strategy. Options to consider:
- **Sit out.** Close MomScanner and come back tomorrow.
- **Tighten settings.** If you must trade, raise score threshold to 80, raise min streak to 90s, raise min OI to 2000.
- **Switch strategy.** If you have a different strategy that works in low-vol markets (covered calls, theta-positive), switch to that.
- **Dismiss and continue.** Click the Dismiss button to hide the banner. It won't reappear during this session even if conditions persist. The banner does not block any functionality.

### What it explicitly does NOT do

- It doesn't prevent you from trading
- It doesn't change any scoring or thresholds
- It doesn't suppress candidates from appearing if they qualify
- It doesn't reset your transition log

It's a warning, not an enforcement mechanism. Your trading decisions remain entirely your own.

---

## Part 3 — Set up the GitHub repository

(Same as prior versions. If your repo is already set up, skip to step 1.7.)

### 1.1 — Create your GitHub account (skip if you already have one)

1. Go to **https://github.com**.
2. Click **Sign up**, enter email, password, username.
3. Verify your email and complete the puzzle.
4. Pick the free plan.

### 1.2 — Create the repository

1. Top-right **+** icon → **New repository**.
2. Name: `MomScanner`. Visibility: Public. Check "Add a README file."
3. Click **Create repository**.

### 1.3 — Add the index.html file

1. **Add file** → **Create new file**.
2. Name: `index.html`.
3. Paste the entire contents of the v6 index.html.
4. Click **Commit new file**.

### 1.4 — Replace the README

1. Click `README.md` → pencil icon.
2. Delete and paste this README. Commit.

### 1.5 — Enable GitHub Pages

1. **Settings** → **Pages**.
2. Source: Deploy from a branch. Branch: `main` / `(root)`. Save.
3. Wait 1-2 minutes. Refresh. Copy the URL shown.

### 1.6 — First-time launch test

1. Open your MomScanner URL.
2. Click the **gear icon** (top right).
3. Set Feed to **Tradier**, paste your API key, set Environment to **Production**.
4. Click **Save Keys**, then **Test Feed**.
5. A toast should say `Feed OK`.
6. Verify the feed pill now reads "Tradier L1" (not "L2" — this is correct).

### 1.7 — Updating from v5 to v6

1. Go to repo → click `index.html` → pencil icon.
2. Ctrl+A → delete → paste new v6 code → Commit.
3. Wait 30-60 seconds. **Hard refresh: Ctrl+Shift+R**.
4. Your active tickers, history, transitions, settings, and API keys all carry over.
5. **Note:** your saved score weights will retain whatever you had in v5 (default was 30/20/20/15/15). To use the new v6 defaults, click **Reset Defaults** in the Score Weights section of Settings, or manually adjust to 10/26/26/19/19.

---

## Part 4 — Schwab Developer API

(Unchanged from prior versions. Schwab is L1+ depending on tier.)

### 2.1 — Register at developer.schwab.com using brokerage credentials.

### 2.2 — Create app

- Name: `MomScanner`
- Callback URL: your GitHub Pages URL (with trailing slash)
- API Products: Accounts and Trading Production + Market Data Production

### 2.3 — Wait 1-3 business days for approval.

### 2.4 — When approved, paste keys in MomScanner Settings → Schwab fields → Save → Connect Schwab → log in → approve.

---

## Part 5 — thinkorswim web scan filters

(Unchanged from v5.)

### Recommended filters

| Filter | Setting |
|---|---|
| Last | Min: **20** · Max: **500** |
| Volume | Min: **2,000,000** |
| Percent Change | Min: **1.00** (no max) |
| Market Cap | Min: **5000** (M = millions, so 5000 M = $5 billion) |
| Option Volume Index | Min: **1.00** |

**Critical:** include **SPY** in your imported list every time, for regime detection.

### Two scans approach

- **MomScanner-Main**: above filters. Run from 9:30 AM to ~2:30 PM, refresh every 20 min.
- **MomScanner-CloseWindow**: same but Volume ≥ 3M, Percent Change between 0.30 and 3.00, OVI ≥ 1.5. Run at 2:55 PM only, to catch consolidation candidates.

---

## Part 6 — The v6 scoring formula

| Component | Weight (default) | What it measures | Reliability on L1 |
|---|---|---|---|
| Volume Pressure | 10% | Tick-direction volume-weighted over 30s rolling window | Good (rewritten in v6 to not depend on bid/ask timing) |
| Relative Volume | 26% | Today's volume vs 20-day average | Excellent (daily aggregate) |
| Price vs EMA | 26% | Distance from 9-EMA, ATR-normalized | Excellent (uses last + day range) |
| Volatility Expansion | 19% | Today's range vs ATR(14) | Excellent (daily aggregate) |
| Options Activity | 19% | ATM spread tightness + OI quality | Excellent (separate options chain endpoint) |

Score 50 = neutral. 75+ = strong signal. ≤25 = strong opposite. EMA smoothing with configurable lag (default 60s, overridden by ToD when enabled). ΔScr = raw - first-seen, zero lag.

### How VP works in v6 specifically

Each poll cycle, the new `updateTickBuffer` function:
1. Compares current `last` to the previously-recorded `last`. Computes sign (+1/-1/0).
2. Computes volume delta since previous poll.
3. Pushes `{timestamp, sign, volDelta}` into the ticker's tick buffer.
4. Trims buffer to last 30 seconds.

Then `computeRawScore` reads the buffer:
1. Sum `sign × volDelta` across the buffer (signed volume).
2. Sum `|volDelta|` (total volume).
3. Compute ratio = signed/total, clamped to [-1, +1].
4. VP = 50 + ratio × 40, clamped to [0, 100].
5. Blend in 30% of direction-arrow signal for stability.

This means VP only swings strongly when there's **persistent directional volume**. A stock oscillating up-and-down on equal volume produces VP near 50, not the noisy bid/ask-position signal of v5.

---

## Part 7 — Time-of-Day Adaptive Tuning (carried from v5, modified in v6)

### The three windows

**Open (9:30–10:00 AM ET)** — score threshold 80, smoothing 90s, streak 90s, min qual 9/10. Strict.

**Midday (10:00 AM–3:00 PM ET)** — your default settings: score 75, smoothing 60s, streak 60s, qual 8/10.

**Close window (3:00–4:00 PM ET)** — score threshold 65, smoothing 20s, streak 20s, min qual 6/10. Loose, for catching late-day breakouts.

### v6 modification: low-vol override

When the regime is `low-vol`, the close-window overlay is **suppressed**. Instead, the midday-late thresholds apply throughout the close window. This prevents flickering candidates on dead afternoons.

Practical effect: on a low-vol day, the Acceleration section may still appear (breakout detector is independent), but the regular Candidates section will be less generous than it would be on a normal trending day during the close window.

### Disabling ToD entirely

In Settings → Time-of-Day Tuning, uncheck the toggle. Your manual base settings then apply at all times.

---

## Part 8 — How to trade with MomScanner v6

### Pre-market (before 9:30 AM ET)

Open MomScanner (your session resumes from yesterday or starts fresh based on the date check). Run thinkorswim scan. Note pre-market movers but don't paste yet.

### 9:30 AM — Initial setup

Paste thinkorswim results into MomScanner. **Make sure SPY is included.** Don't trade. ToD badge will show "Open" — strict thresholds active.

### 9:30-10:00 — Observation window

All rows in warmup. Regime banner activates within 30 seconds. **Watch the regime classification carefully** — if it's low-vol or choppy from the start, expect the Don't-Trade warning to appear by 10:30 AM.

### 10:00 AM — Midday window opens

ToD shifts to "Midday." Standard thresholds active. Candidates section starts populating. With v6's L1-aware scoring, candidates should be **more stable** than in v5.

### Trading midday candidates

When a ticker appears in Candidates, check:
1. **Streak > 1:30** — sustained qualification
2. **Flips < 4** — no warning icon
3. **Sparkline rising steadily** — not spike-and-flatten
4. **Type tag visible** (now appears at promotion time in v6) — DRIFT preferred, THRUST risky, REVR cautious
5. **No Don't-Trade banner active** — if it's red, reconsider

If all five check out → Robinhood → 2-5 DTE → one strike OTM → limit at midpoint.

### Exit triggers (same as v5)

1. Streak breaks (drops to `—`) → sell at bid
2. Demoted from Candidates → check Session Log → limit sell above bid
3. ΔScr decelerating → take profit
4. Score below 60 → market sell
5. 20-min time stop without 15%+ option move → exit

### 3:00 PM — Close window

ToD shifts to "Close Window." On a normal day, looser thresholds activate and Acceleration section appears. **On a low-vol day (v6 override), close-window thresholds stay at midday-strict**, so don't expect the same flood of late-day candidates that v5 would have produced on a quiet afternoon.

### Trading Acceleration entries

Same rules as v5: faster exits (15-25% target), shorter time stop (5-7 min), skip if Flips ≥ 4.

### 4:00 PM — Session close

Click **Session Summary** to generate the report. Print to PDF. Review takeaways.

---

## Part 9 — Settings reference

All settings via the gear icon (top right). Slide-out drawer.

### Data Source
Tradier or Schwab keys, callback URL, environment selection, OAuth connect.

### Options Liquidity Filter
Penny Pilot toggle, max spread %, min OI, max DTE, options check interval.

### Score Weights (v6 defaults)
- Volume Pressure: **10**
- Relative Volume: **26**
- Price vs EMA: **26**
- Volatility Expansion: **19**
- Options Activity: **19**

### Time-of-Day Tuning (v5)
Toggle. Adapts score thresholds and stability streak by market hour.

### Stability Filter (v4)
- Window: 10 cycles
- Min Qual: 8 of 10
- Min Streak: 60 seconds (overridden by ToD)
- Flip Warn: 8

### Behavior
- Smoothing Lag: 60s (overridden by ToD)
- High Threshold: 75 (overridden by ToD)
- Low Threshold: 25
- Min Refresh: 5 seconds

---

## Part 10 — Troubleshooting

**Don't-Trade banner won't go away:** Click the Dismiss button to hide it for the current session. It will not reappear until you reload the page (or until the conditions change again on a future session).

**Volume Pressure component shows 50 always:** The tick buffer needs at least 2 polls with a volume delta to start producing values. First minute or so after a ticker is added, VP will be 50. After that it should respond. If it stays at 50 indefinitely, the volume field may not be flowing — check Test Feed.

**Score decreased compared to v5 on the same ticker:** Expected. v6 weights VP at 10% instead of 30%, and the new VP is more accurate (less noise). Lower your score threshold to 73 or 72 if you want to preserve similar promotion rates.

**Candidates appear less often than in v5:** Also expected, especially on choppy/low-vol days. The L1-aware scoring is more discerning.

**Type column populates immediately on promotion now:** This is the v6 fix. In v5 it appeared only after demotion.

**Regime banner stuck at "unknown":** SPY isn't in your active scan. Add SPY.

**Session resumed with warning toast:** Heartbeat gap detected. Some transitions in that gap are missing. Continue normally.

**Breakout column shows numbers but no `BRK`:** Range expansion is happening but price hasn't broken out yet. Watch closely.

**Acceleration section empty during close window:** Expected on low-vol days (v6 suppresses the section's looser thresholds). Otherwise, no breakouts have triggered yet.

**Session Summary popup blocked:** Allow popups for your GitHub Pages domain.

**Code update not showing:** GitHub Pages caches 30-60 seconds. Hard refresh with Ctrl+Shift+R.

---

## Part 11 — Data safety

All API keys and trading data stored in browser localStorage only. Never transmitted except directly to Tradier/Schwab API endpoints. Repository contains no keys. Public repo is safe.

The session snapshot stored by v5/v6's persistence layer is comprehensive. To clear all data: gear → clear keys, plus Clear Active, Clear History, and Clear Log buttons. Or clear site data in browser settings.

---

## Part 12 — Roadmap

Still pending features:

1. **Schwab token auto-refresh** before 30-minute expiration
2. **WebSocket streaming** if your data tier supports it (would replace polling)
3. **Sound or browser notification** when a candidate promotes or breakout activates
4. **Spread trend indicator** showing whether ATM spread is widening or tightening
5. **Historical ATR/EMA** from a proper bars endpoint (replaces rolling approximation)
6. **Multi-day summary archive browser** to compare today's session against prior sessions
7. **Auto-export at 4:00 PM** — automatic CSV + PDF generation when the close window ends
8. **Per-ticker notes** — small text field per ticker for your own annotations during the session
9. **Backtest mode** — replay a past session from CSVs to test new settings
10. **Score component breakdown panel** — click a ticker to see live VP/RV/PE/VE/OA values, useful for debugging why a stock is or isn't qualifying
