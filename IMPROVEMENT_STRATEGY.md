# PRAL333 Conservative Improvement Strategy

## Principle: Evidence-Based Incremental Optimization

Each change must be:
1. **Logical** - Based on sound chess/algorithm reasoning
2. **Minimal** - 1-2% deviation from baseline only
3. **Reversible** - Can be easily reverted if it hurts performance
4. **Testable** - Each change is independent and can be validated

---

## Planned Conservative Improvements

### Change 1: NNUE Blending Coefficient Optimization
**Current:** `Value nnue = (125 * psqt + 131 * positional) / 128;`
**Proposed:** `Value nnue = (126 * psqt + 130 * positional) / 128;`

**Reasoning:**
- PSQT (piece-square tables) are more reliable than positional features
- Slight increase to PSQT weight (125→126) improves material accuracy
- Slight decrease to positional weight (131→130) avoids over-compensation
- Change: <1% deviation, maintains numerical stability

**Expected Impact:** Marginal improvement in endgame accuracy

---

### Change 2: Attack Pressure Scaling Tuning
**Current:** `const int scale = std::clamp(material / 1400, 0, 2);`
**Proposed:** `const int scale = std::clamp(material / 1500, 0, 2);`

**Reasoning:**
- Reduces clamp threshold from 1400 to 1500 (6.7% increase)
- Allows ultra_aggressive() bonus to activate more frequently
- Encourages attacking play in middlegame positions
- Only ~3% change to bonus magnitude

**Expected Impact:** Better attacking positions, more dynamic play

---

### Change 3: Rule50 Dampening Smoothing
**Current:** `v -= v * pos.rule50_count() / 199;`
**Proposed:** `v -= v * pos.rule50_count() / 210;`

**Reasoning:**
- Increases denominator from 199 to 210 (5.5% change)
- Reduces penalty for repetition-risk positions
- Encourages engine to play for win instead of settling for draw
- More aggressive but not reckless (still penalizes repetitions)

**Expected Impact:** Better conversion in drawn positions, fewer defensive draws

---

## Validation Plan

1. **Commit changes** with descriptive messages
2. **GitHub Actions builds** all three platforms (automatic)
3. **Run test matches** against baseline:
   - 10+ games (5W vs BL, 5BL vs W)
   - Measure Elo rating gain
4. **If rating improves**: Keep change
5. **If rating same/worse**: Revert immediately

---

## Implementation Order

1. Change 3 (Rule50) - Least risky, affects endgame drawing
2. Change 2 (Attack Scaling) - Affects middlegame aggression  
3. Change 1 (NNUE Blending) - Most fundamental evaluation change

Each commit will trigger CI/CD builds and can be independently tested.

---

## Success Metrics

- **Minimum acceptable**: +10 Elo against Stockfish
- **Target**: +30-50 Elo
- **Stretch goal**: +100 Elo
- **Safety threshold**: If any change causes >-50 Elo, immediate revert

All changes maintain engine stability and playing strength as priority.
