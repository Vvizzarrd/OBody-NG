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

PROCESS_ACTOR_EQUIP_EVENT = r"""void OBody::ProcessActorEquipEvent(RE::Actor* a_actor, const bool a_removingArmor, const RE::TESForm* a_equippedArmor) const
{
    const bool isProcessed = IsProcessed(a_actor);
    const bool isBlacklisted = IsBlacklisted(a_actor);
    const bool clotheActive = IsClotheActive(a_actor);
    const bool naked = IsNaked(a_actor, a_removingArmor, a_equippedArmor);
    bool orefitIsApplied = clotheActive;
    bool female;

    if (!isProcessed | isBlacklisted) {
        goto notifyNativeEventListeners;
    }

    if (IsRemovingClothes(a_actor, a_removingArmor, a_equippedArmor)) {
        OnActorRemovingClothes.SendEvent(a_actor);
    }

    // if ORefit is disabled and actor has ORefit morphs, clear them right away.
    if (!setRefit & clotheActive) {
        RemoveClothePreset(a_actor);
        ApplyMorphs(a_actor, true);
        orefitIsApplied = false;
        goto notifyNativeEventListeners;
    }

    female = IsFemale(a_actor);
    if (const auto& presetContainer{PresetManager::PresetContainer::GetInstance()}; (female && presetContainer.femalePresets.empty()) || !female && presetContainer.malePresets.empty()) {
        goto notifyNativeEventListeners;
    }

    if (!naked && a_removingArmor) {
        // Fires when removing their armor
        OnActorNaked.SendEvent(a_actor);
    }

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

notifyNativeEventListeners:
    // It's particularly important that we avoid sending events recursively for this event,
    // because if an event-listener equips or unequips armour in response to it it can
    // easily cause an infinite loop of `TESEquipEvent`s, which would freeze the game
    // until it crashes from a stack overflow.
    SendActorChangeEvent(
        a_actor,
        [&] {
            using Event = ::OBody::API::IActorChangeEventListener;
            Event::OnActorClothingUpdate::Payload payload{nullptr, a_equippedArmor};
            Event::OnActorClothingUpdate::Flags flags{};
            static_assert(Event::OnActorClothingUpdate::Flags::IsClothed == (1 << 0));
            static_assert(Event::OnActorClothingUpdate::Flags::IsORefitApplied == (1 << 1));
            static_assert(Event::OnActorClothingUpdate::Flags::IsORefitEnabled == (1 << 2));
            static_assert(Event::OnActorClothingUpdate::Flags::IsProcessed == (1 << 3));
            static_assert(Event::OnActorClothingUpdate::Flags::IsBlacklisted == (1 << 4));
            static_assert(Event::OnActorClothingUpdate::Flags::ActorIsEquipping == (1 << 5));

            flags = static_cast(flags | uint64_t(!naked));
            flags = static_cast(flags | (uint64_t(orefitIsApplied) << 1));
            flags = static_cast(flags | (uint64_t(setRefit) << 2));
            flags = static_cast(flags | (uint64_t(isProcessed) << 3));
            flags = static_cast(flags | (uint64_t(isBlacklisted) << 4));
            flags = static_cast(flags | (uint64_t(!a_removingArmor) << 5));
            return std::make_pair(flags, payload);
        },
        [](auto listener, auto actor, auto&& args) {
            listener->OnActorClothingUpdate(actor, args.first, args.second);
        });
}"""

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

def replace_process_actor_equip_event(text: str) -> str:
    start_match = re.search(r"void\s+OBody::ProcessActorEquipEvent\s*\(", text)
    if not start_match:
        raise RuntimeError("Could not find ProcessActorEquipEvent start.")

    # Use the next known function as the end marker. This also repairs broken braces caused by the previous script.
    end_match = re.search(r"\n\s*void\s+OBody::GenerateActorBody\s*\(", text[start_match.start():])
    if not end_match:
        # Fallback to brace matching if the file is not broken.
        open_pos = text.find("{", start_match.start())
        close_pos = find_matching_brace(text, open_pos)
        return text[:start_match.start()] + PROCESS_ACTOR_EQUIP_EVENT + text[close_pos + 1:]

    end_pos = start_match.start() + end_match.start()
    return text[:start_match.start()] + PROCESS_ACTOR_EQUIP_EVENT + "\n" + text[end_pos:]

def main():
    if not BODY_CPP.exists():
        raise SystemExit(f"Could not find {BODY_CPP}. Run this from the OBody-NG repo root.")

    original = BODY_CPP.read_text(encoding="utf-8-sig")
    patched = insert_includes(original)
    patched = replace_process_actor_equip_event(patched)

    # Sanity checks: no stray broken recalc marker, and the function exists exactly once.
    if patched.count("void OBody::ProcessActorEquipEvent") != 1:
        raise RuntimeError("Expected exactly one ProcessActorEquipEvent after repair.")

    if 'BETA1_RECALC_BRANCH' in patched:
        raise RuntimeError("Repair failed: Python patch variable text leaked into Body.cpp.")

    # The previous broken script left BEGIN/END markers inside the C++ function.
    # The repaired version intentionally does not need those markers.
    if "// BEGIN Typed ORefit Beta 1 re-equip recalculation" in patched:
        raise RuntimeError("Repair failed: old broken recalc marker still present.")

    backup = BODY_CPP.with_suffix(".cpp.before_beta1_recalc_repair")
    backup.write_text(original, encoding="utf-8", newline="")
    BODY_CPP.write_text(patched, encoding="utf-8", newline="")

    JSONC_OUT.parent.mkdir(parents=True, exist_ok=True)
    if not JSONC_OUT.exists() or "Beta 1" not in JSONC_OUT.read_text(encoding="utf-8", errors="ignore"):
        JSONC_OUT.write_text(JSONC_TEXT + "\n", encoding="utf-8", newline="")
        print(f"Wrote Beta 1 JSONC config to {JSONC_OUT}")

    if JSON_OUT.exists():
        backup_json = JSON_OUT.with_suffix(JSON_OUT.suffix + ".before_beta1_recalc_repair")
        backup_json.write_text(JSON_OUT.read_text(encoding="utf-8"), encoding="utf-8", newline="")
        JSON_OUT.unlink()
        print(f"Backed up and removed old JSON config: {JSON_OUT}")

    print("Repaired ProcessActorEquipEvent and applied armor-swap recalculation safely.")
    print(f"Backup written to {backup}")
    print()
    print("Next:")
    print("  git add src/Body/Body.cpp contrib/Distribution/SKSE/Plugins/OBody_TypedORefit.jsonc")
    print('  git commit -m "Fix typed ORefit armor swap recalculation"')
    print("  git push")

if __name__ == "__main__":
    main()
