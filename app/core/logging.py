from pathlib import Path

APP_DIR = Path(__file__).parent.parent
PROJ_DIR = APP_DIR.parent

DATA_DIR = PROJ_DIR / "data"
TEST_DIR = PROJ_DIR / "test"
LOGS_DIR = PROJ_DIR / "logs"

if __name__ == "__main__":
    None