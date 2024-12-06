from logging import info
import numpy as np
from itertools import combinations


# 1.1 Реализовать функцию REF(), приводящую матрицу к ступенчатому виду
def ref(matrix):
    # Преобразование матрицы в массив numpy
    mat = np.array(matrix)
    n_rows, n_cols = mat.shape
    lead = 0
    for r in range(n_rows):
        if lead >= n_cols:
            return mat
        i = r
        while mat[i, lead] == 0:
            i += 1
            if i == n_rows:
                i, lead = r, lead + 1
                if lead == n_cols:
                    return mat

        # По необходимости меняем строки местами
        mat[[i, r]] = mat[[r, i]]

        # Обработка всех строк ниже текущей
        for i in range(r + 1, n_rows):
            if mat[i, lead] != 0:
                mat[i] = (mat[i] + mat[r]) % 2
        lead += 1
    return mat


# 1.2 Реализовать функцию RREF(), приводящую матрицу к приведённому ступенчатому виду
def rref(mat):
    mat = ref(mat)
    n_rows, n_cols = mat.shape

    # проход по строкам сверху вниз
    for r in range(n_rows - 1, -1, -1):

        # находим ведущий элемент в строке
        lead = np.argmax(mat[r] != 0)
        if mat[r, lead] != 0:

            # обнуляем все элементы, которые выше ведущего
            for i in range(r - 1, -1, -1):
                if mat[i, lead] != 0:
                    mat[i] = (mat[i] + mat[r]) % 2
    while not any(mat[n_rows - 1]):
        mat, n_rows = mat[:-1, :], n_rows - 1
    return mat


# 1.3: Ведущие столбцы и удаление их для создания сокращённой матрицы
def find_lead_columns(matrix):
    lead_columns = []
    for r in range(len(matrix)):
        row = matrix[r]
        for i, val in enumerate(row):
            if val == 1:  # Первый единица в строке - ведущий
                lead_columns.append(i)
                break
    return lead_columns


# Функция, удаляющая ведущие столбцы
def remove_lead_columns(matrix, lead_columns):
    mat = np.array(matrix)
    reduced_matrix = np.delete(mat, lead_columns, axis = 1)
    return reduced_matrix


# Формирование матрицы H
def form_H_matrix(x_matrix, lead_columns, n_cols):

    # инициализация единичной матрицы размером (n - k) на n
    n_rows = np.shape(x_matrix)[1]

    h_matrix = np.zeros((n_cols, n_rows), dtype = int)
    I = np.eye(6, dtype = int)

    h_matrix[lead_columns, :] = x_matrix
    not_lead = [i for i in range(n_cols) if i not in lead_columns]
    h_matrix[not_lead, :] = I

    return h_matrix


# Основная функция для выполнения всех шагов 1.3.
def linear_code(mat):

    # 1.3.1: Преобразование матрицы в ступенчатый вид
    g_star = rref(mat)

    info("G* (RREF матрица) =")
    info(g_star)

    # 1.3.2: Найти ведущие столбцы
    lead_columns = find_lead_columns(g_star)
    info(f"lead = {lead_columns}")

    # 1.3.3: Удалить ведущие столбцы и получить сокращённую матрицу
    x_matrix = remove_lead_columns(g_star, lead_columns)
    info("Сокращённая матрица X =")
    info(x_matrix)

    # 1.3.4: Сформировать проверочную матрицу H
    n_cols = np.shape(mat)[1]
    h_matrix = form_H_matrix(x_matrix, lead_columns, n_cols)
    info("Проверочная матрица H =")
    info(h_matrix)

    return h_matrix


# 1.3
# Функция для нахождения всех кодовых слов из порождающей матрицы
def generate_codewords_from_combinations(g_matrix):
    rows = g_matrix.shape[0]
    codewords = set()

    # Перебираем все возможные комбинации строк матрицы G
    for r in range(1, rows + 1):
        for comb in combinations(range(rows), r):

            # Суммируем строки и добавляем результат в множество
            codeword = np.bitwise_xor.reduce(g_matrix[list(comb)], axis = 0)
            codewords.add(tuple(codeword))

    # Добавляем в множество нулевой вектор
    codewords.add(tuple(np.zeros(g_matrix.shape[1], dtype = int)))

    return np.array(list(codewords))


# Функция для умножения всех двоичных слов длины k на G
def generate_codewords_binary_multiplication(g_matrix):
    k = g_matrix.shape[0]
    n = g_matrix.shape[1]
    codewords = []

    # Генерируем все двоичные слова длины k
    for i in range(2**k):
        binary_word = np.array(list(np.binary_repr(i, k)), dtype = int)
        codeword = np.dot(binary_word, g_matrix) % 2
        codewords.append(codeword)

    return np.array(codewords)


# Функция проверки кодового слова с помощью проверочной матрицы H
def check_codeword(codeword, h_matrix):
    return np.dot(codeword, h_matrix) % 2


# Функция вычисления кодового расстояния
def calculate_code_distance(codewords):
    min_distance = float('inf')

    # Подсчет количества ненулевых элементов для всех попарных разностей кодовых слов
    for i in range(len(codewords)):
        for j in range(i + 1, len(codewords)):
            distance = np.sum(np.bitwise_xor(codewords[i], codewords[j]))
            if distance > 0:
                min_distance = min(min_distance, distance)

    return min_distance
