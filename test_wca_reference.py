#!/usr/bin/env python3
"""
Test to verify WCA standard cube moves using a reference.
"""


def test_wca_r_move():
    """
    Test R move according to WCA standards.

    For WCA standard R move (viewing from the right face):
    - Right face rotates 90° clockwise
    - Adjacent faces cycle: U right → B left (reversed) → D right → F right → U right

    In a solved cube with standard colors:
    U=White, D=Yellow, F=Green, B=Blue, L=Orange, R=Red

    After R move:
    - U right column should have Green (from F)
    - F right column should have Yellow (from D)
    - D right column should have Blue (from B, reversed)
    - B left column should have White (from U, reversed)
    """

    print("WCA R move specification:")
    print("Standard orientation: White top, Green front")
    print("R move cycles: U right → B left (rev) → D right → F right → U right")
    print()

    # Let's verify this matches online cube simulators or references


if __name__ == "__main__":
    test_wca_r_move()
