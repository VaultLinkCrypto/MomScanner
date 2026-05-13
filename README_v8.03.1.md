# MomScanner v8.03.1

Safety hotfix release. Adds the Session Protection Suite (5 layered defenses against accidental session loss) on top of v8.03. **No promotion logic changes, no scoring changes, no UI changes outside of the new protection elements.** This is a focused safety patch — ship it, get protected, then continue gathering data for the larger v8.04 release.

**Live URL:** https://vaultlinkcrypto.github.io/MomScanner/

## Why v8.03.1 exists

On 5/8/2026, an accidental mouse touch caused the Chrome browser to navigate from MomScanner to google.com. On reload, the in-memory OHLC buffer dropped from a full session's worth of bars to only 1,500. Hours of data and real-time visibility were lost mid-session.

Every other feature MomScanner offers depends on the session staying alive. A perfect logger does nothing if a single accidental click can wipe it out. **Session integrity must be bulletproof before anything else.**

v8.03.1 fixes this with five layered defenses, plus a continuous localStorage backup so even worst-case data loss is capped at 30 seconds.

## What's new in v8.03.1

### The five protection layers

**Layer 1 — Before-Unload Confirmation**
When you try to close the tab, refresh, or navigate away, Chrome shows its native "Leave site?" dialog. Requires a deliberate click to actually leave. Catches every form of intentional or accidental tab closure.

**Layer 2 — Back/Forward Navigation Block**
The browser back and forward buttons (and their equivalents: touchpad swipe gestures, mouse thumb buttons) are intercepted before they can navigate. A red banner slides down at the top of the page confirming the block fired.

**Layer 3 — Keyboard Shortcut Block**
The dangerous shortcuts F5, Ctrl+R, Ctrl+Shift+R, Ctrl+F5, and Ctrl+W are intercepted and blocked. A toast notification tells you what was blocked.

**Layer 4 — Right-Click + Mouse Buttons 4/5 Block**
Right-click context menu is blocked (preventing accidental "Reload" or "Back" selections). Mouse buttons 4 and 5 (the thumb buttons on most modern mice, often configured for browser back/forward) are blocked at the page level.

**Layer 5 — Continuous LocalStorage Backup**
Every 30 seconds, MomScanner snapshots the OHLC buffer (and recent transitions) into Chrome's localStorage. If the page ever does reload, you'll be greeted with a restore prompt showing exactly how many bars and transitions are available to recover. Worst-case data loss is capped at 30 seconds.

### The 🏁 End Session button

A new button in the verification banner at the top of the page: **🏁 End Session**. This is the *safe* way to close MomScanner at end of day. It:

1. Forces a final OHLC export to Downloads
2. Forces a final transitions export
3. Forces a final active candidates export
4. Clears the localStorage backup (so next session starts clean)
5. Disables Layer 1 so the browser lets you close the tab without dialog

Click this at 4:00 PM EDT instead of X-ing out the tab.

### Visual status indicator

The verification banner gets a new pill: **🛡️ PROTECTED 5/5**. Hover for details on which layers are armed. The count reflects how many of the five layers are currently active (you can toggle individual layers off in Settings if any interfere with your workflow).

### Restore prompt on reload

If MomScanner detects a same-day OHLC backup in localStorage on page load, you'll see a modal:

> 🛡️ **OHLC Backup Found**
> Found 12,847 OHLC bars + 247 transitions from earlier today (last saved 18s ago). Restore?
> [Discard] [Restore]

Click **Restore** to bring back your session data and continue logging. Click **Discard** to start fresh.

Backups from previous days are auto-cleared on page load (no stale restore prompts).

---

## What carried over unchanged from v8.03

Every feature, every algorithm, every threshold from v8.03 is preserved exactly:

- Two-tier promotion (Early / Confirmed)
- All scoring layers (Trend / Breakout / Pressure)
- Velocity gate
- Velocity-gated Pre-Promotion Watch
- High-Conviction Pattern (still in observation phase for v8.04)
- Improved regime detector with `stock-specific` state
- Per-minute OHLC logger
- Hourly auto-export
- ThinkorSwim deep-links
- All settings, all alarms, all CSV exports

**No promotion logic changed. No score thresholds changed.** v8.03.1 is purely additive — it adds protection without touching anything else.

---

## Deployment ritual (do this carefully)

### Step 1: Download

Click the `index.html` link in this Claude chat to download the file to your computer. The file should be approximately **207 KB**.

### Step 2: Verify on disk before uploading

Open the downloaded file in Notepad and check that:
- Line 6 reads `<title>MomScanner v8.03.1</title>`
- File size is ~207 KB

If either fails, re-download.

### Step 3: Preserve v8.03 as fallback

Go to https://github.com/vaultlinkcrypto/MomScanner. **Before replacing index.html**, rename the current one to `index_V8.03_backup.html` so you can roll back if anything goes wrong.

### Step 4: Upload v8.03.1

Click `index.html` → pencil icon → Ctrl+A → Delete → paste the new code → Commit changes.

### Step 5: Wait and refresh

Wait 30-60 seconds for GitHub Pages to propagate. Then hard-refresh the live page with **Ctrl+Shift+R**.

### Step 6: The verification ritual

Check all four items:

| Check | Should see |
|---|---|
| Header text | `MOMENTUM TERMINAL v8.03.1` |
| Verification banner | `v8.03.1 LOADED ✓` |
| Protection pill | `🛡️ PROTECTED 5/5` (green) |
| Settings panel | New `🛡️ Session Protection (v8.03.1)` section |

If all four pass, you're protected. Test by pressing F5 — you should see the red blocked banner slide down from the top.

### Step 7: Unlock audio

Settings → Audio Alarms → click ▶ Test once.

---

## How to test protection works (do this once, then forget about it)

After deploying v8.03.1 and hard-refreshing:

1. **Press F5.** Red banner should slide down saying "F5 (refresh) blocked".
2. **Press Ctrl+R.** Same banner appears.
3. **Right-click anywhere outside a text field.** Banner appears.
4. **Click the browser back arrow.** Banner appears, you stay on MomScanner.
5. **If you have a mouse with thumb buttons** (buttons 4 and 5), press them. They should be blocked.
6. **Try to close the tab with X.** Chrome will ask "Leave site? Changes you made may not be saved." — that's Layer 1 working.

After confirming all six, you can trust the protection. **Don't disable any layers** unless you have a specific reason — every layer protects a different attack vector.

---

## How to end your session at 4:00 PM

The CORRECT way to close MomScanner at end of day:

1. Click **🏁 End Session** in the verification banner.
2. Confirm the dialog. This automatically:
   - Exports OHLC log to Downloads
   - Exports transitions log to Downloads
   - Exports active candidates to Downloads
   - Clears the backup
   - Disables protection
3. After the toast says "Session ended safely", close the tab.

The INCORRECT way: clicking X without using End Session. You'll get the Layer 1 dialog asking to confirm. Even if you confirm, you may lose any data accumulated since the last hourly auto-export (worst case: 60 minutes).

---

## Daily routine for v8.03.1

### Pre-market (9:25 AM EDT)

1. Open MomScanner in Chrome (Tab 1).
2. Open ThinkorSwim in another tab.
3. **Verify the protection pill reads 🛡️ PROTECTED 5/5.** If it doesn't, check Settings → Session Protection and re-enable any disabled layers.
4. Run the verification ritual (header, banner, OHLC counter).
5. Settings → Audio Alarms → ▶ Test.
6. Add tickers including SPY.

### During the session

You can now:
- Touch your mouse without fear
- Press keyboard shortcuts without fear
- Click the browser back button (it'll be blocked)
- Use the thumb buttons on your mouse (blocked)
- Leave MomScanner unattended for hours

You should NOT:
- Manually close the tab without using 🏁 End Session
- Disable protection layers mid-session unless you have a specific need

### End of session (4:00 PM)

Click **🏁 End Session**. Confirm. Wait for "Session ended safely" toast. Close tab.

---

## Settings reference (Session Protection)

Located at Settings → 🛡️ Session Protection (v8.03.1).

| Toggle | Default | What it controls |
|---|---|---|
| Before-Unload Confirmation | ON | Dialog when closing tab or navigating away |
| Back/Forward Block | ON | Browser back/forward buttons and equivalents |
| Keyboard Shortcut Block | ON | F5, Ctrl+R, Ctrl+Shift+R, Ctrl+W |
| Right-Click Block | ON | Context menu (still works inside text fields) |
| Mouse Buttons 4/5 Block | ON | Thumb buttons on gaming/modern mice |

The localStorage backup is always on and is not toggleable. It runs every 30 seconds regardless of other settings.

---

## Troubleshooting

**Protection pill says "🛡️ PROTECTED 0/5":** All layers are disabled. Re-enable in Settings → Session Protection → toggle each layer → Save.

**Restore prompt appears on a fresh new-day session:** Click "Discard". The backup from yesterday should have auto-cleared but didn't for some reason. Subsequent loads should be clean.

**Restore prompt restored fewer bars than expected:** The localStorage backup keeps the last 80,000 rows max. If your session generated more than 80K rows before the reload, only the most recent 80K were preserved. (For reference: 80K rows = ~7 hours of 200 tickers logged at 1/min, so this is rarely hit.)

**F5 blocking is annoying when I want to refresh:** Use 🏁 End Session first. That's the safe path. If you genuinely need to force-reload mid-session for debugging, disable Layer 3 temporarily in Settings.

**Right-click blocking prevents copy/paste:** Right-click is NOT blocked inside `<input>` and `<textarea>` fields, so Settings still works normally. If you need right-click on the main table (rare), disable Layer 4.

**The protection pill is yellow instead of green:** This indicates fewer than 5 layers armed. Hover for which layers are off.

**Browser shows generic "Leave site?" instead of MomScanner's custom message:** This is expected. Chrome since 2018 only shows its own dialog text. The custom message is set in code but Chrome ignores it. The dialog itself is what saves your session.

**Ctrl+W still closed my tab without the dialog:** Ctrl+W is intercepted by the OS before reaching the page in some Chrome versions. Layer 1 (before-unload) is the actual backstop for this case. If you saw the dialog and dismissed it accidentally, that's how the tab closed — not a protection failure.

---

## Data safety

The localStorage backup increases storage usage by approximately 2-5 MB during an active session. Chrome's localStorage budget for a single origin is 5-10 MB per browser. **At peak buffer size, MomScanner uses about 50% of available localStorage.** If you have other large data in localStorage (custom audio files, very large transition logs), it could hit the limit. v8.03.1 handles this gracefully — if backup save fails, it logs a console warning and tries again next cycle without crashing.

To free space: Settings → Behavior → "Clear All Data" if needed. Don't do this mid-session.

---

## What's NOT in v8.03.1

For clarity:
- ❌ No Velocity Spike Alert (coming in v8.04)
- ❌ No Hot Streak Detector (coming in v8.04)
- ❌ No Big Mover Filter Panel (coming in v8.04)
- ❌ No High-Conviction Badge (coming in v8.04 after more data)
- ❌ No promotion logic changes
- ❌ No scoring changes

v8.03.1 is a focused safety patch. Everything else stays as v8.03.

---

## Roadmap

After v8.03.1 deploys safely and one or two sessions confirm protection works:

- **Continue collecting OHLC logs** with v8.03.1 — same data quality as v8.03, but now session-loss-proof
- **Validate the High-Conviction Pattern** across more regime types (currently 4 sessions, target 7-8)
- **Build v8.04** with Velocity Spike, Hot Streak, Big Mover, and High-Conviction features

The v8.04 spec is locked. Once enough data accumulates for confident threshold-setting, v8.04 will be the next release.
