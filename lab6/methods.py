import numpy as np
import random


# Функция для деления многолченов с остатком
def polynomial_division_remainder(dividend, divisor):
    # Создаем копию делимого для изменения в процессе деления
    remainder = list(dividend)

    # Длина делимого и делителя
    len_divisor = len(divisor)

    # Пока степень остатка >= степени делителя
    while len(remainder) >= len_divisor:
        # Находим сдвиг для делителя, чтобы выровнять его с остатком
        shift = len(remainder) - len_divisor

        # Выполняем XOR между делителем, сдвинутым на shift позиций, и остатком
        for i in range(len_divisor):
            remainder[shift + i] ^= divisor[i]

        # Удаляем все последние нули из остатка, чтобы уменьшить его степень
        while len(remainder) > 0 and remainder[len(remainder) - 1] == 0:
            remainder = remainder[:len(remainder) - 1]

    return np.array(remainder)


# функция для умножения многочленов
def polynomial_multiply(A, B):
    degree_A = len(A)
    degree_B = len(B)
    result = np.zeros(degree_A + degree_B - 1, dtype=int)  # явное указание типа int

    for i in range(degree_B):
        if B[i] == 1:  # если коэффициент в B ненулевой
            result[i:i + degree_A] ^= A.astype(int)  # конвертируем A в целочисленный тип, если нужно

    return result


# Функция для допущения n-кратной ошибки в сообщении и попытки ее исправления
def make_and_correct_error(a, g, error_rate):
    print("\nВходное сообщение:      ", a)
    print("Порождающий полином:    ", g)

    v = polynomial_multiply(a, g)
    print("Отправленное сообщение: ", v)

    w = v.copy()
    error = np.zeros(len(w), dtype=int)

    if error_rate == 1:
        # Однократная ошибка — случайный индекс
        index = random.randint(0, len(w) - 1)
        error[index] = 1
    elif error_rate == 2:
        # Двухкратная ошибка в пределах 3 соседних разрядов
        index1 = random.randint(0, len(w) - 2)
        index2 = index1 + random.choice([1, 2])
        error[index1] = 1
        error[index2] = 1
    else:
        # Для всех остальных случаев (больше двух ошибок) ошибки ставятся случайно
        error_indices = random.sample(range(w.shape[0]), error_rate)
        for index in error_indices:
            error[index] = 1

    w = (w + error) % 2
    print("Сообщение с ошибкой:    ", w)

    s = polynomial_division_remainder(w, g)
    error_templates = None
    if error_rate == 1:
        error_templates = [[1]]
    else:
        error_templates = [[1, 1, 1], [1, 0, 1], [1, 1], [1]]

    idx = 0
    found = False
    for template in error_templates:
        if np.array_equal(s, template):
            found = True
    while not found:
        s = polynomial_division_remainder(polynomial_multiply(s, np.array([0, 1])), g)
        for template in error_templates:
            if np.array_equal(s, template):
                found = True
        idx += 1

    temp = np.zeros(len(w), dtype=int)
    if idx == 0:
        temp[idx] = 1
    else:
        temp[len(temp) - idx] = 1

    e = polynomial_multiply(s, temp)
    e = e[:len(w)]
    message = (w + e) % 2
    print("Исправленное сообщение: ", message)

    if np.array_equal(v, message):
        print("Ошибка исправлена корректно")
    else:
        print("Ошибка исправлена некорректно")
