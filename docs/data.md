# Data

-   The total census population & VAP demographics data comes from the 2020_census_XX-N.csv in the vtd_data repo, 
    where XX is the state abbreviation and N is the suffix.
-   The election data comes from the 2020_election_XX-N.csv in the vtd_data repo.
-   The shapes are copies of tl_2020_FF_vtd20.zip from https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER, 
    where FF is the state FIPS code.

Note: We've already created the precinct contiguity graphs in the baseline repo, 
to support finding baseline candidates.
And we're also already using it in the ensembles repo, to support generating spanning trees.
So, by definition, our ensemble maps will be contiguous.