from pathlib import Path

APP_DIR = Path(__file__).parent
PROJ_DIR = APP_DIR.parent

DATA_DIR = PROJ_DIR / "data"
TEST_DIR = PROJ_DIR / "test"
CONT_DIR = PROJ_DIR / ".devcontainer"

if __name__ == "__main__":
    None