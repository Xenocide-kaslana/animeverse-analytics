from pathlib import Path
import json
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.preprocessing import clean_dataset, save_parquet, validate_dataset


RAW_DATA = ROOT / "data" / "raw" / "anime_dataset_20k.csv"
PROCESSED_DATA = ROOT / "data" / "processed" / "anime_clean.parquet"
VALIDATION_REPORT = ROOT / "data" / "processed" / "phase2_validation.json"


def main() -> None:
    raw = pd.read_csv(RAW_DATA)
    clean = clean_dataset(raw)
    validation = validate_dataset(raw, clean)

    required_checks = [
        validation["row_count_preserved"],
        validation["mal_id_unique"],
        validation["invalid_mal_scores"] == 0,
        validation["invalid_anilist_scores"] == 0,
        validation["invalid_negative_episodes"] == 0,
    ]
    if not all(required_checks):
        raise ValueError(f"Phase 2 validation failed: {validation}")

    save_parquet(clean, PROCESSED_DATA)
    round_trip = pd.read_parquet(PROCESSED_DATA)
    if len(round_trip) != len(raw):
        raise ValueError("Parquet round-trip row count differs from cleaned dataset.")

    validation["round_trip_rows"] = len(round_trip)
    validation["parquet_bytes"] = PROCESSED_DATA.stat().st_size
    VALIDATION_REPORT.write_text(
        json.dumps(validation, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(validation, indent=2, ensure_ascii=False))
    print(f"Saved: {PROCESSED_DATA}")


if __name__ == "__main__":
    main()
