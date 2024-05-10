'''Utilities for Dash learning experiments.'''

import pandas as pd


DATA_DIR = 'cooked'
BIRDS_DATA = f'{DATA_DIR}/birds-ca.csv'
SPECIES_DATA = f'{DATA_DIR}/species-ca.csv'
REGIONS_DATA = f'{DATA_DIR}/regions-ca.csv'


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
