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

## Notes

With three exceptions noted next, `analyze_plan()` computes all the analytics that DRA does:

-   For a variety of reasons, the production TypeScript package (`dra2020/dra-analytics`) does not 
    calculate a few minor things that show up in the UI. The Python port (`dra2020/rdafn`) does either.
    This repo uses the latter, so those few things aren't in the "scorecard" output.
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