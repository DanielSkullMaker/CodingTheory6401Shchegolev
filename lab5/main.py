from methods import get_rm_G_matr,\
    get_err_word

if __name__ == "__main__":
    print("5.1 Написать функцию формирования порождающей матрицы кода Рида-Маллера (r,m) в каноническом виде для произвольно заданных r и m")
    g_matr_test, basis_order_test, vectors_order_test = get_rm_G_matr(5, 4)
    print(g_matr_test)

    print("5.3 Провести экспериментальную проверку алгоритма декодирования для кода Рида-Маллера (2,4)")
    r, m = 2, 4
    rm_g_matr, basis_order, vectors_order = get_rm_G_matr(r, m)
    print(rm_g_matr)
    t_list = [1, 2]
    for t in t_list:
        print(f"Экспериментальная проверка алгоритма декодрования кода Рида-Маллера RM(2, 4) при t = {t}")
        get_err_word(rm_g_matr, r, basis_order, vectors_order, t)
        if t != t_list[-1]:
            print("\n")
