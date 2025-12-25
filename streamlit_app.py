import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Predictions Dashboard',
    page_icon='📊',
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_predictions_data():
    """Grab predictions data from Excel or CSV file.

    This uses caching to avoid having to read the file every time.
    """

    # Путь к папке с данными
    DATA_FOLDER = Path(__file__).parent/'data'
    
    # Попробуем найти Excel файл сначала
    excel_files = list(DATA_FOLDER.glob('*.xlsx')) + list(DATA_FOLDER.glob('*.xls'))
    
    if excel_files:
        # Если нашли Excel файл, читаем его
        data_file = excel_files[0]
        try:
            predictions_df = pd.read_excel(data_file)
            print(f"Successfully read Excel file: {data_file.name}, rows: {len(predictions_df)}")
            return predictions_df
        except Exception as e:
            print(f"Error reading Excel: {e}")
    
    # Если Excel не нашли, пробуем CSV
    csv_file = DATA_FOLDER / 'Sheet1.csv'
    
    if csv_file.exists():
        try:
            predictions_df = pd.read_csv(
                csv_file, 
                encoding='latin-1',
                on_bad_lines='skip',
                engine='python'
            )
            print(f"Successfully read CSV file, rows: {len(predictions_df)}")
            return predictions_df
        except Exception as e:
            print(f"Error reading CSV: {e}")
    
    st.error("Не удалось найти файл с данными. Поместите файл predictions.xlsx или predictions.csv в папку data/")
    return pd.DataFrame()

predictions_df = get_predictions_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# 📊 Predictions Dashboard

Анализ данных предсказаний из вашего проекта по data mining.
'''

# Add some spacing
''
''

if predictions_df.empty:
    st.error("Не удалось загрузить данные")
    st.info("💡 **Совет:** Поместите ваш Excel файл (predictions.xlsx) в папку `data/`")
    st.stop()

# Показываем основную информацию о данных
st.header('Обзор данных', divider='gray')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Всего записей",
        value=f"{len(predictions_df):,}"
    )

with col2:
    st.metric(
        label="Количество колонок",
        value=len(predictions_df.columns)
    )

with col3:
    # Если есть числовые колонки, показываем их количество
    numeric_cols = predictions_df.select_dtypes(include=['number']).columns
    st.metric(
        label="Числовых колонок",
        value=len(numeric_cols)
    )

''
''

# Показываем первые строки данных
st.header('Просмотр данных', divider='gray')

''

# Позволяем выбрать количество строк для отображения
num_rows = st.slider('Количество строк для отображения:', 5, 100, 10)

st.dataframe(predictions_df.head(num_rows), width='stretch')

''
''

# Если есть числовые колонки, показываем статистику
if len(numeric_cols) > 0:
    st.header('Статистика числовых данных', divider='gray')
    
    ''
    
    st.dataframe(predictions_df[numeric_cols].describe(), width='stretch')
    
    ''
    ''
    
    # График для выбранной колонки
    st.header('Визуализация данных', divider='gray')
    
    ''
    
    selected_column = st.selectbox(
        'Выберите колонку для визуализации:',
        numeric_cols
    )
    
    if selected_column:
        # Создаем копию данных с явным индексом для графика
        chart_data = predictions_df[[selected_column]].copy()
        chart_data = chart_data.reset_index(drop=True)
        
        # Рисуем график
        st.line_chart(chart_data)
        
        ''
        ''
        
        # Дополнительная статистика по выбранной колонке
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Минимум", f"{predictions_df[selected_column].min():.2f}")
        with col2:
            st.metric("Максимум", f"{predictions_df[selected_column].max():.2f}")
        with col3:
            st.metric("Среднее", f"{predictions_df[selected_column].mean():.2f}")
        with col4:
            st.metric("Медиана", f"{predictions_df[selected_column].median():.2f}")

''
''

# Дополнительная информация о колонках
st.header('Информация о колонках', divider='gray')

''

# Конвертируем типы данных в строки, чтобы избежать проблем с Arrow
column_info = pd.DataFrame({
    'Колонка': predictions_df.columns,
    'Тип данных': [str(dtype) for dtype in predictions_df.dtypes.values],
    'Пропущенные значения': predictions_df.isnull().sum().values,
    'Уникальные значения': [predictions_df[col].nunique() for col in predictions_df.columns]
})

st.dataframe(column_info, width='stretch')

''
''

# Показываем названия всех колонок
st.header('Список всех колонок', divider='gray')

''

cols_list = st.columns(3)
for idx, col_name in enumerate(predictions_df.columns):
    with cols_list[idx % 3]:
        st.write(f"**{idx + 1}.** {col_name}")