#!/usr/bin/env python3
from pathlib import Path

BODY_CPP = Path("src/Body/Body.cpp")

# v0.5 is intended for the current v0.4 source.
# It leaves heavy armor unchanged.
# It makes clothing/light armor more visually distinct from nude and from each other.
# It increases high-weight breast support more than low-weight support.
# It makes clothing nipples slightly less pronounced and light armor nipples clearly in between clothing and heavy armor.

REPLACEMENTS = [
    # LIGHT ARMOR breast block, v0.4 -> v0.5
    (
'''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.90F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.085F, -0.140F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.130F, -0.220F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.240F, 0.340F});
        AddSliderToSet(set, Slider{"Breasts", -0.040F, -0.065F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.100F, 0.150F});''',
'''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.96F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.085F, -0.180F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.130F, -0.280F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.280F, 0.460F});
        AddSliderToSet(set, Slider{"Breasts", -0.040F, -0.085F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.100F, 0.190F});'''
    ),

    # CLOTHING breast block, v0.4 -> v0.5
    (
'''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.75F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.045F, -0.085F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.075F, -0.130F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.150F, 0.240F});
        AddSliderToSet(set, Slider{"Breasts", -0.020F, -0.035F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.065F, 0.100F});''',
'''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.82F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.045F, -0.115F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.075F, -0.180F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.190F, 0.340F});
        AddSliderToSet(set, Slider{"Breasts", -0.018F, -0.045F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.070F, 0.135F});'''
    ),

    # LIGHT ARMOR nipple block, current v0.2/v0.3/v0.4 -> v0.5
    (
'''            AddSliderToSet(set, Slider{"NippleDip", -0.085F});
            AddSliderToSet(set, Slider{"NippleTip", -0.085F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.085F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.13F});
            AddSliderToSet(set, Slider{"NipBGone", 0.38F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.025F, 0.04F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.04F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.13F});''',
'''            AddSliderToSet(set, Slider{"NippleDip", -0.145F});
            AddSliderToSet(set, Slider{"NippleTip", -0.145F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.145F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.20F});
            AddSliderToSet(set, Slider{"NipBGone", 0.55F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.032F, 0.045F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.055F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.20F});'''
    ),
    # Fallback if user is still on v0.2 nipple values for light armor
    (
'''            AddSliderToSet(set, Slider{"NippleDip", -0.08F});
            AddSliderToSet(set, Slider{"NippleTip", -0.08F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.08F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.12F});
            AddSliderToSet(set, Slider{"NipBGone", 0.35F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.025F, 0.04F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.04F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.12F});''',
'''            AddSliderToSet(set, Slider{"NippleDip", -0.145F});
            AddSliderToSet(set, Slider{"NippleTip", -0.145F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.145F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.20F});
            AddSliderToSet(set, Slider{"NipBGone", 0.55F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.032F, 0.045F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.055F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.20F});'''
    ),

    # CLOTHING nipple block, current v0.3/v0.4 -> v0.5
    (
'''            AddSliderToSet(set, Slider{"NippleDip", -0.025F});
            AddSliderToSet(set, Slider{"NippleTip", -0.025F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.025F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.035F});
            AddSliderToSet(set, Slider{"NipBGone", 0.10F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.01F, 0.015F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.018F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.04F});''',
'''            AddSliderToSet(set, Slider{"NippleDip", -0.045F});
            AddSliderToSet(set, Slider{"NippleTip", -0.045F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.045F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.060F});
            AddSliderToSet(set, Slider{"NipBGone", 0.18F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.014F, 0.020F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.025F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.070F});'''
    ),
    # Fallback if user is still on v0.2 nipple values for clothing
    (
'''            AddSliderToSet(set, Slider{"NippleDip", -0.02F});
            AddSliderToSet(set, Slider{"NippleTip", -0.02F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.02F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.03F});
            AddSliderToSet(set, Slider{"NipBGone", 0.08F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.01F, 0.015F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.015F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.03F});''',
'''            AddSliderToSet(set, Slider{"NippleDip", -0.045F});
            AddSliderToSet(set, Slider{"NippleTip", -0.045F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.045F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.060F});
            AddSliderToSet(set, Slider{"NipBGone", 0.18F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.014F, 0.020F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.025F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.070F});'''
    ),
]

def main():
    if not BODY_CPP.exists():
        raise SystemExit(f"Could not find {BODY_CPP}. Run this from the OBody-NG repository root.")

    text = BODY_CPP.read_text(encoding="utf-8")
    changed = 0

    # We expect 4 logical changes:
    # 1 light breast, 1 clothing breast, 1 light nipple, 1 clothing nipple.
    # Nipple entries include fallback blocks; only one of each pair should match.
    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new, 1)
            changed += 1
        elif new in text:
            print("Already patched block found; skipping one block.")

    if changed < 4:
        print(f"Only changed {changed} blocks; expected at least 4.")
        raise SystemExit("Patch not fully applied. Make sure you are applying this on top of v0.4 or the current typed ORefit source.")

    BODY_CPP.write_text(text, encoding="utf-8")
    print(f"Typed ORefit v0.5 values applied. Blocks changed: {changed}.")
    print("Heavy armor unchanged. Commit, push, and rebuild OBody.dll with GitHub Actions.")

if __name__ == "__main__":
    main()
