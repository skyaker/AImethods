import yaml
from typing import Dict

def load_generation_params(config_path: str) -> Dict[str, float]:
    """
    Загрузка параметров генерации текста из YAML файла.

    :param config_path: Путь к YAML файлу
    :return: Словарь с параметрами генерации
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config['generation_params']
