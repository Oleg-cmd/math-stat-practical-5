import matplotlib.pyplot as plt
import numpy as np
import math
from itertools import groupby

# Выполнение сразу будет записываться в TeX файл
answer_file = open("tex/main.tex", "w")
# Шапка для включения стилей и вывода титульного листа
answer_file.write("\\input{./tex/preamble}\n")
answer_file.write("\\begin{document}\n")
# Костыльно реализуем input{title} из-за каких-то проблем с кодировкой среды разработки...
with open("tex/title.tex", "r", encoding="utf-8") as file:
    for line in file.readlines():
        answer_file.write(line.lstrip())
# answer_file.write('\\input{title}\n')
answer_file.write("\\newpage\n")
answer_file.write("\\smallskip\n")


# Для обозначения заголовков разделов
def header_maker(title):
    answer_file.write("\\textbf{\\large " + title + "}\n\n")
    answer_file.write("\\smallskip\n")


# Для обозначения разделов
def title_maker(title):
    answer_file.write("\\textbf{\\LARGE " + title + "}\n\n")
    answer_file.write("\\smallskip\n")


# Для ввода какого-то текста
def some_text(text):
    answer_file.write(f"\\parindent=0mm{text}\\\\\n")


# Функция для создания таблиц вариационного и статистического рядов
def table_maker(data, flag):
    # Записываем начало таблицы
    answer_file.write("\\renewcommand{\\arraystretch}{1.5}")
    answer_file.write("\\begin{adjustbox}{max width=\\textwidth}\n")

    # Если установлен флаг, то это статистичсекий ряд
    if flag:
        # Выделяем из массива только уникальные значения
        unique_data = [unique for unique, _ in groupby(data)]
        answer_file.write(
            "\\begin{tabular}{|" + "|".join(["c"] * len(unique_data)) + "|}\n"
        )
        answer_file.write("\\hline\n")
        # Записываем строки с данными из массива уникальных значений
        row = " & ".join([f"{{\\large {str(val)}}}" for val in unique_data])
        answer_file.write(row + "\\\\\n")
        answer_file.write("\\hline\n")
        amount_data = [data.count(val) for val in unique_data]
        # Записываем строки с количеством повторений значения в исходном массиве
        row = " & ".join([f"{{\\large {val}}}" for val in amount_data])
        answer_file.write(row + "\\\\\n")
        answer_file.write("\\hline\n")
    else:
        answer_file.write("\\begin{tabular}{|" + "|".join(["c"] * len(data)) + "|}\n")
        answer_file.write("\\hline\n")
        # Записываем строки с данными из массива
        row = " & ".join([f"{{\\large {str(val)}}}" for val in data])
        answer_file.write(row + "\\\\\n")
        answer_file.write("\\hline\n")

    # Завершаем таблицу LaTeX
    answer_file.write("\\end{tabular}\n")
    answer_file.write("\\end{adjustbox}\n")


# Функция для создания таблицы интервального статистического ряда
# Массив с интервалами и количеством попавших в него значений (для эмпирической функции распределения)
interval_data = []


def interval_table_maker(data, h):
    # Количество интервалов
    m = 1 + math.log(len(data), 2)
    start_point = data[0] - h / 2
    next_point = start_point + h
    global interval_data
    for _ in range(round(m) + 1):
        counter = sum(1 for i in data if start_point <= i < next_point)
        interval_data.append([start_point, next_point, counter])
        start_point = next_point
        next_point += h
    intervals = [f"[{round(i[0], 4)};{round(i[1], 4)})" for i in interval_data]
    amounts = [i[-1] for i in interval_data]
    # Записываем начало таблицы
    answer_file.write("\\renewcommand{\\arraystretch}{1.5}")
    answer_file.write("\\begin{adjustbox}{max width=\\textwidth}\n")
    answer_file.write("\\begin{tabular}{|" + "|".join(["c"] * len(intervals)) + "|}\n")
    answer_file.write("\\hline\n")
    # Записываем строки с данными из массива
    row = " & ".join([f"{{\\large {str(val)}}}" for val in intervals])
    answer_file.write(row + "\\\\\n")
    answer_file.write("\\hline\n")
    row = " & ".join([f"{{\\large {val}}}" for val in amounts])
    answer_file.write(row + "\\\\\n")
    answer_file.write("\\hline\n")
    # Завершаем таблицу LaTeX
    answer_file.write("\\end{tabular}\n")
    answer_file.write("\\end{adjustbox}\n")


# Для рисования совокупностей
def collection_maker(data):
    answer_file.write("Для исходной выборки $$F_n^*(x) = \\begin{cases}\n")
    answer_file.write(f"0 & \\text{{при }} x < {data[0]}\\\\\n")
    for number in range(1, len(data)):
        answer_file.write(
            f"{number / len(data)} & \\text{{при }} {data[number - 1]}\\leq x < {data[number]}\\\\\n"
        )
    answer_file.write(f"1 & \\text{{при }} x \\geq {data[-1]}\n")
    answer_file.write("\\end{cases}$$\n")


# Для графика эмпирической функции распределения
def empirical_graph(data):
    answer_data = (
        [np.floor(data[0] - 0.1)] + data[0:] + [np.floor(data[-1] + 2)]
    )  # добавляем еще одно значения для того, чтобы график не прерывался в верхней и нижней точках
    y = [(i / len(data)) for i in range(len(data) + 1)] + [1]
    for i in range(len(y) - 1):
        plt.hlines(y=y[i], xmin=answer_data[i], xmax=answer_data[i + 1], color="blue")

    # Настройка графика: количество делений на осях X и Y
    plt.xlabel("x")
    plt.ylabel("p*")
    plt.grid(True)

    plt.xticks(
        np.arange(-2, 2, 0.4)
    )  # Установка диапазона значений и количества делений на оси X (от -2 до 2 и шаг 0.4)
    plt.yticks(
        np.arange(0, 1.1, 0.1)
    )  # Установка диапазона значений и количества делений на оси Y (от 0 до 1.1 с шагом 0.1)

    # Отображение графика
    plt.savefig("out/empirical_graph.png")
    plt.close()
    answer_file.write(
        "\\begin {figure}[h]\\centering\\includegraphics[width=0.8\\textwidth]{./out/empirical_graph.png}"
        "\\caption{График эмпирической функции распределения}\\label{fig:my_label}\\end{figure}\n"
    )


# Для гистограммы
def bar_chart_maker():
    global interval_data
    intervals = [f"[{interval[0]:.4f};{interval[1]:.4f})" for interval in interval_data]
    values = [(interval[2] / len(selection)) for interval in interval_data]

    bounds = [float(interval.strip("[]()").split(";")[0]) for interval in intervals]
    plt.bar(bounds, values, width=0.6, align="edge", edgecolor="black")
    plt.xlabel("X")
    plt.ylabel("p*")
    plt.savefig("out/bar_char.png")
    plt.close()
    answer_file.write(
        "\\begin {figure}[h]\\centering\\includegraphics[width=0.8\\textwidth]{./out/bar_char.png}"
        "\\caption{Гистограмма}\\label{fig:my_label}\\end{figure}\n"
    )


def frequency_polygon_maker():
    global interval_data
    midpoints = [(interval[0] + interval[1]) / 2 for interval in interval_data]
    values = [interval[2] for interval in interval_data]
    plt.scatter(midpoints, values)
    plt.plot(midpoints, values, linestyle="-", marker="o")
    plt.xlabel("X")
    plt.ylabel("n")
    plt.grid(True)
    plt.xticks(
        np.arange(-2, 2, 0.5)
    )  # Установка диапазона значений и количества делений на оси X (от -2 до 2 и шаг 0.4)
    plt.yticks(
        np.arange(0, 6, 0.5)
    )  # Установка диапазона значений и количества делений на оси Y (от 0 до 1.1 с шагом 0.1)
    plt.savefig("out/frequency_polygon.png")
    plt.close()
    answer_file.write(
        "\\begin {figure}[t]\\centering\\includegraphics[width=0.8\\textwidth]{./out/frequency_polygon.png}"
        "\\caption{Полигон приведенных частот группированной выборки}\\label{fig:my_label}\\end{figure}\n"
    )


# Вариант 12
# Выборка:
selection = [
    0.41,
    1.63,
    -1.53,
    -0.20,
    0.85,
    0.09,
    1.54,
    0.25,
    1.24,
    -0.26,
    1.08,
    0.42,
    -0.92,
    -0.91,
    1.15,
    -0.82,
    0.26,
    0.96,
    1.57,
    0.72,
]

title_maker("Задание")
some_text(
    "Каждый студент получает выборку из 20 чисел. Необходимо определить следующие \
статистические характеристики: вариационный ряд, экстремальные значения и размах, \
оценки математического ожидания и среднеквадратического отклонения, эмпирическую \
функцию распределения и её график, гистограмму и полигон приведенных частот \
группированной выборки. Для расчета характеристик и построения графиков нужно \
написать программу на одном из языков программирования. Листинг программы и \
результаты работы должны быть представлены в отчете по практической работе"
)
header_maker("Вариант №12")
table_maker(selection, False)
title_maker("Выполнение")
# Отсортированная по неубыванию выборка:
sorted_selection = sorted(selection)
header_maker("Вариационный ряд")
table_maker(sorted_selection, False)
header_maker("Статистический ряд")
table_maker(sorted_selection, True)
header_maker("Экстремальные значения")
some_text(
    f"Минимальное значение: $x_{{0}}$ = {sorted_selection[0]}; Максимальное значение: $x_{{20}}$ = {sorted_selection[-1]}"
)
header_maker("Размах")
some_text(
    f"Размах = наибольшее значение - наименьшее значение = $x_{{20}}$ - $x_{{0}}$;"
    f" Размах = {round(sorted_selection[-1] - sorted_selection[0], 3)}"
)
header_maker("Математическое ожидание")
some_text(
    "Для данной выборки статистический ряд будет совпадать с вариационным,"
    " так как каждое значение встречается только раз"
)
some_text(
    f"Выборочное среднее (выборочное математическое ожидание) - среднее арифметическое всех значений выборки,"
    f" считается по формуле:"
    f" $$\\overline{{x_B}} = \\frac{{1}}{{n}} \sum_{{i=1}}^k x_i\cdot n_i$$"
)
# Реализация
x_B = 0
for i in set(sorted_selection):
    x_B += i * sorted_selection.count(i) / len(sorted_selection)

some_text(f"Для исходной выборки $$\\overline{{x_B}} = {x_B}$$")
header_maker("Выбороная дисперсия")
some_text(
    f" Выбороная дисперсия $D_B$ - среднее арифметическое квадратов отклонений"
    f" значений выборки от выборочной средней $\\overline{{x_B}}$, считается по формуле:"
    f" $$D_B = \\frac{{1}}{{n}} \sum_{{i=1}}^k (x_i - \\overline{{x_B}})^2 \cdot n_i$$"
)
# Реализация
D_B = 0
for i in set(sorted_selection):
    D_B += (i - x_B) ** 2 * sorted_selection.count(i) / len(sorted_selection)
answer_file.write("\\newpage\n")
some_text(f"Для исходной выборки $$D_B = {x_B}$$")
header_maker("Среднеквадратическое отклонение")
some_text(
    f" Выборочное среднее квадратическое отклонение выборки определяется формулой"
    f" $$\\sigma_B = \\sqrt{{D_B}}$$"
)

some_text(f"Для исходной выборки $$\\sigma_B = {round(math.sqrt(D_B), 6)}$$")
header_maker("Исправленное выборочное среднее квадратическое отклонение")
some_text(
    f" При решении практических используется величина"
    f" $$S^2 = \\frac{{n}}{{n - 1}} \sum_{{i=1}}^k (x_i - \\overline{{x_B}})^2 \cdot n_i = \\frac{{n}}{{n - 1}}D_B$$"
    f" Которая называется \\textit{{исправленной выборочной дисперсией}}"
)
some_text(
    f" Величина $S = \\sqrt{{S^2}}$ называется исправленным выборочным средним квадратическим отклонением"
)
some_text(
    f"Для исходной выборки $$S = {round(math.sqrt(D_B * len(selection) / (len(selection) - 1)), 6)}$$"
)
header_maker("Эмпирическая функция распределения")
some_text(
    f" Эмпирической (статистической) функцией распределения называется функция $F_n^x(x)$,"
    f" определяющая для каждого значения $x$ частность события $\\{{X < x\\}}$:"
    f" $$F_n^*(x) = p^*\\{{X < x\\}}$$"
)
some_text(
    "Где $p^x = \\frac{{n_x}}{{n}}$ - отношение количесвта вариантов \\{X < x\\} к общему числу вариантов"
)
collection_maker(sorted_selection)
empirical_graph(sorted_selection)
answer_file.write("\\newpage\n")
header_maker("Интервальный статистический ряд")
some_text(
    "Так как признак является непрерывным, то имеет смысл составить интервальный"
    " статический ряд (для дальнейшего использования в функции распределения)."
    " Пользуясь формулой Стерджеса, найдем величину интервала"
    " $$h = \\frac{{x_{{max}} - x_{{min}}}}{{1 + log_2 n}}$$"
)
h = (sorted_selection[-1] - sorted_selection[0]) / (
    1 + math.log(len(sorted_selection), 2)
)
some_text(
    f"Для исходной выборки $$h = {round(h, 6)}$$"
    f"Учитывая рекомендацию по выбору начала первого интервала $x_{{нач}} = x_{{min}} - \\frac{{h}}{{2}}$"
)
interval_table_maker(sorted_selection, h)
bar_chart_maker()
# Для нормального отображения графика
frequency_polygon_maker()
# Завершение документа
answer_file.write("\end{document}")
# Закрытие файла
answer_file.close()
