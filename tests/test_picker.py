from abl.catalog import Sound
from abl.picker import kit_sound, pick_sounds, search, sound_for_tag

ENTRIES = [
    {"name": "Sub 808 Bass.adv", "uri": "query:Sounds#Bass:FileId_6515", "section": "Sounds", "category": "Bass"},
    {"name": "Electric Bass Soft.adg", "uri": "query:Sounds#Bass:FileId_5203", "section": "Sounds", "category": "Bass"},
    {"name": "Upright Bass.adv", "uri": "query:Sounds#Bass:FileId_6516", "section": "Sounds", "category": "Bass"},
    {"name": "E-Piano Rhodish.adg", "uri": "query:Sounds#Piano%20&%20Keys:FileId_4849", "section": "Sounds", "category": "Piano & Keys"},
    {"name": "Organ Funky.adg", "uri": "query:Sounds#Piano%20&%20Keys:FileId_4866", "section": "Sounds", "category": "Piano & Keys"},
    {"name": "Grand Piano.adg", "uri": "query:Sounds#Piano%20&%20Keys:FileId_4857", "section": "Sounds", "category": "Piano & Keys"},
    {"name": "Warm Analog Pad.adg", "uri": "query:Sounds#Pad:FileId_4980", "section": "Sounds", "category": "Pad"},
    {"name": "Pad Bass Lead.adg", "uri": "query:Sounds#Synth%20Lead:FileId_1", "section": "Sounds", "category": "Synth Lead"},
    {"name": "Chicago Kit.adg", "uri": "query:Drums#FileId_5362", "section": "Drums", "category": "Kits"},
    {"name": "Hybrid Kit.adg", "uri": "query:LivePacks#pack/kit", "section": "Packs", "category": "Drumdrops Recording Hybrid Kit/Drums"},
]


def test_search_prefers_the_category_then_the_first_keyword():
    assert search(ENTRIES, ("Pad",), ("Pad",), ("Sounds",)) == Sound("Warm Analog Pad", "query:Sounds#Pad:FileId_4980")


def test_search_falls_through_keywords_in_priority_order():
    assert search(ENTRIES, ("Wurli", "Rhodes", "E-Piano"), ("Piano & Keys",), ("Sounds",)).name == "E-Piano Rhodish"


def test_sound_for_tag_maps_a_clap_label_to_a_library_sound():
    assert sound_for_tag(ENTRIES, "bass", [("an upright acoustic bass", 0.4), ("a synthesizer bass", 0.3)]).name == "Upright Bass"
    assert sound_for_tag(ENTRIES, "keys", [("a hammond organ", 0.5)]).name == "Organ Funky"


def test_sound_for_tag_tries_the_next_label_when_the_first_has_no_match():
    assert sound_for_tag(ENTRIES, "keys", [("a flute", 0.5), ("a grand piano", 0.4)]).name == "Grand Piano"


def test_kit_sound_finds_kits_in_the_core_library_and_in_packs():
    assert kit_sound(ENTRIES, "Chicago Kit").uri == "query:Drums#FileId_5362"
    assert kit_sound(ENTRIES, "Hybrid Kit").uri == "query:LivePacks#pack/kit"
    assert kit_sound(ENTRIES, "Nope Kit") is None


def test_pick_sounds_uses_kit_tags_and_keys_source_with_fallbacks():
    fallback = {"drums": Sound("Dry Session Kit", "query:Drums#FileId_5419"), "bass": Sound("x", "q"), "keys": Sound("y", "q"), "lead": Sound("Sweet Lead", "q")}
    analysis = {
        "kit": {"name": "Chicago Kit", "score": 0.94},
        "instrument_tags": {"bass": [("a deep 808 sub bass", 0.4)], "keys": [("a hammond organ", 0.5)], "lead": [("a flute", 0.2)]},
        "keys_source": "other",
    }
    sounds, reasons = pick_sounds(analysis, ENTRIES, fallback)
    assert sounds["drums"].name == "Chicago Kit" and "closest kit" in reasons["drums"]
    assert sounds["bass"].name == "Sub 808 Bass"
    assert sounds["keys"].name == "Organ Funky"
    assert sounds["lead"].name == "Sweet Lead"  # no flute in this library: fallback kept


def test_pick_sounds_lets_the_piano_stem_override_the_tag():
    analysis = {"instrument_tags": {"keys": [("a warm synth pad", 0.5)]}, "keys_source": "piano"}
    sounds, _ = pick_sounds(analysis, ENTRIES, {})
    assert sounds["keys"].name == "Grand Piano"
