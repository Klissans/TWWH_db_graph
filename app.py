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
                'height': '95vh',
                'background': '#000000',
            }
        )
    ]),

    html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='Schema', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('', id='schema-name'),
                    html.Pre(
                        id='tap-node-json-output',
                        style=styles['json-output']
                    )
                ])
            ])
        ]),
    ])
])


app = dash.Dash(__name__)
app.layout = layout


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='display_table_schema_tap_node'
    ),
    output=Output('tap-node-json-output', 'children'),
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


if __name__ == '__main__':
    app.run_server(debug=False)
