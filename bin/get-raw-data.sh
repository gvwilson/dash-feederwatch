#!/usr/bin/env bash

wget https://clo-pfw-prod.s3.us-west-2.amazonaws.com/data/202306/PFW_all_2021_2023_June2023_Public.zip
unzip PFW_all_2021_2023_June2023_Public.zip
mv PFW_all_2021_2023_June2023_Public.csv raw

wget https://clo-pfw-prod.s3.us-west-2.amazonaws.com/data/202306/PFW_spp_translation_table_May2023.zip
unzip PFW_spp_translation_table_May2023.zip
mv PFW_spp_translation_table_May2023.zip raw
