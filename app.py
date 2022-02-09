import json
import dash
import dash_cytoscape as cyto
from dash import html, dcc
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_bootstrap_components as dbc


with open('graph.json', 'r') as f:
    cytoscape_elements = json.load(f)

with open('schema.json', 'r') as f:
    schema = json.load(f)

with open('assets/stylesheet.json', 'r') as f:
    stylesheet_params = json.load(f)

default_stylesheet = [
    # {
    #     "selector": "core",
    #     "style": {
    #         "selection-box-color": "#000000",
    #         "selection-box-border-color": "#8BB0D0",
    #         "selection-box-opacity": "0.5"
    #     }
    # },
    {
        'selector': 'node[label]',
        'style': {
            'color': '#AAAAAA',
            'text-opacity': 1,
        }
    },
    {
        'selector': 'node',
        'style': {
            'label': 'data(id)',
            'background-color': 'white',
            'font-size': stylesheet_params["default_font_size_mapping"],
            "width": stylesheet_params["default_node_size_mapping"],
            "height": stylesheet_params["default_node_size_mapping"],
        }
    },
    {
        'selector': 'edge',
        'style': {
            'width': stylesheet_params["default_edge_width"],
            'opacity': 0.8,
            'curve-style': 'bezier',
            'line-color': '#555555',
            'target-arrow-color': '#999999',
            'target-arrow-shape': 'triangle',
            # 'target-arrow-size': 15,
        }
    },
]
stylesheet_params['default_stylesheet'] = default_stylesheet

styles = {
    'search-output': {
        'position': 'fixed',
        'overflow-y': 'scroll',
        'width': '32%',
        'height': '92%',
        # 'min-height': '1000px',
        # 'max-height': '99%',
        'border': 'thin lightgrey solid',
    },
    'found-table-button': {
        'width': 'calc(100%)'
    },
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(100% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {
        'height': 'calc(98vh - 105px)'
    }
}



layout = html.Div([
    dcc.Store(id='store', data={'schema': schema, 'stylesheet': stylesheet_params}),

    html.Div(className='eight columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=cytoscape_elements,
            stylesheet=default_stylesheet,
            layout={
                'name': 'preset',
            },
            style={
                'width': '100%',
                'height': '99vh',
                'background': '#000000',
            }
        )
    ]),

    html.Div(className='four columns', children=[
        html.Div(className='tab', children=[
            html.Button('Search', className='tablinks',),
            html.Button('Schema', className='tablinks'),
            html.Button('References', className='tablinks'),
        ]),

        html.Div(className='tabcontent', id='search-tab', children=[
            html.Div(style={'width': '50%', 'display': 'inline'}, children=[
                'Table Name: ',
                dcc.Input(id='input-search-table-name', type='text')
            ]),
            html.Div(id='found-tables', style=styles['search-output'])
        ]),

        html.Div(className='tabcontent', id='schema-tab', style={'display': 'none'}, children=[
            html.H3('', id='schema-name'),
            html.Div(id='table-fields', style=styles['search-output'])
        ]),

        html.Div(className='tabcontent', style={'display': 'none'}, id='references-tab', children=[
            html.Div(id='key-references', style=styles['search-output'])
        ]),
    ])
])

external_stylesheets = [
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
                       ]

if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = layout

    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='display_table_schema_tap_node'
        ),
        output=Output('table-fields', 'children'),
        inputs=[Input('cytoscape', 'tapNode')],
        state=[State('store', 'data')]
    )

    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='display_table_name_tap_node'
        ),
        output=Output('schema-name', 'children'),
        inputs=[Input('cytoscape', 'tapNode')]
    )

    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='highlight_adjacent_nodes_tap_node'
        ),
        output=Output('cytoscape', 'stylesheet'),
        inputs=[Input('cytoscape', 'tapNode')],
        state=[State('store', 'data')]
    )

    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='search_tables_by_name'
        ),
        output=Output('found-tables', 'children'),
        inputs=[Input('input-search-table-name', 'value')],
        state=[State('store', 'data')]
    )

    app.run_server(debug=False)
