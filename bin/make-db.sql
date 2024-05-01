-- Create Feederwatch database

.mode csv

drop table if exists birds;
drop table if exists species;

create table birds(
       loc_id		text not null,
       latitude		real not null,
       longitude	real not null,
       region		text not null,
       obs_year		integer not null,
       obs_month	integer not null,
       obs_day		integer not null,
       species_id	text not null,
       num		integer not null
);
.import cooked/birds-ca.csv birds

create table species(
       species_id	text not null primary key,
       sci_name		text not null,
       en_us		text not null
);
.import cooked/species-ca.csv species
