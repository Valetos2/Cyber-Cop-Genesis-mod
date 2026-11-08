# test04: подтверждения и границы

CONFIRMED2026-11-08. Полный пользовательский отчёт: ../../v36/REPORT_TEST04_RU.md (из корня репозитория v36/REPORT_TEST04_RU.md).

- Scan reset8836 ->view217C=4,brightness2180=8,palette88E6. Native entry873C..8760 already resets all fields. test_fixes04.
- Lamp radiusD050 replaced: abs(worldY-cameraY)*256*radius/(depth*(depth-radius)), minimum1. Avoid difference of rounded screen centres and native OR1. Table endpoint y/(h+0.5) avoids singleton tips. gs0 old1→3→1 reproduced; formula monotonic sweepPASS.
- Lift external penalty320 and same-floor80VBlank. All392casesPASS. Accepted button8E9E records currentmap using4A80, temporarily encodes targetfloor from8E58, then save21+32 without committing current map into target's slot. Lab026C and deniedB2 bypass. BothcampaignroundtripPASS.
- Memorial textE58E/E68E exactlytest02. Sprite opaque crop origin196,62 versus216,72test03. Black target/current palette282C..292B plus immediateCRAMzero; VScrollA0 and HScrollD800 cleared. First/repeatBlastEm screensmatch. Initial diagnosis onlyVScroll was insufficient; HScrollclear also necessary.
- sleep17_begin chains release_ui and native71E2 before existing sound hook: repair214Czero, action7192 removed.
- EquipmentFD84 singleton IDs12..18,20; nativebomb/armour paths retained. Name attributeFF at104A6/104B2/10506 blocks masks/FirstAid for droids. Nativegas31F4 skips droids, FirstAid754C skips droids. Electronics staysuniversal. Character gateFCE2 testedall6.
- AutoaimEC62 stablegroups threat3,camera2,other1,lamp0. Threat IDs8004,8006,801C,8119,811A,811B,801D. Wallbuffer40CE stores depth/64; test centreX and allows atmost4depthunits behind onlymoving threats; crab811B excludedbehindwall. Freecursor bypassesnativeAC1E. NativeD7/A6 contract restored. gs1 oldactor8depth2137 removed.
- Native7D76 and AmigaMissionA440 use floor-indexed visitflags(Genesis2718/Amiga8348) and maxE0access. L1/L2secondterminal cannotawardtwice.
- Mission5F32,27 retainscell82 and initialactor8006 concurrently. CPUverified.
- gs3 nativebarrelB89C and newbarrel constructors share centre84,height42,collision64/84; substitutionrender showsidenticalbase. No new-onlyoffsetfix.
- gs2 player5110,7835/camera5110,7855 insidewallcell19,30; fullrotationrender reproducesclipping. OPEN rootentrycause/safegeometryfix.
- Dropembryo nativeindex25 stride17/height16; all16paddingbyteszero. No transferredspritepaddingbug established.

OPEN: originalAmiga embryo colour exactrender; fullST/DOSintrocreditspaths. Do not claimabsencefromkeywordsearch.
