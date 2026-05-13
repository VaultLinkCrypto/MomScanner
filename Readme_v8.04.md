# MomScanner v8.04 Spec — Bug Fix Release + RVol Sliders
**Created:** 2026-05-13
**Status:** SHIPPED
**Base:** v8.03.1

---

## What shipped in v8.04

### Bug Fix 1 — Velocity gate disabled for Trend layer (CRITICAL)
**Root cause:** v8.03 added a velocity gate (`velOK`) to `rawQualifyLayer()` that checked instantaneous price velocity every 5-second poll cycle. For the Trend layer, this required positive velocity above a threshold continuously — any momentary dip (velocity ≈ 0 or negative for one cycle) returned `watch`, resetting the streak counter. Since DRIFT moves have low, steady velocity by definition, the streak could never reach the 120-second minimum for confirmed Trend candidacy.

**Evidence:** NFLX on 5/12 had Trend score 80-83 for 62 continuous minutes but flickered through 44 candidacy sessions averaging 0.9 minutes each. Session-wide avg candidacy dropped from 77.7m (v7.2, 5/1) to 1.0m (v8.03, 5/12).

**Fix:** Line 3109 — `layerMult` set to 0 for Trend layer, making `required = 0`, effectively disabling the velocity gate for Trend only. Velocity gate remains active for Breakout (1.0x) and Pressure (0.5x).

### Bug Fix 2 — RVol floor lowered for Trend layer + per-layer sliders (CRITICAL)
**Root cause:** `rawQualifyLayer()` required RVol ≥ 1.5x (confirmed) or ≥ 1.2x (early) for all non-Pressure layers. FCEL on 5/13 moved +16.56% with Trend score 84 for 72 consecutive minutes, Spread 3.51%, OI 1,934 — but RVol was 0.60 all day. The RVol gate silently blocked it despite every other condition being met. This bug existed since v7.2 but was masked by the velocity-gate problem making it invisible.

**Evidence:** 12/15 top movers on 5/13 were completely undetected. FCEL (+16.56%), WOLF (+16.53%), ON (+11.15%), BABA (+8.19%) — 20% detection rate.

**Fix:** 
- Default RVol floors: Trend 0.3x/0.2x, Breakout 1.0x/0.8x, Pressure 0.8x/0.5x (confirmed/early)
- Per-layer RVol floor sliders added to Settings → Layer Thresholds panel
- Sliders range 0.0x to 3.0x in 0.1x increments
- `rawQualifyLayer()` reads `th.rvolFloor` / `th.rvolFloorEarly` from settings instead of hardcoded values

### Bug 3 — Pressure score flatline (DOCUMENTED, NOT FIXED)
**Issue:** 54.7% of afternoon OHLC bars have PressureScore = exactly 50.00 because OFI proxy inputs go stale during low-vol midday hours.

**Status:** Deferred to v8.05. This is a data-quality limitation of L1 polling, not a code bug. Potential fixes require either faster polling (API quota cost) or alternative proxy signals.

---

## v8.04 feature backlog (deferred to v8.05+)

| # | Feature | Priority | Status |
|---|---|---|---|
| 0 | Session Protection Suite 🛡️ | CRITICAL | ✅ Shipped v8.03.1 |
| 1 | Velocity Spike Alert ⚡ | HIGHEST | Deferred — need threshold validation with v8.04 data |
| 2 | Hot Streak Detector 🔥 | HIGHEST | Deferred |
| 3 | Big Mover Filter Panel | High | Deferred |
| 4 | High-Conviction Badge ⭐ | High | Deferred |
| 5-14 | Various polish features | Low-Medium | Deferred |

**Rationale for deferral:** The bug fixes in v8.04 fundamentally change candidacy behavior. Previous session data (5/12, 5/13) was collected under the broken velocity gate and high RVol floor. Those sessions' velocity distributions and promotion patterns are not valid baselines for tuning new features. Need 3-5 clean sessions on v8.04 before locking Velocity Spike thresholds or Hot Streak windows.

---

## Deployment steps

1. Go to `https://github.com/vaultlinkcrypto/MomScanner`
2. Click `index.html` → pencil icon
3. Ctrl+A → delete → paste new v8.04 code
4. Commit changes
5. Wait 30-60 seconds, hard refresh: Ctrl+Shift+R
6. All localStorage settings carry over. **New RVol sliders will appear with defaults (Trend 0.3x, Breakout 1.0x, Pressure 0.8x)**
7. Open Settings → Audio Alarms → click ▶ Test to re-unlock audio
8. Open Settings → Layer Thresholds → verify new RVol Floor sliders are visible

## Verification checklist for 5/14 session

- [ ] Header shows "MOMENTUM TERMINAL v8.04"
- [ ] Verification banner shows "v8.04 LOADED ✓"
- [ ] Settings → Layer Thresholds shows RVol Floor sliders for all 3 layers (6 total: confirmed + early)
- [ ] Trend RVol defaults to 0.3x confirmed, 0.2x early
- [ ] Breakout RVol defaults to 1.0x confirmed, 0.8x early
- [ ] Pressure RVol defaults to 0.8x confirmed, 0.5x early
- [ ] Velocity Gates section now says "breakout + pressure only · v8.04: disabled for trend"
- [ ] Candidacy durations are substantially longer than 5/12-5/13 (target: avg > 5 min, not 1 min)
- [ ] Low-RVol tickers with high Trend scores (FCEL-type) now promote
- [ ] OHLC logger continues working normally
- [ ] Session Protection Suite still active
- [ ] Audio alarms still fire on promotions
