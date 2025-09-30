import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
from pandas.plotting import scatter_matrix


data = pd.read_csv('./../data/StudentsPerformance.csv')
data['promedio'] = data[['math score', 'reading score', 'writing score']].mean(axis=1).round(2)


def clasificar_nivel(promedio):
    if promedio >= 90:
        return 'Excelente'
    elif promedio >= 75:
        return 'Bueno'
    elif promedio >= 60:
        return 'Regular'
    else:
        return 'Necesita mejorar'
data['nivel'] = data['promedio'].apply(clasificar_nivel)
porcentaje = data['nivel'].value_counts(normalize=True) * 100


st.set_page_config(page_title="Calificaciones de los  estudiantes", layout="wide")
st.title("Dashboard de rendimiento estudiantil")


with st.sidebar:
    genero = st.selectbox(
        'Seleccionar el género:',
        options=['Todos', 'female', 'male'],
        index=0
    )
    st.markdown("Fuente de datos: [Kaggle](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)")


data_filtrada = data if genero == 'Todos' else data[data['gender'] == genero]

col1, col2, col3 = st.columns(3)
col1.metric("Promedio Matemáticas", f"{data_filtrada['math score'].mean():.2f}")
col2.metric("Promedio Lectura", f"{data_filtrada['reading score'].mean():.2f}")
col3.metric("Promedio Escritura", f"{data_filtrada['writing score'].mean():.2f}")


st.subheader('Calificacion por nivel educativo de los padres')
nivel_promedio = data_filtrada.groupby('parental level of education')[['promedio']].mean().round(2).reset_index()
st.bar_chart(data=nivel_promedio, x='parental level of education', y='promedio', use_container_width=True)


col_izq, col_der = st.columns(2)
with col_izq:
    st.subheader('Correlación entre calificaciones')
    fig_scatter = scatter_matrix(
        data_filtrada[['math score', 'reading score', 'writing score']],
        diagonal='hist',
        color='teal'
    )
    st.pyplot(plt.gcf())
    
with col_der:
    st.subheader('Distribución de niveles')
    niveles = data['nivel'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(niveles, labels=niveles.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    st.pyplot(fig)