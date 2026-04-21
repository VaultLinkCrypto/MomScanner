# MomScanner

Real-time momentum scoring companion for thinkorswim web scan results. Pulls quotes from Tradier or Schwab, computes a smoothed 0–100 score per ticker, filters by live options liquidity, and persists every observation to browser local storage for post-session study.

## Quick overview

- **thinkorswim web** runs the filter. Produces the candidate ticker list.
- **MomScanner** (this tool) pulls live quotes + live options chain data for those tickers, computes the score, auto-hides illiquid options, and tracks them.
- **Tradier L2** is the default feed and enables the options chain filtering.
- Every ticker that ever passes through the tool is saved to local storage and exportable as CSV.

## What's new in this version

- **Penny Pilot whitelist** — roughly 400 tickers known to have tight penny-wide options spreads. Paste anything you want, non-whitelisted tickers get silently rejected at input. Default ON.
- **Live options spread % column** — pulls the ATM call and ATM put at the nearest expiration within your DTE limit, computes real bid/ask spread as a percentage of mid, shows whichever side (call or put) is tighter.
- **Live options OI column** — open interest on the ATM strike.
- **Auto-hide filter** — tickers where spread > your max % OR OI < your minimum are automatically hidden from the active table (still logged to history). Hidden count shown in the table header.
- **Upgraded OA scoring component** — Options Activity now uses real spread and OI data when available, not the previous proxy.
- **Smart tiebreaker** — same score → tighter options spread wins → better stock liquidity breaks further ties.


---

## Part 1 — Set up the GitHub repository (step by step)

This section is written for someone who has never published a GitHub Pages site before. Follow every step in order.

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
4. In the large text area below, **paste the entire contents of the index.html file** I provided.
5. Scroll down. Under "Commit new file" you'll see a message box. It will say "Create index.html" — leave that alone.
6. Click the green **Commit new file** button.

You now have two files in your repository: `README.md` and `index.html`.

### 1.4 — Add the README (optional but recommended)

1. Click on `README.md` in the file list.
2. Click the pencil icon (**Edit this file**) in the top right of the file view.
3. Delete whatever default text is there and paste the contents of this README.
4. Scroll down and click **Commit changes...** then **Commit changes** in the dialog.

### 1.5 — Enable GitHub Pages

This is what makes your tool actually accessible as a web page.

1. On your repository page, click the **Settings** tab (top right, gear icon area).
2. In the left sidebar of Settings, click **Pages**.
3. Under "Build and deployment":
   - **Source:** select **Deploy from a branch** from the dropdown (it usually already is).
   - **Branch:** select **main** from the first dropdown, and **/ (root)** from the second dropdown.
4. Click **Save**.
5. Wait about 1–2 minutes. Refresh the page.
6. At the top of the Pages settings, you'll see a box that says **Your site is live at** followed by a URL like:

   `https://YOUR_USERNAME.github.io/MomScanner/`

7. **Copy that URL.** Bookmark it. That is your MomScanner.

### 1.6 — First-time launch test

1. Open the URL in your browser.
2. You should see the MomScanner interface with a dark theme and the header "MomScanner · Momentum Terminal".
3. Click **Configuration** to expand the settings.
4. In the **Data Source** panel, leave "Feed" set to **Tradier (L1)**.
5. In the **Tradier API Key** box, paste your Tradier key.
6. Click **Save Keys**.
7. Click **Test Feed**. A toast should pop up in the bottom right saying `Feed OK · got 2 quotes · SPY=...`.

If that works, you're ready.

### 1.7 — Updating the file later

When I give you updated code or you want to make changes:

1. Go to `https://github.com/YOUR_USERNAME/MomScanner`.
2. Click on `index.html` in the file list.
3. Click the pencil icon (**Edit this file**).
4. Select all the existing code (Ctrl+A) and delete it.
5. Paste the new code.
6. Scroll down, click **Commit changes...**, then **Commit changes**.
7. Wait 30–60 seconds, refresh your MomScanner URL. The new version is live.

---

## Part 2 — Apply for the Schwab Developer API (for tomorrow)

The Schwab API gives you real-time quotes matching what thinkorswim sees. Your existing brokerage account is what authorizes you.

### 2.1 — Register as a developer

1. Go to **https://developer.schwab.com**.
2. Click **Register** (top right).
3. Sign in with your existing Schwab brokerage account credentials. The developer portal shares authentication with your trading account.
4. If prompted to agree to the developer terms of service, read them and agree.
5. You should now see the developer dashboard.

### 2.2 — Create an application

1. On the developer dashboard, look for **Dashboard** or **My Apps** in the navigation.
2. Click **Add a New App** (or similar wording).
3. Fill out the application form:
   - **App Name:** `MomScanner` (or whatever name you prefer)
   - **Description:** `Personal momentum scanning and scoring tool for equities and options trading`
   - **Callback URL:** paste your GitHub Pages URL exactly, e.g. `https://YOUR_USERNAME.github.io/MomScanner/` (include the trailing slash)
   - **API Products:** select **Accounts and Trading Production** and **Market Data Production** (you need both; market data gives quotes, accounts is required for OAuth authorization)
   - **Order Limit:** set whatever minimum the form allows (you're not placing orders through this tool)
4. Submit the application.

### 2.3 — Wait for approval

- Schwab reviews the application. Historically this has taken **1–3 business days**, sometimes longer. You'll get an email when status changes.
- While waiting, use Tradier L1.

### 2.4 — When approved

1. Go back to **developer.schwab.com** → your app.
2. You'll see an **App Key** (sometimes called "Client ID") and an **App Secret**.
3. Open MomScanner.
4. Expand **Configuration** → **Data Source**.
5. Paste the **App Key** into the "Schwab App Key" field.
6. Paste the **App Secret** into the "Schwab App Secret" field.
7. Make sure the "Schwab Callback URL" field matches exactly what you entered when registering the app.
8. Click **Save Keys**.
9. Change the "Feed" dropdown to **Schwab**.
10. Click **Connect Schwab OAuth**. You'll be redirected to a Schwab login page.
11. Log in with your brokerage credentials, approve the access request.
12. Schwab redirects you back to your MomScanner URL. The tool will automatically exchange the authorization code for an access token and store it.
13. You should see a toast saying **"Schwab connected"** and the feed pill will turn green.
14. Click **Test Feed** to verify.

### 2.5 — Token refresh

Schwab access tokens expire after 30 minutes, refresh tokens last 7 days. The tool does not yet auto-refresh — if you get a "token expired" error, click **Connect Schwab OAuth** again. In a future version I can add auto-refresh.

---

## Part 3 — thinkorswim web scan filter (the pre-filter layer)

This scan runs inside trade.thinkorswim.com and produces the candidate ticker list you paste into MomScanner.

### 3.1 — Set up the scan

1. Log in to **trade.thinkorswim.com**.
2. In the top navigation, click **Scan** (or **Scanner**).
3. If there's an existing "Stock Hacker" screen, use it. Otherwise click **New Scan**.
4. Under **Scan in**, select a broad universe — e.g., "All Symbols" or a union of NYSE/NASDAQ depending on what the web UI exposes. If the web version limits you to a watchlist-based scan, use a large watchlist like "NYSE/NASDAQ Large Cap" plus index ETFs, or combine a few.

### 3.2 — Add the filters

Add each filter one by one using the **Add Filter** button. Use the native filter controls shown in your screenshot where possible — they're faster than custom thinkScript and they do work in the web version.

**Tight filters (recommended, produces ~25-40 symbols):**

| Filter | Operator | Value |
|---|---|---|
| Last | is greater than or equal to | 20 |
| Last | is less than or equal to | 500 |
| Volume | is greater than or equal to | 5,000,000 |
| Market Cap | is greater than or equal to | 10,000,000,000 |
| Percent Change | absolute value is greater than or equal to | 1.5 |
| Option Volume Index | is greater than or equal to | 1.5 |

**Loose filters (if you want more candidates, ~60-100 symbols):**

| Filter | Operator | Value |
|---|---|---|
| Last | is greater than or equal to | 10 |
| Last | is less than or equal to | 500 |
| Volume | is greater than or equal to | 1,000,000 |
| Percent Change | absolute value is greater than or equal to | 1.5 |
| Option Volume Index | is greater than or equal to | 1 |

The key parameters in plain words:
- **Price $20–$500** — keeps you above the zone where $0.05 option spreads destroy OTM trades.
- **Volume ≥ 5M** — strong proxy for tight options spreads at the underlying level.
- **Market Cap ≥ $10B** — large caps almost universally have penny or nickel-wide ATM options.
- **|% Change| ≥ 1.5%** — already moving, about to hit your 2% target.
- **Option Volume Index ≥ 1.5** — options volume running 50% above recent average.

**Important:** The MomScanner Penny Pilot filter is your second line of defense. Even the loose thinkorswim filter + Penny Pilot whitelist will produce cleaner results than the tight thinkorswim filter alone. Let the tool do the cutting.

### 3.3 — Optional thinkScript filter for momentum pre-qualifier

If the web scanner allows custom study filters (button usually labeled **Study** or **Custom** when adding a filter), add this as an extra filter:

```thinkscript
# MomScanner Pre-Qualifier
# Returns true when ATR expansion OR volume spike is present

def atr14 = Average(TrueRange(high, close, low), 14);
def rangeToday = high - low;
def avgVol20 = Average(volume, 20);

def atrExpansion = rangeToday > atr14 * 1.2;
def volSpike = volume > avgVol20 * 1.5;
def pctMove = AbsValue((close / close[1] - 1) * 100) >= 1.5;

plot scan = atrExpansion or volSpike or pctMove;
```

If the web UI does not accept custom studies in scans (it may not — this is version-dependent), the table of native filters above is sufficient.

### 3.4 — Running the scan

1. Click **Scan** (or the equivalent run button).
2. Results appear as a table. Sort by **% Change** descending.
3. Select the top 20–50 rows (however many you want to monitor).
4. Copy the ticker symbols. In most thinkorswim web versions you can right-click the result set and choose **Copy Symbols**, or select all and Ctrl+C.
5. Paste into the MomScanner ticker input box. Click **Add to Scan**.

### 3.5 — How often to refresh the thinkorswim scan

The thinkorswim scan rechecks automatically every few seconds while the tab is open. You do not need to re-paste unless new symbols appear that weren't there before. Good practice: re-scan thinkorswim every 5–15 minutes during active sessions and paste any new symbols into MomScanner.

---

## Part 4 — The scoring formula (reference)

Each scan pass computes a **raw score** from five weighted components:

| Component | Weight (default) | What it measures |
|---|---|---|
| Volume Pressure | 30% | Proxy for buy vs sell pressure using last-trade position between bid and ask, blended with 30s price direction |
| Relative Volume | 20% | Today's cumulative volume vs 20-day average |
| Price vs EMA | 20% | Distance from 9-EMA, ATR-normalized |
| Volatility Expansion | 15% | Today's range vs ATR(14) |
| Options Activity | 15% | Live ATM options spread tightness + open interest |

**Scoring scale:**
- **50** = perfect balance, no directional signal
- **75+** = strong directional probability (green highlight)
- **25 or less** = strong opposite-direction probability (red highlight)
- Direction arrow indicates which way (up = calls, down = puts)

**Smoothing:** the displayed score is an EMA of the raw score with a time constant equal to your configured "Smoothing Lag" (default 60 seconds). This prevents jitter. The **ΔScore** column shows the raw score minus the first-seen score and updates with zero lag, so you can see momentum shifts before the smoothed score catches up.

---

## Part 4.5 — Options Liquidity Filter (the heart of the v2 upgrade)

Located in **Configuration → Options Liquidity Filter**. This panel is what makes MomScanner actually produce tradable candidates instead of just scored noise.

### Penny Pilot Only toggle (default: ON)

When enabled, any ticker you paste into the input that is not on the ~400-ticker CBOE Penny Pilot whitelist is silently rejected at the door. These are the stocks known to trade with $0.01 or $0.05 option increments on weekly/daily expirations — meaning tight spreads by definition.

A toast will tell you how many were accepted vs rejected when you paste, so you know what got cut.

**Turn this OFF if you want to monitor a specific ticker that isn't on the list.** It happens — new IPOs or growing names take time to get added. The rest of the filter layers will still protect you from untradable options.

### Max Options Spread % (default: 15%)

For each active ticker, MomScanner pulls the ATM call and ATM put at the nearest expiration within your DTE limit. It computes `(ask - bid) / mid × 100` and uses whichever side is tighter. If that number exceeds your threshold, the ticker is hidden from the active table (but still logged).

**Reading the Spread% column:**
- **Green (≤5%)** — excellent. You can buy at the ask and only lose a small fraction on entry.
- **Yellow (5-15%)** — tradable with caution. Need strong conviction on direction.
- **Red (>15%)** — do not trade. Auto-hidden by default.

### Min ATM Open Interest (default: 500)

Open interest is "how many contracts exist at this strike right now." Low OI means even if the spread looks okay, you may not find a counterparty when you try to sell. 500 is a floor; 2000+ is safer.

### Max DTE for Spread Check (default: 14 days)

The tool picks the nearest expiration within this window for the spread check. Your strategy runs 0-14 DTE, so 14 is the correct default. If you want to look at only same-week expirations, set it to 7 or less.

### Options Check Interval (default: 60s)

Options spreads change more slowly than stock prices. 60 seconds is plenty — but you can tighten it to 30s if you want faster updates, or loosen to 120-300s if you have many tickers and want to save API calls.

### What the hidden count means

In the Active Scan table header, you'll see something like **"Active Scan: 12 (+18 hidden)"**. The 12 are your tradable candidates right now. The 18 are tickers with known bad options liquidity (too-wide spread, too-low OI, or both). Hidden tickers still update their scores in the background and still show up in History — the filter is presentation-only, not computational.

---

## Part 5 — Troubleshooting

**Tool won't load anything:** open browser dev tools (F12), check Console tab for errors. Most common: API key not saved, or Tradier key has trailing space.

**"Feed error: HTTP 401":** API key invalid or expired. Re-paste the key and click Save Keys, then Test Feed.

**"Feed error: HTTP 429":** rate limited. Increase Min Refresh Seconds in Configuration.

**Scores all stuck at 50:** bid/ask or volume is not coming through. Some thinly-traded tickers have sparse quote data on Tradier sandbox. Switch to production environment (requires production key).

**Schwab OAuth returns me to a page that doesn't load:** the callback URL you set on developer.schwab.com must match EXACTLY, including the trailing slash, and must match what's in the tool's Callback field. Any mismatch breaks the redirect.

**History isn't saving:** browser local storage is full or disabled. In Chrome, check `chrome://settings/content/all` for your site and clear space if needed.

**I made a code change and nothing updated:** GitHub Pages caches for 30–60 seconds. Hard refresh with Ctrl+Shift+R.

---

## Part 6 — Data safety and API keys

All API keys are stored in your browser's localStorage for the domain `https://YOUR_USERNAME.github.io/MomScanner/`. They never leave your browser except to go directly to the Tradier or Schwab API endpoints you configured. The `index.html` file in the GitHub repository does NOT contain any keys — it's pure code. The repository being public is safe.

Anyone with physical access to your browser can read the keys from localStorage. If you use this tool on a shared computer, clear the keys when you're done by pasting over them with empty strings and clicking Save Keys, or by clearing site data.

---

## Part 7 — Roadmap (things I can add later)

- Auto-refresh of Schwab tokens before expiration
- Pre-market and after-hours price pull (Tradier and Schwab both support it via dedicated endpoints)
- Real options chain analysis for tighter liquidity grading
- Historical ATR/EMA from proper chart API instead of the rolling approximation
- WebSocket streaming feed (Schwab supports it; much lower API usage for same refresh rate)
- Alert system when a ticker crosses the high threshold

Tell me when you want any of these.
