# SloughFinder
Personal Project

#Install Pip and dependencies
python -m pip install --upgrade pip

cd ./deps
python -m pip install GDAL-3.0.4-cp36-cp36m-win_amd64.whl
python -m pip install rasterio-1.1.3-cp36-cp36m-win_amd64.whl
python -m pip install -r requirments.txt


#Sentinel 2 file naming conventions:
MMM_MSIXXX_YYYYMMDDHHMMSS_Nxxyy_ROOO_Txxxxx_<Product Discriminator>.SAFE

The products contain two dates.

The first date (YYYYMMDDHHMMSS) is the datatake sensing time.
The second date is the "<Product Discriminator>" field, which is 15 characters in length, and is used to distinguish between different end user products from the same datatake. Depending on the instance, the time in this field can be earlier or slightly later than the datatake sensing time.

The other components of the filename are:

MMM: is the mission ID(S2A/S2B)
MSIXXX: MSIL1C denotes the Level-1C product level/ MSIL2A denotes the Level-2A product level
YYYYMMDDHHMMSS: the datatake sensing start time
Nxxyy: the PDGS Processing Baseline number (e.g. N0204)
ROOO: Relative Orbit number (R001 - R143)
Txxxxx: Tile Number field
SAFE: Product Format (Standard Archive Format for Europe)


#Sentinel 2 Band Combinations:
https://gisgeography.com/sentinel-2-bands-combinations/

Natural Color (B4, B3, B2)
Color Infrared (B8, B4, B3) near-infrared (B8) band, it’s especially good at reflecting chlorophyl
Short-Wave Infrared (B12, B8A, B4) SWIR (B12), NIR (B8A) and red (B4)
Agriculture (B11, B8, B2) SWIR-1 (B11), near-infrared (B8) and blue (B2)
Geology (B12, B11, B2) SWIR-2 (B12), SWIR-1 (B11) and blue (B2) 
Bathymetric (B4, B3, B1) red (B4), green (B3) and coastal band (B1)
Vegetation Index (B8-B4)/(B8+B4) While high values suggest dense canopy, low or negative values indicate urban and water features
Moisture Index (B8A-B11)/(B8A+B11) The moisture index is ideal for finding water stress in plants. It uses the short-wave and near infrared to generate an index of moisture content. In general, wetter vegetation have higher values. But lower moisture index values suggests plants are under stress from insufficient moisture.


#Some extra data processing
https://earth.esa.int/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm


#Some information about the data
https://earth.esa.int/web/sentinel/technical-guides/sentinel-2-msi/products-algorithms

Level-0 is compressed raw data. The Level-0 product contains all the information required to generate the Level-1 (and upper) product levels.

Level-1A is uncompressed raw data with spectral bands coarsely coregistered and ancillary data appended.

Level-1B data is radiometrically corrected radiance data. The physical geometric model is refined using available ground control points and appended to the product, but not applied.

Note: Level-0, Level-1A and Level-1B products are not disseminated to users.

Level-1C product provides orthorectified Top-Of-Atmosphere (TOA) reflectance, with sub-pixel multispectral registration. Cloud and land/water masks are included in the product.

Level-2A product provides orthorectified Bottom-Of-Atmosphere (BOA) reflectance, with sub-pixel multispectral registration. A Scene Classification map (cloud, cloud shadows, vegetation, soils/deserts, water, snow, etc.) is included in the product.

Level-1C and Level-2A products are made available to users via the Copernicus Open Access Hub (SciHub).

