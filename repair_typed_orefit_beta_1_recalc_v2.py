#!/usr/bin/env python3
from pathlib import Path
import re

BODY_CPP = Path("src/Body/Body.cpp")

FIXED_PROCESS_ACTOR_EQUIP_EVENT = r"""void OBody::ProcessActorEquipEvent(RE::Actor* a_actor, const bool a_removingArmor, const RE::TESForm* a_equippedArmor) const
{
    const bool isProcessed = IsProcessed(a_actor);
    const bool isBlacklisted = IsBlacklisted(a_actor);
    const bool clotheActive = IsClotheActive(a_actor);
    const bool naked = IsNaked(a_actor, a_removingArmor, a_equippedArmor);
    bool orefitIsApplied = clotheActive;
    bool female;

    // Typed ORefit Beta 1:
    // Original OBody only recalculated ORefit when the actor moved between
    // "nude" and "clothed". That can leave stale clothing/light/heavy values
    // active when swapping directly between body/chest outfits.
    //
    // Keep this as a simple bool declared before any goto. A lambda declared
    // later in the function would be skipped by the existing goto statements,
    // which MSVC correctly rejects.
    bool equippedArmorTouchesORefitSlots = false;
    if (a_actor && a_equippedArmor) {
        const auto* bodyArmor = a_actor->GetWornArmor(RE::BGSBipedObjectForm::BipedObjectSlot::kBody);
        const auto* outerChestArmor = a_actor->GetWornArmor(RE::BGSBipedObjectForm::BipedObjectSlot::kModChestPrimary);
        const auto* underChestArmor = a_actor->GetWornArmor(RE::BGSBipedObjectForm::BipedObjectSlot::kModChestSecondary);

        equippedArmorTouchesORefitSlots =
            bodyArmor == a_equippedArmor ||
            outerChestArmor == a_equippedArmor ||
            underChestArmor == a_equippedArmor;
    }

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
    } else if (clotheActive && !naked && setRefit && equippedArmorTouchesORefitSlots) {
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

            flags = static_cast<Event::OnActorClothingUpdate::Flags>(flags | uint64_t(!naked));
            flags = static_cast<Event::OnActorClothingUpdate::Flags>(flags | (uint64_t(orefitIsApplied) << 1));
            flags = static_cast<Event::OnActorClothingUpdate::Flags>(flags | (uint64_t(setRefit) << 2));
            flags = static_cast<Event::OnActorClothingUpdate::Flags>(flags | (uint64_t(isProcessed) << 3));
            flags = static_cast<Event::OnActorClothingUpdate::Flags>(flags | (uint64_t(isBlacklisted) << 4));
            flags = static_cast<Event::OnActorClothingUpdate::Flags>(flags | (uint64_t(!a_removingArmor) << 5));
            return std::make_pair(flags, payload);
        },
        [](auto listener, auto actor, auto&& args) {
            listener->OnActorClothingUpdate(actor, args.first, args.second);
        });
}"""

def replace_process_actor_equip_event(text: str) -> str:
    start_match = re.search(r"void\s+OBody::ProcessActorEquipEvent\s*\(", text)
    if not start_match:
        raise RuntimeError("Could not find OBody::ProcessActorEquipEvent.")

    end_match = re.search(r"\n\s*void\s+OBody::GenerateActorBody\s*\(", text[start_match.start():])
    if not end_match:
        raise RuntimeError("Could not find the next function, OBody::GenerateActorBody. Send Body.cpp around ProcessActorEquipEvent.")

    end_pos = start_match.start() + end_match.start()
    return text[:start_match.start()] + FIXED_PROCESS_ACTOR_EQUIP_EVENT + "\n" + text[end_pos:]

def main():
    if not BODY_CPP.exists():
        raise SystemExit("Run this from the OBody-NG repo root. Could not find src/Body/Body.cpp.")

    original = BODY_CPP.read_text(encoding="utf-8-sig")
    patched = replace_process_actor_equip_event(original)

    if patched.count("void OBody::ProcessActorEquipEvent") != 1:
        raise RuntimeError("Repair failed: expected exactly one ProcessActorEquipEvent.")
    if "auto equippedArmorTouchesORefitSlots = [&]" in patched:
        raise RuntimeError("Repair failed: old lambda-based recalc code is still present.")
    if "flags = static_cast(flags |" in patched:
        raise RuntimeError("Repair failed: malformed static_cast still present.")
    if "equippedArmorTouchesORefitSlots()" in patched:
        raise RuntimeError("Repair failed: old lambda call still present.")

    backup = BODY_CPP.with_suffix(".cpp.before_beta1_recalc_v2_repair")
    backup.write_text(original, encoding="utf-8", newline="")
    BODY_CPP.write_text(patched, encoding="utf-8", newline="")

    print("Repaired ProcessActorEquipEvent.")
    print("Fixed:")
    print(" - malformed Event::OnActorClothingUpdate::Flags casts")
    print(" - lambda skipped by existing goto statements")
    print(" - stale ORefit after direct clothing/light/heavy swaps")
    print(f"Backup written to {backup}")
    print()
    print("Next:")
    print("  git add src/Body/Body.cpp")
    print('  git commit -m "Repair typed ORefit armor swap recalculation"')
    print("  git push")

if __name__ == "__main__":
    main()
