# v36 final fixes (2026-11-08)

CONFIRMED — external lift detour now includes one extra80-VBlank dwell at its extreme floor. CALL_PAUSE FFFF0860 is set only for a wrong-direction call, consumed on the step after reaching the waypoint. All392 routes include duplicated waypoint; ordinary/same-floor trips unchanged. test_lift03.py PASS.

CONFIRMED — elevator palette18222 entriesA/B use red0200/0500; bank pointer8CB8 selects the existing shaded keypad bank. Native renderer comparison test05/current changes exactly20pixels, rectangle37..42,4..7. render_indicator06.py PASS. Allowed green lens unchanged.

CONFIRMED — inventory bit6 is damage. Native drop6CFC clears it; map persistence4AA6 also clears it. Pickups use map codes25..3F; bit6 is unused by initial pickup cells in both campaigns. items06.py retains bit6 in drop store6D2C, nearby scanner9EA8, item-to-map9F1E and persistent floor record4AB0. Native pickup RNG6B36 is bypassed only for already-broken items; intact items retain the native chance on pickup (not a new throw-time RNG). Nearby eligibility6F5C masks bit6. World renderer ignores the bit:26 sprite comparisons PASS.52 complete native drops and52 pickups PASS; both campaign floor persistence PASS.

Rejected approaches:9FEE is an icon lookup, not world-to-item conversion. Do not hook it.9EDC+6 overlaps a shared RTS at9EE0; wrap scanner entry9EA8 instead.

OPEN — user reports cursor jumping to top in Kega Fusion with test05.gs0, stationary clicks on Scanman brightness-up.80 real mouse-down/up sequences through BlastEm polling and60 injected stationary events did not reproduce. Cursor Y stayed43. Hardware polling and consume path were inspected; no confirmed cause. No speculative delta filtering was added, and this issue is NOT marked fixed. Reproduction in Kega/version/OS remains necessary. Probe scripts are source-only; the savestate and logs with raw emulator dumps remain private.
