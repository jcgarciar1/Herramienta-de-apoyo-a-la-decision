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



colors_pie = ['rgba(66, 0, 57, 0.8)', 'rgba(216, 30, 91, 0.8)']
colors =["rgba(66, 0, 57, 0.8)","rgba(66, 0, 57, 1)",'rgba(216, 30, 91, 0.8)', 'rgba(216, 30, 91, 1)']


porcentaje = "100%"

horas = {0:(datetime.time(0,0,0),datetime.time(5,0,0)) ,
         1:(datetime.time(5,0,0),datetime.time(9,0,0)) ,
         2:(datetime.time(9,0,0),datetime.time(13,0,0)),
         3:(datetime.time(13,0,0),datetime.time(17,0,0)),
         4:(datetime.time(17,0,0),datetime.time(21,0,0)),
         5:(datetime.time(21,0,0),datetime.time(23,59,59))}
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

tiempos = tiempos[tiempos.movimiento != "UNKNOWN"]
tiemposT2 = tiemposT2[tiemposT2.movimiento != "UNKNOWN"]



tiempos_viaje = pd.read_csv("tiempo_viajes_T1.csv")
tiempos_viaje.hora_inicio = tiempos_viaje.hora_inicio.apply(lambda x: datetime.datetime.strptime(x.split(".")[0], '%H:%M:%S').time())
tiempos_viaje.tiempo_viaje_minutos = tiempos_viaje.tiempo_viaje_minutos.apply(lambda x: round(x,2))

tiempos_viajeT2 = pd.read_csv("tiempo_viajes_T2.csv")
tiempos_viajeT2.hora_inicio = tiempos_viajeT2.hora_inicio.apply(lambda x: datetime.datetime.strptime(x.split(".")[0], '%H:%M:%S').time())
tiempos_viajeT2.tiempo_viaje_minutos = tiempos_viajeT2.tiempo_viaje_minutos.apply(lambda x: round(x,2))


with open('bogota.json', 'r') as openfile:
    # Reading from json file
    bog_regions_geo = json.load(openfile)


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
external_stylesheets = [dbc.themes.BOOTSTRAP]


FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

app = Dash(__name__,
                external_stylesheets= [dbc.themes.BOOTSTRAP, FONT_AWESOME],
           suppress_callback_exceptions = True)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Muévelo", className="display-4"),
        html.Hr(),
        html.P(
            "Visualización de datos del proyecto Muévelo", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Introducción", href="/", active="exact"),
                dbc.NavLink("Datos demográficos", href="/page-1", active="exact"),
                dbc.NavLink("Patrones de transporte", href="/page-2", active="exact"),
                dbc.NavLink("Mapas", href="/page-3", active="exact"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [

        ]
    elif pathname == "/page-1":
        return [
            dbc.Row(
                dbc.Col(html.H2(children=["Distribución de género \t",
                                          html.I(className="fas fa-info-circle fa-xs", id="target",
                                                 style={"color": "black"})], style={"textAlign": "center"}),
                        style={"align": "end"}),
                justify="end"
            ),
            dbc.Tooltip("Pie Chart que muestra la proporción de hombres y mujeres tomados en cuenta en el estudio",
                        target="target"),
            html.Center(html.Div([

                html.Div([
                    html.H5(children='Escoja la localidad a visualizar'),
                    dcc.Checklist(
                        id="dropdown-sexo-localidad",
                        options=["Ciudad Bolivar", "San Cristobal"],
                        value=["Ciudad Bolivar", "San Cristobal"],
                        inline=True,
                        inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                ]),

                # Table container
                html.Div([
                    dcc.Graph(id='sexo')

                ]),
                html.Div([
                    html.Button('Descripción', id='btn-nclicks-1', n_clicks=0,
                                style={'width': '240px', 'height': '40px',
                                       'cursor': 'pointer', 'border': '0px',
                                       'borderRadius': '5px', 'backgroundColor':
                                           'black', 'color': 'white', 'textTransform':
                                           'uppercase', 'fontSize': '15px'}),
                    html.Div(id='container-button-timestamp')
                ], style={'textAlign': 'center'}),
                html.Br()
            ], style={"width": porcentaje}, className="shadow-lg p-3 mb-5 bg-white rounded")),
            dbc.Row(
                dbc.Col(html.H2(children=["Ocupación de los participantes \t",
                                          html.I(className="fas fa-info-circle fa-xs", id="target-ocupaciones",
                                                 style={"color": "black"})], style={"textAlign": "center"}),
                        style={"align": "end"}),
                justify="end"
            ),
            dbc.Tooltip(
                "Diagrama de barras que muestra las ocupaciones de las personas tomadas en cuenta en el estudio",
                target="target-ocupaciones"),

            html.Center(
                html.Div([
                    html.Div([

                        html.Div([
                            html.H5(children='Escoja la localidad a visualizar'),
                            dcc.Checklist(
                                id="dropdown-ocupacion-localidad",
                                options=["Ciudad Bolivar", "San Cristobal"],
                                value=["Ciudad Bolivar", "San Cristobal"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ]),

                        html.Div([
                            html.H5(children='Escoja el sexo a visualizar'),
                            dcc.Checklist(
                                id="dropdown-ocupacion-sexo",
                                options=["Hombres", "Mujeres"],
                                value=["Hombres", "Mujeres"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ], style={"marginLeft": "5%"})], className="d-flex justify-content-center"),

                    # Table container
                    html.Div([
                        dcc.Graph(id='ocupacion')

                    ]),
                    html.Br(),
                    html.Div([
                        html.Button('Descripción', id='btn-nclicks-3', n_clicks=0,
                                    style={'width': '240px', 'height': '40px',
                                           'cursor': 'pointer', 'border': '0px',
                                           'borderRadius': '5px', 'backgroundColor':
                                               'black', 'color': 'white', 'textTransform':
                                               'uppercase', 'fontSize': '15px'}),
                        html.Div(id='container-button-timestamp3')
                    ], style={'textAlign': 'center'}),
                    html.Br()

                ], style={"width": "100%"}, className="shadow-lg p-3 mb-5 bg-white rounded")),
            dbc.Row(
                dbc.Col(html.H2(children=["Distribución de personas por localidad \t",
                                          html.I(className="fas fa-info-circle fa-xs", id="target-localidad",
                                                 style={"color": "black"})], style={"textAlign": "center"}),
                        style={"align": "end"}),
                justify="end"
            ),
            dbc.Tooltip("Pie Chart que muestra la localidad de las personas tomadas en cuenta en el estudio",
                        target="target-localidad"),
            html.Center(html.Div([

                html.Div([
                    html.H5(children='Escoja la localidad a visualizar'),
                    dcc.Checklist(
                        id="dropdown-localidad-sexo",
                        options=["Hombres", "Mujeres"],
                        value=["Hombres", "Mujeres"],
                        inline=True,
                        inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                ]),

                # Table container
                html.Div([
                    dcc.Graph(id='localidad',)

                ]),
                html.Div([
                    html.Button('Descripción', id='btn-nclicks-5', n_clicks=0,
                                style={'width': '240px', 'height': '40px',
                                       'cursor': 'pointer', 'border': '0px',
                                       'borderRadius': '5px', 'backgroundColor':
                                           'black', 'color': 'white', 'textTransform':
                                           'uppercase', 'fontSize': '15px'}),
                    html.Div(id='container-button-timestamp5')
                ], style={'textAlign': 'center'}),
                html.Br()
            ], style={"width": "100%"}, className="shadow-lg p-3 mb-5 bg-white rounded")),

        ]
    elif pathname == "/page-2":
        return [
            dbc.Row(
                dbc.Col(html.H2(children=["Viajes promedio por persona \t",
                                          html.I(className="fas fa-info-circle fa-xs", id="texto_viajes",
                                                 style={"color": "black"})], style={"textAlign": "center"}),
                        style={"align": "end"}),
                justify="end"
            ),
            dbc.Tooltip("Se muestra la cantidad de viajes que una persona realiza en promedio al día",
                        target="texto_viajes"),

            html.Center(
                html.Div([
                    html.Div([

                        html.Div([
                            html.H5(children='Escoja la localidad a visualizar'),
                            dcc.Checklist(
                                id="dropdown-texto-localidad",
                                options=["Ciudad Bolivar", "San Cristobal"],
                                value=["Ciudad Bolivar", "San Cristobal"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ]),

                        html.Div([
                            html.H5(children='Escoja el sexo a visualizar'),
                            dcc.Checklist(
                                id="dropdown-texto-sexo",
                                options=["Hombres", "Mujeres"],
                                value=["Hombres", "Mujeres"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ], style={"marginLeft": "5%"})], className="d-flex justify-content-center"),
                    html.Br(),
                    html.Br(),

                    # Table container
                    html.Div(id='viajes-promedio'),
                    html.Br(),
                    # html.Div([
                    #   html.Button('Descripción', id='btn-nclicks-3', n_clicks=0, style={'width': '240px', 'height': '40px',
                    #        'cursor': 'pointer', 'border': '0px',
                    #       'borderRadius': '5px', 'backgroundColor':
                    #      'black', 'color': 'white', 'textTransform':
                    #     'uppercase', 'fontSize': '15px'}),
                    #  html.Div(id='container-button-timestamp3')
                    # ],style={'textAlign': 'center'}),
                    html.Br(),

                ], style={"width": "100%"}, className="shadow-lg p-3 mb-5 bg-white rounded")),

            dbc.Row(
                dbc.Col(html.H2(children=["Porcentaje de personas que prefieren un tipo de transporte \t",
                                          html.I(className="fas fa-info-circle fa-xs", id="target-preferencia",
                                                 style={"color": "black"})], style={"textAlign": "center"}),
                        style={"align": "end"}),
                justify="end"
            ),
            dbc.Tooltip(
                "Diagrama de barras que muestra el porcentaje de personas que prefieren un tipo de transporte especifico para ir a su actividad principal",
                target="target-preferencia"),
            html.Center(
                html.Div([
                    html.Div([

                        html.Div([
                            html.H5(children='Escoja la localidad a visualizar'),
                            dcc.Checklist(
                                id="dropdown-preferido-localidad",
                                options=["Ciudad Bolivar", "San Cristobal"],
                                value=["Ciudad Bolivar", "San Cristobal"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ]),

                        html.Div([
                            html.H5(children='Escoja el sexo a visualizar'),
                            dcc.Checklist(
                                id="dropdown-preferido-sexo",
                                options=["Hombres", "Mujeres"],
                                value=["Hombres", "Mujeres"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ], style={"marginLeft": "5%"})], className="d-flex justify-content-center"),

                    # Table container
                    html.Div([
                        dcc.Graph(id='Preferencia Transporte')

                    ]),
                    html.Br(),
                    # html.Div([
                    # html.Button('Descripción', id='btn-nclicks-3', n_clicks=0, style={'width': '240px', 'height': '40px',
                    #              'cursor': 'pointer', 'border': '0px',
                    #             'borderRadius': '5px', 'backgroundColor':
                    #            'black', 'color': 'white', 'textTransform':
                    #           'uppercase', 'fontSize': '15px'}),
                    # html.Div(id='container-button-timestamp3')
                    # ],style={'textAlign': 'center'}),
                    html.Br()

                ], style={"width": "100%"}, className="shadow-lg p-3 mb-5 bg-white rounded")),

            dbc.Row(
                dbc.Col(html.H2(children=["Minutos diarios promedio por medio de transporte \t",
                                          html.I(className="fas fa-info-circle fa-xs", id="target-minutos",
                                                 style={"color": "black"})], style={"textAlign": "center"}),
                        style={"align": "end"}),
                justify="end"
            ),
            dbc.Tooltip(
                "Diagrama de barras que muestra los minutos promedios diarios por tipo de transporte",
                target="target-minutos"),

            html.Center(
                html.Div([
                    html.Div([

                        html.Div([
                            html.H5(children='Escoja la localidad a visualizar'),
                            dcc.Checklist(
                                id="dropdown-suma1-localidad",
                                options=["Ciudad Bolivar", "San Cristobal"],
                                value=["Ciudad Bolivar", "San Cristobal"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ]),

                        html.Div([
                            html.H5(children='Escoja el sexo a visualizar'),
                            dcc.Checklist(
                                id="dropdown-suma1-sexo",
                                options=["Hombres", "Mujeres"],
                                value=["Hombres", "Mujeres"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ], style={"marginLeft": "5%"})], className="d-flex justify-content-center"),

                    # Table container
                    html.Div([
                        dcc.Graph(id='suma-transporte')

                    ]),
                    html.Br(),
                    # html.Div([
                    # html.Button('Descripción', id='btn-nclicks-3', n_clicks=0, style={'width': '240px', 'height': '40px',
                    #              'cursor': 'pointer', 'border': '0px',
                    #             'borderRadius': '5px', 'backgroundColor':
                    #            'black', 'color': 'white', 'textTransform':
                    #           'uppercase', 'fontSize': '15px'}),
                    #  html.Div(id='container-button-timestamp3')
                    # ],style={'textAlign': 'center'}),
                    html.Br()

                ], style={"width": "100%"}, className="shadow-lg p-3 mb-5 bg-white rounded")),

        ]
    elif pathname == "/page-3":
        return [
            dbc.Row(
                dbc.Col(html.H2(children=["Porcentaje de personas iniciando o terminando un viaje \t",
                                          html.I(className="fas fa-info-circle fa-xs", id="target-mapa-salidas",
                                                 style={"color": "black"})], style={"textAlign": "center"}),
                        style={"align": "end"}),
                justify="end"
            ),
            dbc.Tooltip(
                "Mapa de calor que muestra la cantidad de personas que estan iniciando o terminando un viaje en una determinada localidad dado el sexo y la localidad a la que pertenecen",
                target="target-mapa-salidas"),

            html.Center(
                html.Div([
                    html.Div([

                        html.Div([
                            html.H5(children='Escoja la localidad de las personas que inician o terminan el viaje'),
                            dcc.Checklist(
                                id="dropdown-mapa-localidad",
                                options=["Ciudad Bolivar", "San Cristobal"],
                                value=["Ciudad Bolivar", "San Cristobal"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ]),

                        html.Div([
                            html.H5(children='Escoja el sexo a visualizar'),
                            dcc.Checklist(
                                id="dropdown-mapa-sexo",
                                options=["Hombres", "Mujeres"],
                                value=["Hombres", "Mujeres"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ], style={"marginLeft": "5%"})], className="d-flex justify-content-center"),
                    html.Br(),
                    html.H5(children='Escoja el intervalo de tiempo',
                            style={"width": "30%", 'display': 'inline-block', "marginLeft": "5%"}),
                    html.Div([
                        dcc.Slider(0, 5, step=None,
                                   marks={
                                       0: '12AM-5AM',
                                       1: '5AM-9AM',
                                       2: '9AM-1PM',
                                       3: '1PM-5PM',
                                       4: '5PM-9PM',
                                       5: '9PM-12AM'
                                   },
                                   value=0,
                                   id='my-slider')], style={"width": "60%", "marginLeft": "0%"}),
                    html.Br(),
                    # Table container
                    dcc.Loading(
                        id='loading2',
                        children=[html.Div([
                            dcc.Graph(id='mapa-frecuencias')

                        ])],
                        type="circle"),
                    html.Br(),
                    # html.Div([
                    #   html.Button('Descripción', id='btn-nclicks-3', n_clicks=0, style={'width': '240px', 'height': '40px',
                    #                 'cursor': 'pointer', 'border': '0px',
                    #                'borderRadius': '5px', 'backgroundColor':
                    #               'black', 'color': 'white', 'textTransform':
                    #              'uppercase', 'fontSize': '15px'}),
                    # html.Div(id='container-button-timestamp3')
                    # ],style={'textAlign': 'center'}),
                    html.Br()

                ], style={"width": "100%"}, className="shadow-lg p-3 mb-5 bg-white rounded")),
            dbc.Row(
                dbc.Col(html.H2(
                    children=["Tiempo promedio en minutos a cada localidad saliendo de una localidad especifica \t",
                              html.I(className="fas fa-info-circle fa-xs", id="target-mapa-horas",
                                     style={"color": "black"})], style={"textAlign": "center"}),
                        style={"align": "end"}),
                justify="end"
            ),
            dbc.Tooltip(
                "Mapas de calor que muestran el tiempo promedio en minutos que una persona se demora saliendo de Ciudad Bolivar, San Cristobal o ambas a otras localidades",
                target="target-mapa-horas"),

            html.Center(
                html.Div([
                    html.Div([

                        html.Div([
                            html.H5(children='Escoja la localidad desde la que inicia el viaje'),
                            dcc.Checklist(
                                id="dropdown-mapa2-localidad",
                                options=["Ciudad Bolivar", "San Cristobal"],
                                value=["Ciudad Bolivar", "San Cristobal"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ]),

                        html.Div([
                            html.H5(children='Escoja el sexo a visualizar'),
                            dcc.Checklist(
                                id="dropdown-mapa2-sexo",
                                options=["Hombres", "Mujeres"],
                                value=["Hombres", "Mujeres"],
                                inline=True,
                                inputStyle={"margin-right": "5px", "margin-left": "10px"}),

                        ], style={"marginLeft": "5%"})], className="d-flex justify-content-center"),
                    html.Br(),
                    html.H3(children='Escoja el intervalo de tiempo',
                            style={"width": "30%", 'display': 'inline-block', "marginLeft": "5%"}),
                    html.Div([
                        dcc.Slider(0, 5, step=None,
                                   marks={
                                       0: '12AM-5AM',
                                       1: '5AM-9AM',
                                       2: '9AM-1PM',
                                       3: '1PM-5PM',
                                       4: '5PM-9PM',
                                       5: '9PM-12AM'
                                   },
                                   value=0,
                                   id='my-slider2')], style={"width": "60%", "marginLeft": "5%"}),

                    html.Br(),
                    # Table container
                    dcc.Loading(
                        id = 'loading',
                    children = [html.Div([
                        dcc.Graph(id='mapa-tiempos')

                    ])],
                    type = "circle"),
                    html.Br(),
                    # html.Div([
                    #   html.Button('Descripción', id='btn-nclicks-3', n_clicks=0, style={'width': '240px', 'height': '40px',
                    #                 'cursor': 'pointer', 'border': '0px',
                    #                'borderRadius': '5px', 'backgroundColor':
                    #               'black', 'color': 'white', 'textTransform':
                    #              'uppercase', 'fontSize': '15px'}),
                    # html.Div(id='container-button-timestamp3')
                    # ],style={'textAlign': 'center'}),
                    html.Br()

                ], style={"width": "100%"}, className="shadow-lg p-3 mb-5 bg-white rounded")),
        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )




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
    Input("dropdown-localidad-sexo", "value"))
def update_localidad(sex):
    datos1 = encuestast1.copy()
    datos2 = encuestast2.copy()
    datos1 = datos1[datos1["Sexo"].isin(sex)]
    datos2 = datos2[datos2["Sexo"].isin(sex)]

    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]], vertical_spacing=0.001,
                        subplot_titles=("Proporción de personas por localidad<br>antes de la pandemia",
                                        "Proporción de personas por localidad<br>después de la pandemia"))

    datos1 = datos1.groupby("localidad").agg({'localidad':'count'})
    datos1.columns = ["cantidad"]
    datos2 = datos2.groupby("localidad").agg({'localidad':'count'})
    datos2.columns = ["cantidad"]
    datos1 = datos1.sort_index()
    datos2 = datos2.sort_index()
    fig.add_trace(go.Pie(
        labels=datos1.index,
        values=datos1.cantidad,
        textinfo='label+percent',
        insidetextorientation='radial',
        name="Antes de la pandemia",
        sort=False,
        marker=dict(colors=colors_pie, line=dict(color='#000000', width=2)),
    ), 1, 1)
    fig.add_trace(go.Pie(
        labels=datos2.index,
        values=datos2.cantidad,
        textinfo='label+percent',
        insidetextorientation='radial',
        name = "Después de la pandemia",
        sort=False,
        marker=dict(colors=colors_pie, line=dict(color='#000000', width=2)),
    ), 1, 2)


    #fig.update_layout(title = "Distribución de personas por localidad antes y después de la pandemia")
    return fig


# Histograma de sexo
@app.callback(
    Output("sexo", "figure"),
    Input("dropdown-sexo-localidad", "value"))
def update_sexo(localidad):
    datos1 = encuestast1.copy()
    datos2 = encuestast2.copy()

    datos1 = datos1[datos1["localidad"].isin(localidad)]
    datos2 = datos2[datos2["localidad"].isin(localidad)]
    fig = make_subplots(rows=1, cols=2,specs=[[{"type": "pie"}, {"type": "pie"}]],vertical_spacing=0.001,subplot_titles=("Distribución de género antes de la pandemia", "Distribución de género después de la pandemia"))

    datos1 = datos1.groupby("Sexo").agg({"Sexo":"count"})
    datos2 = datos2.groupby("Sexo").agg({"Sexo":"count"})

    fig.add_trace(go.Pie(
        labels = datos1.index,
        values = datos1.Sexo,
        textinfo='label+percent',
        insidetextorientation='radial',
        name = "Antes de la pandemia",
        sort=False,
        marker=dict(colors=colors_pie, line=dict(color='#000000', width=2)),
   ), 1, 1)

    fig.add_trace(go.Pie(
        labels=datos2.index,
        values=datos2.Sexo,
        textinfo='label+percent',
        insidetextorientation='radial',
        name = "Después de la pandemia",
        sort=False,
        marker=dict(colors=colors_pie, line=dict(color='#000000', width=2)),
    ), 1, 2)
                        # color_discrete_sequence=['#32373B',   '#C83E4D'])
    return fig

@app.callback(
    Output("ocupacion", "figure"),
    [Input("dropdown-ocupacion-localidad", "value"),
     Input('dropdown-ocupacion-sexo', 'value')])
def ocupacion(localidad,sex):
    datos1 = encuestast1.copy()
    datos2 = encuestast2.copy()

    datos1 = datos1[(datos1.T1_Q15 != "888") & (datos1.T1_Q15 != "Otros") ]
    datos2 = datos2[datos2.T2_Q13.isin(datos1.T1_Q15.unique())]

    datos1 = datos1[datos1["localidad"].isin(localidad)]
    datos2 = datos2[datos2["localidad"].isin(localidad)]
    datos1 = datos1[datos1["Sexo"].isin(sex)]
    datos2 = datos2[datos2["Sexo"].isin(sex)]

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                        shared_yaxes=True, vertical_spacing=0.001,subplot_titles=("Cantidad de personas por<br>ocupación antes de la pandemia", "Cantidad de personas por<br>ocupación después de la pandemia"))

    datos_x1 = datos1.T1_Q15.value_counts().sort_index()
    datos_x2 = datos2.T2_Q13.value_counts().sort_index()

    fig.add_trace(go.Bar(
        y=datos_x1,
        x=datos_x1.index,
        name='Antes de<br>la pandemia',
        marker=dict(
            color=colors[0],
            line=dict(color=colors[1], width=3)
        )), 1, 1)

    fig.add_trace(go.Bar(
        y=datos_x2,
        x=datos_x2.index,
        name='Después de<br>la pandemia',
        marker=dict(
            color=colors[2],
            line=dict(color=colors[3], width=3)
        )), 1, 2)

    fig.update_xaxes(title_text="Ocupación", row=1, col=1)
    fig.update_xaxes(title_text="Ocupación", row=1, col=2)

    fig.update_yaxes(title_text="Número de personas", row=1, col=1)
    fig.update_yaxes(title_text="Número de personas",row=1, col=2)
    return fig

#Histograma preferencia transporte
@app.callback(
    Output("Preferencia Transporte", "figure"),
    [Input("dropdown-preferido-localidad", "value"),
     Input('dropdown-preferido-sexo', 'value')])
def update_preferencias(localidad,sex):

    datos1 = encuestast1.copy()
    datos2= encuestast2.copy()

    datos1 = datos1[datos1["localidad"].isin(localidad)]
    datos2 = datos2[datos2["localidad"].isin(localidad)]
    datos1 = datos1[datos1["Sexo"].isin(sex)]
    datos2 = datos2[datos2["Sexo"].isin(sex)]

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=True, vertical_spacing=0.001,subplot_titles=("Proporción antes de la pandemia", "Proporción después de la pandemia"))
    top_labels = ['Public transport', 'Active Transport', 'TransMicable', 'Informal transport', 'Private Transport']
    x_data1 = []
    for nombre in ['Public transport', 'Active Transport', 'TransMicable', 'Informal transport', 'Private Transport']:
        x_data1.append(len(datos1[datos1["modes"] == nombre]))
    x_data1 = list(map(lambda x: round(x / sum(x_data1),2), x_data1))

    x_data2 = []
    for nombre in ['Public transport', 'Active Transport', 'TransMicable', 'Informal transport', 'Private Transport']:
        x_data2.append(len(datos2[datos2["modes"] == nombre]))
    x_data2 = list(map(lambda x: round(x / sum(x_data2),2), x_data2))


    fig.add_trace(go.Bar(
        y=top_labels,
        x=x_data1,
        name='Antes de la pandemia',
        orientation='h',
        marker=dict(
            color=colors[0],
            line=dict(color=colors[1], width=3)
        )),1,1)

    fig.add_trace(go.Bar(
        y=top_labels,
        x=x_data2,
        name='Después de la pandemia',
        orientation='h',
        marker=dict(
            color=colors[2],
            line=dict(color=colors[3], width=3)
        )), 1, 2)

    fig.update_xaxes(title_text="Porcentaje (%)", row=1, col=1)
    fig.update_xaxes(title_text="Porcentaje (%)", row=1, col=2)

    fig.update_yaxes(title_text="Medio de transporte preferido", row=1, col=1)
    fig.update_yaxes(title_text="Medio de transporte preferido",row=1, col=2)

    return fig


@app.callback(
    Output("mapa-frecuencias", "figure"),
    [Input("dropdown-mapa-localidad", "value"),
     Input('dropdown-mapa-sexo', 'value'),
     Input('my-slider', 'value')])
def prueba(localidad, sex, hora):
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "choropleth"}, {"type": "choropleth"}], [{"type": "choropleth"}, {"type": "choropleth"}]
        ],
        vertical_spacing=0.075,
        horizontal_spacing=0.08,
        subplot_titles=("Porcentaje de inicio de viajes por localidad<br>antes de la pandemia", "Porcentaje de inicio de viajes por localidad<br>después de la pandemia", "Porcentaje de fin de viajes por localidad<br>antes de la pandemia",
                        "Porcentaje de fin de viajes por localidad<br>después de la pandemia")
    )
    data_frame = primeros
    data_frame = data_frame[data_frame["localidad"].isin(localidad)]
    data_frame = data_frame[data_frame["Sexo"].isin(sex)]

    inicio, fin = horas[hora]
    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("dia_inicio")["inicio"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    diff = localidades - set(data_frame.inicio)
    data_frame = pd.concat(
        [data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["inicio", "frecuencia"])])
    data_frame['frecuencia'] = data_frame['frecuencia'].apply(lambda x: round(x,2))

    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.inicio,
        z=data_frame['frecuencia'],
        colorscale=['rgb(255,255,255)', colors[1]],
        colorbar_title="Viajes",
        zmin=0,
        zmax=0.15,
        name='Viajes iniciados pre pandemia',
        hoverinfo='location+z',
        showlegend=False,
        showscale=False,
    ), row=1, col=1)

    data_frame = primerost2
    data_frame = data_frame[data_frame["localidad"].isin(localidad)]
    data_frame = data_frame[data_frame["Sexo"].isin(sex)]

    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("dia_inicio")["inicio"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame = data_frame.reset_index().groupby("inicio").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    diff = localidades - set(data_frame.inicio)
    data_frame = pd.concat(
        [data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["inicio", "frecuencia"])])
    data_frame['frecuencia'] = data_frame['frecuencia'].apply(lambda x: round(x,2))

    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.inicio,
        z=data_frame['frecuencia'],
        colorscale=['rgb(255,255,255)', colors[1]],
        colorbar_title="Viajes",
        zmin=0,
        zmax=0.15,
        name='Viajes iniciados post pandemia',
        hoverinfo='location+z',

    ), row=1, col=2)

    data_frame = ultimos
    data_frame = data_frame[data_frame["localidad"].isin(localidad)]
    data_frame = data_frame[data_frame["Sexo"].isin(sex)]
    data_frame = data_frame[(data_frame.hora_fin >= inicio) & (data_frame.hora_fin <= fin)]
    data_frame = data_frame.groupby("dia_fin")["fin"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame = data_frame.reset_index().groupby("fin").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    diff = localidades - set(data_frame.fin)
    data_frame = pd.concat(
        [data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["fin", "frecuencia"])])

    data_frame['frecuencia'] = data_frame['frecuencia'].apply(lambda x: round(x,2))
    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.fin,
        z=data_frame['frecuencia'],
        colorscale=['rgb(255,255,255)', colors[1]],
        colorbar_title="Viajes",
        zmin=0,
        zmax=0.15,
        name='Pre pandemia',
        hoverinfo='location+z',
        showlegend=False,
        showscale=False,

    ), row=2, col=1)
    data_frame = ultimost2
    data_frame = data_frame[data_frame["localidad"].isin(localidad)]
    data_frame = data_frame[data_frame["Sexo"].isin(sex)]

    data_frame = data_frame[(data_frame.hora_fin >= inicio) & (data_frame.hora_fin <= fin)]
    data_frame = data_frame.groupby("dia_fin")["fin"].value_counts().to_frame()
    data_frame.columns = ["frecuencia"]
    data_frame = data_frame.reset_index().groupby("fin").agg({"frecuencia": "mean"})
    data_frame = (data_frame / data_frame.sum()).reset_index()
    diff = localidades - set(data_frame.fin)
    data_frame = pd.concat(
        [data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["fin", "frecuencia"])])
    data_frame['frecuencia'] = data_frame['frecuencia'].apply(lambda x: round(x,2))

    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.fin,
        z=data_frame['frecuencia'],
        colorscale=['rgb(255,255,255)', colors[1]],
        colorbar_title="Viajes",
        zmin=0,
        zmax=0.15,
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
    fig.update_layout(height=600, dragmode=False)

    return fig




@app.callback(
    Output("viajes-promedio", "children"),
    [Input("dropdown-texto-localidad", "value"),
     Input('dropdown-texto-sexo', 'value')])
def viajes_prom(localidad,sex):
    datos1 = viajes_promedio.copy()
    datos2 = viajes_promedioT2.copy()

    datos1 = datos1[datos1["Sexo"].isin(sex)]
    datos2 = datos2[datos2["Sexo"].isin(sex)]

    datos1 = datos1[datos1["localidad"].isin(localidad)]
    datos2 = datos2[datos2["localidad"].isin(localidad)]

    viajest1 = datos1.viaje.mean()
    viajest2 = datos2.viaje.mean()

    return html.Div([
        html.Div([
            html.H5("En promedio una persona hace ", style={"textAlign": "center"}),
            html.H1(str(round(viajest1, 2)), style={"textAlign": "center", "color": colors[1]}),
            html.H5(" viajes al día antes de la pandemia", style={"textAlign": "center"})
        ], style={"width": "49%", "display": "inline-block"}),
        html.Div([
            html.H5("En promedio una persona hace ",style = {"textAlign":"center"}) ,
            html.H1(str(round(viajest2,2)),style = {"textAlign":"center","color":colors[3]}) ,
            html.H5(" viajes al día después de la pandemia",style = {"textAlign":"center"})
        ],style={"width":"49%","display":"inline-block"}),
    ],style={"display":"flex"},className="shadow-sm p-3 mb-5 bg-white rounded")

@app.callback(
    Output("suma-transporte", "figure"),
    [Input("dropdown-suma1-localidad", "value"),
     Input('dropdown-suma1-sexo', 'value')])
def suma_transporte(localidad,sex):
    datos1 = tiempos.copy()
    datos2 = tiemposT2.copy()

    datos1 = datos1[datos1["localidad"].isin(localidad)]
    datos2 = datos2[datos2["localidad"].isin(localidad)]
    datos1 = datos1[datos1["Sexo"].isin(sex)]
    datos2 = datos2[datos2["Sexo"].isin(sex)]

    datos1 = datos1.groupby(["fecha_inicio_viaje","movimiento","ID"]).agg({"tiempo_minutos":"sum"}).reset_index().groupby(["fecha_inicio_viaje","movimiento"]).agg({"tiempo_minutos":"mean"}).reset_index().groupby("movimiento").agg({"tiempo_minutos":"mean"})
    datos2 = datos2.groupby(["fecha_inicio_viaje","movimiento","ID"]).agg({"tiempo_minutos":"sum"}).reset_index().groupby(["fecha_inicio_viaje","movimiento"]).agg({"tiempo_minutos":"mean"}).reset_index().groupby("movimiento").agg({"tiempo_minutos":"mean"})

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=True, vertical_spacing=0.001,subplot_titles=("Tiempos antes de la pandemia", "Tiempos después de la pandemia"))

    datos1.tiempo_minutos = datos1.tiempo_minutos.apply(lambda x: round(x,2))
    datos2.tiempo_minutos = datos2.tiempo_minutos.apply(lambda x: round(x,2))
    fig.add_trace(go.Bar(
        y=datos1.index,
        x=datos1.tiempo_minutos,
        name='Antes de la pandemia',
        orientation='h',
        marker=dict(
            color=colors[0],
            line=dict(color=colors[1], width=3)
        )),1,1)
    max1 = datos1.tiempo_minutos.max()
    fig.add_trace(go.Bar(
        y=datos2.index,
        x=datos2.tiempo_minutos,
        name='Después de la pandemia',
        orientation='h',
        marker=dict(
            color=colors[2],
            line=dict(color=colors[3], width=3)
        )), 1, 2)

    max2 = datos2.tiempo_minutos.max()

    maximo = max(max1,max2)
    fig.update_xaxes(title_text="Tiempo diario promedio (min)",range=[0, maximo+30], row=1, col=1)
    fig.update_xaxes(title_text="Tiempo diario promedio (min)", range=[0, maximo+30],row=1, col=2)

    fig.update_yaxes(title_text="Medio de transporte utilizado", row=1, col=1)
    fig.update_yaxes(title_text="Medio de transporte utilizado",row=1, col=2)

    return fig

@app.callback(
    Output("mapa-tiempos", "figure"),
    [Input("dropdown-mapa2-localidad", "value"),
     Input('dropdown-mapa2-sexo', 'value'),
     Input('my-slider2', 'value')])
def ultimo_mapa(localidad,sex,hora):
    fig = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "choropleth"}, {"type": "choropleth"}]
        ],
        vertical_spacing=0.075,
        horizontal_spacing=0.08,
        subplot_titles=("Tiempo promedio de viajes saliendo de<br>" +" y ".join(localidad) +" antes de la pandemia", "Tiempo promedio de viajes saliendo de<br>" +" y ".join(localidad) +" después de la pandemia")
    )
    data_frame = tiempos_viaje.copy()
    data_frame = data_frame[data_frame["Sexo"].isin(sex)]
    data_frame = data_frame[data_frame["localidad"].isin(localidad)]
    data_frame = data_frame[data_frame["inicio"].isin(map(lambda x: x.upper(),localidad))]

    inicio, fin = horas[hora]
    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("fin").agg({"tiempo_viaje_minutos":"mean"})
    data_frame = data_frame.reset_index()
    diff = localidades - set(data_frame.fin)
    data_frame = pd.concat([data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["fin", "tiempo_viaje_minutos"])])
    data_frame['tiempo_viaje_minutos'] = data_frame['tiempo_viaje_minutos'].apply(lambda x: round(x,2))
    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.fin,
        z=data_frame['tiempo_viaje_minutos'],
        colorscale=['rgb(255,255,255)', colors[1]],
        colorbar_title="Minutos",
        zmin=0,
        zmax=200,
        name='Minutos de viaje pre pandemia',
        hoverinfo='location+z',

    ), row=1, col=1)

    data_frame = tiempos_viajeT2.copy()
    data_frame = data_frame[data_frame["Sexo"].isin(sex)]
    data_frame = data_frame[data_frame["localidad"].isin(localidad)]
    data_frame = data_frame[data_frame["inicio"].isin(map(lambda x: x.upper(), localidad))]

    data_frame = data_frame[(data_frame.hora_inicio >= inicio) & (data_frame.hora_inicio <= fin)]
    data_frame = data_frame.groupby("fin").agg({"tiempo_viaje_minutos": "mean"})
    data_frame = data_frame.reset_index()
    diff = localidades - set(data_frame.fin)
    data_frame = pd.concat(
        [data_frame, pd.DataFrame(list(zip(diff, np.zeros(len(diff)))), columns=["fin", "tiempo_viaje_minutos"])])

    data_frame['tiempo_viaje_minutos'] = data_frame['tiempo_viaje_minutos'].apply(lambda x: round(x,2))

    fig.add_trace(trace=go.Choropleth(
        featureidkey='properties.LocNombre',
        geojson=bog_regions_geo,
        locations=data_frame.fin,
        z=data_frame['tiempo_viaje_minutos'],
        colorscale=['rgb(255,255,255)', colors[1]],
        colorbar_title="Minutos",
        zmin=0,
        zmax=200,
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
    fig.update_layout(height = 500,dragmode=False)

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
