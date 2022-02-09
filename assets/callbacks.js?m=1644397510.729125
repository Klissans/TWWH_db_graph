function openTab(event, tab_id){
    let tabcontent = document.getElementsByClassName('tabcontent');
    for (let i=0; i< tabcontent.length; i++){
        tabcontent[i].style.display = 'none';
    }
    let tablinks = document.getElementsByClassName('tablinks');
    for (let i=0; i< tablinks.length; i++){
        tablinks[i].className = tablinks[i].className.replace('active', '');
    }
    document.getElementById(tab_id).style.display = 'block';
    event.currentTarget.className += 'active';
}


window.onload = function () {
    let tablinks = document.getElementsByClassName('tablinks');
    for (let i=0; i< tablinks.length; i++){
        let idd = tablinks[i].textContent.toLowerCase() + '-tab';
        tablinks[i].onclick = () => {openTab(event, idd)};
    }
};



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
                    return null;
                }
                let schema = store['schema'][node['data']['id']]['schema'];
                schema['fields'].sort((a, b) => {return a['ca_order'] - b['ca_order']})

                let fields_div = document.getElementById('table-fields');
                fields_div.innerHTML = '';

                let references_div = document.getElementById('key-references');
                references_div.innerHTML = '';

                for (let field of schema['fields']){

                    let field_elem = document.createElement('button');
                    field_elem.className = 'fieldbutton';
                    field_elem.id = `table-field-${field['name']}`;
                    field_elem.style = "width: 100%;";
                    field_elem.setAttribute('data-tooltip', null);
                    field_elem.setAttribute('data-tooltip-label', "tooltip");
                    field_elem.setAttribute('data-tooltip-message', JSON.stringify(field,null,2));

                    if (field['is_key']){
                        let icon_elem = document.createElement('i');
                        icon_elem.className = 'fa fa-key';
                        if (field['is_reference'] != null) {
                            icon_elem.textContent = `${field['name']} => ${field['is_reference'].join(':|:')}`;
                        } else{
                            icon_elem.textContent= field['name'];
                        }
                        field_elem.appendChild(icon_elem);
                    }else if (field['is_reference'] != null){
                        let icon_elem = document.createElement('i');
                        icon_elem.className = 'fa fa-key-skeleton-left-right';
                        icon_elem.textContent = `${field['name']} => ${field['is_reference'].join(':|:')}`;
                        field_elem.appendChild(icon_elem);
                    }else{
                        let name_elem = document.createElement('div');
                        name_elem.textContent= field['name'];
                        field_elem.appendChild(name_elem);
                    }

                    if (field['is_reference'] != null) {
                        let node_id = field['is_reference'][0];
                        field_elem.onclick = function () {
                            let cy_node = cy.nodes(`#${node_id}`);
                            cy_node.trigger('tap');
                            cy.center(cy_node);
                        };
                    }

                    fields_div.appendChild(field_elem);


                    // add references
                    if (field['referenced_by'] !== undefined && field['referenced_by'].length > 0){

                        for (let ref of field['referenced_by']) {
                            let field_elem = document.createElement('button');
                            field_elem.className = 'fieldbutton';
                            field_elem.id = `key-reference-${ref[0]}-${ref[1]}`;
                            field_elem.style = "width: 100%;";

                            let name_elem = document.createElement('div');
                            name_elem.textContent = `${ref[0]}:|:${ref[1]} => ${field['name']}`;
                            field_elem.appendChild(name_elem);

                            let node_id = ref[0];
                            field_elem.onclick = function () {
                                let cy_node = cy.nodes(`#${node_id}`);
                                cy_node.trigger('tap');
                                cy.center(cy_node);
                            };
                            references_div.appendChild(field_elem);
                        }

                    }
                }

                for (let field of schema['localised_fields']){
                    let field_elem = document.createElement('button');
                    field_elem.className += ' locbutton';
                    field_elem.id = `table-field-${field['name']}`;
                    field_elem.style = "width: 100%;";
                    field_elem.innerHTML = field['name'];
                    fields_div.appendChild(field_elem);
                }

            	return null;
        },

        search_tables_by_name:
			function(table_name_substr, store) {
                let schema = store['schema'];
                let tables_div = document.getElementById('found-tables');
                tables_div.innerHTML = '';

                for (let table_name in schema){
                    if (table_name.includes(table_name_substr)) {
                        let button_elem = document.createElement('button');
                        button_elem.id = `found-table-button-${table_name}`;
                        button_elem.style = "width: 100%;";
                        button_elem.innerHTML = table_name;
                        button_elem.onclick = function() {
                            let cy_node = cy.nodes(`#${table_name}`);
                            cy_node.trigger('tap');
                            cy.center(cy_node);
                        };
                        tables_div.appendChild(button_elem);
                    }
                }
            	return null;
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