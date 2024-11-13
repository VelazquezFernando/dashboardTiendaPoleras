import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Título del dashboard
st.title("Dashboard de Ventas de Poleras Personalizadas")
st.subheader("Monitorización de KPI's Clave")

# Leer datos desde el archivo CSV y convertir la columna 'Date' a formato de fecha
df = pd.read_csv('salesData.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Añadir columna con el día de la semana
df['Day of Week'] = df['Date'].dt.day_name()

# Filtros
st.sidebar.header("Filtros")
selected_channel = st.sidebar.multiselect("Canal de Venta", options=df['Sales Channel'].unique(), default=df['Sales Channel'].unique())
selected_product_type = st.sidebar.multiselect("Tipo de Producto", options=df['Product Type'].unique(), default=df['Product Type'].unique())
selected_date = st.sidebar.date_input("Fecha", [pd.to_datetime('2023-01-02'), pd.to_datetime('2023-01-06')])

# Aplicar filtros
filtered_df = df[
    (df['Sales Channel'].isin(selected_channel)) &
    (df['Product Type'].isin(selected_product_type)) &
    (df['Date'] >= pd.to_datetime(selected_date[0])) &
    (df['Date'] <= pd.to_datetime(selected_date[1]))
]

# Mostrar el día de la semana correspondiente a la fecha seleccionada
selected_day = filtered_df['Day of Week'].unique()
if len(selected_day) > 0:
    st.sidebar.write(f"Día seleccionado: {', '.join(selected_day)}")

# KPI: Ventas Totales
total_sales = filtered_df['Revenue'].sum()
st.metric(label="Ventas Totales", value=f"${total_sales:,.2f}")

# KPI: Ventas por Canal de Venta
sales_by_channel = filtered_df.groupby('Sales Channel')['Revenue'].sum().reset_index()
st.bar_chart(sales_by_channel.set_index('Sales Channel'))
st.markdown("**Ventas por Canal de Venta:** Este gráfico compara el rendimiento de tu tienda en línea, redes sociales, ferias, etc.")

# KPI: Tiempo de Producción
avg_production_time = filtered_df['Production Time'].mean()
st.metric(label="Tiempo de Producción Promedio", value=f"{avg_production_time:.2f} horas")

# Gráfico: Tiempo de Producción Promedio por Tipo de Producto
production_time_by_product_type = filtered_df.groupby('Product Type')['Production Time'].mean().reset_index()

fig, ax = plt.subplots()
sns.barplot(x='Product Type', y='Production Time', data=production_time_by_product_type, ax=ax)
ax.set_title("Tiempo de Producción Promedio por Tipo de Producto")
ax.set_xlabel("Tipo de Producto")
ax.set_ylabel("Tiempo de Producción (horas)")
st.pyplot(fig)

st.markdown("**Tiempo de Producción Promedio por Tipo de Producto:** Este gráfico muestra el tiempo promedio que tarda en producirse cada tipo de producto.")

# KPI: Costo por Unidad
avg_cost_per_unit = filtered_df['Cost per Unit'].mean()
st.metric(label="Costo por Unidad Promedio", value=f"${avg_cost_per_unit:.2f}")

# Gráfico: Costo por Unidad Promedio por Tipo de Producto
cost_per_unit_by_product_type = filtered_df.groupby('Product Type')['Cost per Unit'].mean().reset_index()

fig, ax = plt.subplots()
sns.barplot(x='Product Type', y='Cost per Unit', data=cost_per_unit_by_product_type, ax=ax)
ax.set_title("Costo por Unidad Promedio por Tipo de Producto")
ax.set_xlabel("Tipo de Producto")
ax.set_ylabel("Costo por Unidad ($)")
st.pyplot(fig)

st.markdown("**Costo por Unidad Promedio por Tipo de Producto:** Este gráfico muestra el costo promedio por unidad para cada tipo de producto.")

# KPI: Índice de Satisfacción del Cliente
customer_satisfaction = filtered_df['Customer Satisfaction'].mean()
st.metric(label="Índice de Satisfacción del Cliente", value=f"{customer_satisfaction:.2f}/5")

# KPI: Calificación de los Productos
product_ratings = filtered_df['Product Rating'].mean()
st.metric(label="Calificación Promedio de los Productos", value=f"{product_ratings:.2f}/5")

# Función para crear un gráfico de barras comparando diferentes métricas
def create_comparison_plot(data, column, title, ylabel):
    fig, ax = plt.subplots()
    sns.barplot(x='Date', y=column, data=data, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("")  # Etiqueta del eje X en blanco
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

# Ventas Totales por Día
create_comparison_plot(filtered_df, 'Revenue', 'Ventas Totales por Día', 'Revenue')

# Producción por Día
create_comparison_plot(filtered_df, 'Production Time', 'Producción por Día', 'Production Time (horas)')

# Costo por Unidad por Día
create_comparison_plot(filtered_df, 'Cost per Unit', 'Costo por Unidad por Día', 'Cost per Unit')

# Satisfacción del Cliente por Día
create_comparison_plot(filtered_df, 'Customer Satisfaction', 'Satisfacción del Cliente por Día', 'Customer Satisfaction')

# Calificación del Producto por Día
create_comparison_plot(filtered_df, 'Product Rating', 'Calificación del Producto por Día', 'Product Rating')

st.markdown("Estos gráficos muestran las tendencias diarias de varios KPI's importantes para tu tienda de poleras personalizadas.")
