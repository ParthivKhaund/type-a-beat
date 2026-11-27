import pytest

from abl.catalog import CatalogError, ROLE_TRACK_NAMES, default_sound, kit_for_style, pad_map, sound
from abl.patterns import DRUM_STYLES


def test_trap_uses_the_808_core_kit():
    kit = kit_for_style("trap")
    assert kit.name == "808 Core Kit"
    assert kit.uri == "query:Drums#FileId_5409"


@pytest.mark.parametrize("style", sorted(DRUM_STYLES))
def test_every_drum_style_has_a_kit_with_a_query_uri(style):
    assert kit_for_style(style).uri.startswith("query:Drums#")


def test_kit_for_unknown_style_raises():
    with pytest.raises(CatalogError):
        kit_for_style("dubstep")


def test_bass_808_alias_resolves_to_sub_808():
    s = sound("bass", "808")
    assert s.name == "Sub 808 Bass"
    assert s.uri == "query:Sounds#Bass:FileId_6515"


def test_keys_rhodes_alias():
    assert sound("keys", "rhodes").uri.endswith("FileId_4849")


def test_sound_aliases_are_case_insensitive():
    assert sound("keys", "Rhodes") == sound("keys", "rhodes")


def test_unknown_sound_alias_raises_with_options():
    with pytest.raises(CatalogError) as exc:
        sound("bass", "banjo")
    assert "808" in str(exc.value)


def test_default_bass_for_trap_is_an_808():
    assert "808" in default_sound("bass", "trap").name


def test_default_keys_for_lofi_is_rhodes():
    assert "Rhodish" in default_sound("keys", "lofi").name


def test_default_sound_unknown_style_falls_back_to_first_choice():
    assert default_sound("keys", "dubstep").name


def test_808_kit_ride_is_on_the_cymbal_pad():
    assert pad_map("808 Core Kit")["ride"] == 49


def test_unknown_kit_gets_the_general_midi_map():
    m = pad_map("Some Other Kit")
    assert m["kick"] == 36 and m["snare"] == 38 and m["ch"] == 42 and m["oh"] == 46 and m["ride"] == 51


def test_role_track_names_are_capitalised_roles():
    assert ROLE_TRACK_NAMES == {"drums": "Drums", "bass": "Bass", "keys": "Keys", "lead": "Lead"}


def test_keys_has_a_guitar_stand_in():
    assert sound("keys", "guitar").uri == "query:Sounds#Guitar%20&%20Plucked:FileId_5054"
