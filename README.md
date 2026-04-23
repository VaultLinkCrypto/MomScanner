# MomScanner v3

Real-time momentum scoring terminal for thinkorswim web scan results. Pulls quotes and live options chain data from Tradier (L2) or Schwab, computes a smoothed 0–100 score per ticker, auto-classifies actionable candidates, and persists every observation to browser local storage for post-session study.

## What's new in v3

- **Two-tier layout** — the table is split into "Candidates" (actionable trades) and "Watching" (everything else). Your eyes go to the top section only.
- **Action dots** — solid green = buy calls, solid red = buy puts, hollow = tracking, dashed + faded = warming up (< 3 min of data).
- **Inline sparklines** — each row shows a 5-minute score trajectory line. Rising line = building momentum. Flat = no conviction. Dashed = still warming up.
- **Confidence fade** — rows with < 3 minutes of data render at 45% opacity. Prevents acting on premature scores.
- **Slide-out settings** — the entire configuration panel is behind a gear icon in the header. During trading, the screen is 100% data.
- **Color discipline** — red/green are exclusively for directional signals. Spread% uses amber for caution. No more color confusion.
- **Reduced columns** — 11 columns that matter for trade decisions. Pre-Mkt, Aft-Hrs, Opt Liq grade, First Seen moved to CSV export and History.
- **Automatic candidate classification** — tickers promote to Candidates when all 6 criteria are met: Score ≥ threshold, direction arrow sustained, ΔScore positive, Spread% ≤ 5%, OI ≥ 1,000, Rel Vol ≥ 2.0x.
- **Penny Pilot whitelist** — ~400 CBOE penny-increment tickers. Non-whitelisted tickers silently rejected at paste time (when enabled).
- **Live options spread/OI columns** — pulled from Tradier options chain API, auto-hides tickers with wide spreads or low OI.

---

## Part 1 — Set up the GitHub repository (step by step)

### 1.1 — Create your GitHub account (skip if you already have one)

1. Open your web browser and go to **https://github.com**.
2. Click **Sign up** in the top right corner.
3. Enter your email address, create a password, and choose a username. The username becomes part of your site URL, so pick something clean (e.g., `jsmith-trader`). Avoid underscores if you can.
4. Complete the verification puzzle and click **Create account**.
5. Check your email, click the verification link GitHub sends you.
6. When GitHub asks what you want to do, pick the free plan.

### 1.2 — Create the repository

1. After logging in, look at the top-right corner of github.com. Click the **+** icon.
2. From the dropdown menu, click **New repository**.
3. On the "Create a new repository" page:
   - **Repository name:** type `MomScanner` exactly (capital M, capital S, no spaces).
   - **Description:** optional, you can type `Momentum scoring terminal for thinkorswim web`.
   - **Visibility:** choose **Public**. (GitHub Pages requires public on free accounts. Your API keys are stored only in your browser, never in the repo, so this is safe.)
   - **Initialize this repository with:** check the box for **Add a README file**. Leave the other two checkboxes alone.
4. Click the green **Create repository** button at the bottom.

You should now be looking at your new empty repository at `https://github.com/YOUR_USERNAME/MomScanner`.

### 1.3 — Add the index.html file

1. On the repository page, click the **Add file** button near the top right of the file list.
2. From the dropdown, click **Create new file**.
3. At the top of the next page, in the "Name your file..." box, type exactly: `index.html`
4. In the large text area below, **paste the entire contents of the index.html file** provided.
5. Scroll down. Under "Commit new file" you'll see a message box. It will say "Create index.html" — leave that alone.
6. Click the green **Commit new file** button.

You now have two files in your repository: `README.md` and `index.html`.

### 1.4 — Replace the README (optional but recommended)

1. Click on `README.md` in the file list.
2. Click the pencil icon (**Edit this file**) in the top right of the file view.
3. Delete whatever default text is there and paste the contents of this README.
4. Scroll down and click **Commit changes...** then **Commit changes** in the dialog.

### 1.5 — Enable GitHub Pages

1. On your repository page, click the **Settings** tab (top right, gear icon area).
2. In the left sidebar of Settings, click **Pages**.
3. Under "Build and deployment":
   - **Source:** select **Deploy from a branch** from the dropdown.
   - **Branch:** select **main** from the first dropdown, and **/ (root)** from the second dropdown.
4. Click **Save**.
5. Wait about 1–2 minutes. Refresh the page.
6. At the top of the Pages settings, you'll see a box that says **Your site is live at** followed by a URL like:

   `https://YOUR_USERNAME.github.io/MomScanner/`

7. **Copy that URL.** Bookmark it. That is your MomScanner.

### 1.6 — First-time launch test

1. Open the URL in your browser.
2. You should see the MomScanner v3 interface with the dark theme, the header bar, and the input area.
3. Click the **gear icon** in the top right of the header. The settings drawer slides open.
4. In the **Data Source** section, leave "Feed" set to **Tradier**.
5. In the **Tradier API Key** box, paste your Tradier key.
6. Make sure the Tradier Environment is set to **Production**.
7. Click **Save Keys**.
8. Click **Test Feed**. A toast should pop up in the bottom right saying `Feed OK · 2 quotes · SPY=...`.
9. Click the gear icon again (or click the dark overlay) to close the settings drawer.

If that works, you're ready.

### 1.7 — Updating the file later

When you receive updated code:

1. Go to `https://github.com/YOUR_USERNAME/MomScanner`.
2. Click on `index.html` in the file list.
3. Click the pencil icon (**Edit this file**).
4. Select all the existing code (Ctrl+A) and delete it.
5. Paste the new code.
6. Scroll down, click **Commit changes...**, then **Commit changes**.
7. Wait 30–60 seconds, then hard refresh your MomScanner URL with **Ctrl+Shift+R**.

**Verification:** after committing, open `index.html` in the repo and scroll to the bottom. The last line should be `</html>`. If it isn't, the paste was truncated — redo the paste.

---

## Part 2 — Apply for the Schwab Developer API

The Schwab API gives you real-time quotes matching what thinkorswim sees. Your existing brokerage account authorizes you.

### 2.1 — Register as a developer

1. Go to **https://developer.schwab.com**.
2. Click **Register** (top right).
3. Sign in with your existing Schwab brokerage account credentials.
4. Agree to the developer terms of service if prompted.

### 2.2 — Create an application

1. On the developer dashboard, look for **Dashboard** or **My Apps** in the navigation.
2. Click **Add a New App**.
3. Fill out the form:
   - **App Name:** `MomScanner`
   - **Description:** `Personal momentum scanning and scoring tool for equities and options trading`
   - **Callback URL:** paste your GitHub Pages URL exactly, e.g. `https://YOUR_USERNAME.github.io/MomScanner/` (include the trailing slash)
   - **API Products:** select **Accounts and Trading Production** and **Market Data Production**
4. Submit the application.

### 2.3 — Wait for approval

Schwab reviews applications in 1–3 business days typically. You'll get an email when approved. Use Tradier L2 in the meantime.

### 2.4 — When approved

1. Go back to **developer.schwab.com** → your app.
2. Copy your **App Key** and **App Secret**.
3. Open MomScanner and click the gear icon.
4. Paste the App Key and App Secret into the Schwab fields.
5. Make sure the Callback URL field matches exactly what you entered when registering.
6. Click **Save Keys**.
7. Change the Feed dropdown to **Schwab**.
8. Click **Connect Schwab**. You'll be redirected to Schwab login.
9. Log in and approve access.
10. You'll be redirected back to MomScanner. A toast says **"Schwab connected"**.
11. Click **Test Feed** to verify.

### 2.5 — Token refresh

Schwab access tokens expire after 30 minutes. If you get a "token expired" error, click the gear → **Connect Schwab** again. Auto-refresh is on the roadmap.

---

## Part 3 — thinkorswim web scan filter (the pre-filter layer)

### 3.1 — Set up the scan

1. Log in to **trade.thinkorswim.com**.
2. Click **Scan** in the top navigation.
3. Use "Stock Hacker" or create a new scan.
4. Under **Scan in**, select the broadest available universe (NYSE + NASDAQ).

### 3.2 — Add the filters

**Tight filters (recommended, produces ~25-40 symbols):**

| Filter | Operator | Value |
|---|---|---|
| Last | is greater than or equal to | 20 |
| Last | is less than or equal to | 500 |
| Volume | is greater than or equal to | 5,000,000 |
| Market Cap | is greater than or equal to | 10,000,000,000 |
| Percent Change | absolute value is greater than or equal to | 1.5 |
| Option Volume Index | is greater than or equal to | 1.5 |

**Loose filters (more candidates, ~60-100 symbols):**

| Filter | Operator | Value |
|---|---|---|
| Last | is greater than or equal to | 10 |
| Last | is less than or equal to | 500 |
| Volume | is greater than or equal to | 1,000,000 |
| Percent Change | absolute value is greater than or equal to | 1.5 |
| Option Volume Index | is greater than or equal to | 1 |

With the tight filters, you get stocks that almost certainly have tradable options. With the loose filters, you get more candidates and let MomScanner's Penny Pilot whitelist + live spread check do the cutting.

### 3.3 — Optional thinkScript momentum pre-qualifier

If the web scanner supports custom study filters, add this:

```thinkscript
# MomScanner Pre-Qualifier
def atr14 = Average(TrueRange(high, close, low), 14);
def rangeToday = high - low;
def avgVol20 = Average(volume, 20);

def atrExpansion = rangeToday > atr14 * 1.2;
def volSpike = volume > avgVol20 * 1.5;
def pctMove = AbsValue((close / close[1] - 1) * 100) >= 1.5;

plot scan = atrExpansion or volSpike or pctMove;
```

If the web UI doesn't accept custom studies, the native filters above are sufficient.

### 3.4 — Running and importing the scan

1. Click **Scan** to run.
2. Sort by **% Change** descending.
3. Copy the ticker symbols from the results (select rows, right-click → Copy Symbols, or manually select and Ctrl+C).
4. Go to MomScanner, paste into the input box, click **Add to scan**.
5. If Penny Pilot is enabled, a toast tells you how many were accepted vs rejected.
6. Re-scan thinkorswim every 5–15 minutes during the session and paste any new symbols.

---

## Part 4 — How to trade using MomScanner v3 (step-by-step guide)

### Before the open (pre-9:30 AM ET)

Open MomScanner and thinkorswim web side by side. Run the thinkorswim scan to see which symbols have large pre-market moves. Don't paste anything yet — just observe.

### 9:30 to 9:45 — The observation window

Run the scan again now that the market is open. Paste all results into MomScanner. Don't trade during this window. The first 15 minutes are noise — spreads are widest, prices most volatile. Use this time to watch scores initialize and the Spread% column populate. All rows will be faded (warming up) or in the Watching section.

### 9:45 to 10:00 — The narrowing

By now MomScanner has had 15 minutes of data. Rows that have been tracking for 3+ minutes are no longer faded. The sparklines are forming. Look at the **Candidates section at the top**. If tickers have promoted there, they've passed all six criteria automatically — you don't need to check each criterion manually.

If the Candidates section is empty, either the market is quiet or conditions are too strict. You can try lowering the Score threshold from 75 to 70 in Settings.

### 10:00 to 10:15 — The entry decision

For tickers in the Candidates section:

1. **Watch the sparkline.** You want a line that's climbing steadily — not one that spiked and is now flattening. A rising sparkline means momentum is still building.

2. **Watch the ΔScr column.** This updates in real time with no smoothing. You want it positive AND increasing over successive refreshes (+3, +6, +10...). This tells you raw momentum is accelerating.

3. **Check the direction arrow.** Green ▲ sustained for 2+ minutes → buy calls. Red ▼ sustained for 2+ minutes → buy puts. If it's been flipping between ▲ and ▼, wait.

4. **Open Robinhood.** Navigate to the ticker. Find the nearest expiration within 2-5 DTE (avoid 0DTE in wide-spread environments). Pick the strike one step OTM from ATM.

5. **Place a limit order at midpoint.** Halfway between bid and ask. Wait 10-30 seconds for fill. If it doesn't fill, inch up by $0.01 at a time. Never pay the full ask.

### After entry — Monitoring your position

Your position is healthy as long as:
- The ticker remains in the Candidates section
- The sparkline is still rising or flat (not dropping)
- ΔScr stays positive

### Exit triggers (in priority order)

**Trigger 1 — Arrow flip.** If you bought calls and the arrow flips from ▲ to ▼ and stays ▼ for two consecutive refreshes (~10 seconds), sell at the bid immediately. Momentum has reversed.

**Trigger 2 — ΔScr deceleration.** If ΔScr was climbing (+5, +8, +12, +15) and then stalls or drops (+15, +14, +12), place a limit sell slightly above the current bid. This is your profit-taking signal.

**Trigger 3 — Score drops below 60.** If the smoothed Score falls below 60, sell at market. The move is exhausting.

**Trigger 4 — Time stop.** If you've held for 20+ minutes and the option hasn't moved 15%+ in your favor, sell and move on. Momentum trades that work tend to work in the first 5-15 minutes.

### Exit execution

Always sell with a limit order. For profit-taking (Triggers 2-3), sell at midpoint or bid+$0.01. For stop-loss (Trigger 1), sell at the bid — getting out fast matters more than getting a good price on a losing trade.

### Post-trade

After each trade, note the ticker, entry score, exit score, entry ΔScr, hold time, and P/L. Export the active scan CSV periodically. After 10 trades, you'll start seeing which score/sparkline patterns produced your best results. That pattern recognition is the real edge.

---

## Part 5 — The scoring formula

Each poll cycle computes a **raw score** from five weighted components:

| Component | Weight (default) | What it measures |
|---|---|---|
| Volume Pressure | 30% | Buy vs sell pressure proxy from last-trade position between bid/ask, blended with 30s price direction |
| Relative Volume | 20% | Today's volume vs 20-day average |
| Price vs EMA | 20% | Distance from 9-EMA, ATR-normalized |
| Volatility Expansion | 15% | Today's range vs ATR(14) |
| Options Activity | 15% | Live ATM spread tightness + open interest quality |

**Scale:** 50 = balanced (no signal). 75+ = strong directional probability (green highlight). ≤25 = strong opposite direction.

**Smoothing:** The displayed Score is an EMA of the raw score with a time constant equal to your Smoothing Lag setting (default 60s). The ΔScr column shows `raw_score - first_seen_score` with zero lag — it updates every tick.

---

## Part 6 — Options Liquidity Filter

Located in **Settings → Options Liquidity Filter**.

### Penny Pilot Only (default: ON)

Rejects tickers not on the ~400-symbol CBOE penny-increment whitelist. These are the stocks with tight $0.01 or $0.05 option spreads on weekly/daily expirations. Turn OFF only if you need to monitor a specific non-whitelisted ticker.

### Max Options Spread % (default: 15%)

MomScanner pulls the ATM call and ATM put at the nearest expiration within your DTE limit, computes the spread as a percentage of mid, and uses whichever side is tighter. Tickers exceeding this threshold are auto-hidden.

**Reading the Spread% column:**
- **Green (≤5%)** — tradable. You lose a small fraction on entry.
- **Amber (5-15%)** — caution. Need strong conviction.
- **Coral (>15%)** — do not trade. Auto-hidden by default.

### Min ATM Open Interest (default: 500)

Low OI means even if the spread looks okay, you may not find a counterparty on exit. 500 is a floor. 2,000+ is better.

### Max DTE for Spread Check (default: 14 days)

The tool picks the nearest expiration within this window. Set to 7 or less for same-week expirations only.

### Options Check Interval (default: 60s)

Options spreads change slowly. 60 seconds is plenty. Tighten to 30s for faster updates, loosen to 120-300s to save API calls with large ticker lists.

### Hidden count

The table footer shows current filter status. The Watching section header shows how many tickers were hidden. Hidden tickers still track in the background and still appear in History — the filter is presentation-only.

---

## Part 7 — Candidate classification

A ticker promotes from Watching to Candidates when ALL of these are true simultaneously:

1. **Score ≥ threshold** (default 75)
2. **Direction arrow is sustained** (▲ or ▼, not ━)
3. **ΔScore is positive** (momentum still building)
4. **Spread% ≤ 5%** (tight enough to trade profitably)
5. **OI ≥ 1,000** (enough liquidity to exit)
6. **Rel Vol ≥ 2.0x** (the stock is doing at least double its normal volume)

If any one criterion fails, the ticker stays in Watching. This is intentionally strict — the Candidates section should contain only 0-5 rows at any given time. That's the right cognitive load for active decision-making.

### The action dot colors

- **Solid green** — all 6 criteria met, arrow is ▲. This is a call candidate.
- **Solid red** — all 6 criteria met, arrow is ▼. This is a put candidate.
- **Hollow circle** — tracking but not actionable (one or more criteria not met).
- **Dashed circle + faded row** — warming up (< 3 minutes of data). Scores are unreliable. Don't trade.

### The sparkline

Shows the smoothed score's trajectory over the last ~5 minutes, sampled at each data refresh. The line color matches the direction: green for ▲, red for ▼, gray for ━.

**Reading sparklines:**
- **Steady upward climb** — sustained momentum, ideal entry signal.
- **Spike then flatten** — the move may be exhausted. Wait for confirmation before entering.
- **Choppy oscillation** — no real trend. Not tradable.
- **Dashed short line** — warmup period, not enough data yet.

---

## Part 8 — Understanding the spread problem

Your original finding was correct: of 106 thinkorswim scan results, the majority had options bid/ask spreads between $0.05 and $0.90 — too wide for profitable OTM trading.

### Why this happens

Market makers widen spreads during high-volatility regimes, earnings clusters, and macro uncertainty. A stock can have heavy options volume in one strike while every other strike has a $0.50 spread.

### The three-layer defense

**Layer 1 — Tighter thinkorswim filters.** Volume ≥ 5M, Market Cap ≥ $10B, price ≥ $20, OVI ≥ 1.5. This cuts your 106 results to ~25-40.

**Layer 2 — Penny Pilot whitelist.** Hardcoded in MomScanner. Automatically rejects non-whitelisted tickers at paste time. The remaining candidates almost universally have penny or nickel-wide ATM options.

**Layer 3 — Live spread check.** MomScanner pulls the actual ATM options chain from Tradier, computes bid/ask spread as a percentage, and auto-hides anything above your threshold. You see the exact number you'd see on Robinhood.

Together, these three layers collapse the workflow from "scan 106, manually check 106 on Robinhood, trade 3" to "scan 30, MomScanner shows 8-12 tradable, trade 3."

### Spread timing

Spreads tend to be tightest between 10:00-11:30 AM ET and 1:00-2:30 PM ET. The open (9:30-10:00) and close (3:30-4:00) have the widest spreads. Factor this into your entry timing.

### Strike selection in wide-spread environments

Instead of buying the cheapest far-OTM contract, move one or two strikes closer to ATM. A $0.10 spread on a $0.50 contract is 20% friction, but on a $1.50 contract it's only 6.7%. With a $100 budget, 1 contract at $1.50 often outperforms 3 contracts at $0.50 because the breakeven is closer and friction is lower.

---

## Part 9 — Troubleshooting

**Tool won't load anything:** Open browser dev tools (F12), check Console tab. Most common: API key not saved, or key has trailing whitespace.

**"Feed error: HTTP 401":** API key invalid or expired. Re-paste in Settings and click Save Keys, then Test Feed.

**"Feed error: HTTP 429":** Rate limited. Increase Min Refresh Seconds in Settings.

**Scores stuck at 50:** Bid/ask or volume not coming through. Some thinly-traded tickers have sparse data on Tradier sandbox. Ensure Tradier Environment is set to **Production**.

**Candidates section always empty:** Either the market is quiet or criteria are too strict. Try: lower Score threshold from 75 to 70, or Spread% criterion from 5% to 8%. If many tickers have "—" in the Spread% column, the options sweep hasn't reached them yet — wait 2-3 minutes.

**Schwab OAuth returns error page:** The callback URL must match EXACTLY between developer.schwab.com and the Settings field, including the trailing slash.

**Sparklines all flat:** Need at least 2 data points (2 poll cycles). Wait ~10 seconds after adding tickers.

**History not saving:** Browser localStorage full or disabled. In Chrome, check `chrome://settings/content/all` and clear space if needed.

**Code update didn't take effect:** GitHub Pages caches for 30-60 seconds. Hard refresh with **Ctrl+Shift+R**.

---

## Part 10 — Data safety and API keys

All API keys are stored in your browser's localStorage for the domain `https://YOUR_USERNAME.github.io/MomScanner/`. They never leave your browser except to go directly to the Tradier or Schwab API endpoints. The `index.html` file in the GitHub repository does NOT contain any keys. The repository being public is safe.

If you use this tool on a shared computer, clear the keys when done: open Settings, paste empty strings over all key fields, click Save Keys. Or clear site data in browser settings.

---

## Part 11 — Roadmap

Features that can be added in future versions:

- Schwab token auto-refresh before expiration
- L2 WebSocket streaming (true sub-second updates, much lower API usage)
- True buy/sell volume pressure from Tradier Time & Sales stream
- Order book imbalance signal from L2 depth
- Historical ATR/EMA from proper chart API (replaces current rolling approximation)
- Pre-market and after-hours price columns from extended-hours quote endpoints
- Sound or browser notification when a ticker promotes to Candidates
- Spread trend indicator (widening vs tightening over last 5 minutes)
- Alert system when a ticker crosses the score threshold

Tell me when you want any of these.
