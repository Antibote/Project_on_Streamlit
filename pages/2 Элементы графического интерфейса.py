import streamlit as st
st.page_link("./app.py", label="Вернуться на главную")
st.title("Элементы графического интерфейса")

st.markdown("Ниже представлены примеры интерактивных виджетов Streamlit:")


if st.button("Нажми меня"):
    st.success("Кнопка нажата!")


value = st.slider("Выберите значение:", 0, 100, 50)
st.write(f"Текущее значение: {value}")


show_text = st.checkbox("Показать дополнительный текст")
if show_text:
    st.info("Ты зачем нажал? Верни обратно")


option = st.selectbox("Выберите любимый цвет:", ["Красный", "Синий", "Зелёный"])
st.write(f"Ваш выбор: {option}")


feedback = st.text_area("Оставьте отзыв:")
if feedback:
    st.write("Ваш отзыв принят:", feedback)
