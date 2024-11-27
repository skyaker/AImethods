from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.yaml"    

def load_config():
  """
  yaml configuration load with relative path
  """
  with CONFIG_FILE.open("r") as f:
    config = yaml.safe_load(f)

  return config