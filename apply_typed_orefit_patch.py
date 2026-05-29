#!/usr/bin/env python3
"""
Typed ORefit patch for Aietos/OBody-NG.

Run this from the root of a checked-out OBody-NG source tree:
    python apply_typed_orefit_patch.py

What it does:
- Adds Body::RefitClass { Nude, Clothing, LightArmor, HeavyArmor }
- Adds OBody::GetRefitClass(actor)
- Changes GenerateClotheSliders(actor) to GenerateClotheSliders(actor, refitClass)
- Changes ApplyClothePreset() so ORefit fallback morphs differ for Clothing / Light / Heavy.

It intentionally keeps existing OBody behavior first:
1. Outfit-specific refit presets from JSON still win.
2. Actor preset-name + "-Refit" still wins.
3. Female-Refit / Male-Refit still wins.
4. Only the final hardcoded generated fallback becomes armor-class-aware.

This is a source patch, not a binary DLL patch. Rebuild OBody.dll after applying.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
BODY_H = ROOT / "include" / "Body" / "Body.h"
BODY_CPP = ROOT / "src" / "Body" / "Body.cpp"


def find_matching_brace(text: str, open_brace_index: int) -> int:
    depth = 0
    in_string = False
    escape = False
    in_line_comment = False
    in_block_comment = False

    i = open_brace_index
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
            i += 1
            continue

        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 2
                continue
            i += 1
            continue

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == "/" and nxt == "/":
            in_line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            in_block_comment = True
            i += 2
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1

    raise RuntimeError("Could not find matching brace")


def replace_function(text: str, signature_start: str, replacement: str) -> str:
    start = text.find(signature_start)
    if start == -1:
        raise RuntimeError(f"Could not find function signature: {signature_start}")
    brace = text.find("{", start)
    if brace == -1:
        raise RuntimeError(f"Could not find opening brace for: {signature_start}")
    end = find_matching_brace(text, brace) + 1
    return text[:start] + replacement.strip() + text[end:]


def insert_before_function(text: str, signature_start: str, insert_text: str) -> str:
    idx = text.find(signature_start)
    if idx == -1:
        raise RuntimeError(f"Could not find insertion point: {signature_start}")
    if insert_text.strip() in text:
        return text
    return text[:idx] + insert_text.strip() + "\n\n" + text[idx:]


def patch_header() -> None:
    text = BODY_H.read_text(encoding="utf-8")

    if "enum class RefitClass" not in text:
        namespace_pos = text.find("namespace Body")
        brace = text.find("{", namespace_pos)
        if namespace_pos == -1 or brace == -1:
            raise RuntimeError("Could not find namespace Body in Body.h")
        enum_text = """

enum class RefitClass
{
    Nude,
    Clothing,
    LightArmor,
    HeavyArmor
};
"""
        text = text[: brace + 1] + enum_text + text[brace + 1 :]

    if "RefitClass GetRefitClass(RE::Actor* a_actor) const;" not in text:
        marker = "void ApplyClothePreset(RE::Actor* a_actor) const;"
        text = text.replace(marker, marker + " RefitClass GetRefitClass(RE::Actor* a_actor) const;")

    text = text.replace(
        "PresetManager::SliderSet GenerateClotheSliders(RE::Actor* a_actor) const;",
        "PresetManager::SliderSet GenerateClotheSliders(RE::Actor* a_actor, RefitClass a_refitClass) const;",
    )

    BODY_H.write_text(text, encoding="utf-8")


GET_REFIT_CLASS_CPP = r'''
RefitClass OBody::GetRefitClass(RE::Actor* a_actor) const
{
    using Slot = RE::BGSBipedObjectForm::BipedObjectSlot;

    if (!a_actor) {
        return RefitClass::Nude;
    }

    const RE::TESObjectARMO* bodyArmor = a_actor->GetWornArmor(Slot::kBody);
    const RE::TESObjectARMO* outerChest = a_actor->GetWornArmor(Slot::kModChestPrimary);
    const RE::TESObjectARMO* underChest = a_actor->GetWornArmor(Slot::kModChestSecondary);

    // Priority is intentionally strongest-to-softest. A cuirass with ArmorHeavy should win
    // over a light/clothing undergarment in a secondary chest slot.
    const std::array<const RE::TESObjectARMO*, 3> wornChestItems{bodyArmor, outerChest, underChest};

    for (const auto* armor : wornChestItems) {
        if (armor && armor->HasKeywordString("ArmorHeavy")) {
            return RefitClass::HeavyArmor;
        }
    }

    for (const auto* armor : wornChestItems) {
        if (armor && armor->HasKeywordString("ArmorLight")) {
            return RefitClass::LightArmor;
        }
    }

    for (const auto* armor : wornChestItems) {
        if (armor) {
            return RefitClass::Clothing;
        }
    }

    return RefitClass::Nude;
}
'''


APPLY_CLOTHE_PRESET_CPP = r'''
void OBody::ApplyClothePreset(RE::Actor* a_actor) const
{
    const auto& presetContainer{PresetContainer::GetInstance()};
    const bool isFemale = IsFemale(a_actor);
    std::optional a_preset = std::nullopt;
    auto& jsonParser{Parser::JSONParser::GetInstance()};

    // Existing behavior: explicit outfit refit presets from JSON still have highest priority.
    a_preset = jsonParser.GetRefitPresetFromEquippedItems(a_actor, isFemale);
    if (a_preset) {
        ApplySliderSet(a_actor, a_preset->sliders, "OClothe");
        return;
    }

    // Existing behavior: actor-specific refit preset still wins, if present.
    const auto a_presetName = ActorTracker::Registry::GetInstance().GetPresetNameForActor(a_actor, isFemale);
    if (a_presetName) {
        const std::string refitPresetName = *a_presetName + "-Refit";
        a_preset = GetPresetByNameForRandom(
            isFemale ? presetContainer.allFemalePresets : presetContainer.allMalePresets,
            refitPresetName);
    }

    const RefitClass refitClass = GetRefitClass(a_actor);

    if (refitClass == RefitClass::Nude) {
        RemoveClothePreset(a_actor);
        return;
    }

    // New behavior: allow global preset overrides per armor class.
    // If these presets exist in BodySlide, they are used instead of generated hardcoded sliders.
    if (!a_preset) {
        std::string classPresetName;
        if (isFemale) {
            switch (refitClass) {
            case RefitClass::HeavyArmor:
                classPresetName = "Female-Refit-Heavy";
                break;
            case RefitClass::LightArmor:
                classPresetName = "Female-Refit-Light";
                break;
            case RefitClass::Clothing:
                classPresetName = "Female-Refit-Clothing";
                break;
            default:
                classPresetName = "Female-Refit";
                break;
            }
            a_preset = GetPresetByNameForRandom(presetContainer.allFemalePresets, classPresetName);
        } else {
            switch (refitClass) {
            case RefitClass::HeavyArmor:
                classPresetName = "Male-Refit-Heavy";
                break;
            case RefitClass::LightArmor:
                classPresetName = "Male-Refit-Light";
                break;
            case RefitClass::Clothing:
                classPresetName = "Male-Refit-Clothing";
                break;
            default:
                classPresetName = "Male-Refit";
                break;
            }
            a_preset = GetPresetByNameForRandom(presetContainer.allMalePresets, classPresetName);
        }
    }

    // Existing behavior: legacy global refit preset fallback still works.
    if (!a_preset) {
        if (isFemale) {
            a_preset = GetPresetByNameForRandom(presetContainer.allFemalePresets, "Female-Refit");
        } else {
            a_preset = GetPresetByNameForRandom(presetContainer.allMalePresets, "Male-Refit");
        }
    }

    if (a_preset) {
        ApplySliderSet(a_actor, a_preset->sliders, "OClothe");
    } else {
        auto set{GenerateClotheSliders(a_actor, refitClass)};
        ApplySliderSet(a_actor, set, "OClothe");
    }
}
'''


GENERATE_CLOTHE_SLIDERS_CPP = r'''
PresetManager::SliderSet OBody::GenerateClotheSliders(RE::Actor* a_actor, const RefitClass a_refitClass) const
{
    PresetManager::SliderSet set;

    if (a_refitClass == RefitClass::Nude) {
        return set;
    }

    // Shared smoothing: stop the sides/underside of the breasts from caving in under outfits.
    AddSliderToSet(set, DeriveSlider(a_actor, "BreastSideShape", 0.0F));
    AddSliderToSet(set, DeriveSlider(a_actor, "BreastUnderDepth", 0.0F));

    switch (a_refitClass) {
    case RefitClass::HeavyArmor:
        // Rigid cuirass: strongest compression, least forced cleavage/togetherness.
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.20F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.25F, -0.20F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.30F, -0.40F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.05F, 0.10F});
        AddSliderToSet(set, Slider{"Breasts", -0.12F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.10F});
        break;

    case RefitClass::LightArmor:
        // Light armor: moderate shaping, still less aggressive than old one-size ORefit.
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.55F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.15F, -0.10F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.20F, -0.25F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.15F, 0.20F});
        AddSliderToSet(set, Slider{"Breasts", -0.07F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.12F});
        break;

    case RefitClass::Clothing:
    default:
        // Clothing/robes: closest to original ORefit, but toned down slightly.
        AddSliderToSet(set, DeriveSlider(a_actor, "BreastCleavage", 0.85F));
        AddSliderToSet(set, Slider{"BreastGravity2", -0.10F, -0.05F});
        AddSliderToSet(set, Slider{"BreastTopSlope", -0.15F, -0.25F});
        AddSliderToSet(set, Slider{"BreastsTogether", 0.25F, 0.30F});
        AddSliderToSet(set, Slider{"Breasts", -0.05F});
        AddSliderToSet(set, Slider{"BreastHeight", 0.15F});
        break;
    }

    // Existing non-breast smoothing, kept mostly intact.
    AddSliderToSet(set, DeriveSlider(a_actor, "ButtDimples", 0.0F));
    AddSliderToSet(set, DeriveSlider(a_actor, "ButtUnderFold", 0.0F));
    AddSliderToSet(set, Slider{"AppleCheeks", -0.05F});
    AddSliderToSet(set, Slider{"Butt", -0.05F});

    AddSliderToSet(set, DeriveSlider(a_actor, "Clavicle_v2", 0.0F));
    AddSliderToSet(set, DeriveSlider(a_actor, "NavelEven", 1.0F));
    AddSliderToSet(set, DeriveSlider(a_actor, "HipCarved", 0.0F));

    if (setNippleSlidersRefitEnabled) {
        // Heavier armor should hide nipples hardest; clothing is softer; light armor is in between.
        const float nipBGoneTarget = a_refitClass == RefitClass::HeavyArmor ? 1.0F :
                                     a_refitClass == RefitClass::LightArmor ? 0.85F :
                                                                              0.70F;
        const float areolaTarget = a_refitClass == RefitClass::HeavyArmor ? -0.50F :
                                   a_refitClass == RefitClass::LightArmor ? -0.40F :
                                                                            -0.30F;
        const float nipplePerkTarget = a_refitClass == RefitClass::HeavyArmor ? -0.45F :
                                       a_refitClass == RefitClass::LightArmor ? -0.35F :
                                                                                -0.25F;

        AddSliderToSet(set, DeriveSlider(a_actor, "NippleDip", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "NippleTip", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "NipplePuffy_v2", 0.0F));
        AddSliderToSet(set, DeriveSlider(a_actor, "AreolaSize", areolaTarget));
        AddSliderToSet(set, DeriveSlider(a_actor, "NipBGone", nipBGoneTarget));
        AddSliderToSet(set, Slider{"NippleDistance", 0.05F, 0.08F});
        AddSliderToSet(set, Slider{"NippleDown", 0.0F, -0.1F});
        AddSliderToSet(set, DeriveSlider(a_actor, "NipplePerkManga", nipplePerkTarget));
    }

    return set;
}
'''


def patch_cpp() -> None:
    text = BODY_CPP.read_text(encoding="utf-8")

    if "#include <array>" not in text:
        text = text.replace("#include \"STL.h\"", "#include \"STL.h\"\n#include <array>")

    text = insert_before_function(text, "void OBody::ApplyClothePreset(RE::Actor* a_actor) const", GET_REFIT_CLASS_CPP)
    text = replace_function(text, "void OBody::ApplyClothePreset(RE::Actor* a_actor) const", APPLY_CLOTHE_PRESET_CPP)
    text = replace_function(text, "PresetManager::SliderSet OBody::GenerateClotheSliders(RE::Actor* a_actor)", GENERATE_CLOTHE_SLIDERS_CPP)
    text = text.replace("GenerateClotheSliders(a_actor)}", "GenerateClotheSliders(a_actor, GetRefitClass(a_actor))}")

    BODY_CPP.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    if not BODY_H.exists() or not BODY_CPP.exists():
        raise SystemExit(
            "Could not find include/Body/Body.h and src/Body/Body.cpp. "
            "Run this script from the root of the OBody-NG source tree."
        )

    patch_header()
    patch_cpp()
    print("Typed ORefit source patch applied. Rebuild OBody.dll next.")
