#!/usr/bin/env python3
from pathlib import Path
import re

BODY_CPP = Path("src/Body/Body.cpp")
JSONC_OUT = Path("contrib/Distribution/SKSE/Plugins/OBody_TypedORefit.jsonc")
JSON_OUT = Path("contrib/Distribution/SKSE/Plugins/OBody_TypedORefit.json")

JSONC_TEXT = r"""{
  // OBody Typed ORefit config v0.10
  //
  // This file can be edited while the game is running.
  // Save the file, then force OBody to reapply ORefit by unequipping/re-equipping clothing,
  // changing cell, or using an OBody reapply action.
  //
  // The DLL looks for:
  // 1. Data/SKSE/Plugins/OBody_TypedORefit.jsonc
  // 2. Data/SKSE/Plugins/OBody_TypedORefit.json

  "enabled": true,

  "compatibility": {
    // Important:
    // This keeps the original OBody ORefit exemption/masterlist behavior respected.
    //
    // Original OBody has exemption lists in OBody_presetDistributionConfig.json:
    // - blacklistedOutfitsFromORefit
    // - blacklistedOutfitsFromORefitFormID
    // - blacklistedOutfitsFromORefitPlugin
    //
    // v0.10 checks those before applying Typed ORefit sliders.
    "respectOriginalORefitBlacklist": true,

    // Default = safer/original-like behavior.
    //
    // "allRelevantItemsBlacklisted":
    //   Disable Typed ORefit only when all relevant worn body/chest items are blacklisted
    //   and no force-refit item is equipped.
    //
    // "anyBlacklisted":
    //   Disable Typed ORefit if any relevant worn body/chest item is blacklisted.
    //   This is stricter. Use only if you want one exempt item to suppress all ORefit.
    "blacklistMode": "allRelevantItemsBlacklisted"
  },

  "debug": {
    // Set to true to ignore keywordGroups/profileRules during testing.
    // Useful when you want only nude/clothing/lightArmor/heavyArmor fallback behavior.
    "disableKeywordGroups": false,

    // Force one profile for every ORefit application.
    // Leave empty for normal behavior.
    //
    // Examples:
    // "clothing"
    // "clothingBra"
    // "lightArmor"
    // "lightArmorBra"
    // "heavyArmor"
    // "heavyArmorBra"
    "forceProfile": ""
  },

  "keywordGroups": {
    "disabled": {
      // Any relevant body/chest ARMO record with one of these exact keywords
      // gets the disabled profile.
      "keywords": [
        "TypedORefit_Disabled",
        "NoORefit",
        "OBodyNoRefit"
      ]
    },

    "bra": {
      // Exact keyword EditorID matches.
      //
      // These are checked on the ARMO record:
      // ARMO -> KWDA - Keywords
      //
      // It does NOT check armor item names.
      "keywords": [
        "TypedORefit_Bra",
        "TypedORefit_Bikini",
        "ArmorBikini",
        "BikiniArmor"
      ]

      // Partial keyword matching is intentionally NOT enabled in v0.10.
      // I want this version to first stabilize masterlist/exemption behavior.
      // We can add keywordContains safely in v0.11 after v0.10 is confirmed stable.
    },

    "loose": {
      // Loose clothing is too vague for automatic matching.
      // Add exact keywords manually through xEdit/KID if you want a piece to use looseClothing.
      "keywords": [
        "TypedORefit_LooseClothing",
        "ClothingRobes",
        "ClothingRobe"
      ]
    }
  },

  "profileRules": [
    {
      // Highest priority. If disabled keyword is found, no ORefit sliders are applied.
      "baseClass": "*",
      "tag": "disabled",
      "profile": "disabled"
    },
    {
      "baseClass": "clothing",
      "tag": "bra",
      "profile": "clothingBra"
    },
    {
      "baseClass": "lightArmor",
      "tag": "bra",
      "profile": "lightArmorBra"
    },
    {
      "baseClass": "heavyArmor",
      "tag": "bra",
      "profile": "heavyArmorBra"
    },
    {
      "baseClass": "clothing",
      "tag": "loose",
      "profile": "looseClothing"
    }
  ],

  "defaultProfileByArmorClass": {
    "nude": "nude",
    "clothing": "clothing",
    "lightArmor": "lightArmor",
    "heavyArmor": "heavyArmor"
  },

  "profiles": {
    "disabled": {
      "enabled": false,
      "sliders": []
    },

    "nude": {
      "enabled": false,
      "sliders": []
    },

    "looseClothing": {
      "enabled": true,
      "sliders": [
        { "name": "BreastSideShape", "mode": "derive", "target": 0.0 },
        { "name": "BreastUnderDepth", "mode": "derive", "target": 0.0 },
        { "name": "BreastCleavage", "mode": "derive", "target": 0.70 },
        { "name": "BreastGravity2", "mode": "fixed", "min": -0.020, "max": -0.050 },
        { "name": "BreastTopSlope", "mode": "fixed", "min": -0.035, "max": -0.080 },
        { "name": "BreastsTogether", "mode": "fixed", "min": 0.060, "max": 0.120 },
        { "name": "Breasts", "mode": "fixed", "min": -0.006, "max": -0.015 },
        { "name": "BreastHeight", "mode": "fixed", "min": 0.025, "max": 0.060 },

        { "name": "AppleCheeks", "mode": "fixed", "value": -0.015 },
        { "name": "Butt", "mode": "fixed", "value": -0.015 },
        { "name": "NavelEven", "mode": "fixed", "value": 0.08 },

        { "name": "NippleDip", "mode": "fixed", "value": -0.018 },
        { "name": "NippleTip", "mode": "fixed", "value": -0.018 },
        { "name": "NipplePuffy_v2", "mode": "fixed", "value": -0.018 },
        { "name": "AreolaSize", "mode": "fixed", "value": -0.025 },
        { "name": "NipBGone", "mode": "fixed", "value": 0.08 },
        { "name": "NippleDistance", "mode": "fixed", "min": 0.010, "max": 0.015 },
        { "name": "NippleDown", "mode": "fixed", "min": 0.0, "max": -0.018 },
        { "name": "NipplePerkManga", "mode": "fixed", "value": -0.030 }
      ]
    },

    "clothing": {
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

    "clothingBra": {
      "enabled": true,
      "sliders": [
        { "name": "BreastSideShape", "mode": "derive", "target": 0.0 },
        { "name": "BreastUnderDepth", "mode": "derive", "target": 0.0 },
        { "name": "BreastCleavage", "mode": "derive", "target": 0.88 },
        { "name": "BreastGravity2", "mode": "fixed", "min": -0.055, "max": -0.135 },
        { "name": "BreastTopSlope", "mode": "fixed", "min": -0.075, "max": -0.180 },
        { "name": "BreastsTogether", "mode": "fixed", "min": 0.240, "max": 0.420 },
        { "name": "Breasts", "mode": "fixed", "min": -0.018, "max": -0.045 },
        { "name": "BreastHeight", "mode": "fixed", "min": 0.085, "max": 0.160 },

        { "name": "AppleCheeks", "mode": "fixed", "value": -0.015 },
        { "name": "Butt", "mode": "fixed", "value": -0.015 },
        { "name": "NavelEven", "mode": "fixed", "value": 0.08 },

        { "name": "NippleDip", "mode": "fixed", "value": -0.035 },
        { "name": "NippleTip", "mode": "fixed", "value": -0.035 },
        { "name": "NipplePuffy_v2", "mode": "fixed", "value": -0.035 },
        { "name": "AreolaSize", "mode": "fixed", "value": -0.060 },
        { "name": "NipBGone", "mode": "fixed", "value": 0.14 },
        { "name": "NippleDistance", "mode": "fixed", "min": 0.014, "max": 0.020 },
        { "name": "NippleDown", "mode": "fixed", "min": 0.0, "max": -0.025 },
        { "name": "NipplePerkManga", "mode": "fixed", "value": -0.070 }
      ]
    },

    "lightArmor": {
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

    "lightArmorBra": {
      "enabled": true,
      "sliders": [
        { "name": "BreastSideShape", "mode": "derive", "target": 0.0 },
        { "name": "BreastUnderDepth", "mode": "derive", "target": 0.0 },
        { "name": "BreastCleavage", "mode": "derive", "target": 0.94 },
        { "name": "BreastGravity2", "mode": "fixed", "min": -0.070, "max": -0.155 },
        { "name": "BreastTopSlope", "mode": "fixed", "min": -0.130, "max": -0.280 },
        { "name": "BreastsTogether", "mode": "fixed", "min": 0.260, "max": 0.430 },
        { "name": "Breasts", "mode": "fixed", "min": -0.025, "max": -0.060 },
        { "name": "BreastHeight", "mode": "fixed", "min": 0.095, "max": 0.175 },

        { "name": "AppleCheeks", "mode": "fixed", "value": -0.030 },
        { "name": "Butt", "mode": "fixed", "value": -0.030 },
        { "name": "NavelEven", "mode": "fixed", "value": 0.20 },

        { "name": "NippleDip", "mode": "fixed", "value": -0.075 },
        { "name": "NippleTip", "mode": "fixed", "value": -0.075 },
        { "name": "NipplePuffy_v2", "mode": "fixed", "value": -0.075 },
        { "name": "AreolaSize", "mode": "fixed", "value": -0.10 },
        { "name": "NipBGone", "mode": "fixed", "value": 0.28 },
        { "name": "NippleDistance", "mode": "fixed", "min": 0.032, "max": 0.045 },
        { "name": "NippleDown", "mode": "fixed", "min": 0.0, "max": -0.055 },
        { "name": "NipplePerkManga", "mode": "fixed", "value": -0.10 }
      ]
    },

    "heavyArmor": {
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
    },

    "heavyArmorBra": {
      "enabled": true,
      "sliders": [
        { "name": "BreastSideShape", "mode": "derive", "target": 0.0 },
        { "name": "BreastUnderDepth", "mode": "derive", "target": 0.0 },
        { "name": "BreastCleavage", "mode": "derive", "target": 0.98 },
        { "name": "BreastGravity2", "mode": "fixed", "min": -0.090, "max": -0.170 },
        { "name": "BreastTopSlope", "mode": "fixed", "min": -0.20, "max": -0.35 },
        { "name": "BreastsTogether", "mode": "fixed", "min": 0.300, "max": 0.500 },
        { "name": "Breasts", "mode": "fixed", "min": -0.035, "max": -0.075 },
        { "name": "BreastHeight", "mode": "fixed", "min": 0.120, "max": 0.220 },

        { "name": "ButtDimples", "mode": "derive", "target": 0.0 },
        { "name": "ButtUnderFold", "mode": "derive", "target": 0.0 },
        { "name": "AppleCheeks", "mode": "fixed", "value": -0.05 },
        { "name": "Butt", "mode": "fixed", "value": -0.05 },
        { "name": "Clavicle_v2", "mode": "derive", "target": 0.0 },
        { "name": "NavelEven", "mode": "derive", "target": 1.0 },
        { "name": "HipCarved", "mode": "derive", "target": 0.0 },

        { "name": "NippleDip", "mode": "fixed", "value": -0.120 },
        { "name": "NippleTip", "mode": "fixed", "value": -0.120 },
        { "name": "NipplePuffy_v2", "mode": "fixed", "value": -0.120 },
        { "name": "AreolaSize", "mode": "fixed", "value": -0.16 },
        { "name": "NipBGone", "mode": "fixed", "value": 0.45 },
        { "name": "NippleDistance", "mode": "fixed", "min": 0.05, "max": 0.08 },
        { "name": "NippleDown", "mode": "fixed", "min": 0.0, "max": -0.10 },
        { "name": "NipplePerkManga", "mode": "fixed", "value": -0.16 }
      ]
    }
  }
}
"""

V010_BLOCK = r"""
    // BEGIN Typed ORefit JSONC v0.10
    // Runtime-configurable typed ORefit.
    //
    // v0.10 goals:
    // - Keep JSONC runtime editing from v0.9.
    // - Respect original OBody ORefit exemption/masterlist logic.
    // - Add debugging switches for quicker in-game testing.
    //
    // Config file lookup order:
    // 1. Data/SKSE/Plugins/OBody_TypedORefit.jsonc
    // 2. Data/SKSE/Plugins/OBody_TypedORefit.json
    using Slot = RE::BGSBipedObjectForm::BipedObjectSlot;

    const RE::TESObjectARMO* bodyArmor = nullptr;
    const RE::TESObjectARMO* outerChest = nullptr;
    const RE::TESObjectARMO* underChest = nullptr;

    if (a_actor) {
        bodyArmor = a_actor->GetWornArmor(Slot::kBody);
        outerChest = a_actor->GetWornArmor(Slot::kModChestPrimary);
        underChest = a_actor->GetWornArmor(Slot::kModChestSecondary);
    }

    const std::array<const RE::TESObjectARMO*, 3> wornChestItems{bodyArmor, outerChest, underChest};

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

        // Compatibility guard:
        // Original OBody uses OBody_presetDistributionConfig.json to blacklist outfits from ORefit.
        // v0.9 generated typed sliders too early in some cases, so v0.10 checks the original blacklist again.
        //
        // Default mode mirrors original intent:
        // - if there is at least one non-blacklisted relevant chest/body item, ORefit may continue;
        // - if every relevant chest/body item is blacklisted and no force-refit item is equipped, return an empty set.
        if (document.HasMember("compatibility") && document["compatibility"].IsObject()) {
            const auto& compatibility = document["compatibility"];
            const auto respectBlacklist =
                !compatibility.HasMember("respectOriginalORefitBlacklist") ||
                !compatibility["respectOriginalORefitBlacklist"].IsBool() ||
                compatibility["respectOriginalORefitBlacklist"].GetBool();

            if (respectBlacklist && a_actor) {
                auto& originalJsonParser = Parser::JSONParser::GetInstance();

                bool hasRelevantItem = false;
                bool hasBlacklistedRelevantItem = false;
                bool hasNonBlacklistedRelevantItem = false;

                for (const auto* armor : wornChestItems) {
                    if (!armor) {
                        continue;
                    }

                    hasRelevantItem = true;

                    if (originalJsonParser.IsOutfitBlacklisted(*armor)) {
                        hasBlacklistedRelevantItem = true;
                    } else {
                        hasNonBlacklistedRelevantItem = true;
                    }
                }

                auto blacklistMode = std::string{"allRelevantItemsBlacklisted"};
                if (compatibility.HasMember("blacklistMode") && compatibility["blacklistMode"].IsString()) {
                    blacklistMode = compatibility["blacklistMode"].GetString();
                }

                const auto forceRefitEquipped = originalJsonParser.IsAnyForceRefitItemEquipped(a_actor, false, nullptr);

                const auto shouldSuppressForAnyBlacklisted =
                    blacklistMode == "anyBlacklisted" && hasBlacklistedRelevantItem && !forceRefitEquipped;

                const auto shouldSuppressForAllBlacklisted =
                    blacklistMode != "anyBlacklisted" &&
                    hasRelevantItem &&
                    hasBlacklistedRelevantItem &&
                    !hasNonBlacklistedRelevantItem &&
                    !forceRefitEquipped;

                if (shouldSuppressForAnyBlacklisted || shouldSuppressForAllBlacklisted) {
                    // Make the no-refit state explicit. ApplyClothePreset will receive an empty slider set after this.
                    morphInterface->ClearBodyMorphKeys(a_actor, "OClothe");
                    return true;
                }
            }
        }

        auto baseClass = std::string{};
        if (a_refitClass == RefitClass::HeavyArmor) {
            baseClass = "heavyArmor";
        } else if (a_refitClass == RefitClass::LightArmor) {
            baseClass = "lightArmor";
        } else if (a_refitClass == RefitClass::Clothing) {
            baseClass = "clothing";
        } else if (a_refitClass == RefitClass::Nude) {
            baseClass = "nude";
        }

        auto profileName = baseClass;

        if (!baseClass.empty() && document.HasMember("defaultProfileByArmorClass") && document["defaultProfileByArmorClass"].IsObject()) {
            const auto& classMap = document["defaultProfileByArmorClass"];
            if (classMap.HasMember(baseClass.c_str()) && classMap[baseClass.c_str()].IsString()) {
                profileName = classMap[baseClass.c_str()].GetString();
            }
        }

        auto debugDisableKeywordGroups = false;
        if (document.HasMember("debug") && document["debug"].IsObject()) {
            const auto& debug = document["debug"];

            if (debug.HasMember("forceProfile") && debug["forceProfile"].IsString()) {
                const auto forcedProfile = std::string{debug["forceProfile"].GetString()};
                if (!forcedProfile.empty()) {
                    profileName = forcedProfile;
                }
            }

            if (debug.HasMember("disableKeywordGroups") && debug["disableKeywordGroups"].IsBool()) {
                debugDisableKeywordGroups = debug["disableKeywordGroups"].GetBool();
            }
        }

        auto wornArmorHasKeyword = [&](const char* keyword) -> bool {
            if (!keyword) {
                return false;
            }

            for (const auto* armor : wornChestItems) {
                if (armor && armor->HasKeywordString(keyword)) {
                    return true;
                }
            }

            return false;
        };

        auto keywordGroupMatches = [&](const char* groupName) -> bool {
            if (!groupName || debugDisableKeywordGroups || !document.HasMember("keywordGroups") || !document["keywordGroups"].IsObject()) {
                return false;
            }

            const auto& groups = document["keywordGroups"];
            if (!groups.HasMember(groupName)) {
                return false;
            }

            const auto& group = groups[groupName];

            if (group.IsArray()) {
                for (const auto& keyword : group.GetArray()) {
                    if (keyword.IsString() && wornArmorHasKeyword(keyword.GetString())) {
                        return true;
                    }
                }
            }

            if (group.IsObject() && group.HasMember("keywords") && group["keywords"].IsArray()) {
                for (const auto& keyword : group["keywords"].GetArray()) {
                    if (keyword.IsString() && wornArmorHasKeyword(keyword.GetString())) {
                        return true;
                    }
                }
            }

            return false;
        };

        auto matchedTags = std::vector<std::string>{};
        if (!debugDisableKeywordGroups && document.HasMember("keywordGroups") && document["keywordGroups"].IsObject()) {
            const auto& groups = document["keywordGroups"];
            for (auto it = groups.MemberBegin(); it != groups.MemberEnd(); ++it) {
                if (it->name.IsString() && keywordGroupMatches(it->name.GetString())) {
                    matchedTags.emplace_back(it->name.GetString());
                }
            }
        }

        auto hasMatchedTag = [&](const char* tag) -> bool {
            if (!tag) {
                return false;
            }

            for (const auto& matchedTag : matchedTags) {
                if (matchedTag == tag) {
                    return true;
                }
            }

            return false;
        };

        if (!debugDisableKeywordGroups && document.HasMember("profileRules") && document["profileRules"].IsArray()) {
            for (const auto& rule : document["profileRules"].GetArray()) {
                if (!rule.IsObject() ||
                    !rule.HasMember("baseClass") || !rule["baseClass"].IsString() ||
                    !rule.HasMember("tag") || !rule["tag"].IsString() ||
                    !rule.HasMember("profile") || !rule["profile"].IsString()) {
                    continue;
                }

                const auto ruleBaseClass = std::string{rule["baseClass"].GetString()};
                const auto ruleTag = rule["tag"].GetString();

                const auto baseMatches = ruleBaseClass == "*" || ruleBaseClass == baseClass;
                if (baseMatches && hasMatchedTag(ruleTag)) {
                    profileName = rule["profile"].GetString();
                    break;
                }
            }
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
            morphInterface->ClearBodyMorphKeys(a_actor, "OClothe");
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
    // END Typed ORefit JSONC v0.10
"""

REQUIRED_INCLUDES = [
    "#include <array>",
    "#include <cstdio>",
    "#include <string>",
    "#include <vector>",
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

    # Remove any earlier Typed ORefit block.
    func = re.sub(
        r"\n\s*// BEGIN Typed ORefit JSONC? v0\.[0-9]+.*?// END Typed ORefit JSONC? v0\.[0-9]+\n",
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
    func = func[:insert_pos] + "\n" + V010_BLOCK + func[insert_pos:]

    return text[:open_pos] + func + text[close_pos + 1:]

def main():
    if not BODY_CPP.exists():
        raise SystemExit(f"Could not find {BODY_CPP}. Run this from the OBody-NG repo root.")

    original = BODY_CPP.read_text(encoding="utf-8-sig")
    patched = patch_body_cpp(original)

    backup = BODY_CPP.with_suffix(".cpp.v010_backup")
    backup.write_text(original, encoding="utf-8", newline="")
    BODY_CPP.write_text(patched, encoding="utf-8", newline="")

    print(f"Patched {BODY_CPP} with Typed ORefit JSONC v0.10.")
    print(f"Backup written to {backup}")

    JSONC_OUT.parent.mkdir(parents=True, exist_ok=True)

    if JSONC_OUT.exists():
        backup_jsonc = JSONC_OUT.with_suffix(JSONC_OUT.suffix + ".v010_backup")
        backup_jsonc.write_text(JSONC_OUT.read_text(encoding="utf-8"), encoding="utf-8", newline="")
        print(f"Backed up old JSONC to {backup_jsonc}")

    if JSON_OUT.exists():
        backup_json = JSON_OUT.with_suffix(JSON_OUT.suffix + ".v010_backup")
        backup_json.write_text(JSON_OUT.read_text(encoding="utf-8"), encoding="utf-8", newline="")
        print(f"Backed up old JSON to {backup_json}")
        JSON_OUT.unlink()
        print(f"Removed old active JSON file: {JSON_OUT}")

    JSONC_OUT.write_text(JSONC_TEXT + "\n", encoding="utf-8", newline="")
    print(f"Wrote v0.10 JSONC config to {JSONC_OUT}")
    print()
    print("Next:")
    print("  git add src/Body/Body.cpp contrib/Distribution/SKSE/Plugins/OBody_TypedORefit.jsonc")
    print('  git commit -m "Respect ORefit blacklist in typed config"')
    print("  git push")

if __name__ == "__main__":
    main()
