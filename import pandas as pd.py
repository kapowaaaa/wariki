import pandas as pd

# Данные, извлеченные из изображения
data = {
    'hired': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01'],
    'num_hired': [1, 100, 200, 300, 400, 500]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['hired'] = pd.to_datetime(df['hired'])

# Вычисление даты завершения испытательного срока
df['adapt_end'] = df['hired'] + pd.Timedelta(days=42)

# Создание временного ряда для каждого месяца
months = pd.period_range(start='2024-01', end='2024-12', freq='M')
mentors_needed = pd.Series(0.0, index=months)  # Изменяем на float

for index, row in df.iterrows():
    start = row['hired']
    end = row['adapt_end']
    
    # Найти все месяцы, которые пересекаются с периодом испытательного срока
    period = pd.period_range(start=start.to_period('M'), end=end.to_period('M'), freq='M')
    
    for month in period:
        if month in mentors_needed.index:
            mentors_needed[month] += row['num_hired'] / 40.0

# Округлить до ближайшего большего целого числа
mentors_needed = mentors_needed.apply(lambda x: int(-(-x // 1)))  # equivalent to math.ceil

# Вывод количества наставников для апреля, мая и июня 2024 года
required_months = ['2024-04', '2024-05', '2024-06', '2024-03', '2024-01']
for month in required_months:
    print(f"Наставники в {month}: {mentors_needed[month]}")
