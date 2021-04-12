# -*- coding: utf-8 -*-
## @package timeconvs
#  Provides basic timestamp conversions between DVS, Lidar and Realsense timestamps in the Agri-EBV-autumn dataset
#
#  There exists two timestamp formats:
#    1. native   (precisely as it is provided by the sensor)
#                it's microseconds for DVS, nanoseconds for Lidar, milliseconds for Realsense
#                and has initial arbitrary offset
#    2. relative (helpful to display and analyze graphs)
#                it's expressed in seconds and has no initial offset
#
#  Using the timeconvs.json (provided in the dataset for every recording) this module allows to easily convert
#  between the timestamps and formats.
#
#  The following conversion functions are implemented:
#
#    1. between sensors (in native format):
#        - convert_rs_to_dvs()
#        - convert_lidar_to_dvs()
#        - convert_dvs_to_rs()
#        - convert_dvs_to_lidar()
#
#    2. between native and relative formats:
#        - dvs_native_to_relative()
#        - dvs_relative_to_native()
#        - lidar_native_to_relative()
#        - lidar_relative_to_native()
#        - rs_native_to_relative()
#        - rs_relative_to_native()
#
#  Usage example:
#
#    import timeconvs
#    timeconvs_filename = <...timeconvs.json filename...>
#    timeconvs.load_from_file(timeconvs_filename)
#
#    <...load data...>
#    <...use timeconvs functions...>
#

import numpy as np
import json


TIMECONVS = None


## Loads timeconvs.json data from string.
#
#  @type json_string: string
#  @param json_string: timeconvs data as string
def load_from_json_string(json_string):
	global TIMECONVS
	TIMECONVS = json.loads(json_string)


## Loads timeconvs.json data from file.
#
#  @type filename: string
#  @param filename: path to timeconvs.json file
def load_from_file(filename):
	with open(filename, 'r') as infile:
		load_from_json_string(infile.read())


## Converts Realsense native timestamp(s) to DVS native timestamp(s).
#
#  @type rs_ts: float | numpy array
#  @param rs_ts: realsense native timestamp(s)
#
#  @rtype: float | numpy array
#  @return: DVS native timestamp(s) as the same data type value(s)
def convert_rs_to_dvs(rs_ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	is_numpy_array = (type(rs_ts) is np.ndarray)
	if is_numpy_array:
		dvs_ts = np.full_like(rs_ts, 0)
	else:
		dvs_ts = None
	# converting
	for tc in timeconvs["rs_to_dvs"]:
		interval = tc["interval"]
		if tc["inner"]:
			indexes = (rs_ts > interval[0]) & (rs_ts <= interval[1])
		elif interval[0] is None:
			indexes = (rs_ts <= interval[1])
		elif interval[1] is None:
			indexes = (rs_ts > interval[0])
		else:
			raise RuntimeError
		if is_numpy_array:
			dvs_ts[indexes] = rs_ts[indexes] * tc["conv_k"] + tc["conv_b"]
		elif indexes:
			dvs_ts = rs_ts * tc["conv_k"] + tc["conv_b"]
	return dvs_ts


## Converts Lidar native timestamp(s) to DVS native timestamp(s).
#
#  @type lidar_ts: float | numpy array
#  @param lidar_ts: lidar native timestamp(s)
#
#  @rtype: float | numpy array
#  @return: DVS native timestamp(s) as the same data type value(s)
def convert_lidar_to_dvs(lidar_ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	is_numpy_array = (type(lidar_ts) is np.ndarray)
	if is_numpy_array:
		dvs_ts = np.full_like(lidar_ts, 0)
	else:
		dvs_ts = None
	# converting
	for tc in timeconvs["lidar_to_dvs"]:
		interval = tc["interval"]
		if tc["inner"]:
			indexes = (lidar_ts > interval[0]) & (lidar_ts <= interval[1])
		elif interval[0] is None:
			indexes = (lidar_ts <= interval[1])
		elif interval[1] is None:
			indexes = (lidar_ts > interval[0])
		else:
			raise RuntimeError
		if is_numpy_array:
			dvs_ts[indexes] = lidar_ts[indexes] * tc["conv_k"] + tc["conv_b"]
		elif indexes:
			dvs_ts = lidar_ts * tc["conv_k"] + tc["conv_b"]
	return dvs_ts


## Converts DVS native timestamp(s) to Realsense native timestamp(s).
#
#  @type dvs_ts: float | numpy array
#  @param dvs_ts: DVS native timestamp(s)
#
#  @rtype: float | numpy array
#  @return: realsense native timestamp(s) as the same data type value(s)
def convert_dvs_to_rs(dvs_ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	is_numpy_array = (type(dvs_ts) is np.ndarray)
	if is_numpy_array:
		rs_ts = np.full_like(dvs_ts, 0)
	else:
		rs_ts = None
	# converting
	for tc in timeconvs["dvs_to_rs"]:
		interval = tc["interval"]
		if tc["inner"]:
			indexes = (dvs_ts > interval[0]) & (dvs_ts <= interval[1])
		elif interval[0] is None:
			indexes = (dvs_ts <= interval[1])
		elif interval[1] is None:
			indexes = (dvs_ts > interval[0])
		else:
			raise RuntimeError
		if is_numpy_array:
			rs_ts[indexes] = dvs_ts[indexes] * tc["conv_k"] + tc["conv_b"]
		elif indexes:
			rs_ts = dvs_ts * tc["conv_k"] + tc["conv_b"]
	return rs_ts


## Converts DVS native timestamp(s) to Lidar native timestamp(s).
#
#  @type dvs_ts: float | numpy array
#  @param dvs_ts: DVS native timestamp(s)
#
#  @rtype: float | numpy array
#  @return: lidar native timestamp(s) as the same data type value(s)
def convert_dvs_to_lidar(dvs_ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	is_numpy_array = (type(dvs_ts) is np.ndarray)
	if is_numpy_array:
		lidar_ts = np.full_like(dvs_ts, 0)
	else:
		lidar_ts = None
	# converting
	for tc in timeconvs["dvs_to_lidar"]:
		interval = tc["interval"]
		if tc["inner"]:
			indexes = (dvs_ts > interval[0]) & (dvs_ts <= interval[1])
		elif interval[0] is None:
			indexes = (dvs_ts <= interval[1])
		elif interval[1] is None:
			indexes = (dvs_ts > interval[0])
		else:
			raise RuntimeError
		if is_numpy_array:
			lidar_ts[indexes] = dvs_ts[indexes] * tc["conv_k"] + tc["conv_b"]
		elif indexes:
			lidar_ts = dvs_ts * tc["conv_k"] + tc["conv_b"]
	return lidar_ts


## Converts DVS native timestamp(s) to relative.
#
#  @type ts: float | numpy array
#  @param ts: DVS native timestamp(s)
#
#  @rtype: float | numpy array
#  @return: DVS relative timestamp(s) as the same data type value(s)
def dvs_native_to_relative(ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	return ts * timeconvs["dvs_timestamp_scale"] - timeconvs["dvs_offset_s"]


## Converts DVS relative timestamp(s) to native.
#
#  @type ts: float | numpy array
#  @param ts: DVS relative timestamp(s)
#
#  @rtype: float | numpy array
#  @return: DVS native timestamp(s) as the same data type value(s)
def dvs_relative_to_native(ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	return (ts + timeconvs["dvs_offset_s"]) / timeconvs["dvs_timestamp_scale"]


## Converts Lidar native timestamp(s) to relative.
#
#  @type ts: float | numpy array
#  @param ts: lidar native timestamp(s)
#
#  @rtype: float | numpy array
#  @return: lidar relative timestamp(s) as the same data type value(s)
def lidar_native_to_relative(ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	return ts * timeconvs["lidar_timestamp_scale"] - timeconvs["lidar_offset_s"]


## Converts Lidar relative timestamp(s) to native.
#
#  @type ts: float | numpy array
#  @param ts: lidar relative timestamp(s)
#
#  @rtype: float | numpy array
#  @return: lidar native timestamp(s) as the same data type value(s)
def lidar_relative_to_native(ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	return (ts + timeconvs["lidar_offset_s"]) / timeconvs["lidar_timestamp_scale"]


## Converts Realsense native timestamp(s) to relative.
#
#  @type ts: float | numpy array
#  @param ts: realsense native timestamp(s)
#
#  @rtype: float | numpy array
#  @return: realsense relative timestamp(s) as the same data type value(s)
def rs_native_to_relative(ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	return ts * timeconvs["rs_timestamp_scale"] - timeconvs["rs_offset_s"]


## Converts Realsense relative timestamp(s) to native.
#
#  @type ts: float | numpy array
#  @param ts: realsense relative timestamp(s)
#
#  @rtype: float | numpy array
#  @return: realsense native timestamp(s) as the same data type value(s)
def rs_relative_to_native(ts):
	if not TIMECONVS:
		raise RuntimeError
	timeconvs = TIMECONVS
	return (ts + timeconvs["rs_offset_s"]) / timeconvs["rs_timestamp_scale"]

