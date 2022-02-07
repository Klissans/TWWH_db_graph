window.dash_clientside = Object.assign({}, window.dash_clientside,
	{
    clientside: {
        display_table_name_tap_node:
			function(node) {
                if (node === undefined) {
                    return '';
                }
                return node['data']['id'];
        },
        display_table_schema_tap_node:
			function(node, store) {
                if (node === undefined) {
                    return '';
                }
                let schema = store['schema'];
            	return JSON.stringify(schema[node['data']['id']], null,2);
        },
        highlight_adjacent_nodes_tap_node:
			function(node, store) {
                let stylesheet_dict = store['stylesheet'];
                if (node === undefined) {
                    return stylesheet_dict['default_stylesheet'];
                }

                let follower_color = "#0074D9";
                let following_color = "#FF4136";
                let font_size = 88;


                let stylesheet = [
                    {
                        "selector": 'node',
                        'style': {
                            'opacity': 0.3,
                            'font-size': stylesheet_dict['default_font_size_mapping'],
                            "width": stylesheet_dict['default_node_size_mapping'],
                            "height": stylesheet_dict['default_node_size_mapping'],
                            'label': 'data(id)',
                            'color': 'white',
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'width': stylesheet_dict['default_edge_width'],
                            'opacity': 0.2,
                            'curve-style': 'bezier',
                            'line-color': '#555555',
                            'target-arrow-color': '#999999',
                            'target-arrow-shape': 'triangle',
                            //'source-arrow-size': 15,
                        }
                    },
                    {
                        "selector": `node[id = "${node['data']['id']}"]`,
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
                ];

                for (const edge of node['edgesData']){
                    if (edge['source'] === node['data']['id'] && edge['target'] === node['data']['id'] ){
                        stylesheet.push({
                            "selector": `edge[id= "${edge['id']}"]`,
                            "style": {
                                'width': stylesheet_dict['default_edge_width'] * 2,

                                // 'curve-style': 'unbundled-bezier',
                                // "control-point-distances": 120,
                                // "control-point-weights": 1,
                                // 'loop-direction': -30,
                                // 'loop-sweep': -30,

                                'target-arrow-color': 'purple',
                                'target-arrow-shape': 'triangle',
                                "mid-target-arrow-color": 'purple',
                                "mid-target-arrow-shape": "vee",
                                "line-color": 'purple',
                                'opacity': 1,
                                'z-index': 100500
                            }
                        });
                        continue;
                    }
                    if(edge['source'] === node['data']['id']){
                        stylesheet.push({
                            "selector": `node[id = "${edge['target']}"]`,
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
                        stylesheet.push({
                            "selector": `edge[id= "${edge['id']}"]`,
                            "style": {
                                'width': stylesheet_dict['default_edge_width'],
                                'target-arrow-color': following_color,
                                'target-arrow-shape': 'triangle',
                                "mid-target-arrow-color": following_color,
                                "mid-target-arrow-shape": "vee",
                                "line-color": following_color,
                                'opacity': 0.8,
                                'z-index': 5000
                            }
                        })
                    }

                    if (edge['target'] === node['data']['id']) {
                        stylesheet.push({
                            "selector": `node[id = "${edge['source']}"]`,
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
                        stylesheet.push({
                            "selector": `edge[id= "${edge['id']}"]`,
                            "style": {
                                'width': stylesheet_dict['default_edge_width'],
                                'target-arrow-color': follower_color,
                                'target-arrow-shape': 'triangle',
                                "mid-target-arrow-color": follower_color,
                                "mid-target-arrow-shape": "vee",
                                "line-color": follower_color,
                                'opacity': 0.8,
                                'z-index': 5000
                            }
                        })
                    }
                }
                return stylesheet;
        },

    }
});