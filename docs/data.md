# Data

data_dir: str = "~/local/lamba-data"

## Total population & VAP demographics data

This data is in 2020_census_NC-3.csv from the vtd_data repo:

# Election data

This data is in 2020_election_NC.csv from the vtd_data repo:

- VTD shapes in tl_2020_37_vtd20.zip from https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/

## Precinct contiguity graphs 

We've already created these in the baseline repo, to support finding baseline candidates.
We're also already using it in the ensembles repo, to support generating spanning trees.
So, by definition, our ensemble maps will be contiguous.