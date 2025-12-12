# Общие сведения

Ryabykin_MapReduce_Var3

Реализован алгоритм PageRank с использованием библиотеки MRJob

Запуски проводились на операционной системе Ubuntu 24.04 LTS с использованием Python 3.12.3

# Использование

```bash
python pagerank.py input/small.txt --num-pages 4 > output/small.txt
```

Доступны опции командной строки:
| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--num-pages` | Количество страниц в графе (обязательный) | — |
| `--iterations` | Количество итераций | 10 |
| `--damping-factor` | Коэффициент демпфирования | 0.85 |

# Визуализация

Вспомогательный скрипт для визуализации полученного графа с pagerank:

```bash
python visualize.py --input output/small.txt --output images/small.png
```

# Формат входных данных

.txt файл, где каждая строка — страница и её исходящие ссылки:

```
page_id<TAB>outlink1,outlink2,outlink3
```

Пример (`input/small.txt`):
```
A	B,C
B	C
C	A
D	C
```

# Формат выходных данных

.txt файл, где каждая строка - страница, её pagerank и исходящие ссылки:

```
"page_id" "pagerank<TAB>outlinks"
```

Пример (`output/small.txt`):
```
"D"    "0.037500\tC"
"A"    "0.375055\tB,C"
"B"    "0.194937\tC"
"C"    "0.392509\tA"
```
