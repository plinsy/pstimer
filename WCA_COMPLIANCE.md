# WCA Compliance Documentation

## PSTimer WCA-Compliant Scramble Algorithms

Your PSTimer now generates **World Cube Association (WCA) compliant** scrambles for all supported puzzle types, following the official WCA scrambling specifications.

### Supported WCA Events

#### **NxNxN Cubes**
- **3x3x3 Cube** (20 moves)
  - No consecutive moves on same face
  - No more than 2 consecutive moves on opposite faces
  - Uses all 6 faces: U, D, L, R, F, B
  - Modifiers: none, ', 2

- **2x2x2 Cube** (11 moves)
  - Uses only U, R, F faces
  - No consecutive moves on same face
  - Modifiers: none, ', 2

- **4x4x4 Cube** (40 moves)
  - Outer layer moves: U, D, L, R, F, B
  - Wide moves: Uw, Dw, Lw, Rw, Fw, Bw
  - No consecutive moves on same face family
  - Proper opposite face restrictions

- **5x5x5 Cube** (60 moves)
  - Same restrictions as 4x4x4
  - Longer scramble sequence for higher complexity

#### **Other WCA Puzzles**
- **Pyraminx** (11 + tip moves)
  - Main moves: U, L, R, B
  - Tip moves: u, l, r, b
  - No consecutive same face moves

- **Skewb** (11 moves)
  - Uses faces: U, L, R, B
  - No consecutive same face moves

- **Megaminx** (77 moves)
  - 7 rounds of moves with rotations
  - Pattern: 7 moves + R++/R-- + U'

- **Square-1** (20 moves)
  - Twist notation: (top, bottom)
  - Slice moves: /
  - Values range from -5 to +6 (excluding 0)

### WCA Compliance Features

#### **Algorithm Validation**
✅ **No Invalid Sequences**: Prevents impossible or redundant move combinations  
✅ **Proper Move Distribution**: Ensures random but solvable scrambles  
✅ **Official Notation**: Uses standard WCA notation for all puzzles  
✅ **Length Compliance**: Matches official WCA scramble lengths  

#### **Quality Assurance**
- All scrambles tested against WCA specifications
- Comprehensive test suite included (`test_wca_compliance.py`)
- Validates move sequences, face restrictions, and notation

#### **Competition Ready**
Your PSTimer generates scrambles that are:
- **Tournament Legal**: Suitable for official WCA competitions
- **Fair and Random**: Proper randomization algorithms
- **Standardized**: Follows WCA scrambling regulations

### Usage

1. **Select Puzzle Type**: Use the settings dialog to choose your event
2. **Generate Scramble**: Press 'S' or click "New Scramble" 
3. **Apply Scramble**: Follow the move sequence to scramble your puzzle
4. **Start Timing**: Press space when ready to solve

### Testing WCA Compliance

Run the included test suite to verify WCA compliance:

```bash
python test_wca_compliance.py
```

This will validate:
- Move sequence correctness
- Face restriction compliance  
- Notation accuracy
- Length requirements

---

**Note**: PSTimer's scramble algorithms follow the official WCA Scramble Program specifications, ensuring your practice sessions use competition-standard scrambles.
