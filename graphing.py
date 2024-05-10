'''Add click behavior to table-and-chart display.'''

from dash import Dash, Input, Output, callback, dash_table, dcc, html, _dash_renderer
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px

import util


PAGE_SIZE = 15
DISPLAY_GRAPH = 'graph'
DISPLAY_TABLE = 'table'
DISPLAY_SELECTED = 'selected'
CHOOSE_REGION = 'region'
CHOOSE_SPECIES = 'species'
WIDTH_LABEL = 1
WIDTH_DROPDOWN = 4


def main(name):
    '''Main driver.'''
    birds, species, regions = util.load_data()
    species_labels = util.make_labels(species, 'species_id', 'en_us')
    regions_labels = util.make_labels(regions, 'region', 'name')
    components = create_components(birds, species_labels, regions_labels)
    app = do_layout(name, components)
    create_callbacks(birds)
    app.run(debug=True)


def create_components(birds, species_labels, regions_labels):
    '''Create dashboard components (use component IDs as dict keys).'''
    return {
        DISPLAY_GRAPH: dcc.Graph(id=DISPLAY_GRAPH),
        DISPLAY_TABLE: dash_table.DataTable(page_size=PAGE_SIZE, id=DISPLAY_TABLE),
        DISPLAY_SELECTED: html.Pre(id=DISPLAY_SELECTED),
        CHOOSE_REGION: dcc.Dropdown(regions_labels, None, id=CHOOSE_REGION),
        CHOOSE_SPECIES: dcc.Dropdown(species_labels, None, id=CHOOSE_SPECIES),
    }


def do_layout(name, components):
    '''Lay out components using Mantine.'''
    # https://github.com/snehilvj/dash-mantine-components/issues/240
    _dash_renderer._set_react_version('18.2.0')
    app = Dash(name)
    app.layout = dmc.MantineProvider(children=[
        # title
        dmc.Title('FeederWatch with Interactive Graph'),
        # pulldown to select region
        dmc.Grid(children=[
            dmc.GridCol(html.Div('region:'), span=WIDTH_LABEL),
            dmc.GridCol(components[CHOOSE_REGION], span=WIDTH_DROPDOWN),
        ]),
        # pulldown to select species
        dmc.Grid(children=[
            dmc.GridCol(html.Div('species:'), span=WIDTH_LABEL),
            dmc.GridCol(components[CHOOSE_SPECIES], span=WIDTH_DROPDOWN),
        ]),
        # text display of details of point selected in graph
        dmc.Grid(children=[
            dmc.GridCol(html.Div('selected:'), span=WIDTH_LABEL),
            dmc.GridCol(components[DISPLAY_SELECTED], span=WIDTH_DROPDOWN),
        ]),
        # table
        dmc.Grid(children=[dmc.GridCol(components[DISPLAY_TABLE])]),
        # graph
        dmc.Grid(children=[dmc.GridCol(components[DISPLAY_GRAPH])]),
    ])
    return app



def create_callbacks(birds):
    '''Connect component callbacks.'''
    # Re-create graph and table when pulldowns change
    @callback(
        Output(DISPLAY_GRAPH, 'figure'),
        Output(DISPLAY_TABLE, 'data'),
        Input(CHOOSE_REGION, 'value'),
        Input(CHOOSE_SPECIES, 'value')
    )
    def update_graph(region, species):
        temp = birds if region is None else birds[birds['region'] == region]
        temp = temp if species is None else temp[temp['species_id'] == species]
        temp = temp.groupby(['region', 'species_id']).agg(num = ('num', 'sum')).reset_index()
        fig = px.scatter(temp, x='region', y='species_id', size='num')
        fig.update_layout(clickmode='select')
        return (
            fig,
            temp.to_dict('records'),
        )

    # Change text showing selected data when a point is clicked in the graph
    @callback(
        Output(DISPLAY_SELECTED, 'children'),
        Input(DISPLAY_GRAPH, 'selectedData')
    )
    def update_selection(selectedData):
        return str(selectedData)


if __name__ == '__main__':
    main(__name__)
