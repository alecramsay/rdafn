# Data

data_dir: str = "~/local/lamba-data"

## Total population & VAP demographics data

This data is in 2020_census_NC-3.csv from the vtd_data repo:

GEOID20,Tot_2010_tot,Wh_2010_tot,His_2010_tot,BlC_2010_tot,NatC_2010_tot,AsnC_2010_tot,PacC_2010_tot,Tot_2010_vap,Wh_2010_vap,His_2010_vap,BlC_2010_vap,NatC_2010_vap,AsnC_2010_vap,PacC_2010_vap,Tot_2018_acstot,Wh_2018_acstot,His_2018_acstot,BlC_2018_acstot,NatC_2018_acstot,AsnC_2018_acstot,PacC_2018_acstot,Tot_2018_cvap,Wh_2018_cvap,His_2018_cvap,BlC_2018_cvap,NatC_2018_cvap,AsnC_2018_cvap,PacC_2018_cvap,Tot_2019_acstot,Wh_2019_acstot,His_2019_acstot,BlC_2019_acstot,NatC_2019_acstot,AsnC_2019_acstot,PacC_2019_acstot,Tot_2019_cvap,Wh_2019_cvap,His_2019_cvap,BlC_2019_cvap,NatC_2019_cvap,AsnC_2019_cvap,PacC_2019_cvap,Tot_2020_acstot,Wh_2020_acstot,His_2020_acstot,BlC_2020_acstot,NatC_2020_acstot,AsnC_2020_acstot,PacC_2020_acstot,Tot_2020_cvap,Wh_2020_cvap,His_2020_cvap,BlC_2020_cvap,NatC_2020_cvap,AsnC_2020_cvap,PacC_2020_cvap,Tot_2020_tot,Wh_2020_tot,His_2020_tot,BlC_2020_tot,NatC_2020_tot,AsnC_2020_tot,PacC_2020_tot,Tot_2020_vap,Wh_2020_vap,His_2020_vap,BlC_2020_vap,NatC_2020_vap,AsnC_2020_vap,PacC_2020_vap,Tot_2020_nhvap,Wh_2020_nhvap,His_2020_nhvap,Bl_2020_nhvap,Asn_2020_nhvap,Nat_2020_nhvap,Pac_2020_nhvap,OthAl_2020_nhvap,Mix_2020_nhvap

# Election data

This data is in 2020_election_NC.csv from the vtd_data repo:

GEOID20,Tot_2016_ltg,D_2016_ltg,R_2016_ltg,Tot_2016_sen,D_2016_sen,R_2016_sen,Tot_2016_gov,D_2016_gov,R_2016_gov,Tot_2016_ag,D_2016_ag,R_2016_ag,Tot_2016_pres,D_2016_pres,R_2016_pres,Tot_2014_sen,D_2014_sen,R_2014_sen,Tot_2020_ag,D_2020_ag,R_2020_ag,Tot_2020_gov,D_2020_gov,R_2020_gov,Tot_2020_ltg,D_2020_ltg,R_2020_ltg,Tot_2020_sen,D_2020_sen,R_2020_sen,Tot_2020_pres,D_2020_pres,R_2020_pres

- VTD shapes in tl_2020_37_vtd20.zip from https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/

## Precinct contiguity graphs 

We've already created these in the baseline repo, to support finding baseline candidates.
We're also already using it in the ensembles repo, to support generating spanning trees.
So, by definition, our ensemble maps will be contiguous.