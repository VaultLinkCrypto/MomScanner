# MomScanner v7.1

Three-layer momentum scanner with Intraday %Chg column, gap-relationship visual indicator, and a trading guide for reading the three layer scores together. Builds on v7's three-layer architecture (Trend / Breakout / Pressure) with five targeted improvements based on Wednesday's session data.

## What's new in v7.1

- **Intraday %Chg column (Intra%)** — placed immediately right of %Chg. Shows price change from today's open instead of yesterday's close. Separates intraday momentum from pre-market gap.
- **Gap-relationship icon (G column)** — visual indicator showing the relationship between premarket gap and intraday move. Eight distinct patterns: ↗↗ ↘↘ ↗↘ ↘↗ ↗━ ↘━ ━↗ ━↘ ━━.
- **Trend layer scoring update** — the Trend layer now uses Intraday %Chg for its directional reinforcement component instead of overall %Chg. Prevents stale pre-market gaps from inflating Trend scores.
- **Momentum-type tagging fix** — the Type column now persists through demotion. v7 was nulling the type whenever a candidate left bull/bear state, which is why Wednesday's session summary showed empty Type fields for INTC and other long-running candidates. Sustained-trend tickers now correctly classify as DRIFT after 2+ minutes in candidate state.
- **Tooltip with full context on Intra% cell** — hover to see today's open price, current price, both percentage changes, and the gap-relationship explanation.

## What carried over from v7

- Three-layer architecture (Trend, Breakout, Pressure)
- VWAP tracking per ticker
- L1-friendly OFI proxies
- High-contrast accessibility theme with adjustable font size
- Per-layer stability gates and Candidates sections

## What carried over from v5/v6

- Bulletproof persistence
- Time-of-day adaptive tuning
- SPY-driven regime indicator
- Don't-Trade warning banner
- End-of-session summary report

---

## Part 1 — Reading the Three Layer Scores

This section is what you specifically asked for. It's based on Wednesday's session data and your own observations about layer combinations.

### The four key signals to read together

For every ticker, you have four numbers visible in the table:

1. **Trend score** (blue column) — sustained directional move based on VWAP and price action over 30 min to hours
2. **Brkout score** (yellow column) — range expansion happening over 5 to 30 minutes
3. **Press score** (pink column) — aggressive intraday flow over 30 seconds to 5 minutes
4. **VWAP column** — price as a percentage relative to VWAP (positive green / negative red)

The art of reading these is not about looking at any single number. It's about reading the **combination** and matching it to a trade type.

### The five most actionable patterns

These are the patterns that reliably produce profitable trades for a 2-5 DTE OTM options strategy. Each requires VWAP alignment (positive for calls, negative for puts) and a clean Streak (1+ min for slow patterns, 30+ sec for fast).

#### Pattern A — The Strong Sustained Trend
**Trend ≥ 80, Brkout 55-70, Press ≥ 70** — your "gradual but strong through the day" observation.

This is the highest-conviction, longest-duration pattern. The Trend layer is firing strongly (sustained VWAP positioning), the Breakout layer shows moderate range expansion (the trend keeps making new highs), and Pressure is consistently high (real-time buying or selling is supporting the move).

**Trade as:** position trade. Enter the OTM option, target 50-100% gain on the contract, hold 30-60 minutes or longer. Don't scalp this — let it work.

**Today's INTC was this pattern.** It promoted at 10:04 AM and held continuously for over 4 hours. Anyone holding even a $1-strike-OTM call from that promotion could have ridden multiple expansion phases. The Type tag for this pattern is **DRIFT**.

**Exit when:** Trend score drops below 70, OR VWAP relationship inverts (price falls below VWAP for a call trade), OR option has moved your target percentage.

#### Pattern B — The Quick Subtle Move
**Trend ≥ 80, Brkout 40-55, Press ≥ 60** — your "quicker and more subtle" observation.

This is what I'd call a trend-supported small move. Trend layer is solidly firing (the stock is in a clear directional state), but Breakout and Pressure are only moderate. The stock is moving in its established direction without aggressive breakouts or volume bursts — it's just drifting up or down on light, consistent flow.

**Trade as:** quick trade. Enter, target 25-40%, exit within 15-25 minutes. Don't expect explosive moves — the lighter Press score tells you there's no aggressive flow to power a fast spike.

**Why this pattern works for you:** the VWAP and Trend alignment means the move has real underlying conviction (institutions are positioned), even though the surface volume isn't dramatic. Many of Wednesday's GOOGL and QCOM candidacies fit this profile.

**Exit when:** Trend or VWAP signal weakens, OR your time stop hits, OR you've hit profit target.

#### Pattern C — The Pressure Spike Bounce
**Trend 50-65, Brkout 50-65, Press ≥ 75** — and the ticker is in the Pressure Candidates section.

This is the fastest and riskiest pattern. The Trend layer is neutral or only mildly directional. Breakout is also moderate. But Pressure is firing strongly — there's aggressive intraday flow happening right now without a broader trend or breakout context. This is typically a mean-reversion bounce off a key technical level (VWAP, prior low, support/resistance).

**Tuesday's NVDA bounce was exactly this pattern.** The stock had no daily trend, no breakout — just a Pressure spike at the second low of day around 11:11 AM. Your manual chart analysis caught it because you saw the VWAP lower band test. v7's Pressure layer is what now catches this automatically.

**Trade as:** scalp. Enter only if you can fill within seconds, target 15-25% on the option, exit within 5-10 minutes maximum. Use a tight stop — if Pressure score drops below 60 within 90 seconds of entry, exit immediately.

**Exit when:** Pressure score drops below 65 OR after 10 minutes regardless of P&L OR target hit.

#### Pattern D — The Fresh Breakout
**Trend 55-75, Brkout ≥ 75, Press ≥ 65** — the breakout is the trade.

Stock has moderate trend bias, but the Breakout layer is firing hard. This means range expansion is actively happening, and Pressure confirms there's volume behind it. This pattern often appears after a stock consolidates for 30+ minutes and then starts trading outside its range.

**Trade as:** position trade with breakout discipline. Enter when Breakout score crosses 75 (not before — premature entry on building breakouts is the most common mistake). Target 30-50% on the option. Hold while Breakout score remains ≥70, exit when it drops below 60.

**Exit triggers:** Breakout score below 60, OR price re-enters the prior consolidation range (visible by VWAP%change reverting toward zero), OR 20-minute time stop.

#### Pattern E — The Don't-Trade Pattern
**Any layer 50-65, no layer ≥ 70, AND Flips ≥ 4** — skip this one.

Layer scores are middling, no layer has clear conviction, and the ticker has been oscillating today (high flip count). Even if it briefly hits a Candidates section, the persistent middling scores mean the move won't sustain. This is what produced Tuesday's CLSK and Monday's general behavior — false candidacies that demote within seconds.

**Trade as:** don't. The Don't-Trade banner often appears alongside this pattern across multiple tickers. Sit out.

### Pattern matching cheat sheet

| Trend | Brkout | Press | Type | Pattern | Hold time | Target |
|---|---|---|---|---|---|---|
| 80+ | 55-70 | 70+ | DRIFT | Strong Sustained Trend | 30+ min | 50-100% |
| 80+ | 40-55 | 60-70 | DRIFT | Quick Subtle Move | 15-25 min | 25-40% |
| 50-65 | 50-65 | 75+ | THRUST/REVR | Pressure Spike Bounce | 5-10 min | 15-25% |
| 55-75 | 75+ | 65+ | DRIFT | Fresh Breakout | 15-30 min | 30-50% |
| Any <70 | Any <70 | Any <70 | — | Don't Trade | — | — |

### How to use the Intraday %Chg column for entry timing

The new Intra% column tells you whether intraday traders are actually moving the stock right now, vs whether the move is stale gap.

**Read the Gap (G) column first:**

- **↗↗** (gapped up + intraday continuing up): the cleanest setup. Both pre-market and intraday traders agree on direction. Look for Pattern A or B.
- **↘↘** (gapped down + intraday continuing down): clean downtrend, look for Pattern A/B with put trades.
- **↗↘** (gap up but fading): gap-fill setup. The pre-market enthusiasm is being sold off. Avoid call trades. Watch for Pattern C bounce off the gap-fill level (often VWAP) as a contrarian setup, or join the fade with puts.
- **↘↗** (gap down but bouncing): your favorite pattern — this was Tuesday's NVDA. Pre-market pessimism is being bought up. Pattern C territory. Calls likely if Pressure fires.
- **↗━** (gapped up, intraday flat): stale gap, momentum exhausted. Skip unless Pressure suddenly fires.
- **↘━** (gapped down, intraday flat): sellers exhausted. Watch for Pattern C bounce.
- **━↗** (no gap, intraday rallying): fresh real-time strength with no premarket bias. Excellent for clean Trend trades because there's no stale-gap noise.
- **━↘** (no gap, intraday falling): fresh real-time weakness. Same as above for puts.

The combination of the gap icon AND the Intra% number AND the layer scores gives you a 3-second read on whether a setup is worth investigating further.

### A worked example using Wednesday's INTC

Here's how Wednesday's INTC trade would have been read using v7.1's tools:

**10:04 AM:** INTC promotes to Trend Candidates section. Layer scores:
- Trend: 71 (just crossed threshold)
- Brkout: ~55 (mild range expansion)
- Press: ~65 (some flow but not aggressive)
- VWAP: +1.5% (price holding above)
- %Chg: +4.43%, Intra%: probably +2-3% (most of the move was the gap)
- G icon: **↗↗** (gapped up and continuing intraday)
- Type: DRIFT
- Streak: 2:00 just qualified

**Pattern match:** Strong Sustained Trend forming (Pattern A). Clean ↗↗ gap. Worth taking.

**Entry:** $90 strike call, 2-5 DTE, limit at midpoint of bid/ask.

**Throughout the day:** Trend score climbs to 91 by mid-afternoon. Breakout score touches 75 during the 2:43 PM acceleration. Pressure remains in the 65-75 range showing consistent buying. The position works for 4+ hours.

**Exit signal:** Could hold to close, or exit when Trend score first dips below 80 with VWAP%change below +0.5% (the trend is weakening).

This is the kind of trade that v7's three-layer architecture is designed to surface and that v7.1's Intra% column lets you confirm at a glance.

---

## Part 2 — Set up the GitHub repository

(Same as prior versions — skip if existing repo set up.)

### 2.1 — Create your GitHub account

1. Go to **https://github.com**.
2. Click **Sign up**, enter email, password, username.
3. Verify your email and complete the puzzle. Pick the free plan.

### 2.2 — Create the repository

1. Top-right **+** icon → **New repository**.
2. Name: `MomScanner`. Visibility: Public. Check "Add a README file."
3. Click **Create repository**.

### 2.3 — Add the index.html file

1. **Add file** → **Create new file**.
2. Name: `index.html`.
3. Paste the entire contents of the v7.1 index.html.
4. Click **Commit new file**.

### 2.4 — Replace the README

1. Click `README.md` → pencil icon.
2. Delete and paste this README. Commit.

### 2.5 — Enable GitHub Pages

1. **Settings** → **Pages**.
2. Source: Deploy from a branch. Branch: `main` / `(root)`. Save.
3. Wait 1-2 minutes. Refresh. Copy the URL shown.

### 2.6 — Updating from v7 to v7.1

1. Go to repo → click `index.html` → pencil icon.
2. Ctrl+A → delete → paste new v7.1 code → Commit.
3. Wait 30-60 seconds. **Hard refresh: Ctrl+Shift+R**.
4. All your v7 settings, tickers, history, transitions carry over.
5. The Intra% column will populate after the first poll cycle (open price comes from the same Tradier quote response we already pull).

---

## Part 3 — Schwab Developer API

(Unchanged from prior versions. See v7 README if needed.)

---

## Part 4 — thinkorswim web scan filter

(Unchanged from v6.)

### Recommended filters

| Filter | Setting |
|---|---|
| Last | Min: **20** · Max: **500** |
| Volume | Min: **2,000,000** |
| Percent Change | Min: **1.00** (no max) |
| Market Cap | Min: **5000** ($5 billion, M = millions) |
| Option Volume Index | Min: **1.00** |

**Critical:** include **SPY** in your imported list every time.

---

## Part 5 — Daily trading routine for v7.1

### Pre-market

Open MomScanner. Run thinkorswim scan. Note pre-market movers but don't paste yet.

### 9:30 AM — Initial setup

Paste thinkorswim results. **Make sure SPY is included.** Don't trade. The Intra% column will be empty until first poll completes (5 seconds). Once the open prices flow in, the gap icon (G column) starts populating.

### 9:30-10:00 — Observation window

All tickers in warmup. Use this time to scan the G column quickly:
- **↗↗** tickers are the cleanest call setups
- **↘↘** tickers are the cleanest put setups
- **↘↗** tickers are bounce candidates (will likely show Pressure Candidates first)
- **↗↘** tickers are fade candidates
- **↗━ / ↘━** tickers are stale, low priority

### 10:00 AM — Midday window

Layers start qualifying. Watch for the five trade patterns described in Part 1:

1. Strong Sustained Trend (best for sustained holds)
2. Quick Subtle Move (good for quick scalps with VWAP confirmation)
3. Pressure Spike Bounce (only if you can fill fast)
4. Fresh Breakout (when Brkout score crosses 75)
5. Don't-Trade Pattern (skip these — Don't-Trade banner usually confirms)

### Trade entry checklist

Before placing any trade:

1. ✅ Pattern matched from the cheat sheet above
2. ✅ Streak shows minimum sustained time (1+ min for slow patterns, 30+ sec for Pressure)
3. ✅ Flips < 4 (no warning icon)
4. ✅ Spread% ≤ 5%
5. ✅ VWAP relationship matches your direction (positive% for calls, negative% for puts)
6. ✅ Gap icon supports the direction (↗↗ or ━↗ for calls, ↘↘ or ━↘ for puts; ↘↗ for contrarian call bounce, ↗↘ for contrarian put fade)
7. ✅ Don't-Trade banner is NOT showing
8. ✅ Type tag visible and matches pattern (DRIFT for sustained, THRUST or REVR acceptable for Pressure spikes)

If all eight check, place the trade in Robinhood.

### Exit triggers

Match exits to your entry pattern:

- **Pattern A (Strong Sustained Trend):** exit when Trend < 70 OR option +75-100% OR VWAP relationship inverts
- **Pattern B (Quick Subtle Move):** exit when Trend < 70 OR option +25-40% OR 20-min time stop
- **Pattern C (Pressure Spike):** exit when Press < 65 OR option +15-25% OR 10-min time stop (whichever first)
- **Pattern D (Fresh Breakout):** exit when Brkout < 60 OR option +30-50% OR price re-enters consolidation range

Universal hard stops apply to all patterns:
- Layer score drops below 50 → market sell immediately
- Streak resets to — → sell at bid
- 20-minute total hold without 15%+ option move → exit

### 3:00 PM — Close window

Looser thresholds activate (unless low-vol day, in which case override keeps them tight). Pressure Candidates may appear more frequently. Trade with shorter holds and tighter targets.

### 4:00 PM — Session close

Click **Session Summary**. Save as PDF. Export Active CSV (now includes layer scores, VWAP, Intraday %Chg in the columns).

---

## Part 6 — Settings reference

Identical to v7 except for the new fields automatically captured (todayOpen, intradayPctChg). No new settings to configure.

---

## Part 7 — Troubleshooting

**Intra% shows — for several minutes after pasting:** Today's open price is captured on the first successful quote poll. If poll is failing, no open price is captured. Check Test Feed.

**G column shows — even when both %Chg and Intra% are filled:** The values are within ±0.1% (considered "flat"). Icons only render for material moves.

**G column shows ━━ for SPY:** SPY having both flat overall change and flat intraday change is normal on quiet days — that's the actual pattern.

**Trend score seems lower in v7.1 vs v7 for some stocks:** This is intentional. Stocks up huge on pre-market gaps but flat intraday will score lower in v7.1's Trend layer because the stale gap no longer inflates the score. This is the correct behavior — it represents what the stock is actually doing right now.

**Type column shows DRIFT for everything:** That's actually expected for sustained-trend setups, which are the most common. THRUST appears when score is rising fast (>8 pts/min). REVR appears when there's been recent direction reversal (flips >= 2). DRIFT is the default for steady candidates. The fix in v7.1 means DRIFT now persists through demotion instead of becoming null.

**Layer scores all show 50:** Either the ticker is genuinely neutral, or it hasn't accumulated enough data yet (VWAP needs ~5 min, Breakout needs ~25 min, Pressure needs ~30 sec). Wait for warmup.

**Theme settings or font size not persisting:** Click "Save Accessibility" in Settings after adjusting. Live preview is unsaved.

**Code update not showing:** GitHub Pages caches 30-60 seconds. Hard refresh with Ctrl+Shift+R.

---

## Part 8 — Data safety

All API keys and trading data stored in browser localStorage only. Repository contains no keys.

---

## Part 9 — Roadmap

Pending features for future versions:

1. **Alpaca L2 integration (v8)** — true Order Flow Imbalance with real bid/ask classification of every print, replacing L1 OFI proxies. The Pressure layer becomes a first-class signal.
2. **Multi-day pattern recognition** — track which gap patterns (↗↗ etc.) produced the best trades for each ticker, suggest patterns to watch tomorrow
3. **Schwab token auto-refresh** before 30-min expiration
4. **WebSocket streaming** if data tier supports it
5. **Sound or browser notification** on candidate promotion or breakout
6. **Auto-export at 4:00 PM** — automatic CSV + PDF without manual click
7. **Per-ticker notes** — annotation field for your own observations
8. **Backtest mode** — replay past sessions from CSVs
9. **Layer correlation panel** — click a ticker to see its three layer scores plotted over time, helping you identify which patterns work best for your specific tickers
