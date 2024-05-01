"""Create Canadian bird observations as CSV."""

import pandas as pd
import sys


COLUMNS = {
    "LOC_ID": "loc_id",
    "LATITUDE": "latitude",
    "LONGITUDE": "longitude",
    "SUBNATIONAL1_CODE": "region",
    "Year": "year",
    "Month": "month",
    "Day": "day",
    "SPECIES_CODE": "species_id",
    "HOW_MANY": "num",
}


def main():
    """Main driver."""
    infile, outfile = sys.argv[1], sys.argv[2]
    df = pd.read_csv(infile)
    birds = df[list(COLUMNS.keys())].rename(columns=COLUMNS)
    birds = birds[birds["region"].str.startswith("CA")]
    birds.to_csv(outfile, index=False)


if __name__ == "__main__":
    main()
