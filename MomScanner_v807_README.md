# MomScanner v8.07 — Trading Guide & README

**Updated:** 2026-05-27  
**GitHub:** vaultlinkcrypto/MomScanner  
**Deployment:** Single `index.html` → GitHub Pages  
**Includes:** v8.06.1 (CA v2), v8.06.2 (Gate Removal), v8.06.3 (VWAP Velocity), v8.06.4 (OHLC Fix + Exclude + Anti-Throttle), v8.07 (WebSocket Streaming)

---

## What's New in v8.07: WebSocket Streaming

MomScanner now supports two data feed modes, switchable at any time via Settings → Feed Mode:

### WebSocket Mode (New Default)

Opens a persistent `wss://ws.tradier.com` connection that pushes every trade, quote, and summary event in real time. For 199 tickers, this means hundreds of events per second during market hours — every trade print, every bid/ask change, every session high/low update.

The entire WebSocket connection runs inside a Blob-based Web Worker, immune to Chrome's background-tab throttling. Events are batched into 1-second windows and processed through the identical scoring pipeline (TrendScore, BreakoutScore, PressureScore, CA v2, VWAP Velocity, trailing stops, everything).

**What this fixes:** On 5/26 with REST polling, 62.7% of OHLC bars were flat (O=H=L=C) because each ticker only received 1 data point per minute. With WebSocket streaming, OHLC bars are built from actual trade prints — matching what you see on thinkorswim's 1-minute candles.

### REST Mode (Legacy Fallback)

The original polling architecture — `GET /v1/markets/quotes` every 10 seconds in chunks of 40 tickers. Works exactly as before, no changes. Select this if WebSocket is unavailable or if you experience issues.

### How to Switch

**Settings → Feed Mode dropdown:**

| Mode | Label | What It Does |
|------|-------|-------------|
| WebSocket | `WebSocket (real-time)` | Persistent stream, every tick |
| REST | `REST (polling)` | HTTP poll every 10s |

The feed pill in the header shows the current state:
- `Tradier WS ⚡` — WebSocket connected, streaming
- `Tradier WS …` — WebSocket connecting
- `Tradier WS ✗` — WebSocket error
- `Tradier REST` — REST polling active

### Auto-Fallback

If WebSocket fails 3 times consecutively (network error, `ws.tradier.com` blocked, session expired), the system automatically switches to REST polling with a toast notification. You don't need to do anything — it degrades gracefully.

### Cost

$0 additional. WebSocket streaming is included with all Tradier plans:
- Lite: $0/month
- Pro: $10/month  
- Pro Plus: $35/month

Uses the same API key you already have.

### Technical Details

1. On start, MomScanner creates a streaming session via `POST /v1/markets/events/session`
2. Opens `wss://ws.tradier.com/v1/markets/events` with the session ID
3. Subscribes to `trade`, `quote`, and `summary` events for all active tickers
4. The Web Worker batches incoming events per ticker into 1-second windows
5. Every second, the batch is posted to the main thread for scoring
6. One initial REST poll seeds `avgVol20` and `prevClose` (not available via stream)
7. Adding/removing tickers mid-session sends an updated payload — no reconnection needed
8. If no data flows for 15 minutes (very illiquid symbols), the session auto-closes and reconnects

---

## Impact on Existing Features

### OHLC Bars
With WebSocket: true OHLC from actual trade prints. Bars will match thinkorswim.  
With REST: bid/ask estimation + feed delta (v8.06.4 improvements).

### Volume Delta
With WebSocket: exact, derived from cumulative volume in trade events.  
With REST: estimated from poll-to-poll volume differences.

### Price Velocity
With WebSocket: computed from 1-second resolution data (60 samples/min).  
With REST: computed from 10-second resolution data (6 samples/min).

### TrendScore / BreakoutScore / PressureScore
Identical scoring functions in both modes. WebSocket provides more frequent updates (every 1 second vs every 10 seconds), so smoothed scores respond faster to price changes.

### CA v2 (Candle Accumulator)
Identical logic. With WebSocket, the sealed bars used for CA scoring contain true OHLC data, so the structural criteria (HH+HL, defensive structure, close position) are more accurate.

### VWAP Velocity
Identical logic. The VWAP itself is more accurate with WebSocket because it receives actual trade volume deltas instead of estimated ones.

### Trailing Stops
Identical logic. With WebSocket, peak price tracking is more precise because every trade print is captured — a 3-second spike that reverts is now visible.

---

## Previous Versions (included in v8.07)

### v8.06.4: OHLC Fix + Anti-Throttle + Ticker Exclude

- **Web Worker timer** prevents Chrome from throttling polling in background tabs
- **Bid/ask range estimation** for OHLC bars when tick count is low  
- **Feed session high/low delta tracking** captures moves between polls
- **Volume delta fix** — previous bar's volume carries forward for accurate deltas
- **Ticker exclude list** — input field below ticker bar, persists in localStorage
- **Poll rate pill** — shows actual polls/min (green ≥4, yellow 2-3, red ≤1)

### v8.06.3: VWAP Velocity Monitor

Three VWAP states shown as badges in the VWAP column:
- **↗ EXTENDING** (blue) — price pulling away from VWAP, momentum live
- **R REVERTING** (green) — pullback buy signal, 63.3% WR, PF 2.30
- **! OVEREXTENDED** (red) — extension > 1.5%, don't chase

### v8.06.2: Options Gate Removal

Removed `spreadOK` and `oiOK` as hard promotion gates. Options spread and OI are now display-only indicators (colored pills in the table).

### v8.06.1: Candle Accumulator v2

7 structural criteria (18 max points) scored per-window:

| # | Criterion | Max | Key Stat |
|---|-----------|-----|----------|
| 1 | Higher Close Streak | 4 | streak 4 = 56% WR |
| 2 | HH+HL Structure | 4 | Classical uptrend definition |
| 3 | Window Net Move | 3 | Tiered: 0.02/0.10/0.20% |
| 4 | Above VWAP | 1 | Binary confirmation |
| 5 | Defensive Structure | 2 | No lower lows = 48.4% WR |
| 6 | Close in Upper Half | 2 | Consistent buy-side control |
| 7 | Aggressive Green Candle | 2 | Body ≥ 0.15% of price |

Signal levels: Early (E, yellow) ≥ 55%, Confirmed (C, green) ≥ 72%, High Conviction ≥ 80%.

---

## Trading Setups

### Ideal Entry (REVERT + CA Confirmed)
- TrendScore ≥ 65
- CA% ≥ 72% (C badge)
- VWAP State = REVERTING (R badge — pullback buy)
- Price above VWAP, extension < 1.5%

### DRIFT Trade
- TrendScore 65–75, sustained
- CA% 55–72% (E badge)
- VWAP State = EXTENDING or REVERTING
- Low velocity, extension < 1.0%

### When NOT to Enter
- VWAP State = OVEREXTENDED (!) — wait for pullback
- MomentumType = reversal — the move is over
- Extension > 3% — you're chasing (your CLSK trade on 5/26)

---

## Settings Reference

### Feed Settings
| Setting | Default | Options |
|---------|---------|---------|
| Feed | Tradier | Tradier / Schwab |
| Feed Mode | WebSocket | WebSocket (real-time) / REST (polling) |

### v8.06.3 VWAP Velocity
| Setting | Default | Range |
|---------|---------|-------|
| Velocity Lookback | 3 min | 1–10 |
| Extending Threshold | 0.03 %/min | 0.01–0.20 |
| Reverting Threshold | -0.03 %/min | -0.01 to -0.20 |
| Overextended Limit | 1.50% | 0.50–3.00 |

### v8.06.1 Candle Accumulator v2
| Setting | Default | Range |
|---------|---------|-------|
| Confirmed Window | 5 bars | 3–10 |
| Early Window | 3 bars | 2–5 |
| Confirmed Threshold | 72% | 50–95% |
| Early Threshold | 55% | 30–80% |
| Aggressive Candle Body | 0.15% | 0.05–0.50% |

---

## OHLC Export Columns (28 columns)

Timestamp, Ticker, Open, High, Low, Close, Volume, VolumeDelta, VWAP, PctChg, IntradayPctChg, Bid, Ask, SpreadPct, RelVol, PriceVelocity, TrendScore, BreakoutScore, PressureScore, TrendState, BreakoutState, PressureState, MomentumType, Regime, TickCount, VWAPExt, VWAPVel, VWAPState.

With WebSocket mode, TickCount reflects actual trade prints per bar (typically 50-500 for active tickers) vs 1-6 with REST polling.

---

## Backtest Results

### CA v2 (3 days: 5/18–5/20)
| System | WR% | PF |
|--------|-----|-----|
| Old Binary ≥73% | 38.7% | 0.95 |
| CA v2 ≥55% (Early) | 46.4% | 1.63 |
| CA v2 ≥80% (High Conviction) | 55.4% | 2.35 |

### VWAP REVERT (5 days: 5/18–5/22)
| Signal | Trades | WR% | PF |
|--------|--------|-----|-----|
| REVERT (pullback buy) | 1,340 | 44.4% | 1.80 |

---

## Architecture

- **Single HTML file** — ~5,100 lines, no build system, no dependencies
- **Dual feed engine** — WebSocket Worker + REST polling, switchable at runtime
- **Web Worker #1** (timer) — 1-second heartbeat tick, immune to tab throttling
- **Web Worker #2** (WebSocket) — manages WSS connection, batches events, posts to main thread
- **Scoring pipeline** — 20+ functions, identical in both feed modes
- **GitHub Pages deployment** — paste and commit, same as always
- **All settings in localStorage** — carry over across versions

## Deployment

1. Go to `https://github.com/vaultlinkcrypto/MomScanner`
2. Click `index.html` → pencil icon
3. Ctrl+A → delete → paste new code
4. Commit changes
5. Wait 30–60s, hard refresh: Ctrl+Shift+R
6. Settings → Feed Mode: verify "WebSocket (real-time)" is selected
7. Feed pill should show "Tradier WS ⚡" once tickers are added and streaming begins
8. If WebSocket doesn't connect, it will auto-fallback to REST after 3 attempts
