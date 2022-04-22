import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

df = pd.read_excel('movimientos_acelerometria.xlsx')

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



diccio = {1:"Trabajando",2:"No trabajó pero tenía trabajo",3:"Buscando trabajo",4:"Estudiando",5:"Oficios del hogar",6:"Incapacitado permanente"}
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
                external_scripts=external_scripts,
                external_stylesheets= [dbc.themes.BOOTSTRAP, FONT_AWESOME])


app.layout =html.Div([


    html.Div([
        html.H3(children = 'Escoja la localidad a visualizar'),
dcc.Dropdown(
        id="dropdown",
        options=["Ciudad Bolivar","San Cristobal","Ambos"],
        value="Ciudad Bolivar",
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
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', style={'textAlign': 'center','backgroundColor':'#F9F9F9',"border":"1px black solid"})
],style={'width':'50%',"marginLeft": "25%"}),
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
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', style={'textAlign': 'center','backgroundColor':'#F9F9F9',"border":"1px black solid"})
],style={'width':'50%',"marginLeft": "25%"}),
    html.Div([
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


    ], style={'display': 'flex'}),
html.Div([
    html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', style={'textAlign': 'center','backgroundColor':'#F9F9F9',"border":"1px black solid"})
],style={'width':'50%',"marginLeft": "25%"}),
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
],style={'width': '49%', 'display': 'inline-block'})
    ])
])
])



# Histograma de sexo
@app.callback(
    Output("sexo", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_sexo(localidad,sex):
    datos = demograficos.sort_values("Género")
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["Zona"] == localidad]
    fig = px.histogram(datos, x="Género",title = "Distribución de Género antes de la pandemia",color = "Género")
    fig.update_layout(title_x=0.5)
    return fig

@app.callback(
    Output("sexot2", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_sexo2(localidad,sex):
    datos = demograficos.sort_values("Género")
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["Zona"] == localidad]
    fig = px.histogram(datos, x="Género",title = "Distribución de Género despues de la pandemia",color = "Género")
    fig.update_layout(title_x=0.5)
    return fig

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
    fig = px.bar(datos, x="Tipo",y="promedio_semana",title = "Tiempos promedio por semana por cada tipo de transporte").update_layout(yaxis_title="Tiempo promedi por semana")

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
@app.callback(
    Output("edades", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_edades(localidad,sex):
    datos = demograficos
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["Zona"] == localidad]
    fig = px.histogram(datos, x="Edad",title = "Distribución de las edades")
    fig.update_layout(title_x=0.5)
    return fig

#Histograma de edades
@app.callback(
    Output("edades2", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_edades2(localidad,sex):
    datos = demograficos
    if sex != "Ambos":
        datos = datos[datos["Género"] == sex]
    if localidad != "Ambos":
        datos = datos[datos["Zona"] == localidad]
    fig = px.histogram(datos, x="Edad",title = "Distribución de las edades")
    fig.update_layout(title_x=0.5)
    return fig


#Pie de estado conyugal
@app.callback(
    Output("estado-conyugal", "figure"),
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
           names=list(map(lambda x: dic[x],datos["T1_Q12"].value_counts().index)), title='Estado Conyugal')
    fig.update_layout(title_x=0.5)
    return fig

#Pie de estado conyugal
@app.callback(
    Output("estado-conyugal2", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_estado_conyugal2(localidad,sex):
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
                 names=list(map(lambda x: dic[x], datos["T1_Q12"].value_counts().index)), title='Estado Conyugal')
    fig.update_layout(title_x=0.5)
    return fig


#Histograma preferencia transporte
@app.callback(
    Output("Preferencia Transporte", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_preferencias(localidad,sex):
    #mask = (encuestas["T1_localidad"] == localidad) & (encuestas['Género'] == sex) & (encuestas["T1_Q15"].isin(list(ocupacion)))
    dff = encuestas
    if sex != "Ambos":
        dff = dff[dff["Género"] == sex]
    if localidad != "Ambos":
        dff = dff[dff["T1_localidad"] == localidad]

    dff = dff.assign(transporte=dff.T1_Q28.str.split(" ")).explode('transporte')
    lista = list(map(str, range(1, 21)))
    dff = dff[dff.transporte.isin(lista)]
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
    fig = px.histogram(dff, x="transporte",title = "Cantidad de personas por tipo de transporte",labels={'transporte':'Tipo de transporte'}).update_xaxes(categoryorder='total ascending')
    fig.update_layout(title_x=0.5)
    return fig

#Histograma preferencia transporte
@app.callback(
    Output("Preferencia Transportehist", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_preferencias2(localidad,sex):
    #mask = (encuestas["T1_localidad"] == localidad) & (encuestas['Género'] == sex) & (encuestas["T1_Q15"].isin(list(ocupacion)))
    dff = encuestas
    if sex != "Ambos":
        dff = dff[dff["Género"] == sex]
    if localidad != "Ambos":
        dff = dff[dff["T1_localidad"] == localidad]

    dff = dff.assign(transporte=dff.T1_Q28.str.split(" ")).explode('transporte')
    lista = list(map(str, range(1, 21)))
    dff = dff[dff.transporte.isin(lista)]
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
    fig = px.histogram(dff, x="transporte",title = "Cantidad de personas por tipo de transporte",labels={'transporte':'Tipo de transporte'}).update_xaxes(categoryorder='total ascending')
    fig.update_layout(title_x=0.5)
    return fig



@app.callback(
    Output("Preferencia Transporte2", "figure"),
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
    publico = ["1", "2", "3", "4", "5", "6", "7", "8"]
    privado = ["9", "10", "11", "14", "15", "16", "17", "18", "19"]
    otros = ["12", "13", "20"]
    for i in publico:
        diccio[i] = "Transporte Publico"
    for i in privado:
        diccio[i] = "Transporte Privado"
    for i in otros:
        diccio[i] = "Otros"
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
    fig = px.sunburst(dff, path=['Categoria', 'transporte'], values='Count')
    return fig


@app.callback(
    Output("Preferencia Transporte3", "figure"),
    [Input("dropdown", "value")], Input('dropdown2', 'value'))
def update_preferenciasSun2(localidad,sex):
    dff = encuestas
    if sex != "Ambos":
        dff = dff[dff["Género"] == sex]
    if localidad != "Ambos":
        dff = dff[dff["T1_localidad"] == localidad]

    dff = dff.assign(transporte=dff.T1_Q28.str.split(" ")).explode('transporte')
    lista = list(map(str, range(1, 21)))
    dff = dff[dff.transporte.isin(lista)]
    diccio = {}
    publico = ["1", "2", "3", "4", "5", "6", "7", "8"]
    privado = ["9", "10", "11", "14", "15", "16", "17", "18", "19"]
    otros = ["12", "13", "20"]
    for i in publico:
        diccio[i] = "Transporte Publico"
    for i in privado:
        diccio[i] = "Transporte Privado"
    for i in otros:
        diccio[i] = "Otros"
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
    fig = px.sunburst(dff, path=['Categoria', 'transporte'], values='Count')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

