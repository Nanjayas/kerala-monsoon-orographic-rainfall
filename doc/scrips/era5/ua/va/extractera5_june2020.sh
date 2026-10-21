#!/bin/bash
# ERA5 wind extraction for Kerala — June 2020
# Run on an authorised server with access to the ERA5 archive.
# Requires CDO and an existing ~/kerala_project/data/era5 directory.
cdo sellonlatbox,72,79,7,14 /daten/erafive/arch/data/dkrz-sync/ERA5/1hr/atmos/ua/r1i1p1-070000Pa/ua_1hr_reanalysis_era5_r1i1p1-070000Pa_20200601-20200630.nc ~/kerala_project/data/era5/ua_700hPa_kerala_202006.nc
cdo sellonlatbox,72,79,7,14 /daten/erafive/arch/data/dkrz-sync/ERA5/1hr/atmos/va/r1i1p1-070000Pa/va_1hr_reanalysis_era5_r1i1p1-070000Pa_20200601-20200630.nc ~/kerala_project/data/era5/va_700hPa_kerala_202006.nc
