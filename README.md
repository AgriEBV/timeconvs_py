timeconvs.py
============

Script for timestamp conversions in the Agri-EBV-autumn dataset.

> The dataset can be found [here](https://ieee-dataport.org/open-access/agri-ebv-autumn).


How to Run
----------

Requires Python 3 with some standard packages - if necessary, see imports.

The module -- `timeconvs.py` -- uses `timeconvs` JSON strcture, which is supplied with every sequence, to convert between timestamps. Read below for more info.

Note: currently implemented as a module, which allows only a single instance.


More details
------------

### Timestamp formats

1. _native_ - as provide by the sensor
	in microseconds for dvs, in milliseconds for rs, in nanoseconds for lidar
    native timestamps have some arbitrary offset, depending on when and how sensor was turned on
2. _relative_ - in seconds, without an offset (better used in graphs).


### Timeconvs module

Provides conversions:

* between native timestamp formats (can convert a single number or a numpy array):
    * `convert_rs_to_dvs(ts)`
    * `convert_lidar_to_dvs(ts)`
    * `convert_dvs_to_rs(ts)`
    * `convert_dvs_to_lidar(ts)`
* from native to relate and vice versa (can convert only a single float at a time):
	* `dvs_native_to_relative(ts)`
	* `dvs_relative_to_native(ts)`
	* `lidar_native_to_relative(ts)`
	* `lidar_relative_to_native(ts)`
	* `rs_native_to_relative(ts)`
	* `rs_relative_to_native(ts)`

Uses timeconvs.json to do that. Init using:

```python
import timeconvs

recording_name = ...something like "2020-09-22_12-08-19"...

# Timeconvs
timeconvs_filename = f"data/{recording_name}_timeconvs.json"
timeconvs.load_from_file(timeconvs_filename)

<...use the functions now...>
dvs_n_ts = timeconvs.convert_rs_to_dvs(rs_n_ts)
```

