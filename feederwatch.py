# Import packages
from dash import Dash, Input, Output, callback, dash_table, dcc, html
import pandas as pd
import plotly.express as px


PAGE_SIZE = 15
DATA_DIR = "cooked"
BIRDS_DATA = f"{DATA_DIR}/birds-ca.csv"
SPECIES_DATA = f"{DATA_DIR}/species-ca.csv"
REGIONS_DATA = f"{DATA_DIR}/regions-ca.csv"
ALL_ITEMS = "-all-"


# Incorporate data
birds = pd.read_csv(BIRDS_DATA)
species = pd.read_csv(SPECIES_DATA)
regions = pd.read_csv(REGIONS_DATA)

species_dict = {ALL_ITEMS: ALL_ITEMS, **dict(zip(species['species_id'], species['en_us']))}
regions_dict = {ALL_ITEMS: ALL_ITEMS, **dict(zip(regions['region'], regions['name']))}

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='FeederWatch'),
    dcc.Dropdown(regions_dict, ALL_ITEMS, id='region-dropdown'),
    dcc.Dropdown(species_dict, ALL_ITEMS, id='species-dropdown'),
    dash_table.DataTable(page_size=PAGE_SIZE, id='table'),
    dcc.Graph(id='graph')
])

# Connect the dropdown to the chart
@callback(
    Output('graph', 'figure'),
    Output('table', 'data'),
    Input('region-dropdown', 'value'),
    Input('species-dropdown', 'value')
)
def update_graph(region, species):
    temp = birds if region == ALL_ITEMS else birds[birds['region'] == region]
    temp = temp if species == ALL_ITEMS else temp[temp['species_id'] == species]
    temp = temp.groupby(['region', 'species_id']).agg(num = ('num', 'sum')).reset_index()
    return (
        px.scatter(temp, x='region', y='species_id', size='num'),
        temp.to_dict('records'),
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
