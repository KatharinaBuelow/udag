#! /usr/bin/python
# coding: utf-8
import numpy as np

import pandas as pd
import os
import glob
import xarray as xr

#home=os.getcwd()
data_dir='/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/ESGF_ClimatePredictionsDE/tas'
data_out_dir='/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/copy_ESGF_ClimatePredictionsDE/tas'

os.makedirs(data_out_dir, exist_ok=True)

for f in glob.glob(os.path.join(data_dir, '*.nc')):
    # old and new filename
    new_file = os.path.join(
        data_out_dir,
        os.path.basename(f).replace("tasAdjustInterp", "tas")
        )

    # open dataset
    ds = xr.open_dataset(f)

    # rename variable
    ds = ds.rename({"tasAdjustInterp": "tas"})

    # save with new filename
    ds.to_netcdf(new_file)

    print(f"Written: {new_file}")
