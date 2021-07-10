# georem_compile.py
# 
# A Python script for parsing *.csv data from the GeoReM database to find 
# reference values of geological standard reference materials (SRMs).
# 



# ======== ======== ======== ======== ======== ======== ======== ======== 
# user-specified parameters

# character denoting path separators in `*_directory`:
path_sep = "/"

# directory containing GeoReM data download file, omitting base path (`~`)
input_directory = "Downloads" # directory containing GeoReM data download

# data file name, with extension (currently must be `*.csv`)
input_filename = "georem_v30_published.csv"

# directory where compiled output should be saved, omitting base path
output_directory = "gh/pygpen"

# desired name of output file, with extension (currently must be `*.csv`)
output_filename = "georem_srm.csv"


# ======== ======== ======== ======== ======== ======== ======== ======== 
# main script


import os
import pandas as pd



# handle i/o paths:
home = os.path.expanduser("~")

# source in
data_source = home

for d in input_directory.split(path_sep):
	data_source = os.path.join(
		data_source, d
	)

data_source = os.path.join(
	data_source, input_filename
)

# destination out
data_destination = home

for d in output_directory.split(path_sep):
	data_destination = os.path.join(
		data_destination, d
	)

data_destination = os.path.join(
	data_destination, output_filename
)

# data i/o
srm_file = pd.read_csv(
	data_source,
	header=0, # assume 1st row headers
)

# parse data for sample names
srm_list = srm_file["Sample"].unique()

# find reference values for each SRM
ref_vals = []
for srm in srm_list:
	srm_values = srm_file.loc[
		(srm_file["Sample"] == srm) & \
		(srm_file["Origin"].str.lower() == "compiled") & \
		(srm_file["Analyses-Comment"].str.lower().str.contains("ref")), \
		:
	].values()

	if length(srm_values) == 1:
		ref_vals.append([srm_values]) # stash result

# compile data into dataframe
df = pd.DataFrame(
	ref_vals,
	columns=srm_file.columns.tolist(),
)

# save to file
df.to_csv(
	data_destination,
	index=False,
)


# 