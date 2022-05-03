import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table,callback_context
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import json
import datetime
#df = pd.read_excel('movimientos_acelerometria.xlsx')

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.






# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options




#Lectura de datos de encuestas
#T1

encuestast1 = pd.read_csv("modos_t1_resumido.csv")
#T2
encuestast2 = pd.read_csv("modos_t2_resumido.csv")


#Modos de transporte

#Tiempo movimientos
#tiempo_movimiento = pd.read_excel('tiempo_movimiento.xlsx')

#Incidencias
#incidencias = pd.read_excel("incidencias_lugares.xlsx",sheet_name="incidencias_lugares")

#Tiempo lugares
#tiempo_lugares = pd.read_excel("tiempo_lugares.xlsx")

#Lugares Acerelometria
#lugares_acele = pd.read_excel("lugares_acelerometria.xlsx")
#lugares_acele = lugares_acele[(lugares_acele["PA"] != 'invalid') & (lugares_acele["Tipo_total"] != "Unknown")]

#Locaciones (Lat Lon) acelerometria
#acelerometria = pd.read_excel("movimientos_acelerometria.xlsx")

primeros = pd.read_csv("primeros.csv")
primeros.hora_inicio = primeros.hora_inicio.apply(lambda x: datetime.datetime.strptime(x.split(".")[0], '%H:%M:%S').time())

primerost2 = pd.read_csv("primerosT2.csv")
primerost2.hora_inicio = primerost2.hora_inicio.apply(lambda x: datetime.datetime.strptime(x.split(".")[0], '%H:%M:%S').time())

ultimos = pd.read_csv("ultimos.csv")
ultimos.hora_fin = ultimos.hora_fin.apply(lambda x: datetime.datetime.strptime(x.split(".")[0], '%H:%M:%S').time())

ultimost2 = pd.read_csv("ultimosT2.csv")
ultimost2.hora_fin = ultimost2.hora_fin.apply(lambda x: datetime.datetime.strptime(x.split(".")[0], '%H:%M:%S').time())

localidades = set(pd.read_csv("localidades.csv")["0"])

viajes_promedio = pd.read_csv("viajes_diarios_promedioT1.csv")
viajes_promedioT2 = pd.read_csv("viajes_diarios_promedioT2.csv")

tiempos = pd.read_csv("tiempos_tipo.csv")
tiemposT2 = pd.read_csv("tiempos_tipoT2.csv")

tiempos_viaje = pd.read_csv("tiempo_viajes_T1.csv")
tiempos_viaje.hora_inicio = tiempos_viaje.hora_inicio.apply(lambda x: datetime.datetime.strptime(x.split(".")[0], '%H:%M:%S').time())

tiempos_viajeT2 = pd.read_csv("tiempo_viajes_T2.csv")
tiempos_viajeT2.hora_inicio = tiempos_viajeT2.hora_inicio.apply(lambda x: datetime.datetime.strptime(x.split(".")[0], '%H:%M:%S').time())

with open('bogota.json', 'r') as openfile:
    # Reading from json file
    bog_regions_geo = json.load(openfile)

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
        options=["Hombres","Mujeres","Ambos"],
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
],  style={"width": "30%",'display': 'inline-block',"marginLeft": "5%"})],style={"width": "100%",'position':'fixed','z-index': '999'}),


html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
dcc.Tabs([
        dcc.Tab(label='Datos Demograficos', children=[
html.Div(
    [
        html.I(className="fas fa-question-circle fa-lg", id="target"),
        dbc.Tooltip("Gráfico de barras que muestra la proporción de hombres y mujeres tomados en cuenta en el estudio", target="target"),
    ],
    className="p-5 text-muted"
),

                # Table container
                html.Div([
                    dcc.Graph(id='sexo')

                ]),

html.Div([
    html.Button('Descripción', id='btn-nclicks-1', n_clicks=0, style={'width': '240px', 'height': '40px',
                   'cursor': 'pointer', 'border': '0px',
                   'borderRadius': '5px', 'backgroundColor':
                   'black', 'color': 'white', 'textTransform':
                   'uppercase', 'fontSize': '15px'}),
    html.Div(id='container-button-timestamp')
],style={'textAlign': 'center'}),
html.Div(
    [
        html.I(className="fas fa-question-circle fa-lg", id="target-ocupaciones"),
        dbc.Tooltip("Pie-Chart que muestra las ocupaciones de las personas tomadas en cuenta en el estudio", target="target-ocupaciones"),
    ],
    className="p-5 text-muted"
),
                # Table container
                html.Div([
                    dcc.Graph(id='ocupacion')

                ]),

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
        html.I(className="fas fa-question-circle fa-lg", id="target-localidad"),
        dbc.Tooltip("Histograma que muestra la localidad de las personas tomadas en cuenta en el estudio", target="target-localidad"),
    ],
    className="p-5 text-muted"
),


        # Table container
        html.Div([
            dcc.Graph(id='localidad')

        ]),
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
        dbc.Tooltip("Diagrama de barras apiladas que muestra los principales aspectos a mejorar discriminados por el tipo de transporte", target="targethisto"),
    ],
    className="p-5 text-muted"
),
html.Div([
    dcc.Graph(id='Preferencia Transporte'),
]),
html.Div([
    html.Div(id='viajes-promedio'),
]),
html.Div([
    dcc.RangeSlider(5, 23,1,
               value=[5,9],
               id='my-slider'
               )],style={"width":"50%","marginLeft": "30%"},),

html.Div([
    dcc.Graph(id='mapa-frecuencias'),
]),
html.Div([
    dcc.Graph(id='suma-transporte'),
]),
html.Div([
    dcc.RangeSlider(5, 23,1,
               value=[5,9],
               id='my-slider2'
               )],style={"width":"50%","marginLeft": "30%"},),
html.Div([
    dcc.Graph(id='mapa-tiempos'),
]),

    ]),

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


@app.callback(
    Output("localidad", "figure"),
    [Input("dropdown", "value"),
     Input('dropdown2', 'value')])
def update_localidad(localidad,sex):
    datos1 = encuestast1.copy()
    datos2 = encuestast2.copy()
    if sex != "Ambos":
        datos1 = datos1[datos1["Sexo"] == sex]
        datos2 = datos2[datos2["Sexo"] == sex]

    if localidad != "Ambos":
        datos1 = datos1[datos1["localidad"] == localidad]
        datos2 = datos2[datos2["localidad"] == localidad]
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]], vertical_spacing=0.001)

    datos1 = datos1.groupby("localidad").agg({'localidad':'count'}).sort_index()
    datos2 = datos2.groupby("localidad").agg({'localidad':'count'}).sort_index()


    fig.add_trace(go.Pie(
        labels=datos1.index,
        values=datos1.localidad,
        textinfo='label+percent',
        insidetextorientation='radial',
        name="Antes de la pandemia",
        marker=dict(colors=['rgba(38, 24, 74, 0.8)', 'rgba(49,130,189, 0.8)'], line=dict(color='#000000', width=2)),
    ), 1, 1)
    fig.add_trace(go.Pie(
        labels=datos2.index,
        values=datos2.localidad,
        textinfo='label+percent',
        insidetextorientation='radial',
        name = "Despues de la pandemia",
        marker=dict(colors=['rgba(38, 24, 74, 0.8)', 'rgba(49,130,189, 0.8)'], line=dict(color='#000000', width=2)),
    ), 1, 2)

   # fig.update_layout(title_x=0.5)
    return fig


# Histograma de sexo
@app.callback(
    Output("sexo", "figure"),
    [Input("dropdown", "value"),
     Input('dropdown2', 'value')])
def update_sexo(localidad,sex):
    datos1 = encuestast1.copy()
    datos2 = encuestast2.copy()
    if sex != "Ambos":
        datos1 = datos1[datos1["Sexo"] == sex]
        datos2= datos2[datos2["Sexo"] == sex]

    if localidad != "Ambos":
        datos1 = datos1[datos1["localidad"] == localidad]
        datos2 = datos2[datos2["localidad"] == localidad]
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],vertical_spacing=0.001)

    datos1 = datos1.groupby("Sexo").agg({"Sexo":"count"})
    datos2 = datos2.groupby("Sexo").agg({"Sexo":"count"})

    fig.add_trace(go.Pie(
        labels = datos1.index,
        values = datos1.Sexo,
        textinfo='label+percent',
        insidetextorientation='radial',
        name = "Antes de la pandemia",
        marker=dict(colors=['rgba(38, 24, 74, 0.8)', 'rgba(49,130,189, 0.8)'], line=dict(color='#000000', width=2)),
   ), 1, 1)

    fig.add_trace(go.Pie(
        labels=datos2.index,
        values=datos2.Sexo,
        textinfo='label+percent',
        insidetextorientation='radial',
        name = "Despues de la pandemia",
        marker=dict(colors=['rgba(38, 24, 74, 0.8)', 'rgba(49,130,189, 0.8)'], line=dict(color='#000000', width=2)),
    ), 1, 2)
                        # color_discrete_sequence=['#32373B',   '#C83E4D'])
    #fig.update_layout(title_x=0.5,font_family='Tahoma', plot_bgcolor='rgba(67, 129, 193)')
    return fig

@app.callback(
    Output("ocupacion", "figure"),
    [Input("dropdown", "value"),
     Input('dropdown2', 'value')])
def ocupacion(localidad,sex):
    datos1 = encuestast1.copy()
    datos2 = encuestast2.copy()

    datos1 = datos1[(datos1.T1_Q15 != "888") & (datos1.T1_Q15 != "Otros") ]
    datos2 = datos2[datos2.T2_Q13.isin(datos1.T1_Q15.unique())]

    if sex != "Ambos":
        datos1 = datos1[datos1["Sexo"] == sex]
        datos2 = datos2[datos2["Sexo"] == sex]

    if localidad != "Ambos":
        datos1 = datos1[datos1["localidad"] == localidad]
        datos2 = datos2[datos2["localidad"] == localidad]

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                        shared_yaxes=True, vertical_spacing=0.001)

    datos_x1 = datos1.T1_Q15.value_counts().sort_index()
    datos_x2 = datos2.T2_Q13.value_counts().sort_index()

    fig.add_trace(go.Bar(
        y=datos_x1,
        x=datos_x1.index,
        name='Antes de la pandemia',
        marker=dict(
            color='rgba(38, 24, 74, 0.6)',
            line=dict(color='rgba(38, 24, 74, 1)', width=3)
        )), 1, 1)

    fig.add_trace(go.Bar(
        y=datos_x2,
        x=datos_x2.index,
        name='Despues de la pandemia',
        marker=dict(
            color='rgba(38, 24, 74, 0.6)',
            line=dict(color='rgba(38, 24, 74, 1)', width=3)
        )), 1, 2)
    #fig.update_layout(title_x=0.5)
    return fig

#Histograma preferencia transporte
@app.callback(
    Output("Preferencia Transporte", "figure"),
    [Input("dropdown", "value"),
     Input('dropdown2', 'value')])
def update_preferencias(localidad,sex):

    datos1 = encuestast1.copy()
    datos2= encuestast2.copy()

    if sex != "Ambos":
        datos1 = datos1[datos1["Sexo"] == sex]
        datos2 = datos2[datos2["Sexo"] == sex]

    if localidad != "Ambos":
        datos1 = datos1[datos1["localidad"] == localidad]
        datos2 = datos2[datos2["localidad"] == localidad]

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=True, vertical_spacing=0.001)
    top_labels = ['Public transport', 'Active Transport', 'TransMicable', 'Informal transport', 'Private Transport']
    x_data1 = []
    for nombre in ['Public transport', 'Active Transport', 'TransMicable', 'Informal transport', 'Private Transport']:
        x_data1.append(len(datos1[datos1["modes"] == nombre]))
    x_data1 = list(map(lambda x: x / sum(x_data1), x_data1))

    x_data2 = []
    for nombre in ['Public transport', 'Active Transport', 'TransMicable', 'Informal transport', 'Private Transport']:
        x_data2.append(len(datos2[datos2["modes"] == nombre]))
    x_data2 = list(map(lambda x: x / sum(x_data2), x_data2))


    fig.add_trace(go.Bar(
        y=top_labels,
        x=x_data1,
        name='Antes de la pandemia',
        orientation='h',
        marker=dict(
            color='rgba(38, 24, 74, 0.6)',
            line=dict(color='rgba(38, 24, 74, 1)', width=3)
        )),1,1)

    fig.add_trace(go.Bar(
        y=top_labels,
        x=x_data2,
        name='Despues de la pandemia',
        orientation='h',
        marker=dict(
            color='rgba(49,130,189, 0.6)',
            line=dict(color='rgba(49,130,189, 1)', width=3)
        )), 1, 2)

    return fig


def patrones_movimiento(localidad,sexo,hora):
    data_frame = primeros
    inicio,fin = [datetime.time(num) for num in hora]    #inicio,fin = pd.to_datetime(hora.split(","))
    #print(type(data_frame.hora_inicio.loc[0]))
    #inicio,fin = inicio.time(),fin.time()
    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("dia_inicio")["inicio"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame.reset_index().groupby("inicio").agg({"frecuencia":"mean"})
    data_frame = data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = (data_frame/data_frame.sum()).reset_index()
    figure1 = px.choropleth(data_frame=data_frame,
                            geojson=bog_regions_geo,
                            locations='inicio',
                            featureidkey='properties.LocNombre',
                            # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                            color='frecuencia',  # El color depende de las cantidades
                            color_continuous_scale="Greens"  # greens
                            )
    figure1.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

    data_frame = primerost2
    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("dia_inicio")["inicio"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    figure2 = px.choropleth(data_frame=data_frame,
                            geojson=bog_regions_geo,
                            locations='inicio',
                            featureidkey='properties.LocNombre',
                            # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                            color='frecuencia',  # El color depende de las cantidades
                            color_continuous_scale="Greens"  # greens
                            )
    figure2.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

    return figure1,figure2


@app.callback(
    Output("mapa-frecuencias", "figure"),
    [Input("dropdown", "value"),
     Input('dropdown2', 'value'),
     Input('my-slider', 'value')])
def prueba(localidad,sex,hora):
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "choropleth"}, {"type": "choropleth"}],[{"type": "choropleth"},{"type": "choropleth"}]
        ],
        vertical_spacing=0.075,
        horizontal_spacing=0.08,
        subplot_titles=("Inicio de viajes pre pandemia", "Inicio de viajes post pandemia", "Fin de viajes pre pandemia", "Fin de viajes post pandemia")
    )
    data_frame = primeros
    if sex != "Ambos":
        data_frame = data_frame[data_frame["Sexo"] == sex]
    if localidad != "Ambos":
        data_frame = data_frame[data_frame["localidad"] == localidad]

    inicio, fin = [datetime.time(num) for num in hora]
    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("dia_inicio")["inicio"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    diff = localidades - set(data_frame.inicio)
    data_frame = pd.concat([data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["inicio", "frecuencia"])])

    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.inicio,
        z=data_frame['frecuencia'],
        colorscale=['rgb(255,255,255)', "rgba(38, 24, 74, 1)"],
        colorbar_title="Viajes",
        zmin=data_frame['frecuencia'].min(),
        zmax=data_frame['frecuencia'].max(),
        name='Viajes iniciados pre pandemia',
        hoverinfo='location+z',
        showlegend=False,
        showscale=False,
    ), row=1, col=1)

    data_frame = primerost2
    if sex != "Ambos":
        data_frame = data_frame[data_frame["Sexo"] == sex]
    if localidad != "Ambos":
        data_frame = data_frame[data_frame["localidad"] == localidad]
    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("dia_inicio")["inicio"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame = data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    diff = localidades - set(data_frame.inicio)
    data_frame = pd.concat([data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["inicio", "frecuencia"])])
    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.inicio,
        z=data_frame['frecuencia'],
        colorscale=['rgb(255,255,255)', "rgba(38, 24, 74, 1)"],
        colorbar_title="Viajes",
        zmin=data_frame['frecuencia'].min(),
        zmax=data_frame['frecuencia'].max(),
        name='Viajes iniciados post pandemia',
        hoverinfo='location+z',

    ), row=1, col=2)

    data_frame = ultimos
    if sex != "Ambos":
        data_frame = data_frame[data_frame["Sexo"] == sex]
    if localidad != "Ambos":
        data_frame = data_frame[data_frame["localidad"] == localidad]
    inicio, fin = [datetime.time(num) for num in hora]
    data_frame = data_frame[(data_frame.hora_fin >= inicio) & (data_frame.hora_fin <= fin)]
    data_frame = data_frame.groupby("dia_fin")["fin"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame = data_frame.reset_index().groupby("fin").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    diff = localidades - set(data_frame.fin)
    data_frame = pd.concat([data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["fin", "frecuencia"])])
    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.fin,
        z=data_frame['frecuencia'],
        colorscale=['rgb(255,255,255)', "rgba(38, 24, 74, 1)"],
        colorbar_title="Viajes",
        zmin=data_frame['frecuencia'].min(),
        zmax=data_frame['frecuencia'].max(),
        name='Pre pandemia',
        hoverinfo='location+z',
        showlegend=False,
        showscale=False,

    ), row=2, col=1)
    data_frame = ultimost2
    if sex != "Ambos":
        data_frame = data_frame[data_frame["Sexo"] == sex]
    if localidad != "Ambos":
        data_frame = data_frame[data_frame["localidad"] == localidad]
    data_frame = data_frame[(data_frame.hora_fin >= inicio) & (data_frame.hora_fin <= fin)]
    data_frame = data_frame.groupby("dia_fin")["fin"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame = data_frame.reset_index().groupby("fin").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    diff = localidades - set(data_frame.fin)
    data_frame = pd.concat([data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["fin", "frecuencia"])])
    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.fin,
        z=data_frame['frecuencia'],
        colorscale=['rgb(255,255,255)', "rgba(38, 24, 74, 1)"],
        colorbar_title="Viajes",
        zmin=data_frame['frecuencia'].min(),
        zmax=data_frame['frecuencia'].max(),
        name='Post pandemia',
        hoverinfo='location+z',
        showlegend=False,
        showscale=False,

    ), row=2, col=2)
    fig.update_geos(fitbounds="locations",
                    visible=False,
                    )
    hovertemp = '<i>Localidad:</i> %{location} <br>'
    hovertemp += '<i>Porcentaje:</i> %{z:,}'
    fig.update_traces(hovertemplate=hovertemp)
    fig.update_layout(
        title='Porcentaje de personas que inician o terminan un viaje en una localidad especifica dada la hora', title_x=0.5,height =1000)

    return fig




@app.callback(
    Output("viajes-promedio", "children"),
    [Input("dropdown", "value"),
     Input('dropdown2', 'value')])
def viajes_prom(localidad,sex):
    datos1 = viajes_promedio.copy()
    datos2 = viajes_promedioT2.copy()

    if sex != "Ambos":
        datos1 = datos1[datos1["Sexo"] == sex]
        datos2 = datos2[datos2["Sexo"] == sex]

    if localidad != "Ambos":
        datos1 = datos1[datos1["localidad"] == localidad]
        datos2 = datos2[datos2["localidad"] == localidad]

    viajest1 = datos1.viaje.mean()
    viajest2 = datos2.viaje.mean()
    return html.Div([
        html.Div([
            html.H2("En promedio una persona hace ", style={"textAlign": "center"}),
            html.Br(),
            html.H1(str(round(viajest1, 2)), style={"textAlign": "center", "color": "rgba(38, 24, 74, 1)"}),
            html.H2(" viajes al día", style={"textAlign": "center"})
        ], style={"width": "49%", "display": "inline-block"}),
        html.Div([
            html.H2("En promedio una persona hace ",style = {"textAlign":"center"}) ,
            html.Br(),
            html.H1(str(round(viajest2,2)),style = {"textAlign":"center","color":"rgba(49,130,189, 1)"}) ,
            html.H2(" viajes al día",style = {"textAlign":"center"})
        ],style={"width":"49%","display":"inline-block"}),
    ],style={"display":"flex"})

@app.callback(
    Output("suma-transporte", "figure"),
    [Input("dropdown", "value"),
     Input('dropdown2', 'value')])
def suma_transporte(localidad,sex):
    datos1 = tiempos.copy()
    datos2 = tiemposT2.copy()

    if sex != "Ambos":
        datos1 = datos1[datos1["Sexo"] == sex]
        datos2 = datos2[datos2["Sexo"] == sex]

    if localidad != "Ambos":
        datos1 = datos1[datos1["localidad"] == localidad]
        datos2 = datos2[datos2["localidad"] == localidad]

    datos1 = datos1.groupby(["fecha","movimiento"]).agg({"minutos":"sum"}).reset_index().groupby("movimiento").agg({"minutos":"mean"})
    datos2 = datos2.groupby(["fecha","movimiento"]).agg({"minutos":"sum"}).reset_index().groupby("movimiento").agg({"minutos":"mean"})

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=True, vertical_spacing=0.001)

    fig.add_trace(go.Bar(
        y=datos1.index,
        x=datos1.minutos,
        name='Antes de la pandemia',
        orientation='h',
        marker=dict(
            color='rgba(38, 24, 74, 0.6)',
            line=dict(color='rgba(38, 24, 74, 1)', width=3)
        )),1,1)

    fig.add_trace(go.Bar(
        y=datos2.index,
        x=datos2.minutos,
        name='Despues de la pandemia',
        orientation='h',
        marker=dict(
            color='rgba(49,130,189, 0.6)',
            line=dict(color='rgba(49,130,189, 1)', width=3)
        )), 1, 2)

    return fig

@app.callback(
    Output("mapa-tiempos", "figure"),
    [Input("dropdown", "value"),
     Input('dropdown2', 'value'),
     Input('my-slider2', 'value')])
def ultimo_mapa(localidad,sex,hora):
    fig = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "choropleth"}, {"type": "choropleth"}]
        ],
        vertical_spacing=0.075,
        horizontal_spacing=0.08,
        subplot_titles=("Inicio de viajes pre pandemia", "Inicio de viajes post pandemia")
    )
    data_frame = tiempos_viaje.copy()
    if sex != "Ambos":
        data_frame = data_frame[data_frame["Sexo"] == sex]
    if localidad != "Ambos":
        data_frame = data_frame[data_frame["localidad"] == localidad]
        data_frame = data_frame[data_frame["inicio"] == localidad.upper()]

    inicio, fin = [datetime.time(num) for num in hora]
    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("fin").agg({"tiempo_viaje_minutos":"mean"})
    data_frame = data_frame.reset_index()
    diff = localidades - set(data_frame.fin)
    data_frame = pd.concat([data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["fin", "tiempo_viaje_minutos"])])

    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.fin,
        z=data_frame['tiempo_viaje_minutos'],
        colorscale=['rgb(255,255,255)', "rgba(38, 24, 74, 1)"],
        colorbar_title="Minutos",
        zmin=data_frame['tiempo_viaje_minutos'].min(),
        zmax=data_frame['tiempo_viaje_minutos'].max(),
        name='Minutos de viaje pre pandemia',
        hoverinfo='location+z',

    ), row=1, col=1)

    data_frame = tiempos_viajeT2.copy()
    if sex != "Ambos":
        data_frame = data_frame[data_frame["Sexo"] == sex]
    if localidad != "Ambos":
        data_frame = data_frame[data_frame["localidad"] == localidad]
        data_frame = data_frame[data_frame["inicio"] == localidad.upper()]

    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("fin").agg({"tiempo_viaje_minutos": "mean"})
    data_frame = data_frame.reset_index()
    diff = localidades - set(data_frame.fin)
    data_frame = pd.concat(
        [data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["fin", "tiempo_viaje_minutos"])])
    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.fin,
        z=data_frame['tiempo_viaje_minutos'],
        colorscale=['rgb(255,255,255)', "rgba(38, 24, 74, 1)"],
        colorbar_title="Minutos",
        zmin=data_frame['tiempo_viaje_minutos'].min(),
        zmax=data_frame['tiempo_viaje_minutos'].max(),
        name='Minutos de viaje post pandemia',
        hoverinfo='location+z',
        showlegend=False,
        showscale=False,

    ), row=1, col=2)


    fig.update_geos(fitbounds="locations",
                    visible=False,
                    )
    hovertemp = '<i>Localidad:</i> %{location} <br>'
    hovertemp += '<i>Minutos promedio:</i> %{z:,}'
    fig.update_traces(hovertemplate=hovertemp)
    fig.update_layout(
        title='Porcentaje de personas que inician o terminan un viaje en una localidad especifica dada la hora', title_x=0.5,height = 1000)

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
