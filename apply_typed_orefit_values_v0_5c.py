#!/usr/bin/env python3
from pathlib import Path

BODY_CPP = Path("src/Body/Body.cpp")

# v0.5c: robust patcher.
# Supports clothing/light breast blocks from v0.2, v0.3, or v0.4.
# Supports clothing/light nipple blocks from v0.2, v0.3/v0.4, or already v0.5.
# Treats already-patched blocks as success.
# Heavy armor is untouched.

LIGHT_BREAST_OLD = [
'''        AddSliderToSet(set, Slider{"BreastSideShape", -0.04F});
        AddSliderToSet(set, Slider{"BreastUnderDepth", -0.04F});
        AddSliderToSet(set, Slider{"BreastCleavage", 0.12F});
        AddSliderToSet(set, Slider{"BreastGravity2", -0.06F, -0.04F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.10F, -0.15F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.16F, 0.20F});
        AddSliderToSet(set, Slider{"Breasts", -0.035F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.08F});''',
'''        AddSliderToSet(set, Slider{"BreastSideShape", -0.04F, -0.055F});
        AddSliderToSet(set, Slider{"BreastUnderDepth", -0.04F, -0.055F});
        AddSliderToSet(set, Slider{"BreastCleavage", 0.13F, 0.18F});
        AddSliderToSet(set, Slider{"BreastGravity2", -0.065F, -0.095F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.11F, -0.17F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.18F, 0.25F});
        AddSliderToSet(set, Slider{"Breasts", -0.03F, -0.05F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.08F, 0.11F});''',
'''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.90F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.085F, -0.140F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.130F, -0.220F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.240F, 0.340F});
        AddSliderToSet(set, Slider{"Breasts", -0.040F, -0.065F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.100F, 0.150F});'''
]

LIGHT_BREAST_NEW = '''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.96F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.085F, -0.180F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.130F, -0.280F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.280F, 0.460F});
        AddSliderToSet(set, Slider{"Breasts", -0.040F, -0.085F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.100F, 0.190F});'''

CLOTHING_BREAST_OLD = [
'''        AddSliderToSet(set, Slider{"BreastSideShape", -0.015F});
        AddSliderToSet(set, Slider{"BreastUnderDepth", -0.015F});
        AddSliderToSet(set, Slider{"BreastCleavage", 0.04F});
        AddSliderToSet(set, Slider{"BreastGravity2", -0.03F, -0.02F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.05F, -0.08F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.08F, 0.10F});
        AddSliderToSet(set, Slider{"Breasts", -0.015F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.04F});''',
'''        AddSliderToSet(set, Slider{"BreastSideShape", -0.015F, -0.02F});
        AddSliderToSet(set, Slider{"BreastUnderDepth", -0.015F, -0.02F});
        AddSliderToSet(set, Slider{"BreastCleavage", 0.05F, 0.08F});
        AddSliderToSet(set, Slider{"BreastGravity2", -0.035F, -0.055F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.055F, -0.09F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.10F, 0.14F});
        AddSliderToSet(set, Slider{"Breasts", -0.012F, -0.02F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.04F, 0.06F});''',
'''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.75F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.045F, -0.085F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.075F, -0.130F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.150F, 0.240F});
        AddSliderToSet(set, Slider{"Breasts", -0.020F, -0.035F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.065F, 0.100F});'''
]

CLOTHING_BREAST_NEW = '''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.82F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.045F, -0.115F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.075F, -0.180F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.190F, 0.340F});
        AddSliderToSet(set, Slider{"Breasts", -0.018F, -0.045F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.070F, 0.135F});'''

LIGHT_NIPPLE_OLD = [
'''            AddSliderToSet(set, Slider{"NippleDip", -0.08F});
            AddSliderToSet(set, Slider{"NippleTip", -0.08F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.08F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.12F});
            AddSliderToSet(set, Slider{"NipBGone", 0.35F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.025F, 0.04F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.04F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.12F});''',
'''            AddSliderToSet(set, Slider{"NippleDip", -0.085F});
            AddSliderToSet(set, Slider{"NippleTip", -0.085F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.085F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.13F});
            AddSliderToSet(set, Slider{"NipBGone", 0.38F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.025F, 0.04F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.04F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.13F});'''
]

LIGHT_NIPPLE_NEW = '''            AddSliderToSet(set, Slider{"NippleDip", -0.145F});
            AddSliderToSet(set, Slider{"NippleTip", -0.145F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.145F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.20F});
            AddSliderToSet(set, Slider{"NipBGone", 0.55F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.032F, 0.045F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.055F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.20F});'''

CLOTHING_NIPPLE_OLD = [
'''            AddSliderToSet(set, Slider{"NippleDip", -0.02F});
            AddSliderToSet(set, Slider{"NippleTip", -0.02F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.02F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.03F});
            AddSliderToSet(set, Slider{"NipBGone", 0.08F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.01F, 0.015F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.015F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.03F});''',
'''            AddSliderToSet(set, Slider{"NippleDip", -0.025F});
            AddSliderToSet(set, Slider{"NippleTip", -0.025F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.025F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.035F});
            AddSliderToSet(set, Slider{"NipBGone", 0.10F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.01F, 0.015F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.018F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.04F});'''
]

CLOTHING_NIPPLE_NEW = '''            AddSliderToSet(set, Slider{"NippleDip", -0.045F});
            AddSliderToSet(set, Slider{"NippleTip", -0.045F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.045F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.060F});
            AddSliderToSet(set, Slider{"NipBGone", 0.18F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.014F, 0.020F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.025F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.070F});'''

GROUPS = [
    ("light armor breast", LIGHT_BREAST_OLD, LIGHT_BREAST_NEW),
    ("clothing breast", CLOTHING_BREAST_OLD, CLOTHING_BREAST_NEW),
    ("light armor nipples", LIGHT_NIPPLE_OLD, LIGHT_NIPPLE_NEW),
    ("clothing nipples", CLOTHING_NIPPLE_OLD, CLOTHING_NIPPLE_NEW),
]

def patch_group(text, label, old_list, new):
    if new in text:
        print(f"{label}: already patched")
        return text, "already"
    for old in old_list:
        if old in text:
            print(f"{label}: patched")
            return text.replace(old, new, 1), "patched"
    print(f"{label}: missing")
    return text, "missing"

def main():
    if not BODY_CPP.exists():
        raise SystemExit(f"Could not find {BODY_CPP}. Run this from the OBody-NG repository root.")

    text = BODY_CPP.read_text(encoding="utf-8")
    status = {}

    for label, old_list, new in GROUPS:
        text, result = patch_group(text, label, old_list, new)
        status[label] = result

    missing = [k for k, v in status.items() if v == "missing"]
    if missing:
        print("\nMissing blocks:")
        for label in missing:
            print(" -", label)
        raise SystemExit("Patch not fully applied. Send lines around GenerateClotheSliders from Body.cpp.")

    BODY_CPP.write_text(text, encoding="utf-8")
    print("\nTyped ORefit v0.5c patch complete.")
    print("Status:", status)
    print("Commit, push, and rebuild OBody.dll with GitHub Actions.")

if __name__ == "__main__":
    main()
