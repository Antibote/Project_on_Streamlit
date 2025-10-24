import streamlit as st
import pandas as pd
import numpy as np
st.page_link("./app.py", label="Вернуться на главную")
st.title("Работа с таблицами")

st.markdown("Пример отображения и обработки данных в таблицах.")

# Создаем DataFrame
data = pd.DataFrame({
    "Температура, °C": np.random.randint(15, 35, 10),
    "Влажность, %": np.random.randint(30, 90, 10),
    "Скорость ветра, м/с": np.random.uniform(0.5, 5.0, 10).round(2)
})

st.write("Исходные данные:")
st.dataframe(data)

# Фильтрация по температуре
temp_filter = st.slider("Показать только строки с температурой выше:", 15, 35, 20)
filtered = data[data["Температура, °C"] > temp_filter]

st.write(f"Результат фильтрации (T > {temp_filter} °C):")
st.dataframe(filtered)

