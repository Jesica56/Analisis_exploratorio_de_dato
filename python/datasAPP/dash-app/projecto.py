import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.express as px

data = pd.read_csv('./../data/StudentsPerformance.csv')
data['promedio'] = data[['math score', 'reading score', 'writing score']].mean(axis=1).round(2)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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


navbar = dbc.NavbarSimple(
    brand = "Dashboard de estudiantes",
    children=[
        dash.html.A(
            'Fuente de datos',
            href='https://www.kaggle.com/datasets/spscientist/students-performance-in-exams',
            target = '_blank',
            style={'color': 'white', 'textDecoration': 'none'}
        )
    ],
    fluid=True,
)

menu = dash.html.Div(
    dash.dcc.Dropdown(
        id='menu',
        options=[{'label': 'Todos', 'value': 'todos'},
                 {'label': 'Mujer', 'value': 'female'},
                 {'label': 'Hombre', 'value': 'male'}     
                 ],
        value='todos',
        clearable=False,
        searchable=False,
        style={'width': '95%', 'margin-top': '5px'}        
    ),
    style={
        'display': 'flex',
        'justify-content': 'center'
            }
    )

carta = dash.html.Div([
   dbc.Row(
         [
              dbc.Col(dbc.Card(
                dbc.CardBody([
                     dash.html.H5("Promedio Matemáticas", className="card-title"),
                     dash.html.H2(id='promedio_mat', className="card-text")
                ])
              ), width=4),
              dbc.Col(dbc.Card(
                dbc.CardBody([
                     dash.html.H5("Promedio Lectura", className="card-title"),
                     dash.html.H2(id='promedio_lec', className="card-text")
                ])
              ), width=4),
              dbc.Col(dbc.Card(
                dbc.CardBody([
                     dash.html.H5("Promedio Escritura", className="card-title"),
                     dash.html.H2(id='promedio_esc', className="card-text")
                ])
              ), width=4)
         ],
         className="mb-4",
         style={'margin': '10px'}
   )
],style={'marginTop': '20Ppx','marginLeft': '10px', 'marginRight': '10px'})

grafico = dash.html.Div(dash.dcc.Graph(id='grafico_barra'))

grafico_matrix = dash.html.Div([
    dash.dcc.Graph(
                id='scatter_plot',
                figure= px.scatter_matrix(
                    data,
                    dimensions=['math score', 'reading score', 'writing score'],
                        title = 'Correlacion entre calificaciones'))
])

grafico_pastel = dash.html.Div([
            dash.dcc.Graph(
                id='pie_plot', 
                figure=px.pie(names = porcentaje.index, 
                values = porcentaje.values,
                title = 'Porcentaje de niveles de desempeño'))
])


@app.callback(       
        dash.Output('promedio_mat', 'children'),
        dash.Output('promedio_lec', 'children'),
        dash.Output('promedio_esc', 'children'),
        dash.Output('grafico_barra', 'figure'),
        dash.Input('menu', 'value')
    )

def update_dashborad(value):
    data_filtrada = data if value == 'todos' else data[data['gender'] == value]
    
    
    promedio_mat = data_filtrada['math score'].mean().round(2)
    promedio_lec = data_filtrada['reading score'].mean().round(2)
    promedio_esc = data_filtrada['writing score'].mean().round(2)
    
    promedio_por_nivel = data_filtrada.groupby('parental level of education')[['math score', 'reading score', 'writing score']].mean().reset_index()
    promedio_por_nivel['promedio_general'] = promedio_por_nivel[['math score', 'reading score', 'writing score']].mean(axis=1).round(2)
    
    grafico_barra = px.bar(promedio_por_nivel, 
                           x='parental level of education', 
                           y='promedio_general',
                           labels={
                               'parental level of education': 'Nivel educativo de los padres', 
                               'promedio_general': 'Promedio General'},
                           title='Promedio General por Nivel Educativo de los Padres'
                           )
    
    return f'{promedio_mat}%', f'{promedio_lec}%', f'{promedio_esc}%', grafico_barra

app.layout = dash.html.Div([
    dbc.Row(navbar),
    dbc.Row(menu),
    dbc.Row(carta),
    dbc.Row(grafico),
    dbc.Row(grafico_matrix),
    dbc.Row(grafico_pastel),
])

if __name__ == '__main__':
    app.run(debug=True)
