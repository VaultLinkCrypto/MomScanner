# MomScanner v4

Real-time momentum scoring terminal for thinkorswim web scan results. Pulls quotes and live options chain data from Tradier (L2) or Schwab, computes a smoothed 0–100 score per ticker, applies a two-stage stability filter to prevent false-positive candidate flipping, logs every state transition for post-session review, and persists all data to browser local storage.

## What's new in v4

- **Two-stage candidate classification** — raw 6-criteria qualification (Stage 1) is now gated by a stability filter (Stage 2). A ticker must qualify consistently over a rolling window AND hold direction for a minimum streak before promoting to Candidates. Prevents the rapid green/red dot flipping seen on choppy days.
- **Streak column** — shows how long the ticker has been continuously qualifying in its current direction. Resets on any failure or reversal. Format: `45s` or `2:15`.
- **Flips column** — count of state transitions since the ticker was added. Colored amber near warn threshold, red above it. High flip count = choppy ticker, avoid regardless of current dot color.
- **Session Log panel** — every state transition (bull ↔ watch ↔ bear) is logged with timestamp, score, price, spread, and context. Session stats at the top: promotion count, demotion count, average candidate duration, most-flipped ticker.
- **Transition CSV export** — separate export for the full transition log, one row per state change.
- **Stability settings panel** — configurable window size, min qualifying cycles, min streak duration, and flip-count warn threshold. Adjustable live, no code change needed.

## What carried over from v3

- Two-tier layout (Candidates / Watching)
- Action dots (green = calls, red = puts, hollow = tracking, dashed = warmup)
- Inline sparklines (5-minute score trajectory)
- Confidence fade (< 3 min data = faded row)
- Slide-out settings (gear icon)
- Color discipline (red/green only for direction)
- Penny Pilot whitelist (~400 symbols)
- Live options spread % and OI columns with auto-hide
- Smoothed scoring with 5 weighted components
- History archive with CSV export
- Schwab OAuth + Tradier L2 dual-feed support

---

## Part 1 — Set up the GitHub repository (step by step)

### 1.1 — Create your GitHub account (skip if you already have one)

1. Open your web browser and go to **https://github.com**.
2. Click **Sign up** in the top right corner.
3. Enter your email address, create a password, and choose a username.
4. Complete the verification puzzle and click **Create account**.
5. Check your email, click the verification link.
6. Pick the free plan.

### 1.2 — Create the repository

1. Log in to github.com. Click the **+** icon in the top right.
2. Click **New repository**.
3. Fill in:
   - **Repository name:** `MomScanner`
   - **Visibility:** Public
   - **Initialize with:** check **Add a README file**
4. Click **Create repository**.

### 1.3 — Add the index.html file

1. On the repository page, click **Add file** → **Create new file**.
2. Name the file: `index.html`
3. Paste the entire contents of the index.html file.
4. Click **Commit new file**.

### 1.4 — Replace the README

1. Click on `README.md` in the file list.
2. Click the pencil icon.
3. Delete the existing text and paste this README.
4. Click **Commit changes...** → **Commit changes**.

### 1.5 — Enable GitHub Pages

1. Click **Settings** tab.
2. In the left sidebar, click **Pages**.
3. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main** / **/ (root)**
4. Click **Save**.
5. Wait 1–2 minutes. Refresh. Copy the URL shown under "Your site is live at."

### 1.6 — First-time launch test

1. Open your MomScanner URL.
2. Click the **gear icon** (top right).
3. Set Feed to **Tradier**, paste your API key, set Environment to **Production**.
4. Click **Save Keys**, then **Test Feed**.
5. A toast should say `Feed OK`.

### 1.7 — Updating the file later

1. Go to your repo on GitHub.
2. Click `index.html` → pencil icon.
3. Ctrl+A, delete, paste new code.
4. Commit changes.
5. Wait 30–60 seconds. Hard refresh with **Ctrl+Shift+R**.

**Verification:** after committing, open the file and scroll to the bottom. Last line should be `</html>`.

---

## Part 2 — Schwab Developer API setup

### 2.1 — Register

1. Go to **https://developer.schwab.com** → **Register**.
2. Sign in with your brokerage credentials.

### 2.2 — Create an app

1. Dashboard → **Add a New App**.
2. Fill in:
   - **App Name:** `MomScanner`
   - **Description:** `Personal momentum scanning tool`
   - **Callback URL:** your GitHub Pages URL (include trailing slash)
   - **API Products:** Accounts and Trading Production + Market Data Production
3. Submit.

### 2.3 — Wait for approval (1–3 business days)

Use Tradier L2 in the meantime.

### 2.4 — When approved

1. Copy App Key and App Secret from developer.schwab.com.
2. In MomScanner, gear icon → paste both into Schwab fields.
3. Set Callback URL to match exactly.
4. Save Keys → change Feed to Schwab → Connect Schwab.
5. Log in at Schwab → approve → redirected back → toast says "Schwab connected."

### 2.5 — Token refresh

Schwab tokens expire after 30 minutes. Click gear → Connect Schwab again when you see a "token expired" error.

---

## Part 3 — thinkorswim web scan filter

### 3.1 — Set up the scan

1. Log in to **trade.thinkorswim.com** → **Scan**.
2. Create a new scan or edit your existing one.
3. Set **Scan In** to **All Symbols**.

### 3.2 — Add the filters

**Recommended filters (produces ~40-70 symbols):**

| Filter | Setting |
|---|---|
| Last | Min: **20** · Max: **500** |
| Volume | Min: **2,000,000** |
| Percent Change | Min: **1.00** (leave Max blank) |
| Market Cap | Min: **5000** (the M suffix means millions, so 5000 M = $5 billion) |
| Option Volume Index | Min: **1.00** |

**Critical note on Market Cap:** The thinkorswim web scanner displays an "M" suffix next to the value field, meaning the unit is millions. Enter `5000` to mean $5 billion. Entering `5000000000` would mean $5 quadrillion and return zero results.

**Note on Percent Change:** Setting Min to 1.00 with no Max only catches upward movers. To catch both directions, either remove Percent Change entirely and let MomScanner's scoring handle it, or accept the narrower scan.

Do not add any Fundamental Filters.

### 3.3 — Optional thinkScript pre-qualifier

```thinkscript
def atr14 = Average(TrueRange(high, close, low), 14);
def rangeToday = high - low;
def avgVol20 = Average(volume, 20);
def atrExpansion = rangeToday > atr14 * 1.2;
def volSpike = volume > avgVol20 * 1.5;
def pctMove = AbsValue((close / close[1] - 1) * 100) >= 1.5;
plot scan = atrExpansion or volSpike or pctMove;
```

### 3.4 — Running and importing

1. Click **Scan**. Copy ticker symbols from results.
2. Paste into MomScanner → **Add to scan**.
3. Re-scan thinkorswim every 5–15 minutes during the session.

---

## Part 4 — The Stability Filter (v4 core feature)

### Why this exists

On choppy market days, tickers rapidly oscillate across the 6-criteria threshold — qualifying as bull for 2 minutes, dropping, reappearing as bear for 1 minute, dropping again. This makes the Candidates section unreliable. The stability filter requires consistent qualification before promoting.

### Two-stage classification

**Stage 1 (raw qualification):** Does this ticker meet ALL 6 criteria right now?

1. Score ≥ threshold (default 75)
2. Direction arrow sustained (▲ or ▼, not ━)
3. ΔScore positive
4. Spread% ≤ 5%
5. OI ≥ 1,000
6. Rel Vol ≥ 2.0x

**Stage 2 (stability gate):** The raw result is pushed into a rolling window. Promotion requires:

- Qualified in at least **N of the last M cycles** (default: 8 of 10), AND
- Continuously qualifying in the **same direction** for the **minimum streak duration** (default: 60 seconds)

### The four stability settings

Located in gear icon → **Stability Filter (v4)**.

**Stability Window (default: 10)**
Number of recent poll cycles to examine. At 5-second refresh, 10 cycles ≈ 50 seconds.

**Min Qualifying Cycles (default: 8)**
How many of the window cycles must qualify. 8/10 = 80% rate. Set to 10/10 for maximum strictness.

**Min Streak Before Promote (default: 60 seconds)**
Continuous qualification duration required. Most impactful setting.
- **30s** — fast entry on trending days
- **60s** — balanced default
- **120s** — strict, only sustained moves on choppy days

**Max Flip Count Warn (default: 8)**
Flips column turns amber at half this value, red when exceeding it. Visual warning only.

### Tuning guidance

- **Too few candidates** → lower Min Qualifying Cycles to 6, lower Min Streak to 30s
- **Still seeing flipping** → raise Min Qualifying Cycles to 9-10, raise Min Streak to 90-120s
- **Just right** → candidates appear 2-4 times per session, each lasting 3+ minutes

---

## Part 5 — The Streak Column

Shows continuous qualification duration in the current direction.

- `—` = not qualifying
- `45s` = qualifying for 45 seconds
- `2:15` = 2 minutes 15 seconds sustained
- Green text = bull. Red text = bear.

**Trading rules:**
- **Streak < 1:00** — don't trade, move not proven
- **Streak 1:30–3:00** — ideal entry zone, move established but not exhausted
- **Streak > 5:00** — caution, check sparkline for flattening

Streak resets to zero when any criterion fails or direction reverses. Streak dropping from `2:30` to `—` is an exit signal.

---

## Part 6 — The Flips Column

Counts total state transitions since the ticker was added.

- **Gray** — low count, stable
- **Amber** — approaching warn threshold
- **Red** — exceeding threshold, too choppy

**Trading rules:**
- **Flips < 3** — clean mover, trust the signal
- **Flips 3–6** — some oscillation, verify with sparkline
- **Flips > 8** — avoid trading this ticker today

---

## Part 7 — The Session Log

Expandable panel between main table and History.

### What it records

Every state transition: timestamp, ticker, from-state → to-state, smooth score, raw score, price, % change, spread%, relative volume. States labeled: 🟢 BULL, 🔴 BEAR, ○ WATCH, ⌛ WARMUP.

### Session stats

- **Promotions** — total promotions to Candidates
- **Demotions** — total demotions from Candidates
- **Avg Candidate** — average time in Candidates before demotion. Under 30s = choppy day. Over 2 min = trending.
- **Most Flipped** — ticker with most transitions, with count

### Export and management

- **Export Transitions CSV** — full log, one row per transition
- **Reload** — restore from localStorage after a glitch
- **Clear Log** — start fresh

Persists last 2,000 entries in localStorage across refreshes.

---

## Part 8 — How to trade using MomScanner v4

### Before the open

Open MomScanner and thinkorswim side by side. Observe pre-market movers.

### 9:30 to 9:45 — Observation window

Paste thinkorswim results. Don't trade. Everything is in warmup.

### 9:45 to 10:00 — Stability warmup

Raw scores are established. Stability filter needs 60+ seconds of sustained qualification. Candidates section will be empty until ~9:46-9:50 on trending days, possibly later on choppy days. This is by design.

### 10:00 onward — Trading

When a ticker appears in Candidates, check:

1. **Streak > 1:30** — sustained qualification
2. **Flips < 4** — not choppy
3. **Sparkline climbing steadily** — not spike-and-flatten

If all three pass → open Robinhood → nearest 2-5 DTE → one strike OTM → limit order at midpoint.

### Exit triggers

1. **Streak breaks** (drops to `—`) → sell at bid immediately
2. **Demoted from Candidates** → check Session Log for reason → limit sell above bid
3. **ΔScr decelerating** → profit-taking → limit sell at midpoint
4. **Score below 60** → sell at market
5. **Time stop: 20 minutes** without 15%+ option move → sell

### Post-session review

1. Export Transitions CSV and Active CSV
2. For each trade: find promotion and demotion transitions, calculate duration
3. Check Avg Candidate stat — under 1 min means tighten stability for tomorrow, over 3 min means you can loosen for faster entry

---

## Part 9 — Scoring formula

| Component | Weight | Source |
|---|---|---|
| Volume Pressure | 30% | Uptick/downtick proxy + 30s direction |
| Relative Volume | 20% | Today's volume vs 20-day average |
| Price vs EMA | 20% | Distance from 9-EMA, ATR-normalized |
| Volatility Expansion | 15% | Range vs ATR(14) |
| Options Activity | 15% | ATM spread tightness + OI quality |

Score 50 = neutral. 75+ = strong signal. ≤25 = strong opposite. Smoothing via EMA (default 60s lag). ΔScr = raw − first-seen, zero lag.

---

## Part 10 — Options Liquidity Filter

- **Penny Pilot Only** (default ON): rejects non-whitelisted tickers at paste
- **Max Spread %** (default 15%): auto-hides wide-spread tickers. Green ≤5%, amber 5-15%, coral >15%
- **Min OI** (default 500): auto-hides low open interest
- **Max DTE** (default 14): picks nearest expiration within window
- **Check Interval** (default 60s): options chain poll frequency

---

## Part 11 — Troubleshooting

**No candidates all day:** Lower Min Qualifying Cycles to 6, Min Streak to 30s. Check thinkorswim scan is producing results.

**Candidates appear then vanish in seconds:** Stability filter working correctly. Don't chase. Lower Min Streak only if market is clearly trending.

**Session Log shows rapid transitions:** Choppy day. Raise Min Streak to 90-120s. Trade only tickers with Flips < 3.

**Streak shows time but no green/red dot:** Ticker is qualifying raw (Stage 1) but hasn't met the stability window (Stage 2). Wait for window to fill.

**Feed errors:** Re-paste API key, ensure Production environment, Test Feed.

**Scores at 50:** Ensure Tradier Production, not Sandbox.

**Schwab OAuth fails:** Callback URL must match exactly including trailing slash.

**Update not showing:** Hard refresh with Ctrl+Shift+R.

---

## Part 12 — Data safety

All API keys stored in browser localStorage only. Never transmitted except to Tradier/Schwab API endpoints directly. Repository contains no keys. Public repo is safe. On shared computers, clear keys when done.

---

## Part 13 — Roadmap

1. End-of-session summary report
2. Regime indicator (trending/choppy/low-vol banner based on SPY)
3. Momentum-type classifier (thrust vs drift)
4. L2 WebSocket streaming
5. True buy/sell volume pressure from Time & Sales
6. Schwab token auto-refresh
7. Sound/browser notification on candidate promotion
8. Spread trend indicator (widening vs tightening)
9. Historical ATR/EMA from chart API
