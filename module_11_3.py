"""
coding: utf-8
Дегтярев Виталий (группа 22/08)
Домашнее задание №11.3
Домашнее задание по теме "Интроспекция"
"""

import inspect

# Подопытный класс
class BlackBox:

    def __init__(self):
        self.param_0 = 1
        self.param_1 = [10, ['a', 'b', 'c'], True]
        self.param_2 = {
                        'one': 123,
                        'two': 345,
                        'three': 989,
                         }

    def __str__(self):
        return 'BlackBox: ' + str(self.param_0) + str(self.param_1) + str(self.param_2)

    def add(self):
        self.param_0 += self.param_0

# Анализирующая объекты Python функция
def introspection_info(obj):
    obj_info = dict() # Определение словаря, содержащего данные исследуемого объекта
    obj_info['object'] = obj # Значение содержащееся в объекте
    obj_info['type'] = type(obj) # Определение типа объекта
    obj_info['attributes'] = [arg for arg in dir(obj) if not arg.startswith('_')] # dir с фильтрацией публичных атрибутов
    obj_info['methods'] = [arg for arg in dir(obj) if callable(getattr(obj, arg))] # dir с фильтрацией методов посредством функции callable
    obj_info['module'] = inspect.getmodule(obj) # Определение принадлежности модулю
    obj_info['iterable'] = hasattr(obj, '__iter__') # Проверка на "итерируемость"
    obj_info['callable'] = callable(obj)  # Проверка на "вызываемость"
    obj_info['builtin'] = inspect.isbuiltin(obj)  # Проверка на "встроенность"
    return obj_info


if __name__ == '__main__':
    # Исследование объекта "целое число"
    number_info = introspection_info(42)
    print('\n')
    for key, value in number_info.items():
        print(key, ' : ', value)

    # Исследование объекта "список"
    list_info = introspection_info([106, '7', ['c', 'a', 'b'], True])
    print('\n')
    for key, value in list_info.items():
        print(key, ' : ', value)

    # Исследование объекта "объект класса"
    bb_1 = BlackBox()
    print('\n')
    object_info = introspection_info(bb_1)
    for key, value in object_info.items():
        print(key, ' : ', value)

    # Исследование объекта "встроенная функция"
    builtin_function_info = introspection_info(print)
    print('\n')
    for key, value in builtin_function_info.items():
        print(key, ' : ', value)

    # Исследование объекта "метод объекта"
    method_info = introspection_info(bb_1.add)
    print('\n')
    for key, value in method_info.items():
        print(key, ' : ', value)

    # Исследование объекта "функция"
    function_info = introspection_info(introspection_info)
    print('\n')
    for key, value in function_info.items():
        print(key, ' : ', value)