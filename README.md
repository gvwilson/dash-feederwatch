# Dash Feederwatch

A [Dash][dash] visualization of [Feederwatch][feederwatch] data.

- Create a Python virtual environment and run `pip install requirements.txt` to install required software.
  - Please use Python 3.11.
- Run `make` on its own in the root directory to see available commands.
- Run `make data` to re-create the SQLite database `feederwatch.db`.

## Data

### Birds

- Source: [Project FeederWatch][feederwatch]
- Raw: `raw/PFW_all_2021_2023_June2023_Public.csv`
- URL: <https://clo-pfw-prod.s3.us-west-2.amazonaws.com/data/202306/PFW_all_2021_2023_June2023_Public.zip>
- Obtained: 2024-05-01
- Cooked: `cooked/seen-ca.csv`
- Using: `bin/birds-ca.py`

| Variable   | Data Type   | Definition                                       |
| ---------- | ----------- | ------------------------------------------------ |
| loc_id     | categorical | Unique identifier for survey site                |
| latitude   | continuous  | Latitude in decimal degrees for survey site      |
| longitude  | continuous  | Longitude in decimal degrees for survey site     |
| year       | discrete    | Year of first day of two-day observation period  |
| month      | discrete    | Month of first day of two-day observation period |
| day        | discrete    | Day of first day of two-day observation period   |
| species_id | categorical | Bird species observed (6-letter species code)    |
| num        | discrete    | Maximum number of individuals seen at one time   |

### Species

- Source: [Project FeederWatch][feederwatch]
- Raw: `raw/PFW_spp_translation_table_May2023.csv`
- URL: <https://clo-pfw-prod.s3.us-west-2.amazonaws.com/data/202306/PFW_spp_translation_table_May2023.zip>
- Obtained: 2024-05-01
- Cooked: `cooked/species-ca.csv`
- Using: `bin/species-ca.py`

| Variable   | Data Type   | Definition         |
| ---------- | ----------- | ------------------ |
| species_id | categorical | Species identifier |
| sci_name   | text        | Scientific name    |
| en_us      | text        | Common name        |

[dash]: https://dash.plotly.com
[feederwatch]: https://feederwatch.org
