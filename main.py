import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table,callback_context
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

#df = pd.read_excel('movimientos_acelerometria.xlsx')

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.






# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
#df.groupby("Tipo").agg({})

#fig = px.bar(df, x=df["Tipo"].unique(), y=df.groupby(["Tipo","sexo"])['distancia_casa'].mean().reset_index()[df.groupby(["Tipo","sexo"])['distancia_casa'].mean().reset_index()['sexo'] == "F"],color="sexo", barmode="group")

#

df2 = pd.read_excel('tiempo_lugares.xlsx')
encuestas = pd.read_csv('t1-transmicable.csv', encoding='ISO-8859-1',sep = ";")
demograficos = pd.read_excel('ResumenParticipantes.xlsx',sheet_name = "participants_202004291506")
demograficos["Zona"] = demograficos["Zona"].replace({"Ciudad Bolívar" : "Ciudad Bolivar", "San Cristóbal": "San Cristobal"})
encuestas = demograficos.merge(encuestas, left_on = "id1", right_on = "T1_ID")
tiempo_movimiento = pd.read_excel('tiempo_movimiento.xlsx')



diccio = {1:"Trabajando",2:"No trabajó pero tenía trabajo",3:"Buscando trabajo",4:"Estudiando",5:"Oficios del hogar",6:"Incapacitado permanente",7:"Otros"}
encuestas = encuestas.replace({"T1_Q15":diccio})

colors = {
    'background': '#ede2e1',
    'text': '#7FDBFF'
}



def generate_table(max_rows=10):
    hola = encuestas['T1_Q10'].describe().to_frame().reset_index()
    return dash_table.DataTable(hola.to_dict('records'), [{"name": i, "id": i} for i in hola.columns])

external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

app = Dash(__name__,
                external_stylesheets= [dbc.themes.BOOTSTRAP, FONT_AWESOME])


app.layout =html.Div([


    html.Div([
        html.H3(children = 'Escoja la localidad a visualizar'),
dcc.Dropdown(
        id="dropdown",
        options=["Ciudad Bolivar","San Cristobal","Ambos"],
        value="Ambos",
        clearable=False)

],  style={"width": "30%",'display': 'inline-block',"marginLeft": "5%"}),
  html.Div([
        html.H3(children = 'Escoja el sexo'),
        dcc.Dropdown(
        id="dropdown2",
        options=["M","F","Ambos"],
        value="Ambos",
        clearable=False,
    )
        #dcc.Dropdown(
         #   id="dropdown3",
          #  options=["Trabajando","No trabajó pero tenía trabajo","Buscando trabajo","Estudiando","Oficios del hogar","Incapacitado permanente"],
           # value="Trabajando",
            #clearable=False,
            #multi=True
        #)
],  style={"width": "30%",'display': 'inline-block',"marginLeft": "5%"}),
dcc.Tabs([
        dcc.Tab(label='Datos Demograficos', children=[
html.Div(
    [
        html.I(className="fas fa-question-circle fa-lg", id="target"),
        dbc.Tooltip("Gráfico de barras que muestra la proporción de hombres y mujeres tomados en cuenta en el estudio", target="target"),
    ],
    className="p-5 text-muted"
),
            html.Div([

                # Table container
                html.Div([
                    dcc.Graph(id='sexo')

                ], style={'width': '49%', 'display': 'inline-block'}),

                # Graph container
                html.Div([

                    dcc.Graph(id='sexot2')

                ], style={'width': '49%', 'display': 'inline-block'}),

            ], style={'display': 'flex'}),
html.Div([
    html.Button('Descripción', id='btn-nclicks-1', n_clicks=0, style={'width': '240px', 'height': '40px',
                   'cursor': 'pointer', 'border': '0px',
                   'borderRadius': '5px', 'backgroundColor':
                   'black', 'color': 'white', 'textTransform':
                   'uppercase', 'fontSize': '15px'}),
    html.Div(id='container-button-timestamp')
],style={'textAlign': 'center'}),

            html.Div([

                # Table container
                html.Div([
                    dcc.Graph(id='ocupacion')

                ], style={'width': '49%', 'display': 'inline-block'}),

                # Graph container
                html.Div([

                    dcc.Graph(id='ocupacion2')

                ], style={'width': '49%', 'display': 'inline-block'}),

            ], style={'display': 'flex'}),
html.Div([
    html.Button('Descripción', id='btn-nclicks-2', n_clicks=0, style={'width': '240px', 'height': '40px',
                   'cursor': 'pointer', 'border': '0px',
                   'borderRadius': '5px', 'backgroundColor':
                   'black', 'color': 'white', 'textTransform':
                   'uppercase', 'fontSize': '15px'}),
    html.Div(id='container-button-timestamp2')
],style={'textAlign': 'center'}),
html.Div(
    [
        html.I(className="fas fa-question-circle fa-lg", id="target2"),
        dbc.Tooltip("Histograma que muestra la distribución de edades de las personas que participaron en el estudio", target="target2"),
    ],
    className="p-5 text-muted"
),

    html.Div([

        # Table container
        html.Div([
            dcc.Graph(id='edades')

        ], style={'width': '49%', 'display': 'inline-block'}),


        # Graph container
        html.Div([
            dcc.Graph(id='edades2')

        ], style={'width': '49%', 'display': 'inline-block'}),



    ], style={'display': 'flex'}),
html.Div([
    html.Button('Descripción', id='btn-nclicks-3', n_clicks=0, style={'width': '240px', 'height': '40px',
                   'cursor': 'pointer', 'border': '0px',
                   'borderRadius': '5px', 'backgroundColor':
                   'black', 'color': 'white', 'textTransform':
                   'uppercase', 'fontSize': '15px'}),
    html.Div(id='container-button-timestamp3')
],style={'textAlign': 'center'}),


html.Div(
    [
        html.I(className="fas fa-question-circle fa-lg", id="target3"),
        dbc.Tooltip("Pie-Chart que muestra el estado conyugal de las personas que participaron en el estudio", target="target3"),
    ],
    className="p-5 text-muted"
),
        # Table container
        html.Div([
            dcc.Graph(id='estado-conyugal')

        ], style={'width': '49%', 'display': 'inline-block'}),
        # Table container
        html.Div([
            dcc.Graph(id='estado-conyugal2')

        ], style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    html.Button('Descripción', id='btn-nclicks-4', n_clicks=0, style={'width': '240px', 'height': '40px',
                   'cursor': 'pointer', 'border': '0px',
                   'borderRadius': '5px', 'backgroundColor':
                   'black', 'color': 'white', 'textTransform':
                   'uppercase', 'fontSize': '15px'}),
    html.Div(id='container-button-timestamp4')
],style={'textAlign': 'center'}),
html.Div([

        # Table container
        html.Div([
            dcc.Graph(id='localidad')

        ], style={'width': '49%', 'display': 'inline-block'}),


        # Graph container
        html.Div([
            dcc.Graph(id='localidad2')

        ], style={'width': '49%', 'display': 'inline-block'}),



    ], style={'display': 'flex'}),
html.Div([
    html.Button('Descripción', id='btn-nclicks-5', n_clicks=0, style={'width': '240px', 'height': '40px',
                   'cursor': 'pointer', 'border': '0px',
                   'borderRadius': '5px', 'backgroundColor':
                   'black', 'color': 'white', 'textTransform':
                   'uppercase', 'fontSize': '15px'}),
    html.Div(id='container-button-timestamp5')
],style={'textAlign': 'center'}),
]),
dcc.Tab(label='Patrones de transporte', children=[
html.Div(
    [
        html.I(className="fas fa-question-circle fa-lg", id="targethisto"),
        dbc.Tooltip("Histograma que muestra la cantidad de personas que usan determinado método de transporte", target="targethisto"),
    ],
    className="p-5 text-muted"
),
html.Div([
    dcc.Graph(id='Preferencia Transporte'),
], style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(id='Preferencia Transportehist'),
], style={'width': '49%', 'display': 'inline-block'}),
html.Div(
    [
        html.I(className="fas fa-question-circle fa-lg", id="targetsun"),
        dbc.Tooltip("Sunburst Graph que muestra la cantidad de personas que usan determinado método de transporte", target="targetsun"),
    ],
    className="p-5 text-muted"
),
html.Div([
    dcc.Graph(id='Preferencia Transporte2'),
], style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(id='Preferencia Transporte3'),
], style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    html.H1("Transmicable")
]),
html.Div([
    dcc.Graph(id='Pie-Cable'),
], style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(id='Pie-Cable2'),
], style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(
        id='dificil'
    )
],style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(
        id='dificil2'
    )
],style={'width': '49%', 'display': 'inline-block'})
    ]),
dcc.Tab(label='Análisis de tiempo', children=[
html.Div(
    [
        html.I(className="fas fa-question-circle fa-lg", id="targetpie"),
        dbc.Tooltip("Pie Chart que muestra la proporción del tiempo promedio de los encuestados en cada lugar", target="targetpie"),
    ],
    className="p-5 text-muted"
),
html.Div([
    dcc.Graph(
        id='pie-chart'
    )
], style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(
        id='pie-chart2'
    )
], style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(
        id='tiempos'
    )
],style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(
        id='tiempos2'
    )
],style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(
        id='tiempos3'
    )
],style={'width': '49%', 'display': 'inline-block'}),
html.Div([
    dcc.Graph(
        id='tiempos4'
    )
],style={'width': '49%', 'display': 'inline-block'}),

    ])
])
])


@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        if btn1 % 2 != 0:
            return html.Br(),html.Div([
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', style={'textAlign': 'center',"border":"1px black solid"})
],style={'width':'80%',"marginLeft": "10%"})
        else:
            return

@app.callback(
    Output('container-button-timestamp2', 'children'),
    Input('btn-nclicks-2', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-2' in changed_id:
        if btn1 % 2 != 0:
            return html.Br(),html.Div([
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', style={'textAlign': 'center',"border":"1px black solid"})
],style={'width':'80%',"marginLeft": "10%"})
        else:
            return

@app.callback(
    Output('container-button-timestamp3', 'children'),
    Input('btn-nclicks-3', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-3' in changed_id:
        if btn1 % 2 != 0:
            return html.Br(),html.Div([
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', style={'textAlign': 'center',"border":"1px black solid"})
],style={'width':'80%',"marginLeft": "10%"})
        else:
            return

@app.callback(
    Output('container-button-timestamp4', 'children'),
    Input('btn-nclicks-4', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-4' in changed_id:
        if btn1 % 2 != 0:
            return html.Br(),html.Div([
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', style={'textAlign': 'center',"border":"1px black solid"})
],style={'width':'80%',"marginLeft": "10%"})
        else:
            return

@app.callback(
    Output('container-button-timestamp5', 'children'),
    Input('btn-nclicks-5', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-5' in changed_id:
        if btn1 % 2 != 0:
            return html.Br(),html.Div([
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', style={'textAlign': 'center',"border":"1px black solid"})
],style={'width':'80%',"marginLeft": "10%"})
        else:
            return


@app.callback([
    Output("localidad", "figure"),
    Output("localidad2", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_localidad(localidad,sex):
    datos = demograficos.sort_values("Género")
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["Zona"] == localidad]
    fig = px.histogram(datos, x="Zona",title = "Número de personas por localidad",color = "Zona",opacity=0.6,
                         color_discrete_sequence=['#32373B',
                                                  '#C83E4D'])
    fig.update_layout(title_x=0.5)
    return fig,fig


# Histograma de sexo
@app.callback([
    Output("sexo", "figure"),
    Output("sexot2", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_sexo(localidad,sex):
    datos = demograficos.sort_values("Género")
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["Zona"] == localidad]
    fig = px.histogram(datos, x="Género",title = "Distribución de Género antes de la pandemia",color = "Género",opacity=0.6,
                         color_discrete_sequence=['#32373B',
                                                  '#C83E4D'])
    fig.update_layout(title_x=0.5,font_family='Tahoma', plot_bgcolor='rgba(67, 129, 193)')
    return fig,fig


@app.callback(
    Output("tiempos", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_sexo3(localidad,sex):
    datos = tiempo_movimiento
    if sex != "Ambos":
        datos = datos[datos["sexo"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["localidad"] == localidad]
    datos = datos.groupby("Tipo").agg({"promedio_semana": "mean"}).reset_index().sort_values("promedio_semana",ascending = False)
    fig = px.bar(datos, x="Tipo",y="promedio_semana",title = "Tiempos promedio por semana por cada tipo de transporte").update_layout(yaxis_title="Tiempo promedio por semana")

    fig.update_layout(title_x=0.5)
    return fig

@app.callback(
    Output("tiempos2", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_sexo4(localidad,sex):
    datos = tiempo_movimiento
    if sex != "Ambos":
        datos = datos[datos["sexo"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["localidad"] == localidad]
    datos = datos.groupby("Tipo").agg({"promedio_semana": "mean"}).reset_index().sort_values("promedio_semana",ascending = False)
    fig = px.bar(datos, x="Tipo",y="promedio_semana",title = "Tiempos promedio por semana por cada tipo de transporte").update_layout(yaxis_title="Tiempo promedio por semana")

    fig.update_layout(title_x=0.5)
    return fig

@app.callback(
    Output("tiempos3", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_sexo5(localidad,sex):
    datos = tiempo_movimiento
    if sex != "Ambos":
        datos = datos[datos["sexo"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["localidad"] == localidad]
    datos = datos.groupby("Tipo").agg({"promedio_semana": "mean"}).reset_index().sort_values("promedio_semana",ascending = False)
    fig = go.Figure(data=[go.Pie(labels=datos["Tipo"], values=datos["promedio_semana"],textinfo='label+percent', hole=.3)])

    fig.update_layout(title_x=0.5)
    return fig

@app.callback(
    Output("tiempos4", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_sexo6(localidad,sex):
    datos = tiempo_movimiento
    if sex != "Ambos":
        datos = datos[datos["sexo"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["localidad"] == localidad]
    datos = datos.groupby("Tipo").agg({"promedio_semana": "mean"}).reset_index().sort_values("promedio_semana",ascending = False)

    fig = go.Figure(data=[go.Pie(labels=datos["Tipo"], values=datos["promedio_semana"],textinfo='label+percent', hole=.3)])
    fig.update_layout(title_x=0.5)
    return fig

@app.callback(
    Output("pie-chart", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_pie_chart(day,sex):
    datos = df2
    if sex != "Ambos":
        datos = datos[df2["sexo"] == sex]
    if day != "Ambos":
        datos = datos[df2["localidad"] == day]
    grupo = datos.groupby('Tipo_total')['mean(TIEMPO_MINUTO)'].mean().to_frame()
    grupo["Porcentaje"] = grupo / grupo.sum()
    grupo = grupo[grupo["Porcentaje"] >= 0.04]
    fig = px.pie(values=grupo["mean(TIEMPO_MINUTO)"], names=grupo.index, title='Tiempo Promedio en Cada Lugar')
    fig.update_layout(title_x=0.5)
    return fig

@app.callback(
    Output("pie-chart2", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_pie_chart2(day,sex):
    datos = df2
    if sex != "Ambos":
        datos = datos[df2["sexo"] == sex]
    if day != "Ambos":
        datos = datos[df2["localidad"] == day]
    grupo = datos.groupby('Tipo_total')['mean(TIEMPO_MINUTO)'].mean().to_frame()
    grupo["Porcentaje"] = grupo / grupo.sum()
    grupo = grupo[grupo["Porcentaje"] >= 0.04]
    fig = px.pie(values= grupo["mean(TIEMPO_MINUTO)"], names=grupo.index, title='Tiempo Promedio en Cada Lugar')
    fig.update_layout(title_x=0.5)
    return fig



#Histograma de edades
@app.callback([
    Output("edades", "figure"),
    Output("edades2", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_edades(localidad,sex):
    datos = demograficos
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["Zona"] == localidad]
    fig = px.histogram(datos, x="Edad",title = "Distribución de las edades",opacity=0.6,color_discrete_sequence=['#32373B'])
    fig.update_layout(title_x=0.5)
    return fig,fig


#Pie de estado conyugal
@app.callback([
    Output("estado-conyugal", "figure"),
    Output("estado-conyugal2", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_estado_conyugal(localidad,sex):
    dic = {1: "Soltero",
           2: "Viudo",
           3: "Casado",
           4: "Unión Libre",
           5: "Divorciado",
           6: "Separado"}
    datos = encuestas
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["T1_localidad"] == localidad]

    fig = px.pie(datos, values=datos["T1_Q12"].value_counts(),
           names=list(map(lambda x: dic[x],datos["T1_Q12"].value_counts().index)), title='Estado Conyugal',opacity=0.7, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(title_x=0.5,font_family='Tahoma')

    return fig,fig

@app.callback([
    Output("ocupacion", "figure"),
    Output("ocupacion2", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def ocupacion(localidad,sex):
    datos = encuestas
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["T1_localidad"] == localidad]
    fig = px.pie(values=datos["T1_Q15"].value_counts(),
                 names= datos["T1_Q15"].value_counts().index, title='Ocupación',opacity=0.7,color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(title_x=0.5)
    return fig,fig

#Histograma preferencia transporte
@app.callback([
    Output("Preferencia Transporte", "figure"),
    Output("Preferencia Transportehist", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_preferencias(localidad,sex):
    dff = encuestas
    if sex != "Ambos":
        dff = dff[dff["Género"] == sex]
    if localidad != "Ambos":
        dff = dff[dff["T1_localidad"] == localidad]
    diccio = {1: "Reducir el tiempo de viaje",
              2: "Mejorar el confort en el vehiculo",
              3: "Mejorar la confiabilidad del horario de llegada del servicio",
              4: "Mejorar la seguridad en el vehiculo",
              5: "Mejorar la seguridad durante la espera en la parada o estación",
              6: "Mejorar la seguridad vial",
              7: "Aumentar la cobertura geografica",
              8: "Aumentar la cobertura horaria",
              9: "Mejorar la frecuencia del servicio",
              10: "Reducir la tarifa",
              11: "Reducir la contaminación",
              12: "No hay nada que mejorar",
              13: "No usa el servicio",
              98: "Otro"}
    diccioAlimen = {1: "Reducir el tiempo de viaje",
                    2: "Mejorar el confort en el vehiculo",
                    3: "Mejorar la confiabilidad del horario de llegada del servicio",
                    4: "Mejorar la seguridad en el vehiculo",
                    5: "Mejorar la seguridad durante la espera en la parada o estación",
                    6: "Mejorar la seguridad vial",
                    7: "Aumentar la cobertura geografica",
                    8: "Aumentar la cobertura horaria",
                    9: "Mejorar la frecuencia del servicio",
                    10: "Reducir la contaminación",
                    11: "No hay nada que mejorar",
                    12: "No usa el servicio",
                    98: "Otro"}

    diccioCable = {1: "Reducir el tiempo de viaje",
                   2: "Mejorar el confort en el vehiculo",
                   3: "Mejorar la confiabilidad del horario de llegada del servicio",
                   4: "Mejorar la seguridad en el vehiculo",
                   5: "Mejorar la seguridad durante la espera en la parada o estación",
                   6: "Mejorar la seguridad vial",
                   7: "Mejorar la facilidad para entrar",
                   8: "Reducir la fila para entrar",
                   9: "Aumentar la cobertura geografica",
                   10: "Aumentar la cobertura horaria",
                   11: "Mejorar la frecuencia del servicio",
                   12: "Reducir la tarifa",
                   13: "Reducir la contaminación",
                   14: "No hay nada que mejorar",
                   15: "No usa el servicio",
                   98: "Otro"}
    dff = dff.replace({"T1_Q36": diccio,"T1_Q37":diccioAlimen,"T1_Q38":diccioCable,"T1_Q39":diccio})
    transmi = dff[["T1_Q36"]].value_counts()
    y_val = (list(map(lambda x: x[0],list(transmi.index))))
    x_val = list(transmi[y_val])

    cable = dff[["T1_Q38"]].value_counts()
    y_val2 = (list(map(lambda x: x[0], list(cable.index))))
    x_val2 = list(cable[y_val2])

    alimenta = dff[["T1_Q37"]].value_counts()
    y_val3 = (list(map(lambda x: x[0], list(alimenta.index))))
    x_val3 = list(alimenta[y_val3])

    sitp = dff[["T1_Q39"]].value_counts()
    y_val4 = (list(map(lambda x: x[0], list(sitp.index))))
    x_val4 = list(sitp[y_val4])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=y_val,
        x=x_val,
        name='Transmilenio',
        orientation='h',
        marker=dict(
            color='rgba(200, 62, 77, 0.6)',
            line=dict(color='rgba(200, 62, 77, 0.6)', width=4)
        )

    ))
    fig.add_trace(go.Bar(
        y=y_val2,
        x=x_val2,
        name='TransMicable',
        orientation='h',
    marker = dict(
        color='rgba(58, 71, 80, 0.6)',
        line=dict(color='rgba(58, 71, 80, 1.0)', width=4)
    )
    ))
    fig.add_trace(go.Bar(
        y=y_val3,
        x=x_val3,
        name='Alimentador',
        orientation='h',
        marker=dict(
            color='rgba(49,163,84, 0.6)',
            line=dict(color='rgba(49,163,84, 0.6)', width=4)
        )
    ))
    fig.add_trace(go.Bar(
        y=y_val4,
        x=x_val4,
        name='SITP',
        orientation='h',
        marker=dict(
            color='rgba(49,130,189, 0.6)',
            line=dict(color='rgba(49,130,189, 0.6)', width=4)
        )
    ))

    fig.update_layout(title_x=0.5)
    fig.update_layout(barmode='stack',yaxis={'categoryorder':'total descending'},
        autosize=False,
        height=700,
        width = 950,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ))
    return fig,fig



@app.callback([
    Output("Preferencia Transporte2", "figure"),
    Output("Preferencia Transporte3", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_preferenciasSun(localidad,sex):
    dff = encuestas
    if sex != "Ambos":
        dff = dff[dff["Género"] == sex]
    if localidad != "Ambos":
        dff = dff[dff["T1_localidad"] == localidad]

    dff = dff.assign(transporte=dff.T1_Q28.str.split(" ")).explode('transporte')
    lista = list(map(str, range(1, 21)))
    dff = dff[dff.transporte.isin(lista)]
    diccio = {}
    publico = ["1", "2", "3", "4", "5", "6", "7", "8","9","10"]
    privado = ["11", "14", "15", "16", "17", "18", "19"]
    otros = ["12", "13", "20"]
    for i in publico:
        diccio[i] = "Transporte Publico"
    for i in privado:
        diccio[i] = "Transporte Privado"
    for i in otros:
        diccio[i] = "Transporte Activo"

    dff["Categoria"] = dff.replace({"transporte": diccio})["transporte"]
    diccio = {"1": "Buses del SITP (azul, naranja o vinotinto",
              "2": "SITP provisionales",
              "3": "Público tradicional (Bus, buseta, Microbus/Colectivo",
              "4": "Transmilenio",
              "5": "Alimentador",
              "6": "TransmiCable",
              "7": "Taxi",
              "8": "Mototaxi/Bicitaxi",
              "9": "Taxi Pirata",
              "10": "Vehiculo Pirata",
              "11": "Transporte especial informal",
              "12": "Bicicleta",
              "13": "Bicicleta con motor",
              "14": "Moto como conductor",
              "15": "Moto como pasajero",
              "16": "Vehiculo privado como conductor",
              "17": "Vehiculo privado como pasajero",
              "18": "Bus privado",
              "19": "Uber",
              "20": "A pie"}
    dff = dff.replace({"transporte": diccio})
    dff["Count"] = 1
    cuenta = dff.groupby("transporte").agg({"id": "count"}).sort_values("id")
    dff = dff[dff["transporte"].isin(cuenta[cuenta.id >= 10].index)]
    fig = px.sunburst(dff, path=['Categoria', 'transporte'], values='Count',color_discrete_sequence=['#32373B','#C83E4D','#4381C1','#59CD90','#D295BF'])
    return fig,fig


@app.callback([
    Output("Pie-Cable", "figure"),
    Output("Pie-Cable2", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def transmicable(localidad,sex):
    dff = encuestas
    if sex != "Ambos":
        dff = dff[dff["Género"] == sex]
    if localidad != "Ambos":
        dff = dff[dff["T1_localidad"] == localidad]

    dff["T1_Q116"] = dff["T1_Q116"].replace({1:"Sí",2:"No"})
    resp = dff["T1_Q116"].value_counts().reset_index().sort_values('index')
    fig = px.pie(resp, values='T1_Q116', names='index', title='¿Ha utilizado el TransMicable?',opacity=0.7,color_discrete_sequence=['#32373B','#C83E4D'])
    return fig,fig

@app.callback([
    Output("dificil", "figure"),
    Output("dificil2", "figure")],
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def dificil(localidad,sex):
    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
              'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
              'rgba(190, 192, 213, 1)','rgba(70, 70, 30, 1)','rgba(120, 120, 213, 1)']
    top_labels = ['Diligencias y tramites', 'Recreación o deporte ', 'Socializar', 'Atención de salud',
                  'Compras y mercado',"Llevar o recoger a alguien","Otro"]

    y_data = ['Buses del SITP (azul, naranja o vinotinto',
     'SITP provisionales',
     'Público tradicional (Bus, buseta, Microbus/Colectivo',
     'Transmilenio',
     'Alimentador',
     'TransmiCable',
     'Taxi',
     'Mototaxi/Bicitaxi',
     'Taxi Pirata',
     'Vehiculo Pirata',
     'Transporte especial informal',
     'Bicicleta',
     'Bicicleta con motor',
     'Moto como conductor',
     'Moto como pasajero',
     'Vehiculo privado como conductor',
     'Vehiculo privado como pasajero',
     'Bus privado',
     'Uber',
     'A pie']

    dff = encuestas
    if sex != "Ambos":
        dff = dff[dff["Género"] == sex]
    if localidad != "Ambos":
        dff = dff[dff["T1_localidad"] == localidad]
    dff = dff[["T1_Q34_1","T1_Q34_2","T1_Q34_3","T1_Q34_4","T1_Q34_5","T1_Q34_6","T1_Q34_7"]]

    diccio = {1: "Buses del SITP (azul, naranja o vinotinto",
              2: "SITP provisionales",
              3: "Público tradicional (Bus, buseta, Microbus/Colectivo",
              4: "Transmilenio",
              5: "Alimentador",
              6: "TransmiCable",
              7: "Taxi",
              8: "Mototaxi/Bicitaxi",
              9: "Taxi Pirata",
              10: "Vehiculo Pirata",
              11: "Transporte especial informal",
              12: "Bicicleta",
              13: "Bicicleta con motor",
              14: "Moto como conductor",
              15: "Moto como pasajero",
              16: "Vehiculo privado como conductor",
              17: "Vehiculo privado como pasajero",
              18: "Bus privado",
              19: "Uber",
              20: "A pie"}
    dff = dff.replace(diccio)
    x_data = []
    for columna in dff.columns:
        agregar = []
        for nombre in diccio.values():
            agregar.append(len(dff[dff[columna] == nombre]))
        x_data.append(agregar)
    #x_data = list(map(lambda x: list(map(lambda y: y / sum(x), x)), x_data))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=list(diccio.values()),
        x=x_data[0],
        name=top_labels[0],
        orientation='h',

    ))
    fig.add_trace(go.Bar(
        y=list(diccio.values()),
        x=x_data[1],
        name=top_labels[1],
        orientation='h',

    ))
    fig.add_trace(go.Bar(
        y=list(diccio.values()),
        x=x_data[2],
        name=top_labels[2],
        orientation='h',

    ))
    fig.add_trace(go.Bar(
        y=list(diccio.values()),
        x=x_data[3],
        name=top_labels[3],
        orientation='h',

    ))
    fig.add_trace(go.Bar(
        y=list(diccio.values()),
        x=x_data[4],
        name=top_labels[4],
        orientation='h',

    ))
    fig.add_trace(go.Bar(
        y=list(diccio.values()),
        x=x_data[5],
        name=top_labels[5],
        orientation='h',

    ))
    fig.add_trace(go.Bar(
        y=list(diccio.values()),
        x=x_data[6],
        name=top_labels[6],
        orientation='h',

    ))


    fig.update_layout(barmode='stack',yaxis={'categoryorder':'total descending'},
        autosize=False,
        height=700,
        width = 950,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ))
    return fig,fig





if __name__ == '__main__':
    app.run_server(debug=True)
