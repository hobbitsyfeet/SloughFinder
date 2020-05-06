from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from collections import OrderedDict

from os import listdir
from os.path import isfile, join
import os



from zipfile import ZipFile

def current_data(display=True):
    onlyfiles = [f for f in listdir("./") if isfile(join('./', f))]
    zips = []
    for file in onlyfiles:
        if file[-3:] != "zip":
            del(file)
        else:
            zips.append(file)

    date_dict = {"01":"January",
                    "02":"Febuary",
                    "03":"March",
                    "04":"April",
                    "05":"May",
                    "06":"June",
                    "07":"July",
                    "08":"August",
                    "09":"September",
                    "10":"October",
                    "11":"November",
                    "12":"December"
    }

    if display:
        print("You currently have data from these dates:")
    data_dict = {}
    for file in zips:
        year = file[11:15]
        month = file[15:17]
        day = file[17:19]
        hour = file[20:22]
        minute = file[22:24]
        second = file[24:26]
        ampm = "AM"
        if int(hour) > 12:
            hour = int(hour) - 12
            ampm = "PM"
        date_str = year +" " + date_dict[str(month)] + " "+ day +" "+ str(hour)+":"+str(minute) +ampm

        name = file[:-4]
        data_dict[name] = date_str
        if display:
            print(date_str)

    


    return data_dict


def unzip_new(display=True):
    onlyfiles = [f for f in listdir("./") if isfile(join('./', f))]
    zips = []
    for file in onlyfiles:
        if file[-3:] != "zip":
            del(file)
        else:
            zips.append(file)
    if display:
        print("Checking...")
    #Check if the file has been unzipped
    folders = next(os.walk('.'))[1]
    for folder in folders:

        for zipped in zips:
            if folder[:-5] == zipped[:-4]:
                if display:
                    print("Already unzipped",zipped)
                zips.remove(zipped)

    if len(zips) > 0:
        if display:
            print("Unzipping new data...")
        for zipped in zips:
            if display:
                print(zipped)
            with ZipFile(zipped, 'r') as zipObj:
                if display:
                    print("Unzipping (" + zipped + ")")
                # Extract all the contents of zip file in current directory
                zipObj.extractall()
                if display:
                    print("Unzipping complete.")

if __name__ == "__main__":
    
    '''
    Sentinel-2 Level-1C is an orthoimage product, i.e. a map projection of the acquired image using a system DEM to correct ground geometric distortions. 
    Pixel radiometric measurements are provided in Top-Of-Atmosphere (TOA) reflectances (coded in 12 bits) with all parameters to transform them into radiances.
    '''
    '''
    https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/FullTextSearch?redirectedfrom=SciHubUserGuide.3FullTextSearch
    Possible values for for <producttype> are the following, listed per mission:

    Sentinel-1: SLC, GRD, OCN
    Sentinel-2: S2MSI2A,S2MSI1C, S2MS2Ap
    Sentinel-3: SR_1_SRA___, SR_1_SRA_A, SR_1_SRA_BS, SR_2_LAN___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_LST___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGP___.
    Sentinel-5P: L1B_IR_SIR, L1B_IR_UVN, L1B_RA_BD1, L1B_RA_BD2, L1B_RA_BD3, L1B_RA_BD4, L1B_RA_BD5, L1B_RA_BD6, L1B_RA_BD7, L1B_RA_BD8, L2__AER_AI, L2__AER_LH, L2__CH4, L2__CLOUD_, L2__CO____, L2__HCHO__, L2__NO2___, L2__NP_BD3, L2__NP_BD6, L2__NP_BD7, L2__O3_TCL, L2__O3____, L2__SO2___. 
    '''

    api = SentinelAPI('USERNAME', 'PASSWORD', 'https://scihub.copernicus.eu/dhus')

    if(api.query(date=('NOW-7DAYS', 'NOW'), producttype='SLC')):
        print("Successfuly logged in")

    current_data()

    tiles = ['11VMC']


    query_kwargs = {
            'platformname': 'Sentinel-2',
            'producttype': 'S2MSI1C', #NOTE this Sentinel 2 MSI level 1c.
            'date': ('NOW-7DAYS', 'NOW')}

    products = OrderedDict()

    for tile in tiles:
        kw = query_kwargs.copy()
        kw['tileid'] = tile
        pp = api.query(**kw)
        products.update(pp)

    #api.download_all(products)

    #footprint = geojson_to_wkt(read_geojson('./home.geojson'))
    #products = api.query(data,
    #                     producttype='SLC',
    #                     orbitdirection='ASCENDING')
    print("Total Products:", len(products))

    api.download_all(products)

    unzip_new()
