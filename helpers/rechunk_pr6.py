#! /usr/bin/python
# coding: utf-8

from pathlib import Path
import shutil
import subprocess
import xarray as xr

nccopy = shutil.which("nccopy") or shutil.which(
    "/sw/spack-levante/mambaforge-22.9.0-2-Linux-x86_64-kptncg/bin/nccopy"
)
if nccopy is None:
    raise FileNotFoundError(
        "nccopy wurde weder im PATH noch unter dem bekannten Systempfad gefunden."
    )

# das problem ist, das die Dateinen riesig sind und nicht zeitnah eingelesen werden konnten, 
# sie werden hier zerlegt, damit dask damit klar kommt

input_dir='/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/DWD-Referenz-Ensembles_v2026/data/copy_CORDEX-ADJUST-INTERP-CMIP6/pr'
output_dir='/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/DWD-Referenz-Ensembles_v2026/data/copy_CORDEX-ADJUST-INTERP-CMIP6/rechunked/pr'

input_dir = Path(input_dir)
output_dir = Path(output_dir)

output_dir.mkdir(exist_ok=True)

# Datei einen Tag pro Chunk bei vollständigem räumlichem Gitter nehmen

#for source in sorted(input_dir.glob("*pr_HYR-5_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1-DWD-MQDM-v1-DWD-PCA-v1_*.nc")):
for source in sorted(input_dir.glob("*.nc")):
    target = output_dir / source.name
    if target.exists():
        raise FileExistsError(f"Ausgabedatei existiert bereits: {target}")

    with xr.open_dataset(source, decode_times=False) as ds:
        chunks = f"time/1,y/{ds.sizes['y']},x/{ds.sizes['x']}"

    print(f"Verarbeite: {source.name}", flush=True)
    subprocess.run(
        [nccopy, "-d", "0", "-c", chunks, str(source), str(target)],
        check=True,
    )
