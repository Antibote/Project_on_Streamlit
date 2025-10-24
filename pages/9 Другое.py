import streamlit as st
import pandas as pd
import json
import csv
from shapely.geometry import shape
import geopandas as gpd
import pydeck as pdk

# Увеличиваем лимит размера полей CSV
csv.field_size_limit(10_000_000)

st.page_link("./app.py", label="⬅ Вернуться на главную")
st.title("Маршруты мусороуборочных машин в Америке")

@st.cache_data
def load_data():
    df = pd.read_csv("dataset/solid-waste-and-recycling-collection-routes-1.csv", sep=";")
    return df

df = load_data()

# Проверяем, что колонка geo_shape есть
if "geo_shape" not in df.columns:
    st.error("В файле отсутствует колонка 'geo_shape'. Проверь формат CSV.")
    st.stop()

# Удаляем строки с пустой геометрией
df = df.dropna(subset=["geo_shape"])

# Функция для разбора поля geo_shape (оно содержит JSON с координатами)
def parse_geometry(geo_str):
    try:
        geojson = json.loads(geo_str)
        return shape(geojson)
    except Exception:
        return None

df["geometry"] = df["geo_shape"].apply(parse_geometry)
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326").dropna(subset=["geometry"])

# Фильтр по дню недели
selected_day = st.selectbox("Выберите день недели:", sorted(gdf["day"].dropna().unique()))

day_gdf = gdf[gdf["day"] == selected_day]

if day_gdf.empty:
    st.warning(f"Нет данных для {selected_day}")
else:
    st.subheader(f"Отображение маршрутов на {selected_day.lower()}")

    # Получаем координаты для центра карты
    centroid = day_gdf.geometry.centroid.unary_union.centroid
    center = [centroid.y, centroid.x]

    # Преобразуем полигоны в формат GeoJSON
    geojson = day_gdf.__geo_interface__

    # Создаем слой
    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        opacity=0.5,
        stroked=True,
        filled=True,
        extruded=False,
        get_fill_color=[0, 200, 100, 100],
        get_line_color=[0, 0, 0],
    )

    view_state = pdk.ViewState(latitude=center[0], longitude=center[1], zoom=11)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    st.metric("Средняя площадь маршрута (м²)", f"{day_gdf['square_miles'].mean() * 2_589_988.11:,.0f}")
