from logging import info, INFO, basicConfig
import numpy as np
from methods import rref,\
    find_lead_columns,\
    remove_lead_columns,\
    form_H_matrix,\
    generate_codewords_from_combinations,\
    generate_codewords_binary_multiplication,\
    check_codeword,\
    calculate_code_distance


# Основная функция для выполнения всех шагов лабораторной работы
def linear_code_with_errors(mat):

    g_star = rref(mat)
    lead_columns = find_lead_columns(g_star)
    x_matrix = remove_lead_columns(g_star, lead_columns)
    n_cols = np.shape(mat)[1]
    h_matrix = form_H_matrix(x_matrix, lead_columns, n_cols)

    info("G* (RREF матрица) =")
    info(f"{g_star}\n")
    info(f"lead = {lead_columns}\n")
    info("Сокращённая матрица x_matrix =")
    info(f"{x_matrix}\n")
    info("Проверочная матрица H =")
    info(f"{h_matrix}\n")

    # 1.4.1: Генерация всех кодовых слов через сложение строк
    codewords_1 = generate_codewords_from_combinations(g_star)
    info("Все кодовые слова (способ 1):")
    info(f"{codewords_1}\n")

    # 1.4.2: Генерация кодовых слов умножением двоичных слов на G
    codewords_2 = generate_codewords_binary_multiplication(g_star)
    info("Все кодовые слова (способ 2):")
    info(f"{codewords_2}\n")

    # Проверка, что множества кодовых слов совпадают
    assert set(map(tuple, codewords_1)) == set(map(tuple, codewords_2)), "Наборы кодовых слов не совпадают!"

    # Проверка кодовых слов с помощью матрицы H
    for codeword in codewords_1:
        result = check_codeword(codeword, h_matrix)
        assert np.all(result == 0), f"Ошибка: кодовое слово {codeword} не прошло проверку матрицей H"

    info("Все кодовые слова прошли проверку матрицей H.")

    # 1.4: Вычисление кодового расстояния
    d = calculate_code_distance(codewords_1)
    t = 0
    if t == 0:
        t = 1
    else:
        t = (d - 1) // 2
    info(f"Кодовое расстояние d = {d}")
    info(f"Кратность обнаруживаемой ошибки t = {t}\n")

    # Проверка ошибки кратности t
    e1 = np.zeros(n_cols, dtype=int)
    e1[2] = 1  # Внесение ошибки в один бит
    v = codewords_1[4]
    info(f"e1 = {e1}")
    info(f"v = {v}")
    v_e1 = (v + e1) % 2
    info(f"v + e1 = {v_e1}")
    info(f"(v + e1)@H = {check_codeword(v_e1, h_matrix)} - error\n")

    # Проверка ошибки кратности t + 1
    e2 = np.zeros(n_cols, dtype=int)
    e2[6] = 1
    e2[9] = 1  # Внесение ошибки в два бита
    info(f"e2 = {e2}")
    v_e2 = (v + e2) % 2
    info(f"v + e2 = {v_e2}")
    info(f"(v + e2)@H = {check_codeword(v_e2, h_matrix)} - no error")

    return h_matrix


if __name__ == '__main__':
    # basicConfig(level=INFO, filename="lab_1", filemode="w")
    basicConfig(level=INFO)
    # Пример
    matrix = ([[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
               [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
               [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
               [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
               [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
               [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]]
    )
    linear_code_with_errors(matrix)
