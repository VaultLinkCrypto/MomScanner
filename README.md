# MomScanner v5

Real-time momentum scoring terminal with bulletproof persistence, time-of-day adaptive thresholds, late-day breakout detection, market regime classification, momentum-type tagging, and end-of-session reporting. Built on top of v4's stability filter and session log foundation.

## What's new in v5

- **Bulletproof persistence** — every poll cycle and every state transition saves to localStorage immediately. A mid-session GitHub deploy, browser refresh, lock screen, or laptop lid close no longer loses your session. Includes heartbeat detection that warns when an outage occurred.
- **Time-of-day adaptive tuning** — score thresholds and stability requirements automatically adjust based on the market hour: strict at the 9:30 open (avoid noise), default midday, loose in the 3:00-4:00 PM close window (catch INTC-style late-day moves).
- **Acceleration section** — a new third tier above Candidates appears only during the close window, populated by tickers showing consolidation-breakout patterns. These are the late-day moves that slip past standard criteria.
- **Consolidation breakout detector** — continuously compares the last 5 minutes of price action to the prior 25 minutes. When range expands and price breaks out of the consolidation, a "Brk" badge appears.
- **Market regime indicator** — banner at the top classifies the day from SPY's behavior over a rolling 30 minutes: trending-bullish, trending-bearish, choppy, low-volatility, or mixed. Stability filter auto-tightens on choppy days and loosens on trending days.
- **Momentum-type classifier** — labels each candidate as DRIFT (steady, ideal for OTM options), THRUST (sharp short move, risky entry), or REVR (direction reversal after prior move).
- **Flip counter warning icon** — a red `!` badge appears next to the ticker name when flip count exceeds threshold, visible even inside Candidates as a passive caution.
- **End-of-session summary report** — generates a one-page HTML report (printable to PDF) with all session stats, top candidates, most-flipped tickers, regime breakdown, and contextual takeaways.
- **Session boundary detection** — recognizes when a saved snapshot is from a previous trading day and starts a fresh session automatically.

## What carried over from v4

- Two-stage candidate classification (raw qualification + stability gate)
- Streak column and Flips column
- Session Log with full transition history and CSV export
- Transition CSV export
- Stability settings (window, min qual cycles, min streak, flip warn)

## What carried over from v3

- Two-tier layout, action dots, sparklines, confidence fade, slide-out settings, color discipline
- Penny Pilot whitelist
- Live options spread/OI columns with auto-hide
- Smoothed scoring with 5 weighted components
- Schwab + Tradier dual-feed support

---

## Part 1 — Set up the GitHub repository

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
3. Paste the entire contents of the v5 index.html.
4. Click **Commit new file**.

### 1.4 — Replace the README

1. Click `README.md` → pencil icon.
2. Delete and paste this README. Commit.

### 1.5 — Enable GitHub Pages

1. **Settings** → **Pages**.
2. Source: Deploy from a branch. Branch: `main` / `(root)`. Save.
3. Wait 1-2 minutes. Refresh. Copy the URL shown.

### 1.6 — Updating later

1. Go to repo → click `index.html` → pencil icon.
2. Ctrl+A → delete → paste new code → Commit.
3. Wait 30-60 seconds. **Hard refresh: Ctrl+Shift+R**.

**v5 advantage:** thanks to bulletproof persistence, mid-session deploys no longer lose your session data. After Ctrl+Shift+R, MomScanner restores all active tickers, scores, streaks, flips, and transition history exactly where you left off.

---

## Part 2 — Schwab Developer API

### 2.1 — Register at developer.schwab.com using your brokerage credentials

### 2.2 — Create app

- Name: `MomScanner`
- Callback URL: your GitHub Pages URL (with trailing slash)
- API Products: Accounts and Trading Production + Market Data Production

### 2.3 — Wait 1-3 business days for approval

### 2.4 — When approved

1. Copy App Key + App Secret from developer dashboard.
2. In MomScanner: gear icon → paste both → set Callback URL → Save Keys.
3. Change Feed dropdown to Schwab → Connect Schwab → log in → approve.
4. You'll be redirected back; toast says "Schwab connected."

### 2.5 — Token refresh

Tokens expire after 30 min. Click gear → Connect Schwab again when needed.

---

## Part 3 — thinkorswim web scan filter

### 3.1 — Set up the scan

1. trade.thinkorswim.com → **Scan** → new or existing scan.
2. Set **Scan In** to **All Symbols**.

### 3.2 — Recommended filters

| Filter | Setting |
|---|---|
| Last | Min: **20** · Max: **500** |
| Volume | Min: **2,000,000** |
| Percent Change | Min: **1.00** (leave Max blank) |
| Market Cap | Min: **5000** (M suffix means millions, so 5000 M = $5 billion) |
| Option Volume Index | Min: **1.00** |

**Critical Market Cap note:** the field shows an "M" suffix meaning millions. Enter `5000` for $5B, NOT `5000000000`.

**v5 recommendation: ALWAYS include SPY in your imported list.** The regime indicator depends on SPY price data flowing through the active scan. Without SPY, the regime banner stays at "unknown" and stability auto-adjustment can't activate.

### 3.3 — Running and importing

1. Click **Scan**. Copy ticker symbols.
2. Paste into MomScanner → **Add to scan**.
3. **Add SPY** if not already in your thinkorswim watchlist.
4. Re-scan thinkorswim every 5-15 minutes during the session.

---

## Part 4 — Bulletproof Persistence (v5 core)

### What it solves

In v4, the transition log saved to localStorage every 20 entries, and the active ticker list was stored as just a list of symbols. This meant:
- A mid-session page refresh restarted every ticker's 3-minute warmup
- A browser crash could lose up to 19 transitions
- A GitHub Pages deploy mid-session wiped working state
- A laptop lid close or Windows lock had no recovery indicator

### What v5 does

**Every poll cycle** writes a complete state snapshot to localStorage including all ticker fields (scores, price history, score history, stability window, streak state, flip count, options data, momentum type, breakout state).

**Every single transition** writes immediately to the transition log — zero tolerance for data loss between transitions.

**Every 15 seconds** a heartbeat writes the current timestamp to a dedicated localStorage key.

**Every 30 seconds** even when paused or idle, the full state saves as a safety net.

**On page load**, MomScanner restores every ticker's complete state — preserving `firstSeen` timestamps so warmup periods don't restart, and resuming the rolling stability windows mid-stream. If the heartbeat shows a gap greater than 5 minutes from the last alive timestamp, a toast warns you that some data in that window may be missing.

**Session boundary detection** checks the date stamp of the saved snapshot. If it's from a previous day or older than 12 hours, MomScanner starts a fresh session automatically and shows a toast explaining what happened.

### What this means for your workflow

You can now:
- Deploy code updates mid-session without losing data
- Lock your computer for lunch and return without restarting
- Recover from a browser crash with at most 30 seconds of lost state
- Run multi-day continuous sessions if you want (each market day starts fresh)

### Safety constraints

- localStorage has a ~5-10 MB limit per domain. The full state snapshot is small (typically under 100 KB even with 100 active tickers), so this isn't a concern in practice.
- If localStorage somehow fills up, console warnings will appear but the app continues running on in-memory state.

---

## Part 5 — Time-of-Day Adaptive Tuning (v5)

### Why this exists

Your INTC observation revealed it: morning momentum and late-day momentum are structurally different. A score threshold tuned for 10:30 AM breakouts is too strict for 3:30 PM re-accelerations, and vice versa. v5 applies different settings automatically based on ET time.

### The three windows

**Open (9:30–10:00 AM ET)** — score threshold raised to 80, smoothing lag 90s, min streak 90s, min qualifying cycles 9. The market is at its noisiest, spreads are widest, signals are least reliable. Strict thresholds keep junk out.

**Midday (10:00 AM–3:00 PM ET)** — your default settings: score 75, smoothing 60s, streak 60s, 8/10 qualifying. Standard momentum trading window.

**Close window (3:00–4:00 PM ET)** — score threshold lowered to 65, smoothing lag 20s, min streak 20s, min qualifying cycles 6. Late-day moves are short and need fast signals. The 3:30-4:00 PM acceleration that drove INTC qualifies under these settings but never under the default.

### How to control it

Settings → **Time-of-Day Tuning (v5)** has a single toggle: enable adaptive thresholds. Default is ON. When OFF, your manual settings apply at all times.

The header shows a "ToD: [window]" badge so you always know which set of thresholds is currently active. The badge updates automatically every minute.

### Trade behavior implications

- **Don't be alarmed if Candidates is empty 9:30-10:00.** Strict open window settings deliberately avoid promotions in the noisy first 30 minutes.
- **Expect more candidates in the close window.** Looser settings + acceleration section + breakout detection all activate at 3:00 PM. This is when MomScanner is most aggressive.
- **Manual override** — if you want loose settings all day, disable ToD tuning and lower your base thresholds. If you want strict all day, disable ToD and raise them.

---

## Part 6 — Consolidation Breakout Detector & Acceleration Section (v5)

### What the breakout detector does

For every ticker on every poll, MomScanner maintains two rolling price windows: the last 5 minutes (short) and the last 30 minutes (long). It computes:

1. **Range ratio** — short-window range divided by long-window range (excluding the short window itself, so the long window is the "consolidation" baseline)
2. **Price position** — is the current price outside the long-window high/low?
3. **Move from average** — how far is current price from the long-window mean?

A score is built from these signals (range ratio ≥1.5 → +30 points, ≥2.5 → +20 more, price outside range → +30, move from avg ≥0.5% → +10, ≥1.5% → +10 more). When the breakout score reaches 60 with price actually outside the range, the ticker is flagged as an active breakout.

### The Brk column

Shows the breakout state as a small badge:

- **`BRK`** in solid amber — active breakout, score ≥ 60 with price outside range. This is the trade signal.
- **Number 30-59** in faded amber — building breakout, range expanding but price still in range. Watch closely.
- **`—`** — no breakout signal, normal consolidation behavior.

Hover the badge for the breakout direction (up or down) and exact score.

### The Acceleration section

A new top-tier section above Candidates that appears **only during the close window (3:00-4:00 PM ET)**. It contains tickers with active breakouts (Brk = BRK badge) that aren't already in Candidates. This is critical because:

- A breakout often triggers before the standard 6-criteria check would qualify the ticker.
- During the close window, most of the move could be over by the time stability gates clear.
- Acceleration entries are intentionally fast — you trade them with tighter exits.

The Acceleration section sorts by breakout score (not smooth score). Rows have an amber left-border to visually distinguish them from regular candidates.

### How to trade Acceleration entries

These are different from regular Candidates:

- **Confirmation needed** — verify the breakout is real (price clearly outside range, volume picking up) before entering.
- **Tighter exits** — set a profit target of 15-25% on the option, NOT the 50%+ you might wait for on a midday candidate. Late-day moves don't last.
- **Time stop is shorter** — if it's not working in 5-7 minutes, exit. There's not enough session left to wait.
- **Skip if Flips ≥ 4** — the ticker has been choppy today, don't trust the breakout.

---

## Part 7 — Market Regime Indicator (v5)

### What it does

The regime banner at the top of the screen classifies today's market based on SPY's last 30 minutes of price action. Five possible states:

- **Trending Bullish** — SPY net up ≥0.6% with limited reversals. Stability streak requirement auto-loosens to 0.75x (45s instead of 60s) for faster entries.
- **Trending Bearish** — same as above but downward.
- **Choppy** — many direction reversals in the window. Stability streak auto-tightens to 1.5x (90s instead of 60s) to filter out noise. Detail text reminds you to trade only high-conviction setups.
- **Low Volatility Drift** — tight range, small net move. Detail text warns that momentum trades may be scarce.
- **Mixed** — some movement but not clearly trending or choppy. Default settings.

### Requirements

- **SPY must be in your active scan**. The regime detector reads SPY's price from the regular quote feed.
- **At least 6 SPY data points** are needed (around 30 seconds of polling) before classification activates.
- The banner shows "unknown · Tip: Add SPY to the scan for market regime detection" until SPY data flows.

### How it changes behavior

When the regime is choppy or trending, your effective stability streak duration is automatically multiplied (1.5x for choppy, 0.75x for trending). This is a passive overlay — your saved Stability settings aren't changed, just the values used for runtime calculations. The regime confidence (0-100%) is shown in the detail text.

### Trading guidance by regime

- **Trending bullish/bearish** — bias toward your dominant-direction trades (more calls in trending-bull, more puts in trending-bear). Faster promotions mean earlier entries.
- **Choppy** — be picky. Most candidates will be traps. Look for high Streak (90s+), low Flips (≤2), and DRIFT momentum type.
- **Low-vol** — consider sitting out. Premium decay will be your enemy on quiet days.
- **Mixed** — trade as normal but maintain extra discipline on exits.

---

## Part 8 — Momentum Type Classifier (v5)

### What it does

For each ticker that's currently a candidate (bull or bear), MomScanner examines the score's recent velocity and total movement to assign one of three types:

**DRIFT** — score climbed steadily over 3+ minutes, with moderate velocity (under 8 points/minute). Total gain is at least 6 points across the 5-minute window. This is the slow-and-steady pattern that gives you time to find a strike, fill at midpoint, and ride the move. **Ideal for your $100 OTM strategy.**

**THRUST** — score spiked rapidly (8+ points/minute) with a total gain ≥12 points. This is a sharp short-lived move, often news-driven. Risky for retail entries because by the time you can fill an OTM option, the move may have already exhausted itself. **Trade only if you can fill within seconds.**

**REVR (Reversal)** — current candidacy follows a recent direction reversal (flip count ≥ 2). The momentum is real but the prior counter-direction move may have set up a snap-back. Higher risk/reward profile. **Only for experienced moves.**

### How to use it

The Type column in the table shows a small colored badge with the type abbreviation. Hover for the score velocity in points/minute.

Trading guidance:
- **DRIFT** — primary entry candidates. Take these with confidence.
- **THRUST** — only enter if you can fill an option order in under 30 seconds AND the spread is tight.
- **REVR** — verify with a recent sparkline showing the prior reversal pattern. Skip if uncertain.

The session summary at end-of-day shows a count of each type encountered, helping you correlate which types produced your best trades.

---

## Part 9 — End-of-Session Summary Report (v5)

### How to generate

Click the **Session Summary** button in the table footer (next to Export CSV). A new browser window opens with a one-page report.

### What's included

**Stats tiles:** tickers tracked, total transitions, promotions, demotions, average candidate duration, longest candidate, peak score across all tickers, momentum-type breakdown (drift/thrust/reversal counts).

**Top 10 longest-running candidates table:** each ticker with total time spent in candidate status, number of separate candidate sessions, average duration per session, dominant direction, peak score reached, momentum type, % change for the day, flip count.

**Most-flipped tickers (avoid list):** the 5 tickers with the most state transitions today. These were traps — note them for tomorrow.

**Market regime breakdown:** transitions logged under each regime classification. Tells you what kind of day it was.

**Key takeaways:** automatically generated bullets based on what kind of day it was. Examples:
- "Candidate durations were short (<1 min avg). Today was choppy. Consider tightening stability for tomorrow."
- "Dominated by DRIFT momentum — ideal for your OTM options strategy."
- "Most-flipped ticker: ORCL (11 transitions). Note for tomorrow: this symbol was indecisive."

### Saving the report

Click the **Print / Save as PDF** button at the bottom of the report. Use your browser's print dialog and select "Save as PDF" as the destination. Save by date (e.g., `MomScanner_Summary_2026-04-24.pdf`) for your trading journal.

The summary is also saved to localStorage by date — future versions can browse historical summaries from prior sessions.

---

## Part 10 — How to trade with MomScanner v5

### Pre-market

Open MomScanner. Run thinkorswim scan. Note pre-market movers but don't paste yet.

### 9:30 AM — Initial setup

Paste thinkorswim results into MomScanner. **Make sure SPY is included.** Don't trade. ToD badge will show "Open" — strict thresholds active.

### 9:30-10:00 — Observation window

All rows in warmup. Regime banner activates within ~30 seconds once SPY data flows. Watch the regime classification — it tells you what kind of day to expect. Open window deliberately produces few or no candidates.

### 10:00 AM — Midday window opens

ToD badge shifts to "Midday." Standard thresholds active. Candidates section starts populating as tickers complete their 3-minute warmup AND meet the stability gate (8/10 qualifying cycles + 60-second sustained streak).

### Trading midday candidates

When a ticker appears in Candidates, check:
1. **Streak > 1:30**
2. **Flips < 4** (no warning icon)
3. **Sparkline rising**
4. **Type = DRIFT** (preferred) or THRUST (only if you can fill fast)

If all check out → Robinhood → 2-5 DTE → one strike OTM → limit at midpoint.

### Exit triggers (same as v4)

1. Streak breaks (drops to `—`) → sell at bid
2. Demoted from Candidates → check Session Log for reason → limit sell above bid
3. ΔScr decelerating → take profit
4. Score below 60 → market sell
5. 20-minute time stop without 15%+ option move → exit

### 3:00 PM — Close window opens

ToD badge shifts to "Close Window." Looser thresholds active. **Acceleration section appears at the top of the table.** Watch it carefully. Late-day breakouts will populate here.

### Trading Acceleration entries

Different rules than midday:
- **Faster exits** — target 15-25% on the option, not 50%+
- **Shorter time stop** — exit at 5-7 minutes if not working
- **Skip if Flips ≥ 4** — choppy ticker, don't trust the breakout
- **Verify the breakout is real** — Brk = BRK badge, price visibly outside the recent range

### 4:00 PM — Session close

Click **Session Summary** to generate the report. Print to PDF. Review:
- Did your trades cluster around DRIFT setups (good) or THRUST (mixed)?
- What was the Avg Candidate duration? Tells you what tomorrow's stability tuning should be.
- Which tickers were most-flipped? Add them to a mental "avoid in similar market conditions" list.

### Post-session

Export Active CSV and Transitions CSV for archival. Save the PDF summary by date. After 5-10 sessions, patterns will emerge in your summaries that drive concrete tuning decisions.

---

## Part 11 — Settings reference

All settings accessible via the gear icon (top right). Slide-out drawer.

### Data Source
Tradier or Schwab keys, callback URL, environment selection, OAuth connect.

### Options Liquidity Filter
Penny Pilot toggle, max spread %, min OI, max DTE, options check interval.

### Score Weights
5 weighted components summing to 100. Defaults: VP 30, RV 20, PE 20, VE 15, OA 15.

### Time-of-Day Tuning (v5)
Enable/disable adaptive thresholds. When enabled, score threshold and stability streak duration auto-adjust by market hour.

### Stability Filter (v4)
- Window: 10 cycles default
- Min Qual: 8 of 10 default
- Min Streak: 60 seconds default (overridden by ToD when enabled)
- Flip Warn: 8 default

### Behavior
- Smoothing Lag: 60s default (overridden by ToD when enabled)
- High Threshold: 75 (overridden by ToD)
- Low Threshold: 25
- Min Refresh: 5 seconds

---

## Part 12 — Troubleshooting

**No candidates appearing in the morning:** The Open window (9:30-10:00) deliberately uses strict thresholds. This is normal. Wait for 10:00 AM when ToD shifts to Midday.

**Regime banner stuck at "unknown":** SPY isn't in your active scan. Add SPY. Wait 30 seconds for data to accumulate.

**Session resumed with warning toast:** A heartbeat gap was detected (laptop sleep, browser closed, OS crash, etc.). Some transitions in that gap are missing. Continue the session normally — current state is intact.

**Breakout column shows numbers but no `BRK`:** Range expansion is happening but price hasn't broken out yet. Watch closely — it's building.

**Acceleration section empty during close window:** No active breakouts. Either there are no good late-day setups or your active scan doesn't include the right tickers. Re-run thinkorswim scan and paste fresh symbols.

**Type column shows `—`:** The ticker isn't currently a candidate, or score history is too short for classification. Will populate once it qualifies.

**Session Summary popup blocked:** Allow popups for your GitHub Pages domain.

**Stability filter still feels too strict despite ToD:** You can lower the base settings (Stability Filter section in settings). The ToD overlay multiplies/reduces those base values, so reducing the base reduces the overall effective values.

**Tickers from yesterday won't go away:** v5 should auto-detect a new session, but if it doesn't, click **Clear Active** in the input bar (history archive is preserved).

**Score velocity in tooltip seems wrong:** Score velocity is computed over the last 2 minutes of polling. If a ticker just promoted, velocity will read low until enough samples accumulate.

**Feed errors:** Re-paste API key, ensure Production environment, click Test Feed.

**Code update not showing:** GitHub Pages caches 30-60 seconds. Hard refresh with Ctrl+Shift+R.

---

## Part 13 — Data safety

All API keys and trading data stored in browser localStorage only. Never transmitted except directly to Tradier/Schwab API endpoints. Repository contains no keys. Public repo is safe.

The session snapshot stored by v5's persistence layer is comprehensive — it includes price history and score history. This data also stays in your browser. To clear all data, use the gear → clear keys, plus Clear Active, Clear History, and Clear Log buttons. Or clear site data in your browser settings.

---

## Part 14 — Roadmap (still pending)

These were proposed but not yet built:

1. **Schwab token auto-refresh** before 30-minute expiration
2. **L2 WebSocket streaming** for true sub-second updates and lower API usage
3. **True buy/sell volume pressure** from Tradier Time & Sales stream
4. **Sound or browser notification** when a candidate promotes or breakout activates
5. **Spread trend indicator** showing whether ATM spread is widening or tightening over the last 5 minutes
6. **Historical ATR/EMA** from a proper bars endpoint (replaces the rolling approximation)
7. **Multi-day summary archive browser** to compare today's session against prior sessions visually
8. **Auto-export at 4:00 PM** — automatic CSV + PDF summary generation when the close window ends, no manual click needed
9. **Per-ticker notes** — small text field per ticker for your own annotations during the session
10. **Backtest mode** — replay a past session from the Active CSV to test new settings before live use

Tell me when you want any of these.
