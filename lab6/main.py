import numpy as np
from methods import make_and_correct_error

if __name__ == "__main__":
    # Входное сообщение a и порождающий полином g = 1 + x^2 + x^3
    a = np.array([1, 0, 0, 1])
    g = np.array([1, 0, 1, 1])

    # Исследование для однократной ошибки
    make_and_correct_error(a, g, 1)

    # Исследование для двухкратной ошибки
    make_and_correct_error(a, g, 2)

    # Исследование для трехкратной ошибки
    make_and_correct_error(a, g, 3)

    # Входное сообщение a и порождающий полином g = 1 + x^3 + x^4 + x^5 + x^6
    a = np.array([1, 0, 0, 1, 0, 0, 0, 1, 1])
    g = np.array([1, 0, 0, 1, 1, 1, 1])

    # Исследование для однократной ошибки
    make_and_correct_error(a, g, 1)

    # Исследование для двухкратной ошибки
    make_and_correct_error(a, g, 2)

    # Исследование для трехкратной ошибки
    make_and_correct_error(a, g, 3)

    # Исследование для четырехкратной ошибки
    make_and_correct_error(a, g, 4)
