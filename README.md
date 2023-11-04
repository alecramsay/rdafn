# rdafn

Compute Dave's Redistricting (DRA) analytics for an ensemble of redistricting plans.

## Installation

```bash
$ git clone https://github.com/alecramsay/rdafn
$ cd rdafn
$ pip install -r requirements.txt
$ ./sample.py
```

## Usage

See `sample.py` for an example of how to use the library.
See sample results from `analyze_plan()` in `sample_NC_scorecard.txt`.

## Data

The data we use to score plans comes from the following sources:

-   The total census population & VAP demographics data comes from the 2020_census_XX-N.csv
    in the DRA [vtd_data](https://github.com/dra2020/vtd_data) GitHub repository, 
    where XX is the state abbreviation and N is the suffix.
    We take the latest version of the data, which is the one with the highest N.
-   The election data comes from the 2020_election_XX-N.csv in the same repo.
-   The shapes are copies of tl_2020_FF_vtd20.zip from [the Census Bureau](https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER), 
    where FF is the state FIPS code, e.g., 37 for North Carolina.

Some things to note:

-   We've already created the precinct contiguity graphs as part of finding root map candidates
    in my [baseline](https://github.com/alecramsay/baseline) GitHub repo,
    and we're also already using the graph in Todd's [ensembles](https://github.com/proebsting/ensembles) repo
    to support generating spanning trees.
    So, by definition, the plans in the ensemble we will score are contiguous&#8212;we don't check that.
-   While we used the official 2020 census total population data 
    to generate the the root maps in my [baseline](https://github.com/alecramsay/baseline) repo,
    as opposed to adjusted population data (if any), 
    we use the adjusted population data here to score ensemble plans.

## Notes

With three exceptions noted next, `analyze_plan()` computes all the analytics that DRA does:

-   For a variety of reasons, DRA's production TypeScript package 
    [dra-analytics](https://github.com/dra2020/dra-analytics) 
    does not calculate a few minor things that show up in the UI. 
    The Python port [rdafn](https://github.com/dra2020/rdapy) does not either.
    This repo uses the latter, so those few things also aren't in the "scorecard" output.
-   To keep the results simple, district-level results are suppressed. The scorecard is a simple flat
    dictionary of metric key/value pairs.
-   To maximize throughput KIWYSI compactness is not calculated. The simple naive approach to performing
    compactness calculations is to dissolve precinct shapes into district shapes, but dissolve is very
    expensive operation. Analyzing a congressional plan for North Carolina take ~60 seconds. A much 
    faster approach is to convert precinct shapes into topologies using TopoJSON like DRA does and then
    merging precincts into district shapes. That approach takes ~5 seconds, virtually all of the time
    being calling TopoJSON `merge()` from Python and marshalling the result back from JavaScript. I could
    have chosen to implement a Python native version of `merge()`. Instead, I chose to skip KIWYSI 
    compactness (which requires actual district shapes) and just calculate the two main compactness
    metrics in DRA: Reock and Polsby-Popper. Together these only depend on district area, perimeter, and
    diameter, and with some pre-processing once per state (analogous to converting shapes into a topology)
    these values can be imputed without ever creating the district shapes. The result is that analyzing
    a congressional plan for North Carolina &#8212; calculating *all* the analytics &#8212; takes a small fraction
    of a second.

## Testing

```bash
$ pytest --disable-warnings
```