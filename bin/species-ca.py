"""Create lookup table of species identifiers."""

import pandas as pd
import sys


COLUMNS = {
    "species_code": "species_id",
    "scientific_name": "sci_name",
    "american_english_name": "en_us",
}


def main():
    """Main driver."""
    infile, outfile = sys.argv[1], sys.argv[2]
    df = pd.read_csv(infile)
    species = df[list(COLUMNS.keys())].rename(columns=COLUMNS)
    species.to_csv(outfile, index=False)


if __name__ == "__main__":
    main()
