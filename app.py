import json
import dash
import dash_cytoscape as cyto
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


with open('graph.json', 'r') as f:
    cytoscape_elements = json.load(f)

with open('schema.json', 'r') as f:
    schema = json.load(f)

default_edge_width = 10
default_font_size_mapping = "mapData(degree, 0, 50, 55, 99)"
default_node_size_mapping = "mapData(degree, 0, 70, 50, 100)"

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
                    'font-size': default_font_size_mapping,
                    "width": default_node_size_mapping,
                    "height": default_node_size_mapping,
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': default_edge_width,
                    'opacity': 0.8,
                    'curve-style': 'bezier',
                    'line-color': '#555555',
                    'target-arrow-color': '#999999',
                    'target-arrow-shape': 'triangle',
                    # 'target-arrow-size': 15,
                }
            },
        ]

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


@app.callback(Output('tap-node-json-output', 'children'),
              [Input('cytoscape', 'tapNode')])
def display_tap_node(node):
    if not node:
        return ''
    return json.dumps(schema[node['data']['id']], indent=2)


@app.callback(Output('schema-name', 'children'),
              [Input('cytoscape', 'tapNode')])
def display_tap_node(node):
    if not node:
        return ''
    return node['data']['id']


@app.callback(Output('cytoscape', 'stylesheet'),
              [Input('cytoscape', 'tapNode')])
def generate_stylesheet(node):
    follower_color = "#0074D9"
    following_color = "#FF4136"
    font_size = 88
    if not node:
        return default_stylesheet

    stylesheet = [
        {
        "selector": 'node',
        'style': {
            'opacity': 0.3,
            'font-size': default_font_size_mapping,
            "width": default_node_size_mapping,
            "height": default_node_size_mapping,
            'label': 'data(id)',
            'color': 'white',
        }
    },
        {
        'selector': 'edge',
        'style': {
            'width': default_edge_width,
            'opacity': 0.2,
            'curve-style': 'bezier',
            'line-color': '#555555',
            'target-arrow-color': '#999999',
            'target-arrow-shape': 'triangle',
            # 'source-arrow-size': 15,
        }
    },
        {
        "selector": f'''node[id = "{node['data']['id']}"]''',
        "style": {
            'background-color': 'purple',
            "opacity": 1,
            "border-color": "white",
            "border-width": 2,
            "border-opacity": 1,

            "label": "data(label)",
            'font-size': font_size,
            "text-opacity": 1,
            'color': 'purple',
            'text-outline-color': 'white',
            'text-outline-width': 1,
            'z-index': 9999
        }
    }
    ]

    for edge in node['edgesData']:

        if edge['source'] == node['data']['id'] and edge['target'] == node['data']['id']:
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    'width': default_edge_width*2,

                    # 'curve-style': 'unbundled-bezier',
                    # "control-point-distances": 120,
                    # "control-point-weights": 1,
                    # 'loop-direction': -30,
                    # 'loop-sweep': -30,

                    'target-arrow-color': 'purple',
                    'target-arrow-shape': 'triangle',
                    "mid-target-arrow-color": 'purple',
                    "mid-target-arrow-shape": "vee",
                    "line-color": 'purple',
                    'opacity': 1,
                    'z-index': 100500
                }
            })
            continue

        if edge['source'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['target']),
                "style": {
                    'color': following_color,
                    'font-size': font_size,
                    'text-outline-color': '#EEEEEE',
                    'text-outline-width': 1,
                    'background-color': following_color,
                    'opacity': 0.9,
                    "border-color": "white",
                    "border-width": 2,
                    "border-opacity": 1,
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    'width': default_edge_width,
                    'target-arrow-color': following_color,
                    'target-arrow-shape': 'triangle',
                    "mid-target-arrow-color": following_color,
                    "mid-target-arrow-shape": "vee",
                    "line-color": following_color,
                    'opacity': 0.8,
                    'z-index': 5000
                }
            })

        if edge['target'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['source']),
                "style": {
                    'color': follower_color,
                    'font-size': font_size,
                    'text-outline-color': '#EEEEEE',
                    'text-outline-width': 1,
                    'background-color': follower_color,
                    'opacity': 0.9,
                    "border-color": "white",
                    "border-width": 2,
                    "border-opacity": 1,
                    'z-index': 9999
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    'width': default_edge_width,
                    'target-arrow-color': follower_color,
                    'target-arrow-shape': 'triangle',
                    "mid-target-arrow-color": follower_color,
                    "mid-target-arrow-shape": "vee",
                    "line-color": follower_color,
                    'opacity': 0.8,
                    'z-index': 5000
                }
            })

    return stylesheet


if __name__ == '__main__':
    app.run_server(debug=False)
