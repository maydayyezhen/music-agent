from .critic import analyze_continuity
from .generator import generate_bass_line, generate_texture_events, materialize_clip
from .schema import (
    CONTINUITY_DEFAULTS,
    TEXTURE_FAMILIES,
    TEXTURE_TYPES,
    normalize_continuity,
    resolve_texture,
)
from .voicing import plan_smooth_voicings, voicing_cost

__all__ = [
    "CONTINUITY_DEFAULTS",
    "TEXTURE_FAMILIES",
    "TEXTURE_TYPES",
    "analyze_continuity",
    "generate_bass_line",
    "generate_texture_events",
    "materialize_clip",
    "normalize_continuity",
    "plan_smooth_voicings",
    "resolve_texture",
    "voicing_cost",
]
