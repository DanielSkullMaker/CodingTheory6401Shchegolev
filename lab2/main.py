import random
import methods
from logging import info, INFO, basicConfig
import numpy as np

if __name__ == "__main__":
    basicConfig(level=INFO)
    info("Часть 1")
    s_matrix = np.array([[1, 0, 0, 1, 0, 1, 1],
                         [1, 1, 0, 0, 0, 0, 1],
                         [0, 0, 1, 1, 0, 0, 1],
                         [1, 0, 1, 0, 1, 0, 1],
                         [0, 0, 1, 1, 1, 1, 0]])
    g_matrix = methods.RREF(methods.REF(s_matrix))
    info(f"Порождающая матрица G: {g_matrix}")
    
    G_standard = methods.standard_view(g_matrix)
    info(f"Порождающая матрица G в стандартном виде: {g_matrix}")
    
    h_matrix = methods.h_matrix(G_standard)
    info(f"Проверочная матрица H: {h_matrix}")
    
    syndrome_table = methods.generate_syndrome_table(h_matrix, 1)
    info(f"Таблица синдромов: {syndrome_table}")
    
    u = np.array([1, 0, 0, 1])
    info(f"Кодовое слово длины k = 4: {u}")
    
    v = u @ G_standard % 2
    info(f"Отправленное кодовое слово длины n = 7: {v}")
    
    error = np.array([0] * 7)
    error[random.randint(0, 6)] = 1
    info(f"Возникшая ошибка: {error}")
    
    v = (v + error) % 2
    info(f"Принятое с ошибкой слово: {v}")
    
    syndrome = v @ h_matrix % 2
    info(f"Синдром принятого сообщения: {syndrome}")
    
    error = np.array([0] * 7)
    error[syndrome_table[tuple(syndrome)][0]] = 1
    v = (v + error) % 2
    info(f"Исправленное сообщение: {v}")
    info("Отправленное и исправленное сообщение совпадают\n")

    info(f"Кодовое слово длины k = 4: {u}")
    info(f"Отправленное кодовое слово длины n = 7: {v}")
    error = np.zeros(7, dtype = int)
    a, b = random.sample(range(7), 2)
    error[a], error[b] = 1, 1
    info(f"Возникшая ошибка: {error}")
    
    v = (v + error) % 2
    info(f"Принятое с ошибкой слово: {v}")
    
    syndrome = v @ h_matrix % 2
    info(f"Синдром принятого сообщения: {syndrome}")
    
    error = np.array([0] * 7)
    error[syndrome_table[tuple(syndrome)][0]] = 1
    v = (v + error) % 2
    info(f"Исправленное сообщение: {v}")
    info("Отправленное и исправленное сообщение не совпадают")


    info("2 часть")
    G_standard = np.array([[1,0,0,0,1,1,1,1,0,0,0,0],
                            [0,1,0,0,0,1,1,1,1,1,0,0],
                            [0,0,1,0,1,0,0,1,1,1,1,0],
                            [0,0,0,1,0,0,1,1,0,0,1,1]])
    info(f"Порождающая матрица G в стандартном виде: {G_standard}")

    h_matrix = methods.h_matrix(G_standard)
    info(f"Проверочная матрица H: {h_matrix}")

    syndrome_table = methods.generate_syndrome_table(h_matrix, 2)
    info(f"Таблица синдромов: {syndrome_table}")

    u = np.array([0, 0, 1, 0])
    info(f"Кодовое слово длины k = 4: {u}")

    v = u @ G_standard % 2
    info(f"Отправленное кодовое слово длины n = 12: {v}")

    error = np.array([0] * 12)
    error[random.randint(0, 11)] = 1
    info(f"Возникшая ошибка: {error}")

    v = (v + error) % 2
    info(f"Принятое с ошибкой слово: {v}")

    syndrome = v @ h_matrix % 2
    info(f"Синдром принятого сообщения: {syndrome}")

    error = np.array([0] * 12)
    for index in syndrome_table[tuple(syndrome)]:
        error[index] = 1
    v = (v + error) % 2
    info(f"Исправленное сообщение: {v}")
    info("Отправленное и исправленное сообщение совпадают\n")

    info(f"Кодовое слово длины k = 4: {u}")
    info(f"Отправленное кодовое слово длины n = 12: {v}")
    error = np.array([0] * 12)
    a, b = random.sample(range(12), 2)
    error[a], error[b] = 1, 1
    info(f"Возникшая ошибка: {error}")

    v = (v + error) % 2
    info(f"Принятое с ошибкой слово: {v}")

    syndrome = v @ h_matrix % 2
    info(f"Синдром принятого сообщения: {syndrome}")
    error = np.array([0] * 12)
    for index in syndrome_table[tuple(syndrome)]:
        error[index] = 1
    v = (v + error) % 2
    info(f"Исправленное сообщение: {v}")
    info("Отправленное и исправленное сообщение совпадают/n")

    info(f"Кодовое слово длины k = 4: {u}")
    info(f"Отправленное кодовое слово длины n = 12: {v}")
    error = np.array([0] * 12)
    a, b, c = random.sample(range(12), 3)
    error[a], error[b], error[c] = 1, 1, 1
    info(f"Возникшая ошибка: {error}")
    v = (v + error) % 2
    info(f"Принятое с ошибкой слово: {v}")
    syndrome = v @ h_matrix % 2
    info(f"Синдром принятого сообщения: {syndrome}")
    error = np.array([0] * 12)
    if tuple(syndrome) in syndrome_table:
        for index in syndrome_table[tuple(syndrome)]:
            error[index] = 1
        v = (v + error) % 2
        info(f"Исправленное сообщение: {v}")
        info("Отправленное и исправленное сообщение не совпадают")
    else:
        info("Синдрома, соответствующего данной ошибке, не найдено в таблице синдромов. Сообщение исправить невозможно.")
