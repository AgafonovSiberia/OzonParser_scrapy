import json
from typing import List

BLOCK_NAMES = ("Общие", "Основные")
OS_PARAMS_NAMES = ("AndroidVersion", "iOSVer")


def get_characteristics(data_json: dict) -> List:
    """
    Позволяет получить блок, содержащий характеристики товара
    :param data_json: json-response from OZON-API
    :return:
    """
    widgets = data_json["widgetStates"]["webCharacteristics-939965-pdpPage2column-2"]
    widgets = json.loads(widgets)
    return widgets.get("characteristics")


def get_cached_data(characteristics: list) -> List[dict]:
    """
    Сохраняет в один список все параметры (словари) блоков, указанных в BLOCK_NAMES
    :param characteristics: List[dict] список всех блоков, содержащихся в характеристиках
    :return: List[dict]
    """
    cached_data = []
    for block in characteristics:
        block_name = block.get("title")
        if block_name in BLOCK_NAMES:
            cached_data.extend(block.get("short"))
    return cached_data


def get_os_version(cached_data: List[dict]) -> str:
    """
    :param cached_data: список параметров, содержащих версию ОС
    :return: str - (os_version)
    """
    for record in cached_data:
        current_key = record.get("key")
        if current_key in OS_PARAMS_NAMES:
            version = record.get("values")[0].get("text")
    return version if version else "Android_without_version"


def parse_os_from_json(data_json: dict):
    """
    Позволяет получить версию ОС смартфона
    :param data_json: json-response from OZON-API
    :return: str - (os_version)
    """
    characteristics = get_characteristics(data_json=data_json)
    cached_data = get_cached_data(characteristics=characteristics)
    return get_os_version(cached_data=cached_data)






