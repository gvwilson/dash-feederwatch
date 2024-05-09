from dash import Dash, Input, Output, callback, dash_table, dcc, html, _dash_renderer
import dash_bootstrap_components as dbc
import dash_design_kit as ddk
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import sys


PAGE_SIZE = 15
DATA_DIR = 'cooked'
BIRDS_DATA = f'{DATA_DIR}/birds-ca.csv'
SPECIES_DATA = f'{DATA_DIR}/species-ca.csv'
REGIONS_DATA = f'{DATA_DIR}/regions-ca.csv'
COMPONENT_GRAPH = 'graph'
COMPONENT_TABLE = 'table'
SELECT_REGION = 'region'
SELECT_SPECIES = 'species'
WIDTH_LABEL = 1
WIDTH_DROPDOWN = 4


def main(name):
    '''Main driver.'''
    styling = sys.argv[1]
    layout = globals().get(f'layout_{styling}', None)
    assert layout, f'unknown layout {layout}'

    birds, species, regions = load_data()
    species_labels = make_labels(species, 'species_id', 'en_us')
    regions_labels = make_labels(regions, 'region', 'name')
    
    table_cls = ddk.DataTable if styling == 'ddk' else dash_table.DataTable
    components = create_components(birds, table_cls, species_labels, regions_labels)
    app = layout(name, components)
    create_callbacks(birds)

    app.run(debug=True)


def create_callbacks(birds):
    '''Connect components.'''
    @callback(
        Output(COMPONENT_GRAPH, 'figure'),
        Output(COMPONENT_TABLE, 'data'),
        Input(SELECT_REGION, 'value'),
        Input(SELECT_SPECIES, 'value')
    )
    def update_graph(region, species):
        temp = birds if region is None else birds[birds['region'] == region]
        temp = temp if species is None else temp[temp['species_id'] == species]
        temp = temp.groupby(['region', 'species_id']).agg(num = ('num', 'sum')).reset_index()
        return (
            px.scatter(temp, x='region', y='species_id', size='num'),
            temp.to_dict('records'),
        )


def create_components(birds, table_cls, species_labels, regions_labels):
    return {
        COMPONENT_GRAPH: dcc.Graph(id=COMPONENT_GRAPH),
        COMPONENT_TABLE: table_cls(page_size=PAGE_SIZE, id=COMPONENT_TABLE),
        SELECT_REGION: dcc.Dropdown(regions_labels, None, id=SELECT_REGION),
        SELECT_SPECIES: dcc.Dropdown(species_labels, None, id=SELECT_SPECIES),
    }


def layout_bootstrap(name, components):
    '''Organize components using Bootstrap.'''
    WIDTH_LABEL = 1
    WIDTH_DROPDOWN = 4
    app = Dash(name, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = dbc.Container([
        dbc.Row(dbc.Col(html.H1(children='FeederWatch with Bootstrap Layout'))),
        dbc.Row([
            dbc.Col(html.Div('region:'), width=WIDTH_LABEL),
            dbc.Col(components[SELECT_REGION], width=WIDTH_DROPDOWN),
        ]),
        dbc.Row([
            dbc.Col(html.Div('species:'), width=WIDTH_LABEL),
            dbc.Col(components[SELECT_SPECIES], width=WIDTH_DROPDOWN),
        ]),
        dbc.Row(dbc.Col(components[COMPONENT_TABLE])),
        dbc.Row(dbc.Col(components[COMPONENT_GRAPH])),
    ])
    return app


def layout_ddk(name, components):
    '''Organize components using Dash Design Kit.'''
    app = Dash(name)
    app.layout = ddk.App(show_editor=True, children=[
        ddk.Header([
            ddk.Title('FeederWatch with DDK Layout')
        ]),
        ddk.ControlCard(
            orientation='horizontal',
            label_position='left',
            children=[
                ddk.ControlItem(
                    label='region',
                    children=[
                        components[SELECT_REGION]
                    ]
                ),
                ddk.ControlItem(
                    label='species',
                    children=[
                        components[SELECT_SPECIES]
                    ]
                ),
            ],
        ),
        ddk.Block(children=[
            ddk.Card(ddk.ControlItem(components[COMPONENT_TABLE]), width=50),
            ddk.Card(ddk.ControlItem(components[COMPONENT_GRAPH]), width=50),
        ]),
    ])
    return app


def layout_mantine(name, components):
    '''Organize components using Mantine.'''
    # https://github.com/snehilvj/dash-mantine-components/issues/240
    _dash_renderer._set_react_version('18.2.0')
    app = Dash(name)
    app.layout = dmc.MantineProvider(children=[
        dmc.Title('FeederWatch with Mantine Layout'),
        dmc.Grid(children=[
            dmc.GridCol(html.Div('region:'), span=WIDTH_LABEL),
            dmc.GridCol(components[SELECT_REGION], span=WIDTH_DROPDOWN),
        ]),
        dmc.Grid(children=[
            dmc.GridCol(html.Div('species:'), span=WIDTH_LABEL),
            dmc.GridCol(components[SELECT_SPECIES], span=WIDTH_DROPDOWN),
        ]),
        dmc.Grid(children=[dmc.GridCol(components[COMPONENT_TABLE])]),
        dmc.Grid(children=[dmc.GridCol(components[COMPONENT_GRAPH])]),
    ])
    return app


def load_data():
    '''Prepare application data.'''
    birds = pd.read_csv(BIRDS_DATA)
    species_seen = set(birds['species_id'])

    species = pd.read_csv(SPECIES_DATA)
    species = species[species['species_id'].isin(species_seen)]

    regions = pd.read_csv(REGIONS_DATA)

    return birds, species, regions


def make_labels(df, key_col, value_col):
    '''Make label dictionary for dropdown.'''
    pairs = zip(df[key_col], df[value_col])
    return dict(sorted(pairs))


if __name__ == '__main__':
    main(__name__)
