from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "anime_dataset_20k.csv"
PROCESSED_DATA_PATH = ROOT_DIR / "data" / "processed" / "anime_clean.parquet"
PHASE2_VALIDATION_PATH = ROOT_DIR / "data" / "processed" / "phase2_validation.json"

PLATFORM_COLUMNS = {
    "Crunchyroll": "is_crunchyroll",
    "Netflix": "is_netflix",
    "HiDive": "is_hidive",
    "Funimation": "is_funimation",
    "Amazon Prime": "is_amazon_prime",
    "Disney+": "is_disney_plus",
    "Hulu": "is_hulu",
    "VRV": "is_vrv",
    "Bilibili": "is_bilibili",
    "YouTube": "is_youtube",
}

MIN_RATING_MEMBERS = 1000
MIN_STUDIO_ANIME = 5
MIN_GENRE_ANIME = 30
