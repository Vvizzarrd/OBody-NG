#!/usr/bin/env python3
from pathlib import Path
import re

BODY_CPP = Path("src/Body/Body.cpp")
JSONC_OUT = Path("contrib/Distribution/SKSE/Plugins/OBody_TypedORefit.jsonc")
JSON_OUT = Path("contrib/Distribution/SKSE/Plugins/OBody_TypedORefit.json")

JSONC_TEXT = r"""{
  // OBody Typed ORefit Beta 1 clean + recalc config
  //
  // Goal:
  // Keep original OBody behavior intact.
  //
  // Original OBody still decides:
  // - whether ORefit should run
  // - whether an outfit is blacklisted/exempt
  // - whether an outfit is force-refit
  // - whether an outfit-specific refit preset should be used
  //
  // This file only changes the generated fallback ORefit slider values
  // for the three vanilla armor classes:
  //
  // - clothing
  // - lightArmor
  // - heavyArmor
  //
  // Nude receives no generated refit sliders.

  // Human-readable config version. The DLL currently ignores this field.
  "configVersion": "Beta 1 clean + recalc",

  // If false, Typed ORefit is disabled and original OBody fallback generation is used.
  // This does NOT disable ORefit globally. Use the OBody MCM/menu for that.
  "enabled": true,

  // Runtime editing:
  // This file is read when OBody generates fallback ORefit sliders.
  // You can edit it while the game is running, save the file,
  // then force OBody to recalculate by unequipping/re-equipping clothing
  // or reapplying OBody.
  "profiles": {
    "nude": {
      // Nude means no generated ORefit sliders.
      "enabled": false,
      "sliders": []
    },

    "clothing": {
      // Normal clothing.
      // Mild support/compression compared to nude.
      "enabled": true,
      "sliders": [
        { "name": "BreastSideShape", "mode": "derive", "target": 0.0 },
        { "name": "BreastUnderDepth", "mode": "derive", "target": 0.0 },
        { "name": "BreastCleavage", "mode": "derive", "target": 0.82 },
        { "name": "BreastGravity2", "mode": "fixed", "min": -0.045, "max": -0.115 },
        { "name": "BreastTopSlope", "mode": "fixed", "min": -0.075, "max": -0.180 },
        { "name": "BreastsTogether", "mode": "fixed", "min": 0.190, "max": 0.340 },
        { "name": "Breasts", "mode": "fixed", "min": -0.018, "max": -0.045 },
        { "name": "BreastHeight", "mode": "fixed", "min": 0.070, "max": 0.135 },

        { "name": "AppleCheeks", "mode": "fixed", "value": -0.015 },
        { "name": "Butt", "mode": "fixed", "value": -0.015 },
        { "name": "NavelEven", "mode": "fixed", "value": 0.08 },

        { "name": "NippleDip", "mode": "fixed", "value": -0.045 },
        { "name": "NippleTip", "mode": "fixed", "value": -0.045 },
        { "name": "NipplePuffy_v2", "mode": "fixed", "value": -0.045 },
        { "name": "AreolaSize", "mode": "fixed", "value": -0.060 },
        { "name": "NipBGone", "mode": "fixed", "value": 0.18 },
        { "name": "NippleDistance", "mode": "fixed", "min": 0.014, "max": 0.020 },
        { "name": "NippleDown", "mode": "fixed", "min": 0.0, "max": -0.025 },
        { "name": "NipplePerkManga", "mode": "fixed", "value": -0.070 }
      ]
    },

    "lightArmor": {
      // Light armor.
      // Stronger support/compression than clothing, but less than heavy armor.
      "enabled": true,
      "sliders": [
        { "name": "BreastSideShape", "mode": "derive", "target": 0.0 },
        { "name": "BreastUnderDepth", "mode": "derive", "target": 0.0 },
        { "name": "BreastCleavage", "mode": "derive", "target": 0.96 },
        { "name": "BreastGravity2", "mode": "fixed", "min": -0.085, "max": -0.180 },
        { "name": "BreastTopSlope", "mode": "fixed", "min": -0.130, "max": -0.280 },
        { "name": "BreastsTogether", "mode": "fixed", "min": 0.280, "max": 0.460 },
        { "name": "Breasts", "mode": "fixed", "min": -0.040, "max": -0.085 },
        { "name": "BreastHeight", "mode": "fixed", "min": 0.100, "max": 0.190 },

        { "name": "AppleCheeks", "mode": "fixed", "value": -0.030 },
        { "name": "Butt", "mode": "fixed", "value": -0.030 },
        { "name": "NavelEven", "mode": "fixed", "value": 0.20 },

        { "name": "NippleDip", "mode": "fixed", "value": -0.145 },
        { "name": "NippleTip", "mode": "fixed", "value": -0.145 },
        { "name": "NipplePuffy_v2", "mode": "fixed", "value": -0.145 },
        { "name": "AreolaSize", "mode": "fixed", "value": -0.20 },
        { "name": "NipBGone", "mode": "fixed", "value": 0.55 },
        { "name": "NippleDistance", "mode": "fixed", "min": 0.032, "max": 0.045 },
        { "name": "NippleDown", "mode": "fixed", "min": 0.0, "max": -0.055 },
        { "name": "NipplePerkManga", "mode": "fixed", "value": -0.20 }
      ]
    },

    "heavyArmor": {
      // Heavy armor.
      // Strongest generated support/compression.
      //
      // These keep the heavy armor behavior close to the values you liked earlier.
      "enabled": true,
      "sliders": [
        { "name": "BreastSideShape", "mode": "derive", "target": 0.0 },
        { "name": "BreastUnderDepth", "mode": "derive", "target": 0.0 },
        { "name": "BreastCleavage", "mode": "derive", "target": 1.0 },
        { "name": "BreastGravity2", "mode": "fixed", "min": -0.10, "max": -0.05 },
        { "name": "BreastTopSlope", "mode": "fixed", "min": -0.20, "max": -0.35 },
        { "name": "BreastsTogether", "mode": "fixed", "min": 0.30, "max": 0.35 },
        { "name": "Breasts", "mode": "fixed", "value": -0.05 },
        { "name": "BreastHeight", "mode": "fixed", "value": 0.15 },

        { "name": "ButtDimples", "mode": "derive", "target": 0.0 },
        { "name": "ButtUnderFold", "mode": "derive", "target": 0.0 },
        { "name": "AppleCheeks", "mode": "fixed", "value": -0.05 },
        { "name": "Butt", "mode": "fixed", "value": -0.05 },
        { "name": "Clavicle_v2", "mode": "derive", "target": 0.0 },
        { "name": "NavelEven", "mode": "derive", "target": 1.0 },
        { "name": "HipCarved", "mode": "derive", "target": 0.0 },

        { "name": "NippleDip", "mode": "derive", "target": 0.0 },
        { "name": "NippleTip", "mode": "derive", "target": 0.0 },
        { "name": "NipplePuffy_v2", "mode": "derive", "target": 0.0 },
        { "name": "AreolaSize", "mode": "derive", "target": -0.30 },
        { "name": "NipBGone", "mode": "derive", "target": 1.0 },
        { "name": "NippleDistance", "mode": "fixed", "min": 0.05, "max": 0.08 },
        { "name": "NippleDown", "mode": "fixed", "min": 0.0, "max": -0.10 },
        { "name": "NipplePerkManga", "mode": "derive", "target": -0.25 }
      ]
    }
  }
}
"""

V011_BLOCK = r"""
    // BEGIN Typed ORefit JSONC Beta 1 clean + recalc
    // Clean armor-class-only Typed ORefit.
    //
    // This intentionally does NOT do:
    // - keyword matching
    // - custom blacklist logic
    // - custom force-refit logic
    // - slot scanning
    // - bra/loose special routing
    //
    // Original OBody remains responsible for:
    // - whether ORefit should run
    // - blacklist/exemption behavior
    // - force-refit behavior
    // - outfit-specific refit presets
    //
    // This block only replaces the generated fallback slider values
    // when original OBody has already reached GenerateClotheSliders().
    auto TryApplyTypedORefitJson = [&]() -> bool {
        FILE* file = nullptr;

        fopen_s(&file, "Data/SKSE/Plugins/OBody_TypedORefit.jsonc", "rb");
        if (!file) {
            fopen_s(&file, "Data/SKSE/Plugins/OBody_TypedORefit.json", "rb");
        }

        if (!file) {
            return false;
        }

        char readBuffer[65536];
        rapidjson::FileReadStream stream(file, readBuffer, sizeof(readBuffer));
        rapidjson::Document document;
        document.ParseStream<rapidjson::kParseCommentsFlag | rapidjson::kParseTrailingCommasFlag>(stream);
        fclose(file);

        if (document.HasParseError() || !document.IsObject()) {
            return false;
        }

        if (document.HasMember("enabled") && document["enabled"].IsBool() && !document["enabled"].GetBool()) {
            return false;
        }

        auto profileName = std::string{};

        if (a_refitClass == RefitClass::HeavyArmor) {
            profileName = "heavyArmor";
        } else if (a_refitClass == RefitClass::LightArmor) {
            profileName = "lightArmor";
        } else if (a_refitClass == RefitClass::Clothing) {
            profileName = "clothing";
        } else if (a_refitClass == RefitClass::Nude) {
            profileName = "nude";
        }

        if (profileName.empty()) {
            return false;
        }

        if (!document.HasMember("profiles") || !document["profiles"].IsObject()) {
            return false;
        }

        const auto& profiles = document["profiles"];
        if (!profiles.HasMember(profileName.c_str()) || !profiles[profileName.c_str()].IsObject()) {
            return false;
        }

        const auto& profile = profiles[profileName.c_str()];
        if (profile.HasMember("enabled") && profile["enabled"].IsBool() && !profile["enabled"].GetBool()) {
            return true;
        }

        if (!profile.HasMember("sliders") || !profile["sliders"].IsArray()) {
            return false;
        }

        for (const auto& slider : profile["sliders"].GetArray()) {
            if (!slider.IsObject() || !slider.HasMember("name") || !slider["name"].IsString()) {
                continue;
            }

            if (slider.HasMember("mode") && slider["mode"].IsString()) {
                const auto mode = std::string{slider["mode"].GetString()};
                if (mode == "none" || mode == "disabled") {
                    continue;
                }
            }

            const auto name = std::string{slider["name"].GetString()};

            auto hasNumber = [&](const char* key) {
                return slider.HasMember(key) && slider[key].IsNumber();
            };

            auto getNumber = [&](const char* key, float fallback) {
                return hasNumber(key) ? slider[key].GetFloat() : fallback;
            };

            if (hasNumber("target")) {
                AddSliderToSet(set, DeriveSlider(a_actor, name.c_str(), getNumber("target", 0.0F)));
                continue;
            }

            if (slider.HasMember("random") && slider["random"].IsArray() && slider["random"].Size() == 2 &&
                slider["random"][0].IsNumber() && slider["random"][1].IsNumber()) {
                AddSliderToSet(set, Slider{name.c_str(), stl::random(slider["random"][0].GetFloat(), slider["random"][1].GetFloat())});
                continue;
            }

            if (hasNumber("min") && hasNumber("max")) {
                AddSliderToSet(set, Slider{name.c_str(), getNumber("min", 0.0F), getNumber("max", 0.0F)});
                continue;
            }

            if (hasNumber("low") && hasNumber("high")) {
                AddSliderToSet(set, Slider{name.c_str(), getNumber("low", 0.0F), getNumber("high", 0.0F)});
                continue;
            }

            if (hasNumber("value")) {
                AddSliderToSet(set, Slider{name.c_str(), getNumber("value", 0.0F)});
                continue;
            }
        }

        return true;
    };

    if (TryApplyTypedORefitJson()) {
        return set;
    }
    // END Typed ORefit JSONC Beta 1 clean + recalc
"""

REQUIRED_INCLUDES = [
    "#include <cstdio>",
    "#include <string>",
    "#include <rapidjson/document.h>",
    "#include <rapidjson/filereadstream.h>",
]

def insert_includes(text: str) -> str:
    missing = [inc for inc in REQUIRED_INCLUDES if inc not in text]
    if not missing:
        return text

    lines = text.splitlines(keepends=True)
    last_include = max((i for i, line in enumerate(lines) if line.lstrip().startswith("#include")), default=-1)
    if last_include == -1:
        raise RuntimeError("Could not find include block in Body.cpp.")

    return "".join(lines[:last_include + 1]) + "".join(inc + "\n" for inc in missing) + "".join(lines[last_include + 1:])

def find_matching_brace(text: str, open_pos: int) -> int:
    depth = 0
    in_string = False
    in_char = False
    escape = False
    line_comment = False
    block_comment = False

    for i in range(open_pos, len(text)):
        c = text[i]
        n = text[i + 1] if i + 1 < len(text) else ""

        if line_comment:
            if c == "\n":
                line_comment = False
            continue

        if block_comment:
            if c == "*" and n == "/":
                block_comment = False
            continue

        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_string = False
            continue

        if in_char:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == "'":
                in_char = False
            continue

        if c == "/" and n == "/":
            line_comment = True
            continue

        if c == "/" and n == "*":
            block_comment = True
            continue

        if c == '"':
            in_string = True
            continue

        if c == "'":
            in_char = True
            continue

        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i

    raise RuntimeError("Could not find matching brace.")

def find_generate_func(text: str):
    m = re.search(r"PresetManager::SliderSet\s+OBody::GenerateClotheSliders\s*\([^)]*\)\s*const\s*\{", text)
    if not m:
        raise RuntimeError("Could not find OBody::GenerateClotheSliders definition.")

    open_pos = text.find("{", m.start())
    close_pos = find_matching_brace(text, open_pos)
    return open_pos, close_pos

def patch_body_cpp(text: str) -> str:
    text = insert_includes(text)
    open_pos, close_pos = find_generate_func(text)
    func = text[open_pos:close_pos + 1]

    # Remove any prior Typed ORefit block.
    func = re.sub(
        r"\n\s*// BEGIN Typed ORefit JSONC? v0\.[0-9]+.*?// END Typed ORefit JSONC? v0\.[0-9]+(?: clean)?\n",
        "\n",
        func,
        count=1,
        flags=re.DOTALL,
    )

    # Fallback more general removal if previous end marker variant was different.
    func = re.sub(
        r"\n\s*// BEGIN Typed ORefit.*?// END Typed ORefit.*?\n",
        "\n",
        func,
        count=1,
        flags=re.DOTALL,
    )

    set_decl = "    PresetManager::SliderSet set;"
    idx = func.find(set_decl)
    if idx == -1:
        raise RuntimeError('Could not find exact line: "    PresetManager::SliderSet set;"')

    insert_pos = idx + len(set_decl)
    func = func[:insert_pos] + "\n" + V011_BLOCK + func[insert_pos:]

    return text[:open_pos] + func + text[close_pos + 1:]

BETA1_RECALC_BRANCH = r"""
    // BEGIN Typed ORefit Beta 1 re-equip recalculation
    // Original OBody only applied ORefit when going from nude -> clothed
    // and removed it when going from clothed -> nude.
    //
    // That was fine when every outfit used the same generic ORefit values.
    // Typed ORefit is different: clothing, light armor, and heavy armor can
    // have different generated fallback values.
    //
    // So when the actor is already clothed and a body/chest armor event happens,
    // recalculate OClothe instead of leaving the old clothing profile in place.
    auto equippedArmorTouchesORefitSlots = [&]() -> bool {
        using Slot = RE::BGSBipedObjectForm::BipedObjectSlot;

        if (!a_actor || !a_equippedArmor) {
            return false;
        }

        const auto* body = a_actor->GetWornArmor(Slot::kBody);
        const auto* outerChest = a_actor->GetWornArmor(Slot::kModChestPrimary);
        const auto* underChest = a_actor->GetWornArmor(Slot::kModChestSecondary);

        return body == a_equippedArmor || outerChest == a_equippedArmor || underChest == a_equippedArmor;
    };

    if (clotheActive && naked) {
        logger::info("Removing clothed preset to actor {}", a_actor->GetName());
        RemoveClothePreset(a_actor);
        ApplyMorphs(a_actor, true);
        orefitIsApplied = false;
    } else if (!clotheActive && !naked && setRefit) {
        logger::info("Applying clothed preset to actor {}", a_actor->GetName());
        ApplyClothePreset(a_actor);
        ApplyMorphs(a_actor, true);
        orefitIsApplied = true;
    } else if (clotheActive && !naked && setRefit && equippedArmorTouchesORefitSlots()) {
        logger::info("Reapplying clothed preset to actor {} after body/chest equipment change", a_actor->GetName());
        RemoveClothePreset(a_actor);
        ApplyClothePreset(a_actor);
        ApplyMorphs(a_actor, true);
        orefitIsApplied = true;
    }
    // END Typed ORefit Beta 1 re-equip recalculation
"""

def find_process_actor_equip_event(text: str):
    m = re.search(
        r"void\s+OBody::ProcessActorEquipEvent\s*\([^)]*\)\s*const\s*\{",
        text
    )
    if not m:
        raise RuntimeError("Could not find OBody::ProcessActorEquipEvent definition.")

    open_pos = text.find("{", m.start())
    close_pos = find_matching_brace(text, open_pos)
    return open_pos, close_pos

def patch_process_actor_equip_event(text: str) -> str:
    open_pos, close_pos = find_process_actor_equip_event(text)
    func = text[open_pos:close_pos + 1]

    # Remove a previous Beta 1 recalc block, if the script is re-run.
    func = re.sub(
        r"\n\s*// BEGIN Typed ORefit Beta 1 re-equip recalculation.*?// END Typed ORefit Beta 1 re-equip recalculation\n",
        "\n",
        func,
        count=1,
        flags=re.DOTALL,
    )

    # Replace the original ORefit apply/remove branch.
    branch_pattern = re.compile(
        r"""
        \n\s*if\s*\(\s*clotheActive\s*&&\s*naked\s*\)\s*\{
        .*?
        \}\s*else\s+if\s*\(\s*!\s*clotheActive\s*&&\s*!\s*naked\s*&&\s*setRefit\s*\)\s*\{
        .*?
        \}
        """,
        re.DOTALL | re.VERBOSE,
    )

    patched_func, count = branch_pattern.subn("\n" + BETA1_RECALC_BRANCH, func, count=1)
    if count != 1:
        raise RuntimeError(
            "Could not replace the ORefit apply/remove branch in ProcessActorEquipEvent. "
            "Send the current ProcessActorEquipEvent function body if this happens."
        )

    return text[:open_pos] + patched_func + text[close_pos + 1:]


def main():
    if not BODY_CPP.exists():
        raise SystemExit(f"Could not find {BODY_CPP}. Run this from the OBody-NG repo root.")

    original = BODY_CPP.read_text(encoding="utf-8-sig")
    patched = patch_body_cpp(original)
    patched = patch_process_actor_equip_event(patched)

    begin_count = patched.count("// BEGIN Typed ORefit JSONC Beta 1 clean + recalc")
    end_count = patched.count("// END Typed ORefit JSONC Beta 1 clean + recalc")
    if begin_count != 1 or end_count != 1:
        raise RuntimeError(
            f"Patch sanity check failed: expected exactly one Beta 1 block, "
            f"found {begin_count} BEGIN markers and {end_count} END markers."
        )

    recalc_begin_count = patched.count("// BEGIN Typed ORefit Beta 1 re-equip recalculation")
    recalc_end_count = patched.count("// END Typed ORefit Beta 1 re-equip recalculation")
    if recalc_begin_count != 1 or recalc_end_count != 1:
        raise RuntimeError(
            f"Patch sanity check failed: expected exactly one Beta 1 recalc block, "
            f"found {recalc_begin_count} BEGIN markers and {recalc_end_count} END markers."
        )

    forbidden_markers = [
        "keywordGroups",
        "profileRules",
        "forceProfile",
        "respectOriginalORefitBlacklist",
        "keywordContains",
    ]
    generated_block_start = patched.find("// BEGIN Typed ORefit JSONC Beta 1 clean + recalc")
    generated_block_end = patched.find("// END Typed ORefit JSONC Beta 1 clean + recalc")
    generated_block = patched[generated_block_start:generated_block_end]
    for marker in forbidden_markers:
        if marker in generated_block:
            raise RuntimeError(
                f"Patch sanity check failed: experimental marker still present in Beta 1 block: {marker}"
            )

    backup = BODY_CPP.with_suffix(".cpp.beta1_clean_backup")
    backup.write_text(original, encoding="utf-8", newline="")
    BODY_CPP.write_text(patched, encoding="utf-8", newline="")

    print(f"Patched {BODY_CPP} with clean Typed ORefit JSONC Beta 1.")
    print(f"Backup written to {backup}")

    JSONC_OUT.parent.mkdir(parents=True, exist_ok=True)

    if JSONC_OUT.exists():
        backup_jsonc = JSONC_OUT.with_suffix(JSONC_OUT.suffix + ".beta1_clean_backup")
        backup_jsonc.write_text(JSONC_OUT.read_text(encoding="utf-8"), encoding="utf-8", newline="")
        print(f"Backed up old JSONC to {backup_jsonc}")

    if JSON_OUT.exists():
        backup_json = JSON_OUT.with_suffix(JSON_OUT.suffix + ".beta1_clean_backup")
        backup_json.write_text(JSON_OUT.read_text(encoding="utf-8"), encoding="utf-8", newline="")
        print(f"Backed up old JSON to {backup_json}")
        JSON_OUT.unlink()
        print(f"Removed old active JSON file: {JSON_OUT}")

    JSONC_OUT.write_text(JSONC_TEXT + "\n", encoding="utf-8", newline="")
    print(f"Wrote clean Beta 1 JSONC config to {JSONC_OUT}")
    print()
    print("Sanity checks passed: exactly one clean Beta 1 block and one recalc block are present.")
    print()
    print("Next:")
    print("  git add src/Body/Body.cpp contrib/Distribution/SKSE/Plugins/OBody_TypedORefit.jsonc")
    print('  git commit -m "Create clean typed ORefit beta 1 with armor swap recalculation"')
    print("  git push")

if __name__ == "__main__":
    main()
