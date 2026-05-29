#!/usr/bin/env python3
from pathlib import Path

BODY_CPP = Path("src/Body/Body.cpp")

# Relaxed/fixed v0.5 patcher.
# It treats "already patched" blocks as success and still writes any remaining changes.

GROUPS = [
    {
        "label": "light armor breast",
        "old": [
'''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.90F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.085F, -0.140F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.130F, -0.220F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.240F, 0.340F});
        AddSliderToSet(set, Slider{"Breasts", -0.040F, -0.065F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.100F, 0.150F});'''
        ],
        "new": '''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.96F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.085F, -0.180F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.130F, -0.280F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.280F, 0.460F});
        AddSliderToSet(set, Slider{"Breasts", -0.040F, -0.085F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.100F, 0.190F});'''
    },
    {
        "label": "clothing breast",
        "old": [
'''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.75F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.045F, -0.085F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.075F, -0.130F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.150F, 0.240F});
        AddSliderToSet(set, Slider{"Breasts", -0.020F, -0.035F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.065F, 0.100F});'''
        ],
        "new": '''        AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.82F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.045F, -0.115F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.075F, -0.180F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.190F, 0.340F});
        AddSliderToSet(set, Slider{"Breasts", -0.018F, -0.045F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.070F, 0.135F});'''
    },
    {
        "label": "light armor nipples",
        "old": [
'''            AddSliderToSet(set, Slider{"NippleDip", -0.085F});
            AddSliderToSet(set, Slider{"NippleTip", -0.085F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.085F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.13F});
            AddSliderToSet(set, Slider{"NipBGone", 0.38F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.025F, 0.04F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.04F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.13F});''',
'''            AddSliderToSet(set, Slider{"NippleDip", -0.08F});
            AddSliderToSet(set, Slider{"NippleTip", -0.08F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.08F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.12F});
            AddSliderToSet(set, Slider{"NipBGone", 0.35F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.025F, 0.04F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.04F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.12F});'''
        ],
        "new": '''            AddSliderToSet(set, Slider{"NippleDip", -0.145F});
            AddSliderToSet(set, Slider{"NippleTip", -0.145F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.145F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.20F});
            AddSliderToSet(set, Slider{"NipBGone", 0.55F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.032F, 0.045F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.055F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.20F});'''
    },
    {
        "label": "clothing nipples",
        "old": [
'''            AddSliderToSet(set, Slider{"NippleDip", -0.025F});
            AddSliderToSet(set, Slider{"NippleTip", -0.025F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.025F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.035F});
            AddSliderToSet(set, Slider{"NipBGone", 0.10F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.01F, 0.015F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.018F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.04F});''',
'''            AddSliderToSet(set, Slider{"NippleDip", -0.02F});
            AddSliderToSet(set, Slider{"NippleTip", -0.02F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.02F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.03F});
            AddSliderToSet(set, Slider{"NipBGone", 0.08F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.01F, 0.015F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.015F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.03F});'''
        ],
        "new": '''            AddSliderToSet(set, Slider{"NippleDip", -0.045F});
            AddSliderToSet(set, Slider{"NippleTip", -0.045F});
            AddSliderToSet(set, Slider{"NipplePuffy_v2", -0.045F});
            AddSliderToSet(set, Slider{"AreolaSize", -0.060F});
            AddSliderToSet(set, Slider{"NipBGone", 0.18F});
            AddSliderToSet(set, Slider{"NippleDistance", 0.014F, 0.020F});
            AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.025F});
            AddSliderToSet(set, Slider{"NipplePerkManga", -0.070F});'''
    },
]

def main():
    if not BODY_CPP.exists():
        raise SystemExit(f"Could not find {BODY_CPP}. Run this from the OBody-NG repository root.")

    text = BODY_CPP.read_text(encoding="utf-8")
    changed = 0
    already = 0
    missing = []

    for group in GROUPS:
        label = group["label"]
        new = group["new"]

        if new in text:
            print(f"{label}: already patched")
            already += 1
            continue

        replaced = False
        for old in group["old"]:
            if old in text:
                text = text.replace(old, new, 1)
                print(f"{label}: patched")
                changed += 1
                replaced = True
                break

        if not replaced:
            missing.append(label)

    if missing:
        print("Missing blocks:")
        for label in missing:
            print(" -", label)
        raise SystemExit("Patch not fully applied. Send the relevant Body.cpp section if this happens.")

    BODY_CPP.write_text(text, encoding="utf-8")
    print(f"Typed ORefit v0.5b patch complete. Changed: {changed}, already patched: {already}.")
    print("Commit, push, and rebuild OBody.dll with GitHub Actions.")

if __name__ == "__main__":
    main()
