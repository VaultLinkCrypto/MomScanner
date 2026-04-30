# MomScanner v7.2

Audio alarms for new candidates, Pre-Promotion Watch indicator for early heat detection, and Near-Miss panel showing strong-score tickers blocked by options-liquidity gates. Builds on v7.1 with three additions targeting the observations from Wednesday's session: missed early moves, untradable options on otherwise-strong stocks, and the need for off-screen alerts.

## What's new in v7.2

- **Audio Alarms** — plays a sound on every new candidate promotion. Choose from four built-in sounds (Bell, Chime, Alert, Tick) or upload your own MP3/WAV file (≤1MB, ≤3 seconds recommended). Volume slider, cooldown timer, optional softer alarm for Pre-Promotion Watch heat-ups, all configurable in Settings.
- **Pre-Promotion Watch indicator** — a pulsing ↑ icon appears next to a ticker's symbol when both (a) Trend or Breakout score has reached the build-up zone (≥60), AND (b) Pressure score crossed ≥60 within the last 90 seconds. This is a 30-90 second advance warning that the ticker is about to qualify, addressing the v7.1 observation that "the easy move had already happened by the time it became a candidate."
- **Near-Miss panel** — collapsible panel between the main table and the Session Log. Shows tickers with strong layer scores (≥70) that are blocked from candidacy by spread, OI, or RVol gates. Lists exactly what's blocking each one. Useful for understanding broader market direction even when MomScanner's own filters reject the options trade.

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
- SPY-driven regime indicator
- Don't-Trade warning banner
- Momentum-type classifier
- End-of-session summary report

---

## Part 1 — Audio Alarms (v7.2)

### Why this matters

You can't keep your eyes glued to MomScanner for 6.5 hours. While you're looking at thinkorswim charts, watching CNBC, or stepping away briefly, the scanner needs a way to call you back when something interesting happens. Audio alarms solve this.

### What triggers the alarm

The alarm fires when **any layer (Trend, Breakout, or Pressure) promotes a ticker from watch/warmup to bull or bear**. It does NOT fire when:

- A ticker flips between bull and bear (already-active candidate changing direction)
- A ticker is demoted from bull/bear to watch
- A pre-promotion heat occurs (unless you enable that option separately)

This is intentional. Hearing the alarm should mean "a NEW opportunity just appeared" — not "an existing candidate did something."

### How to enable

1. Click the **gear icon** (top right).
2. Scroll to **Audio Alarms (v7.2)** section.
3. Check **"Play sound when a new candidate appears."**
4. Choose a sound from the dropdown (default is Bell).
5. **Click the ▶ Test button** — this is critical. Browser security requires you to interact with the page before any audio can play. The Test button counts as that interaction.
6. Click **Save Audio Settings**.

After this, alarms will fire automatically whenever a new candidate promotes during your session.

### Built-in sounds

Generated programmatically via the Web Audio API — no external file dependency, work offline, sized appropriately:

- **Bell (default)** — two-tone bell, ~0.5 seconds. Pleasant, not jarring.
- **Soft Chime** — descending three-note chime, ~0.9 seconds. Most subtle option.
- **Sharp Alert** — double-pulse square wave, ~0.3 seconds. Most attention-grabbing.
- **Tick** — single short ping, ~0.1 seconds. Minimal interruption.

### Custom sounds (MP3 or WAV)

If the built-ins don't suit you, upload your own:

1. Choose **"Custom file (uploaded)"** in the dropdown.
2. Click **Choose File** in the Upload row.
3. Select an MP3 or WAV file from your computer.
4. **Maximum file size: 1MB.**
5. **Recommended length: 1-3 seconds.** Longer sounds will play in full but may overlap if multiple promotions happen close together.

The file is stored as a base64 data URL in your browser's localStorage. It persists across sessions but stays only on your local browser — no upload to any server.

**Common sound suggestions for trading alerts:**
- A short bell, gong, or chime (1-2 seconds)
- A "ding" or "ping" notification sound
- A spoken word like "Alert" or "Candidate"
- A trading floor bell sample (often available free online)

Avoid: voiced sentences, music clips, anything requiring more than 3 seconds of attention.

### Volume slider

Range: 0 to 100 in 5-point increments. The volume applies to both built-in and custom sounds. Default 70% is a good starting point — loud enough to hear from the next room but not jarring.

### Cooldown timer

Range: 0 to 30 seconds. Prevents rapid-fire alerts when multiple tickers promote within seconds of each other (which happens often during the close window).

- **0 seconds** — every promotion plays. Can be very chatty.
- **3 seconds (default)** — good balance. You hear cluster events but they don't overlap.
- **10+ seconds** — minimal alerts. You hear "something is happening" but not how many.

### Pre-promotion alarm option

Separate checkbox in the same panel. When enabled, plays the same sound at **40% softer volume** when a Pre-Promotion Watch heat is detected (see Part 2 below). This gives you advance warning even before the actual promotion. Honors the same cooldown timer as the main alarm.

I'd recommend leaving this disabled at first while you learn the patterns, then enable it once you trust the Pre-Promotion indicator.

### Important: browser audio policy

Modern browsers block audio playback until the user interacts with the page. Specifically:

- **Before clicking Test:** No audio will play, even if alarms fire on a promotion. The browser silently rejects the playback.
- **After clicking Test:** Audio is unlocked for the rest of the session.
- **After page reload:** You need to click Test again (or any other button) to re-unlock audio.

The Test button's primary purpose is the unlock. The secondary purpose is letting you preview the sound. **Always click Test once at the start of each trading session** to ensure alarms will work.

If you reload the page mid-session and forget to click Test, alarms won't play silently for the rest of the day. To verify audio is working: open settings, click Test. If you hear it, you're good.

---

## Part 2 — Pre-Promotion Watch Indicator (v7.2)

### Why this matters

In Wednesday's session, you observed that several stocks "had their price movement above the VWAP support line and VWAP Mean value, and the easy-to-spot price action movement had already happened by the time they were listed as candidates." This is a real tension in the design: the stability gates (8 of 10 cycles + 60-second streak) prevent v6's flickering false candidates, but they also delay promotion until AFTER the move is established.

The Pre-Promotion Watch indicator addresses this by giving you 30-90 seconds of advance warning when a ticker is heating up but hasn't yet cleared the stability gate.

### What triggers the indicator

A small pulsing ↑ icon appears next to the ticker symbol when ALL of the following are true:

1. The ticker is currently in the **Watching** section (not already a candidate)
2. **Trend score ≥ 60** OR **Breakout score ≥ 60** — at least one slow layer is in build-up zone
3. **Pressure score crossed above 60 within the last 90 seconds** — fast layer is firing right now

The combination is what matters. A high Trend score alone is not enough — that's why this isn't a Candidate yet. A Pressure spike alone is not enough — that's a fleeting flicker. The combination of "slow layer building" + "fast layer just fired" is the signature of an imminent promotion.

### How to use it

When you see the ↑ icon:

1. **Open thinkorswim**, pull up the chart.
2. **Verify with chart action:** Is the stock breaking above VWAP? Bouncing off support? Making a new intraday high? The chart confirms or rejects what MomScanner sees.
3. **Pre-position your option order:** Open Robinhood, find the right strike (one OTM), set up a limit order at midpoint price. Don't submit yet.
4. **Watch for promotion:** When the layer score actually clears the stability gate (the dot turns solid green or red), submit the order.

This workflow turns a 60-90 second delay into a head start. By the time MomScanner officially promotes the ticker, your chart is already up and your order is ready to submit.

### When to ignore it

Not every Pre-Promotion eventually promotes. The slow layer may fade before the stability gate clears. Ignore the indicator when:

- The Don't-Trade banner is showing (the broader market isn't supporting the move)
- Flips count is already ≥ 4 (the ticker is too choppy to trust)
- VWAP relationship is opposite to the implied direction (e.g., Trend score 65 but price below VWAP — mixed signal)
- The Pressure score has dropped back below 60 (the heat is fading, not building)

### Why the icon pulses

The pulsing animation is intentional — it's catching your eye in your peripheral vision while you're focused elsewhere. Combined with the optional Pre-Promotion audio alarm, you get both visual and audio signals for an event that's not yet a confirmed Candidate.

---

## Part 3 — Near-Miss Panel (v7.2)

### Why this matters

Wednesday's session showed 56 tickers with strong layer scores (≥65 in at least one layer) that never qualified as Candidates. Of those, 51 were trading above VWAP — meaning your "above VWAP" intuition was correct, the scanner was tracking these stocks, but the options-liquidity filters (spread ≤5%, OI ≥1000, RVol ≥1.5) were preventing them from showing up as actionable.

This is the scanner doing its job correctly — those stocks would be bad options trades because the spread eats your profit before the stock moves. But it also means you have no visibility into the broader market direction those stocks represent.

The Near-Miss panel gives you that visibility without compromising the strict options-liquidity gates.

### What it shows

A sortable table listing tickers with at least one layer score ≥70 that are NOT currently a candidate. For each, you see:

- All three layer scores (Trend, Brkout, Press)
- Price position relative to VWAP (in %)
- Overall %Chg (vs yesterday's close)
- Intraday %Chg (vs today's open)
- Options spread %, OI, and RVol (the values being filtered)
- **Blocked By** column listing the specific gate(s) preventing candidacy

### How to use it

The panel is collapsed by default. Click its header to expand. Then:

**For market context:** Scan the panel during slow periods. If many tickers show strong scores but are all blocked by wide spreads, that tells you about today's options market structure (often happens on low-volume mornings or earnings days).

**For stock trades:** If you also trade stocks (not just options), the Near-Miss panel surfaces stocks moving meaningfully today that you might trade as shares. Same scoring, no options-liquidity filter.

**For tomorrow's planning:** Note which tickers consistently appear in Near-Miss. They're often "almost-tradable" symbols that may have tighter options activity on different days. Worth watching them on similar setups.

**For confirming the broader move:** If your candidate is INTC up 3% but you also see SWKS, NVTS, AVGO, and AMD in the Near-Miss panel all up 2%+ above VWAP, that's a sector confirmation. Semiconductors are moving as a group. Your INTC position is more likely to sustain.

### What blocks tickers most often

Based on Wednesday's data, in order of frequency:

1. **Wide options spread** (>5%) — the most common blocker. Affects stocks under $50 and most low-volume names.
2. **Low RVol** (<1.5x) — stocks moving on news without unusual volume.
3. **Low OI** (<1000) — niche tickers with thin option markets.
4. **Streak not held** — strong score but hasn't sustained the minimum streak duration yet.

The Blocked By column tells you exactly which ones apply for each ticker.

---

## Part 4 — Set up the GitHub repository

### Important: keeping v7.1 accessible

You've saved v7.1 as `index_V7.1.html` in your repo. With GitHub Pages, you can access both files independently:

- `https://YOUR_USERNAME.github.io/MomScanner/` → loads `index.html` (now v7.2)
- `https://YOUR_USERNAME.github.io/MomScanner/index_V7.1.html` → loads v7.1

Both run independently. They share the same localStorage origin (same domain), which means your settings, history, and tickers carry across both. If you want truly isolated state between v7.1 and v7.2, run them in different browsers.

### 4.1 — Updating from v7.1 to v7.2

1. Go to repo → click `index.html` → pencil icon.
2. Ctrl+A → delete → paste new v7.2 code → Commit.
3. Wait 30-60 seconds. **Hard refresh: Ctrl+Shift+R.**
4. All your v7.1 settings, tickers, history, and transitions carry over.
5. **Click the gear icon, scroll to Audio Alarms, click ▶ Test once.** This unlocks the audio system for the session.

### 4.2 — Verifying the upgrade worked

After hard refresh:
- Header should read "MOMENTUM TERMINAL v7.2"
- Settings drawer should have a new "Audio Alarms (v7.2)" section
- Below the main table you should see a new "NEAR-MISS" panel (collapsed by default)
- Pre-Promotion ↑ icon will appear next to ticker symbols when conditions are met

---

## Part 5 — Daily trading routine for v7.2

### Pre-market

1. Open MomScanner in your browser.
2. **Open settings → Audio Alarms → click ▶ Test** to unlock audio for the session.
3. Verify audio settings (volume, cooldown, sound choice) are correct for the day.
4. Run thinkorswim scan, get list of symbols. Don't paste yet.

### 9:30 AM

Paste tickers including SPY. Audio system is already unlocked from the Test click.

### Throughout the session

- When you hear the alarm, look at MomScanner. A new candidate just appeared in one of the three layer Candidates sections.
- When you see a pulsing ↑ icon next to a ticker in Watching, the ticker is heating up. Pre-position your trade if you trust the setup.
- During slow periods, expand the Near-Miss panel to see what's moving in the broader market.

### Audio cooldown management

The default 3-second cooldown is good for most trading. If you find yourself missing alerts:
- Lower cooldown to 1-2 seconds during the close window (more activity)
- Raise to 5-10 seconds during quiet midday hours (avoid noise)

### 4:00 PM session close

Click Session Summary. The summary now also shows audio-alarm-related transitions (any layer promotion that triggered the alarm).

---

## Part 6 — Reading the three layer scores (carried from v7.1)

### The five trade patterns

These are the patterns that reliably produce profitable trades. v7.2 doesn't change the pattern logic — it just gets you to the patterns faster (audio + pre-promote indicator).

| Trend | Brkout | Press | Type | Pattern | Hold time | Target |
|---|---|---|---|---|---|---|
| 80+ | 55-70 | 70+ | DRIFT | Strong Sustained Trend | 30+ min | 50-100% |
| 80+ | 40-55 | 60-70 | DRIFT | Quick Subtle Move | 15-25 min | 25-40% |
| 50-65 | 50-65 | 75+ | THRUST/REVR | Pressure Spike Bounce | 5-10 min | 15-25% |
| 55-75 | 75+ | 65+ | DRIFT | Fresh Breakout | 15-30 min | 30-50% |
| Any <70 | Any <70 | Any <70 | — | Don't Trade | — | — |

### Trade entry checklist (10 items, expanded for v7.2)

1. ✅ Audio alarm fired (you heard the new candidate)
2. ✅ Pattern matched from the cheat sheet
3. ✅ Streak shows minimum sustained time (1+ min for slow patterns, 30+ sec for Pressure)
4. ✅ Flips < 4 (no warning icon next to ticker)
5. ✅ Spread% ≤ 5%
6. ✅ VWAP relationship matches your direction
7. ✅ Gap icon supports the direction
8. ✅ Don't-Trade banner is NOT showing
9. ✅ Type tag visible and matches pattern
10. ✅ (NEW) If Pre-Promotion ↑ was visible 30-60 seconds before promotion, that's a confirmation — these promotions are typically more sustained

If all check, place the trade.

---

## Part 7 — Settings reference

### Data Source
Tradier or Schwab keys, callback URL, environment selection.

### Options Liquidity Filter
Penny Pilot toggle, max spread %, min OI, max DTE, options check interval.

### Score Weights (legacy)
Sliders only affect the legacy single-score view. v7+ uses layer thresholds instead.

### Time-of-Day Tuning (v5)
Toggle. Adapts thresholds across the three time windows.

### Stability Filter (v4)
Window, Min Qual, Min Streak, Flip Warn.

### Behavior
Smoothing Lag, High Threshold, Low Threshold, Min Refresh.

### Audio Alarms (v7.2) — NEW
Enable, Pre-Promote secondary alarm, Sound choice (4 built-in + custom), Test button, Volume, Cooldown.

### Accessibility (v7)
Theme picker (4 options), Base font size slider (11-22px), live preview, save.

---

## Part 8 — Troubleshooting

**Audio alarm doesn't play when a candidate promotes:** Click the ▶ Test button in Settings → Audio Alarms. Browser policy requires a user gesture before audio can play. Test counts. After Test plays once, alarms will fire automatically for the rest of the session.

**Audio plays for the Test button but not for actual promotions:** Check that "Play sound when a new candidate appears" is checked. Also verify Cooldown isn't set so high that alarms are being suppressed.

**Custom sound won't upload:** File must be ≤ 1MB and MP3 or WAV format. If your file is too large, trim it to under 3 seconds using any audio editor (Audacity is free).

**Custom sound uploaded but doesn't play on alarm:** Check that the dropdown is set to "Custom file (uploaded)" and not one of the built-ins. Click Save Audio Settings.

**↑ icon never appears:** Pre-Promotion requires (a) Trend or Breakout ≥ 60 AND (b) Pressure crossed ≥ 60 in last 90 seconds. On low-vol days where Pressure stays neutral, this combination won't occur. Normal.

**↑ icon appears constantly:** Indicates very active intraday flow on multiple tickers. On a real trending day this is expected. If it feels like noise, the Pre-Promotion logic is working — many of these heat-ups will not promote, which is why we don't fire the loud alarm by default.

**Near-Miss panel always empty:** No tickers have score ≥70 with options-gate failures. On low-vol or low-volume sessions this is normal. Otherwise check that your active scan has loaded enough tickers with real movement.

**Browser console shows audio errors:** Check DevTools → Console. If you see "DOMException: play() failed" — that's the user-gesture requirement. Click Test in settings.

**Code update not showing:** GitHub Pages caches 30-60 seconds. Hard refresh with Ctrl+Shift+R.

---

## Part 9 — Data safety

All API keys, sound files (as base64 data URLs), trading data — stored in browser localStorage only. Never transmitted except directly to Tradier/Schwab API endpoints. Repository contains no keys.

The audio file you upload stays in your browser. If you clear site data, your custom sound is also cleared and you'll need to re-upload it.

---

## Part 10 — Roadmap

Pending features for future versions:

1. **Alpaca L2 integration (v8)** — true Order Flow Imbalance with real bid/ask classification.
2. **Schwab token auto-refresh.**
3. **Multiple custom sounds** — assign different sounds per layer (e.g., Bell for Trend, Chime for Breakout, Tick for Pressure).
4. **Browser desktop notifications** — system tray alerts when MomScanner tab is in the background.
5. **Spread trend indicator** — widening vs tightening over last 5 minutes.
6. **Multi-day summary archive browser.**
7. **Auto-export at 4:00 PM** — automatic CSV + PDF.
8. **Per-ticker notes** — annotation field.
9. **Backtest mode** — replay sessions from CSVs.
10. **Voice narration option** — short spoken phrase like "INTC, Trend, Bull" instead of a sound effect.
