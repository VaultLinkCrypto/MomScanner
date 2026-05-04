# MomScanner v8.02

Per-minute OHLC logger with all derived signals, hourly auto-export, and silent-save to a folder of your choice. Every ticker on your scan is sampled once per minute, with 25 columns of data captured per row, ready for backtesting and statistical pattern discovery. Builds on v8.01 by adding the File System Access API integration so hourly auto-saves no longer require you to be at the computer.

**Live URL:** https://vaultlinkcrypto.github.io/MomScanner/

## What's new in v8.02

- **Silent-save to a chosen folder** — at the start of each session, click **📁 Choose OHLC Folder** once and navigate to (for example) `My Documents/MomScanner_Claude`. From then on, both the manual **Export OHLC ⏱** button and every hourly auto-export write CSVs directly into that folder with **no save dialog, no popup, no need to be at the computer**. If you're in a meeting when the hourly auto-export fires, the file just appears in the folder.
- **Status indicator** — the foot bar shows whether silent-save is active (green: `📁 MomScanner_Claude (silent save)`) or files are going to the default Downloads folder (gray: `📁 Downloads (default)`).
- **Graceful fallback** — if the browser doesn't support the File System Access API (older Chrome, Firefox, Safari), exports still work via standard browser downloads. No feature is lost; only the silent-save convenience.

## What's new in v8.01

- **Per-Minute OHLC Logger** — every ticker on your scan is now logged once per minute with full OHLC + 22 derived columns: VWAP, %Chg, IntradayPctChg, Bid/Ask, SpreadPct, RelVol, PriceVelocity, the three layer scores and states (Trend/Breakout/Pressure), MomentumType, Regime, and TickCount (data-quality indicator). Output is a clean CSV with no annotations, ready for ingestion into Python pandas, Excel, or any analysis tool.
- **Hourly auto-export** — fires every 60 minutes as crash insurance. Combined with the v8.02 silent-save feature, this means you never lose more than an hour of session data even if Chrome crashes or the tab is accidentally closed.
- **Manual Export OHLC ⏱ button** — sits in the foot bar next to Export CSV. Flushes any in-flight bar (so the last incomplete minute is captured) and writes the full session log immediately.
- **Live bar count** — the foot bar shows current OHLC log size (e.g. "OHLC: 1,247 bars logged").
- **Zero new network traffic** — the logger samples the existing 5-second polls. No new API calls. No bandwidth increase.

## What carried over from v8

- ThinkorSwim deep-links on every ticker symbol (using protocol-relative URLs to preserve TOS login)
- Velocity column showing cents/minute over last 60s
- Velocity gate as 4th promotion check (default 0.03%/min, scaled per ticker price)
- Velocity-gated Pre-Promotion Watch
- Per-Layer Threshold sliders replacing orphaned v6 weight sliders
- Improved regime detector with `stock-specific` state for SPY-flat-but-tickers-moving days

## What carried over from v7.2

- Audio alarms (Bell / Chime / Alert / Tick + custom MP3/WAV upload, volume, cooldown)
- Pre-Promotion Watch ↑ icon (now velocity-gated)
- Near-Miss panel (collapsible, sortable, with "Stale momentum" block tag)

## What carried over from older versions

- Three-layer architecture (Trend / Breakout / Pressure)
- Intraday %Chg column and Gap-relationship icon
- VWAP tracking per ticker
- L1-friendly OFI proxies
- High-contrast accessibility theme with adjustable font size
- Pattern-based trading guide with five named patterns
- Bulletproof persistence
- Time-of-day adaptive tuning
- SPY-driven regime indicator
- Don't-Trade warning banner
- Momentum-type classifier
- End-of-session summary report
- All CSV exports (active + transitions)

---

## Part 1 — Per-minute OHLC logger (v8.01)

### Why this matters

The original transitions log only records state changes — a single ticker like INTC might generate 23 rows over a session, with median gap of 240 seconds between samples. That's not enough resolution for statistical backtesting. The May 1 simulation against v8 demonstrated the limit: only 4 of 13 promotions had enough surrounding samples to compute realized velocity at all.

With per-minute OHLC logging, every ticker generates exactly one row per minute regardless of state changes. A 6.5-hour session with 50 tickers produces ~19,500 rows. With 500 tickers, ~195,000 rows. This is the data density needed to find patterns that work.

### What gets logged

One row per ticker per minute, sealed at the start of the next minute. Each row contains 25 columns:

| Column | Description |
|---|---|
| Timestamp | ISO 8601, sealed at minute boundary |
| Ticker | Symbol |
| Open | First price seen in the minute |
| High | Max price during the minute |
| Low | Min price during the minute |
| Close | Last price seen in the minute |
| Volume | Cumulative session volume at minute close |
| VolumeDelta | Volume gained during this minute |
| VWAP | Session VWAP at minute close |
| PctChg | %change vs yesterday's close (includes pre-market gap) |
| IntradayPctChg | %change vs today's open (intraday only) |
| Bid / Ask | Bid and ask at minute close |
| SpreadPct | (ask−bid)/last × 100 at minute close |
| RelVol | Volume vs 20-day average at minute close |
| PriceVelocity | Cents/minute over last 60s, signed |
| TrendScore | Trend layer score at minute close |
| BreakoutScore | Breakout layer score at minute close |
| PressureScore | Pressure layer score at minute close |
| TrendState | watch / bull / bear (Trend layer) |
| BreakoutState | watch / bull / bear (Breakout layer) |
| PressureState | watch / bull / bear (Pressure layer) |
| MomentumType | DRIFT / THRUST / REVERSAL or empty |
| Regime | Session regime at minute close |
| TickCount | Number of polls aggregated into this bar (data quality) |

A typical session with 5-second polls produces ~12 ticks per minute. If TickCount is much lower than 12 for a given row, that minute had data gaps — useful flag for backtesting confidence.

### Capacity and performance

- **Per-row size:** ~150 bytes
- **500 tickers × 390 trading minutes:** ~195,000 rows × 150 bytes = ~30 MB raw / ~6 MB CSV
- **RAM impact on a 16 GB laptop:** negligible (the buffer is roughly 1/500 of available memory)
- **Network impact:** zero — the logger only samples polls already in flight
- **DOM impact:** zero — bars are held in memory only, never rendered to the page
- **Hard cap:** 800,000 rows. If exceeded (extreme multi-day sessions), oldest rows are dropped first.

---

## Part 2 — Silent-save to a chosen folder (v8.02)

### Why this matters

Hourly auto-export was added in v8.01 as crash insurance. In v8.01, that auto-export went through the standard Chrome download mechanism. If your Chrome's "Ask where to save each file before downloading" was set to ON, you'd get a save-dialog popup every hour — and if you weren't at the computer (in a meeting, away at lunch, on a call), the dialog would sit there indefinitely and nothing would save.

v8.02 fixes this with the File System Access API. Once per session you grant permission to a specific folder. From then on, MomScanner writes files directly into that folder, bypassing Chrome's download mechanism entirely. **No dialog. No popup. No need to be present.**

### How to use it

1. At the start of your trading day, open MomScanner.
2. Click the **📁 Choose OHLC Folder** button in the foot bar.
3. The native folder picker opens. Navigate to `My Documents` (or wherever you want), and either select an existing folder like `MomScanner_Claude` or create a new one.
4. Click **Select Folder**.
5. Toast confirms: "OHLC folder set: MomScanner_Claude — auto-exports will save here silently"
6. Status indicator turns green: `📁 MomScanner_Claude (silent save)`

That's it. From this point on:
- Every hourly auto-export writes silently to `MomScanner_Claude`
- The manual **Export OHLC ⏱** button also writes there
- Both work even if you're not at your desk

### Why permission must be granted each session

Chrome and Edge will not remember the folder permission across page reloads or browser restarts. This is a deliberate browser security boundary, not a MomScanner choice. The reasoning: a malicious or compromised website should not be able to silently write to your filesystem indefinitely just because you once said yes.

This means **every trading day, click "Choose OHLC Folder" once** — usually 5 seconds of work right before the bell rings. No way around it.

### Browser compatibility

| Browser | Silent-save supported? | Fallback behavior |
|---|---|---|
| Chrome 86+ (Windows/Mac/Linux) | Yes | n/a |
| Edge 86+ | Yes | n/a |
| Opera 72+ | Yes | n/a |
| Brave (Chrome-based) | Yes | n/a |
| Firefox | No | Standard downloads (silent if Chrome-style settings) |
| Safari | No | Standard downloads |
| Chrome on iOS/Android | Limited | Standard downloads |

If your browser doesn't support the API, the **📁 Choose OHLC Folder** button shows a toast explaining that fallback applies, and exports continue working through the standard download mechanism.

### Without silent-save: what to expect from auto-exports

If you don't click Choose OHLC Folder (or your browser doesn't support it), the hourly auto-export and manual export use Chrome's standard download mechanism. Behavior depends on your `chrome://settings/downloads` configuration:

- **"Ask where to save each file" OFF (Chrome default since 2020):** Files save silently to your default Downloads folder. No popup. No interruption. You don't need to be present. This is fine for most users.
- **"Ask where to save each file" ON:** Save dialog appears for every download. If you're away from the computer when the hourly auto-export fires, the dialog sits there waiting for your click.

To check your setting: open Chrome → `chrome://settings/downloads`. If you want hourly auto-saves to work while you're away, either turn that toggle OFF or use the v8.02 silent-save folder picker.

---

## Part 3 — How to use the data for backtesting

The OHLC CSV is designed to be loaded directly into pandas:

```python
import pandas as pd
df = pd.read_csv('momscanner_ohlc_minute_1746302400000.csv', parse_dates=['Timestamp'])
df = df.set_index(['Ticker', 'Timestamp']).sort_index()
```

From there, you can:
- Filter to a single ticker: `df.loc['INTC']`
- Compute rolling features: 5-min velocity, 15-min velocity, range expansion ratios
- Identify "ideal trade" moments: where would buying a call/put at this minute have produced ≥1% in the underlying (≥20% on options) within 30 minutes?
- Label each minute with the future outcome
- Train classifiers (or run clustering) to find which combinations of TrendScore + BreakoutScore + PressureScore + PriceVelocity + VWAP relationship + RelVol reliably preceded the labeled moments

After 20-30 days of logged data, you'll have enough to find statistically meaningful patterns — and those patterns become the v9 promotion logic, replacing intuition with evidence.

### Backtesting checklist

When loading a session CSV:

1. ✅ Verify TickCount column for data quality. Most rows should be ≥10 (5s polls × 60s). Rows with TickCount ≤3 had data gaps — discard or flag.
2. ✅ Verify session boundaries. The first minute is usually incomplete (scanner started mid-minute). The last minute may also be incomplete if you exported before the natural end. Both flushed to the buffer; check Open vs Close to identify partials.
3. ✅ Cross-reference with Transitions CSV. Each row in the Transitions log should align to a minute in the OHLC log within ±60s.
4. ✅ Check Regime distribution. If the entire session shows the same regime, the detector may have been stuck — useful diagnostic for v8 regime improvements.

---

## Part 4 — Updating to v8.02

### From v8.01 to v8.02

1. Go to https://github.com/vaultlinkcrypto/MomScanner
2. Click `index.html` → click the pencil (edit) icon
3. **Ctrl+A** to select all → **Delete** → paste new v8.02 code
4. Click **Commit changes**
5. Wait 30-60 seconds, then on the live page hit **Ctrl+Shift+R** (hard refresh)
6. Open Settings → **Audio Alarms → click ▶ Test once** to re-unlock audio for the session

All your v8.01 settings, tickers, history, and transitions carry over via localStorage. (The OHLC log itself doesn't persist across page reloads — it's session-only. That's intentional, to keep memory and storage clean.)

### Verifying the upgrade

After hard refresh:
- Header should read **"MOMENTUM TERMINAL v8.02"**
- Foot bar should show two new elements: **📁 Choose OHLC Folder** button and **📁 Downloads (default)** status indicator
- Click the folder button — native folder picker should open

---

## Part 5 — Daily trading routine for v8.02

### Pre-market

1. Open MomScanner in Chrome (Tab 1).
2. Open ThinkorSwim in another tab in the same browser window.
3. Open Settings → Audio Alarms → click **▶ Test** to unlock audio.
4. **Click 📁 Choose OHLC Folder** in the foot bar. Navigate to `My Documents/MomScanner_Claude` (create the folder if needed). Click Select Folder.
5. Verify status indicator turned green: `📁 MomScanner_Claude (silent save)`.
6. Verify Layer Thresholds & Timing settings are at the values you want.
7. Run thinkorswim scan, get list of symbols. Don't paste yet.

### 9:30 AM

Paste tickers including SPY into MomScanner. Audio is already unlocked. Velocity buffer starts filling. OHLC logger starts logging.

### Throughout the session

- React to alarms and Vel column as before.
- The auto-export fires every 60 minutes (10:30, 11:30, 12:30, etc. if you started at 9:30). With silent-save active, a new file appears in `MomScanner_Claude` with no popup.
- You can be in a meeting when this fires. The file just appears.
- The foot bar OHLC count grows steadily through the day (e.g. "OHLC: 12,847 bars logged" by 3 PM with 30 tickers).

### 4:00 PM session close

Click **Export OHLC ⏱** to write a final consolidated CSV. This flushes the in-flight 3:59 minute bar into the buffer, then writes the full day to your folder.

Then click **Export Transitions CSV** for the state-change log, and **Session Summary** for the human-readable PDF report.

**Do not close the MomScanner browser tab during the session.** All session data is held in browser memory. Closing the tab early loses anything not yet exported. With v8.02 silent-save plus hourly auto-export, the worst-case data loss from a crash is one hour.

---

## Part 6 — Settings reference

### Data Source
Tradier or Schwab keys, callback URL, environment selection.

### Options Liquidity Filter
Penny Pilot toggle, max spread %, min OI, max DTE, options check interval.

### Layer Thresholds & Timing (v8)
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
Window, Min Qual, Min Streak, Flip Warn (legacy controls).

### Behavior
Smoothing Lag, High Threshold, Low Threshold, Min Refresh.

### Foot Bar Buttons (v8.01 / v8.02)
- **Export CSV** — active candidates snapshot
- **Export OHLC ⏱** — full per-minute OHLC log (uses silent-save if folder chosen)
- **📁 Choose OHLC Folder** — pick a folder for silent-save
- **Session Summary** — end-of-day PDF report

---

## Part 7 — Troubleshooting

**Choose OHLC Folder button does nothing:** Your browser doesn't support the File System Access API. You'll see a toast explaining this. Files will still save via standard downloads — check your Chrome download settings to make sure dialogs aren't enabled.

**Folder picker opens but selection didn't take:** Did you click Cancel instead of Select Folder? Try again. If it still fails, check the browser console for permission errors.

**Status says silent-save is active but files aren't appearing:** Verify the folder still exists and isn't locked. If the underlying folder is moved or deleted during the session, the next save will fail and fall back to download. The toast will tell you "Folder permission revoked — saving to Downloads instead."

**Hourly auto-export missed an hour:** The auto-export fires every 3,600,000 ms (1 hour) from page load, not at clock-aligned :00 boundaries. So if you opened MomScanner at 9:23, exports fire at 10:23, 11:23, etc. This is by design — clock-aligned exports could collide with manual exports.

**OHLC bar count stays at 0 for several minutes:** Each ticker's first bar isn't sealed until the *second* minute begins. With 50 tickers added at 9:30:30, your first 50 sealed bars appear at 9:31:00. Expected behavior.

**OHLC export says "No OHLC bars logged yet":** Same as above. Wait one more minute.

**TickCount column shows 0 or 1 for every row:** The poll loop isn't running. Check the feed status pill in the header. If it says ERR, your API key is invalid or the feed is down.

**Vel column shows "—" for all tickers:** Velocity buffer needs ≥20 seconds of price samples. Wait 30 seconds. If still "—", the feed isn't returning fresh prices.

**Clicking a ticker reloads MomScanner instead of opening TOS:** This should never happen — every link uses `target="_blank"`. If it does, screenshot the URL bar after the broken navigation and report it.

**Pre-Promotion ↑ icon never appears:** Pre-Promote requires four conditions: Trend or Breakout ≥ 60, Pressure crossed 60 in last 90s, |velocity| above half-gate, and velocity accelerating. On low-vol days this combination won't occur. Normal.

**Audio alarm doesn't play when a candidate promotes:** Click the ▶ Test button in Settings → Audio Alarms. Browser policy requires a user gesture before audio can play.

**Code update not showing:** GitHub Pages caches 30-60 seconds. Hard refresh with Ctrl+Shift+R.

---

## Part 8 — Data safety

All API keys, sound files, ticker history, transitions log, and OHLC buffer — held in browser memory and (where applicable) localStorage. Never transmitted except directly to Tradier/Schwab API endpoints. Repository contains no keys.

The OHLC buffer is **session-only** and not persisted to localStorage during the session — that would slow polling and could exceed localStorage's 5-10 MB limit by mid-day with 500 tickers. Persistence is achieved via the hourly auto-export instead. The combination of:
- 5-second polls feeding the in-memory buffer
- Hourly silent-save writing to your chosen folder
- Manual Export OHLC ⏱ at end of session

...gives you complete coverage with worst-case 1-hour data loss on crash.

ThinkorSwim deep-links open in **new tabs** (`target="_blank"`) precisely so MomScanner is never accidentally replaced. Click as many ticker symbols as you want. Tab 1 stays MomScanner.

---

## Part 9 — Roadmap

Pending features for future versions:

1. **MomScanner Lab (separate Python project)** — backtest framework that ingests the OHLC CSVs, defines "ideal trade" labels, and discovers which signal combinations preceded those moments. Requires ~20+ days of data first.
2. **v9 — data-driven promotion gates** — replace the current intuition-driven layer thresholds with patterns the Lab discovers.
3. **Alpaca L2 integration** — true Order Flow Imbalance with real bid/ask classification.
4. **Schwab token auto-refresh.**
5. **Multiple custom sounds per layer.**
6. **Browser desktop notifications** — system tray alerts when MomScanner tab is in the background.
7. **Spread trend indicator** — widening vs tightening over last 5 minutes.
8. **Multi-day summary archive browser.**
9. **Per-ticker notes** — annotation field on the watching row.
10. **Configurable broker links** — choose between TOS, TradingView, Webull, etc.
11. **Velocity sparkline column.**
