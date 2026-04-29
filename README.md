# MomScanner v7

Three-layer momentum scanner for thinkorswim companion use, built around VWAP-anchored trend detection and L1-friendly Order Flow Imbalance (OFI) proxies. The single blended score from prior versions is replaced by three independent layer scores that capture different time horizons and signal types. Designed for high-contrast accessibility from the ground up.

## What's new in v7

- **Three-layer architecture** — TREND (slow, 30min-hours, VWAP-driven), BREAKOUT (medium, 5-30min, range expansion), PRESSURE (fast, 30s-5min, OFI proxies). Each layer has its own score, classification, stability gate, and Candidates section.
- **VWAP tracking** — session-cumulative VWAP computed per ticker from price+volume snapshots, with 30-minute slope history. New VWAP column shows price as a percentage relative to VWAP.
- **OFI proxies (L1-friendly)** — three blended proxies replacing v6's tick-direction Volume Pressure: (1) bid-ask quote-position averaged over 60s, (2) volume-rate vs session average, (3) size-weighted decaying tick clusters with burst detection.
- **Three independent Candidates sections** — Trend Candidates (sustained moves), Breakout Candidates (range expansions), Pressure Candidates (aggressive flow). A ticker appears only in its strongest active layer's section.
- **Accessibility-first design** — high-contrast theme is the default (pure black background, pure white text). Three additional themes available (medium contrast, original v6 colors, light mode). Base font size adjustable 11px-22px with all UI elements scaling together. Explicitly designed for users with visual sensitivity.
- **Per-layer stability** — each layer has its own qualifying threshold, rolling window, minimum streak, and flip count. The composite Flip Count column shows the sum across all three layers.
- **Layer-aware row coloring** — when a ticker is in a layer's Candidates section, its row gets a colored left border matching the layer (blue for trend, yellow for breakout, pink for pressure).

## What's removed from v6

- **Single blended score** — replaced by three layer scores. The "Score" column is gone.
- **Single high-threshold setting** — replaced by per-layer thresholds (Settings → Layer Thresholds).
- **EMA-9 component** — redundant with VWAP, removed from primary scoring path.
- **Smoothing lag setting** — each layer now has its own appropriate time constant (5min for Trend, 90s for Breakout, 30s for Pressure).
- **The "Acceleration" section** — redundant with the new Breakout layer Candidates section, which works the same way but is layer-aware.

## What carried over from v6/v5/v4

- Bulletproof persistence (every poll/transition saves immediately)
- Time-of-day adaptive tuning (Open/Midday/Close window)
- Market regime indicator (SPY-driven)
- Don't-Trade warning banner
- Momentum-type classifier (DRIFT / THRUST / REVR)
- End-of-session summary report
- Schwab + Tradier dual-feed support, Penny Pilot whitelist, options liquidity filter

---

## Part 1 — Set up the GitHub repository (same as before)

If your existing MomScanner repo is set up, skip to step 1.7.

### 1.1 — Create your GitHub account if you don't already have one

1. Go to **https://github.com**.
2. Click **Sign up**, enter email, password, username.
3. Verify your email and complete the puzzle. Pick the free plan.

### 1.2 — Create the repository

1. Top-right **+** icon → **New repository**.
2. Name: `MomScanner`. Visibility: Public. Check "Add a README file."
3. Click **Create repository**.

### 1.3 — Add the index.html file

1. **Add file** → **Create new file**.
2. Name: `index.html`.
3. Paste the entire contents of the v7 index.html.
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

### 1.7 — Updating from v6 to v7

1. Go to repo → click `index.html` → pencil icon.
2. Ctrl+A → delete → paste new v7 code → Commit.
3. Wait 30-60 seconds. **Hard refresh: Ctrl+Shift+R**.
4. Your active tickers, history, transitions, settings, and API keys all carry over.
5. **Note:** v7 introduces new state fields (VWAP, layer scores, layer stability) that won't exist in your v6 saved state. The first session after upgrade will rebuild this state from scratch — expect Layer Candidates sections to be empty until tickers accumulate enough VWAP history (typically 5-10 minutes after pasting).

---

## Part 2 — The Three-Layer Architecture

### Why three layers instead of one score?

The single blended score in v3-v6 averaged together fast and slow signals, hiding diagnostic information. A stock could score 65 because it had moderate everything, or because trend was 80 and pressure was 50, or because trend was 50 and pressure was 80. You couldn't tell which.

In v7, each layer is independent. You see exactly what's firing. Your trade decisions can be based on the specific pattern that matters: a sustained trend bounce (trend layer firing alone), a breakout from consolidation (breakout layer firing), or aggressive intraday flow (pressure layer firing). The layers give you diagnostic clarity that a single number can't.

### TREND Layer (slow signal, 30min-hours horizon)

Captures the "3 percent in 3 hours" subtle moves you specifically asked for in our v7 design conversation.

**What it measures:** Whether the stock is in a sustained directional move based on its position relative to VWAP, the slope of VWAP itself, and confirmation from relative volume and percent change.

**Components:**
1. *Price-vs-VWAP, ATR-normalized* (40 points): How many ATRs above or below VWAP is the stock? Sustained price above VWAP = institutional buying. Below = institutional selling.
2. *VWAP slope direction* (15 points): Is VWAP itself rising or falling over the last 30 minutes? Reinforces the directional component.
3. *RVol confirmation* (10 points): Is volume confirming the directional bias?
4. *PctChg reinforcement* (10 points): Is the day's overall change consistent with the layer's signal?

**Smoothing:** 5-minute time constant. Trend changes slowly by design.

**Default qualifying threshold:** 65, with 120-second minimum streak. Requires sustained confirmation before promoting to a Trend Candidate.

### BREAKOUT Layer (medium signal, 5-30min horizon)

Captures range expansion patterns where a stock has been consolidating and starts breaking out.

**What it measures:** Combination of v6's consolidation-breakout detector (last 5 min range vs prior 25 min range), VWAP-derived band breaks (price escaping ±1.5 standard deviations of recent VWAP), and volume confirmation.

**Smoothing:** 90-second time constant. Faster than trend, slower than pressure.

**Default qualifying threshold:** 70, with 30-second minimum streak. Breakouts can be valid quickly, but require some sustainment to qualify.

### PRESSURE Layer (fast signal, 30s-5min horizon)

Captures aggressive intraday order flow — moments when buying or selling is dominant for short windows.

**What it measures:** Three OFI proxies blended together. None is reliable individually on L1 data, but the combination produces a robust pressure read.

**Proxies:**
1. *Quote-position OFI averaged over 60s* (40 points): Where in the bid-ask spread are recent prints landing? Average over 60s smooths out the per-tick timing noise that hurt v5's Volume Pressure.
2. *Volume-rate OFI* (30 points): Is recent volume rate (last 60s) much higher than session average? Combined with directional bias to amplify or dampen.
3. *Size-weighted tick clusters with burst detection* (30 points): Sum of `sign × sqrt(volDelta) × decay` over the tick buffer. Plus an extra burst bonus when 5+ same-direction ticks happen within 10 seconds (potential institutional sweep).

**Smoothing:** 30-second time constant. Fast layer needs to respond quickly.

**Default qualifying threshold:** 72, with 15-second minimum streak. Pressure events are short-lived by nature.

### How the three layers interact

Each layer has its own classification (warmup → watch → bull/bear). A ticker can be:
- A Trend Candidate AND a Pressure Candidate simultaneously (sustained trend + aggressive flow now)
- A Breakout Candidate only (consolidation just broke)
- In Watching (no layer qualifies)
- In Warmup (less than 3 minutes of data)

The UI shows each ticker in only one section based on priority: **Pressure > Breakout > Trend > Watching**. The fastest signal wins for placement, because Pressure events are usually the trade trigger — if Pressure is firing, that's what you act on first. The other layer scores are still visible in the row's score columns, so you see the full picture.

### How VWAP is incorporated across layers

VWAP isn't one signal — it appears in different forms across all three layers:

- **Trend layer:** Uses VWAP position (price-vs-VWAP) and VWAP slope (rising/falling over 30 minutes) as primary signals.
- **Breakout layer:** Uses VWAP-derived bands (±1.5 standard deviations of recent VWAP history) as breakout boundaries.
- **Pressure layer:** Doesn't use VWAP directly. Pressure is short-horizon and OFI-driven.

This is intentional. VWAP is a slow indicator — it's most reliable for confirming sustained moves. Using it for the fast pressure layer would dampen pressure signals unnecessarily.

### How OFI proxies work specifically

True Order Flow Imbalance requires Level 2 streaming data. We can't get that on Tradier L1. The three proxies approximate it:

**Proxy 1 — Quote-position averaged over 60s.**
Where in the bid-ask spread do trades land? Trades at ask = buying. Trades at bid = selling. v5 used per-tick bid-ask position, which was noisy because bid/ask snapshots don't refresh in perfect sync with last-trade snapshots. v7's fix: average the position over the last 60 seconds. Individual snapshot timing errors cancel out in the average.

**Proxy 2 — Volume-rate OFI.**
Compare recent volume rate (last 60s) to session-average volume rate. If recent rate is 3x average, something is happening. Combined with direction (from tick buffer), this tells whether aggressive flow is buy-side or sell-side.

**Proxy 3 — Size-weighted decaying tick clusters with burst detection.**
For each tick in the buffer, weight the sign by sqrt(volume delta). Apply exponential decay so recent ticks count more (half-life ~14s). Add a bonus when 5+ same-direction ticks happen within 10 seconds (potential institutional sweep).

All three feed into the Pressure score. The exact blend is documented in `computePressureScore` in the source code.

---

## Part 3 — Accessibility (v7)

### Why this is foundational

If column headers are too faint to read against the background, none of the rest of the tool matters. v7 makes accessibility a first-class concern.

### The four themes

- **High Contrast (default):** Pure black background, pure white text. Brightened accent colors (yellow for accent, brighter green/red for direction). All text uses --text (white), --text-dim (very high contrast light gray), or --text-faint (still readable). Recommended for visual sensitivity.
- **Medium Contrast:** Slightly less harsh than high contrast. Off-white text on near-black background. Brightened accents but not as aggressive.
- **Original v6:** The exact theme from v6, for users who prefer it.
- **Light:** White background, black text. Uses darker accents that work on light backgrounds. Useful in bright environments.

### Font size scaling

The base font size is adjustable from 11px to 22px in 1px increments. All UI text scales together — column headers, ticker symbols, score numbers, table cells, settings labels, badges, everything. Tables grow taller, badges grow proportionally, layout adapts.

The system uses CSS calc() with a single `--font-base` variable, so there are no orphan sizes that don't scale.

### How to change accessibility settings

1. Click the **gear icon** (top right).
2. Scroll to **Accessibility (v7)** section.
3. Pick a theme from the dropdown — preview applies immediately.
4. Drag the **Base Font Size** slider — preview applies immediately.
5. Click **Save Accessibility** to persist your choices to localStorage.

Settings persist across browser refreshes and survive the v7→v8 upgrade in the future.

### Recommended for post-eye-surgery users

Use **High Contrast** theme with base font size **17px or 18px**. The grid expands proportionally and column headers become large enough to read at a glance.

---

## Part 4 — Schwab Developer API (unchanged from prior versions)

### 4.1 — Register at developer.schwab.com using brokerage credentials

### 4.2 — Create app

- Name: `MomScanner`
- Callback URL: your GitHub Pages URL (with trailing slash)
- API Products: Accounts and Trading Production + Market Data Production

### 4.3 — Wait 1-3 business days for approval

### 4.4 — When approved, paste keys in MomScanner Settings

In MomScanner, gear icon → Schwab fields → paste App Key and App Secret → Save Keys → change Feed dropdown to Schwab → Connect Schwab → log in → approve.

---

## Part 5 — thinkorswim web scan filter

(Unchanged from v6.)

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
- **MomScanner-CloseWindow**: same but Volume ≥ 3M, Percent Change between 0.30 and 3.00, OVI ≥ 1.5. Run at 2:55 PM only, to catch consolidation candidates that may break out in the close window.

---

## Part 6 — How to trade with v7

### Pre-market

Open MomScanner. Run thinkorswim scan. Note pre-market movers but don't paste yet.

### 9:30 AM — Initial setup

Paste thinkorswim results. **Make sure SPY is included.** Don't trade. ToD badge will show "Open" — strict thresholds active. All three layers in warmup.

### 9:30-10:00 — Observation window

Layer scores initialize to 50 and start moving. VWAP tracking begins accumulating. Regime banner activates within 30 seconds. None of the three layer Candidates sections will populate this early — they all need at least 3 minutes of warmup plus stability gate.

### 10:00 AM — Midday window

ToD shifts to "Midday." Layer scores have meaningful data. Trend Candidates may start appearing as VWAP positioning sustains. Pressure Candidates may flicker briefly during high-volume moments.

### Trading midday — reading the layers

When a ticker appears in a Candidates section, the section it appears in tells you the type of trade:

**Trend Candidate** (blue left border) — sustained move. Examples: a stock holding above VWAP for 30+ minutes with rising VWAP slope. Trade like a position trade: target 25-50% on the option, hold for 15-30 minutes, exit when trend layer score drops or VWAP slope flattens.

**Breakout Candidate** (yellow left border) — range expansion happening now. Trade with tighter targets: 20-30% on the option, 10-15 minute hold. Exit when breakout score drops below 60 or price re-enters the prior range.

**Pressure Candidate** (pink left border) — aggressive flow right now. The fastest, most volatile setup. Trade only if you can fill within seconds. Target 15-25%, exit within 5 minutes.

### Trading checklist (any layer)

Before entering, verify:
1. **Score in the qualifying layer is 65+** (Trend) or 70+ (Breakout) or 72+ (Pressure)
2. **Streak column shows sustained time** (1:30+ for Trend, 30s+ for Breakout, 15s+ for Pressure — all minimum stability gate values)
3. **Flips column < 4** (no warning icon)
4. **No Don't-Trade banner** active
5. **VWAP column matches your direction** (positive % for calls, negative for puts)
6. **Spread% ≤ 5%** (tight enough for tradable options)
7. **Type tag visible** (DRIFT preferred for Trend setups, THRUST acceptable for Pressure setups, REVR cautious always)

If all check out, place the trade in Robinhood: 2-5 DTE, one strike OTM, limit order at midpoint.

### Exit triggers

1. **Layer score drops below 60** in the qualifying layer → market sell
2. **Streak resets to —** → sell at bid
3. **Demoted from layer Candidates** → check Session Log for reason → limit sell above bid
4. **VWAP relationship inverts** (was positive, now negative for a call trade) → exit
5. **20-min time stop** without 15%+ option move → exit

### 3:00 PM — Close window

ToD shifts to "Close Window." Looser thresholds active for layers that allow it. On a low-vol day, the Don't-Trade override prevents looser thresholds from generating noise.

### 4:00 PM — Session close

Click **Session Summary** to generate the report. Print to PDF. Note which layer produced your best trades for tomorrow's planning.

---

## Part 7 — Settings reference

### Data Source
Tradier or Schwab keys, callback URL, environment selection, OAuth connect.

### Options Liquidity Filter
Penny Pilot toggle, max spread %, min OI, max DTE, options check interval.

### Score Weights (legacy — not used in v7's primary path)
The five weights (VP, RV, PE, VE, OA) only affect the legacy single-score view, which is no longer the primary scoring path in v7. Layer thresholds are the operational controls.

### Time-of-Day Tuning (v5)
Toggle. Adapts thresholds across the three time windows.

### Stability Filter (v4)
- Window: 10 cycles default
- Min Qual: 8 of 10 default
- Min Streak: 60 seconds (overridden by ToD)
- Flip Warn: 8

These apply to the *legacy* single-classification path. v7's layer-specific stability uses its own internal defaults (see Part 2 above).

### Behavior
- Smoothing Lag: 60s (overridden by per-layer time constants in v7)
- High Threshold: 75 (legacy — v7 uses per-layer thresholds)
- Low Threshold: 25
- Min Refresh: 5 seconds

### Accessibility (v7)
Theme picker (4 options) and base font size slider (11-22px). Live preview as you adjust. Click Save to persist.

---

## Part 8 — Troubleshooting

**Layer score stays at 50 indefinitely:** That layer's components don't have enough data yet. Trend needs ~5 minutes of VWAP history. Breakout needs ~25 minutes (it compares short and long ranges). Pressure needs ~30 seconds of tick data. After warmup completes, scores should start moving.

**VWAP column shows "—":** Volume hasn't accumulated yet. VWAP requires at least one volume delta to compute. Wait 1-2 polls.

**No Trend Candidates appearing all day:** The Trend layer requires sustained directional bias — score 65+ AND price-vs-VWAP direction maintained for 120+ seconds. On purely sideways days, this won't fire. That's correct behavior.

**Pressure Candidates flickering rapidly:** Pressure has a 15-second minimum streak by design (fastest layer). On choppy days expect frequent transitions in this layer specifically. The Don't-Trade banner will appear if these are happening with no sustained candidacies.

**Layer score columns hard to read:** Open Settings → Accessibility → bump base font size to 17 or 18. Or pick the High Contrast theme if you're not already on it.

**Theme change doesn't persist:** Make sure to click "Save Accessibility" after picking a theme. Without saving, the preview is live but won't survive a refresh.

**Three layer scores all reading similar values:** Either the ticker is in a balanced state across signals (legitimate), or VWAP/tick data hasn't accumulated enough yet (early in session). Wait or check VWAP column.

**Regime banner stuck at "unknown":** SPY isn't in your active scan. Add SPY.

**Code update not showing:** GitHub Pages caches 30-60 seconds. Hard refresh with Ctrl+Shift+R.

---

## Part 9 — Data safety

All API keys and trading data stored in browser localStorage only. Never transmitted except directly to Tradier/Schwab API endpoints. Repository contains no keys. Public repo is safe.

The session snapshot stored by v5/v6/v7's persistence layer is comprehensive — includes price history, score history, layer states, VWAP state, tick buffers. To clear all data: gear → clear keys, plus Clear Active, Clear History, Clear Log buttons. Or clear site data in browser settings.

---

## Part 10 — Roadmap

Pending features for future versions:

1. **Alpaca L2 integration (v8)** — true Order Flow Imbalance with real bid/ask classification of every print, replacing the L1 OFI proxies. The Pressure layer becomes a genuine first-class signal.
2. **Schwab token auto-refresh** before 30-minute expiration
3. **WebSocket streaming** if your data tier supports it
4. **Sound or browser notification** when a candidate promotes
5. **Spread trend indicator** showing whether ATM spread is widening or tightening
6. **Historical ATR/EMA** from a proper bars endpoint (replaces rolling approximation)
7. **Multi-day summary archive browser** to compare today's session against prior sessions
8. **Auto-export at 4:00 PM** — automatic CSV + PDF generation when the close window ends
9. **Per-ticker notes** — small text field per ticker for your own annotations
10. **Backtest mode** — replay a past session from CSVs to test new settings
