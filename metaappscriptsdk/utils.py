# Супер мелкие функции, которые нужны в от 3 исптозований
import json


def chunks(list_, count_items_in_chunk):
    """
    разбить list (l) на куски по n элементов

    :param list_:
    :param count_items_in_chunk:
    :return:
    """
    for i in range(0, len(list_), count_items_in_chunk):
        yield list_[i:i + count_items_in_chunk]


def pretty_json(obj):
    """
    Представить объект в вище json красиво отформатированной строки
    :param obj:
    :return:
    """
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
