from dash import Dash, Input, Output, callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


PAGE_SIZE = 15
DATA_DIR = 'cooked'
BIRDS_DATA = f'{DATA_DIR}/birds-ca.csv'
SPECIES_DATA = f'{DATA_DIR}/species-ca.csv'
REGIONS_DATA = f'{DATA_DIR}/regions-ca.csv'
ALL_ITEMS = '-all-'
WIDTH_LABEL = 1
WIDTH_DROPDOWN = 4
COMPONENT_GRAPH = 'graph'
COMPONENT_TABLE = 'table'
SELECT_REGION = 'region'
SELECT_SPECIES = 'species'


def main(name):
    '''Main driver.'''
    birds, species_labels, regions_labels = load_data()
    app = Dash(name)
    define_layout(app, species_labels, regions_labels)
    create_callbacks(birds)
    app.run(debug=True)


def load_data():
    '''Prepare application data.'''
    birds = pd.read_csv(BIRDS_DATA)
    species_seen = set(birds['species_id'])

    species = pd.read_csv(SPECIES_DATA)
    species = species[species['species_id'].isin(species_seen)]
    species_labels = {ALL_ITEMS: ALL_ITEMS, **dict(zip(species['species_id'], species['en_us']))}

    regions = pd.read_csv(REGIONS_DATA)
    regions_labels = {ALL_ITEMS: ALL_ITEMS, **dict(zip(regions['region'], regions['name']))}

    return birds, species_labels, regions_labels


def define_layout(app, species_labels, regions_labels):
    '''Organize components.'''
    app.layout = dbc.Container([
        dbc.Row(dbc.Col(html.Div(children='FeederWatch'))),
        dbc.Row([
            dbc.Col(html.Div('region:'), width=WIDTH_LABEL),
            dbc.Col(dcc.Dropdown(regions_labels, ALL_ITEMS, id=SELECT_REGION), width=WIDTH_DROPDOWN),
        ]),
        dbc.Row([
            dbc.Col(html.Div('species:'), width=WIDTH_LABEL),
            dbc.Col(dcc.Dropdown(species_labels, ALL_ITEMS, id=SELECT_SPECIES), width=WIDTH_DROPDOWN),
        ]),
        dbc.Row(dbc.Col(dash_table.DataTable(page_size=PAGE_SIZE, id=COMPONENT_TABLE))),
        dbc.Row(dbc.Col(dcc.Graph(id=COMPONENT_GRAPH))),
    ])


def create_callbacks(birds):
    '''Connect components.'''
    @callback(
        Output(COMPONENT_GRAPH, 'figure'),
        Output(COMPONENT_TABLE, 'data'),
        Input(SELECT_REGION, 'value'),
        Input(SELECT_SPECIES, 'value')
    )
    def update_graph(region, species):
        temp = birds if region == ALL_ITEMS else birds[birds['region'] == region]
        temp = temp if species == ALL_ITEMS else temp[temp['species_id'] == species]
        temp = temp.groupby(['region', 'species_id']).agg(num = ('num', 'sum')).reset_index()
        return (
            px.scatter(temp, x='region', y='species_id', size='num'),
            temp.to_dict('records'),
        )


if __name__ == '__main__':
    main(__name__)
