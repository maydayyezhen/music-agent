from __future__ import annotations

from copy import deepcopy

from build_song import HERE, SECTIONS, TEMPO, build, manifest, write_json


def clamp_complexity_budgets(composition: dict) -> dict:
    """Keep section attention budgets inside the repository's validated 0..5 scale.

    This changes project metadata only. Notes, harmony, articulations, timing,
    instruments and rendering configuration remain untouched.
    """

    result = deepcopy(composition)
    for section in result.get("sections", []):
        budget = section.get("complexity_budget", {})
        for role, value in list(budget.items()):
            if isinstance(value, (int, float)):
                budget[role] = max(0, min(5, value))
    return result


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    v1 = clamp_complexity_budgets(build("v1"))
    v2 = clamp_complexity_budgets(build("v2"))

    write_json("composition_v1.json", v1)
    write_json("composition_v2.json", v2)
    write_json("composition.json", v2)
    write_json("composition.normalized.json", v2)
    write_json("core_motif.json", v2["core_motif"])
    write_json("manifest.json", manifest())

    print(
        f"Built validated Afterglow Current: "
        f"{sum(bars for _, bars, _ in SECTIONS)} bars at {TEMPO} BPM"
    )


if __name__ == "__main__":
    main()
