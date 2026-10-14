Welcome to DEUTSCHLAND ENSEMBLE:

The german weater service has two ensembles.

Stored locally on levante:

cmip6-foreced Ensemble:

       /work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/DWD-Referenz-Ensembles_v2026

cmip5-forced-Ensemble:

	/work/ch0636/eddy/pool/sims/DATEN_DEUTSCHLAND/ESGF_ClimatePredictionsDE


## Index Calculation
To work with index_calculation, we had to fix the naming of the files
	
	rename.py
	rename_cmip6.py
	rename_tas.py
	start_rename.sh
	start_rename_cmip6.sh
	start_rename_tas.sh

### Catalogue

The catalogues for each ensemble are stored here:

    /work/ch0636/g300047/UDAG/index_calculation

## Index calculation

Katharinas environment : indexcalculation13 (you just need to install index_calculation from gitlab in python3.13)

	index_calculation -p CORDEX-CMIP6 create_scripts -idx TG -intake /work/ch0636/g300047/UDAG/index_calculation/catalogue6/CORDEX-CMIP6.json -scrpt_dir /scratch/g/g300047/index_calculation -out_dir /work/ch0636/g300047/UDAG/index_calculation -ofreq year -submit

#### Results:

	/work/ch0636/g300047/UDAG/index_calculation


## Einzugsgebiete:

Shape files are in the directory:

Shapefiles_Nukleus

create environment from geo.yml

	conda env create -f geo.yml

Look at shapefile with:

	read_shapefile.ipynb
	
	
Für die Paper hatten wir genutzt:

	Wakos_Festland (Martina: Ostfriesland)
	Duisburg_3x3
	IAWAK-EE (Martina TSA: Türingen, Sachen Anhalt, Sachen  oder Weiße Elster)
	Klimakonform
	ISAP
	KARE

File:

	udag_regions.shp

 Zeitscheibe:
 
 	1971-2000
 	2040-2069
 	2070-2099

 Season, annual, 
 Change tas, pr [%]


