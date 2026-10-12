#! /usr/bin/python
# coding: utf-8
import numpy as np

import pandas as pd
import os
import glob
import shutil

data_dir='/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/DWD-Referenz-Ensembles_v2026/data/CORDEX-ADJUST-INTERP-CMIP6/bias-adjusted-interpolated/HYR-LAEA-5/'
data_out_dir='/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/DWD-Referenz-Ensembles_v2026/data/copy_CORDEX-ADJUST-INTERP-CMIP6/tas'

os.makedirs(data_out_dir, exist_ok=True)

for f in glob.glob(os.path.join(data_dir, '*/*/*/*/*/*/*/*/tas/*/*.nc')):
    # old and new filename
    new_file = os.path.join(
        data_out_dir,
        os.path.basename(f).replace("MBCn-PCA_day", "day")
        )

    shutil.copy2(f, new_file)


    print(f"Written: {new_file}")


data_dir='/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/DWD-Referenz-Ensembles_v2026/data/CORDEX-ADJUST-INTERP-CMIP6/bias-adjusted-interpolated/HYR-LAEA-5/'
data_out_dir='/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/DWD-Referenz-Ensembles_v2026/data/copy_CORDEX-ADJUST-INTERP-CMIP6/pr'

os.makedirs(data_out_dir, exist_ok=True)

for f in glob.glob(os.path.join(data_dir, '*/*/*/*/*/*/*/*/pr/*/*.nc')):
    # old and new filename                                                                                                                                                   
    newfile = os.path.join(
        data_out_dir,
        os.path.basename(f).replace("IDW-QDM_day", "day")
        )

    shutil.copy2(f, newfile)


    print(f"Written: {new_file}")
