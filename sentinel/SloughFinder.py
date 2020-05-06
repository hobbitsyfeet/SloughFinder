from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import rasterio as rio
from rasterio import plot
from rasterio.plot import show
import matplotlib.pyplot as plt
from matplotlib import pyplot
from os import listdir
from os.path import isfile, join
import os
import numpy as np

import images_processing as img
from DownloadData import current_data

'''
How are the values calculated within Sentinel Hub and how are they returned as an output?
    if format is 32-bit float, it is 0-1
    if format is 16-bit, it is 0-65535; 0 -> 0 and 1 -> 65535
    if format is 8-bit, it is 0-255; 0 -> 0 and 1 -> 255
    
    Note: The valid range for imshow with RGB data ([0..1] for floats or [0..255] for integers).
'''
def choose_data(newest=True):
    data_dict = current_data(False)
    print("Choose your data by entering the cooresponding number:")
    count = 1
    for data in data_dict:
        print(str(count) + ")" , data_dict[data])
        count+=1  
    
    select = int(input())
    
    print("You selected", list(data_dict.keys())[select-1])
    return list(data_dict.keys())[select-1]

def get_band(folder,band_num):
    band_files = [f for f in listdir(folder) if isfile(join(folder, f))]

    for band in band_files:
        temp_band = band[-6:-4]
        if str(band_num) == temp_band:
            print("Getting Band", band)
            return band

def save_nir(Folder):

    b8 = rio.open(Folder+get_band(Folder,"04"))

    # read Red(b4) and NIR(b8) as arrays
    nir = b8.read()

    # Calculate ndvi
    nir = nir.astype(float)

    # nir = rio.plot.adjust_band(nir, kind='linear')
    nir = nir/65536
    # Write the NDVI image
    meta = b8.meta
    meta.update(driver='GTiff')
    meta.update(dtype=rio.float32)

    with rio.open('NIR.tiff', 'w', **meta) as dst:
        dst.write(nir.astype(rio.float32))


def save_rgb(Folder):
    red = rio.open(Folder+get_band(Folder,"04"))
    green = rio.open(Folder+get_band(Folder,"03"))
    blue = rio.open(Folder+get_band(Folder,"02"))

    #number of raster bands
    b4 = blue
    b4.count
    #number of raster columns
    b4.width
    #number of raster rows
    b4.height
    # #plot band 
    #type of raster byte
    b4.dtypes[0]
    #raster sytem of reference
    b4.crs
    #raster transform parameters
    b4.transform

    #raster values as matrix array
    # b4.read(1)

    red = red.read(1)
    green = green.read(1)
    blue = blue.read(1)


    red_max = max(np.amax(red, axis=1))
    red_min = min(np.amin(red,axis=1))
    green_max = max(np.amax(green, axis=1))
    green_min = min(np.amin(green,axis=1))
    blue_max = max(np.amax(blue,axis=1))
    blue_min = min(np.amin(blue,axis=1))
    #Scale it to [0,1]
    #((Input - InputLow) / (InputHigh - InputLow))
    #      * (OutputHigh - OutputLow) + OutputLow
    # red=((red-red_min)/(65535-red_min))*255 + 255
    # green = ((green-green_min)/(65535-green_min))*255 + 255
    # blue = ((blue-blue_min)/(65535-blue_min))*255 + 255
    red = rio.plot.adjust_band(red)*255
    green = rio.plot.adjust_band(green)*255
    blue = rio.plot.adjust_band(blue)*255

    red = img.exposure(red, 2)
    green = img.exposure(green,2)
    blue = img.exposure(blue,2)
    #Linearly scale brightness
    #rgb = (red+green+blue)/3
    

    # rgb_max = max(np.amax(rgb, axis=1))
    # rgb_min = min(np.amin(rgb, axis=1))

    # rgb = ((rgb-0)/(255-0))
    # print(rgb)
    # red = red+(rgb*255)*1.5
    # blue = blue+(rgb*255)*1.5
    # green = green + (rgb*255)*1.5



    red = np.clip((red), 1, 255).astype(np.uint8)
    blue = np.clip((blue), 1, 255).astype(np.uint8)
    green = np.clip((green), 1, 255).astype(np.uint8)

    red_max = max(np.amax(red, axis=1))
    red_min = min(np.amin(red,axis=1))

    with rio.open('RGB.tiff','w',driver='Gtiff', width=b4.width, height=b4.height, 
                count=3,transform=b4.transform, dtype=rio.uint8) as rgb:
        rgb.write(red,1)
        rgb.write(green,2)
        rgb.write(blue,3)
        rgb.close()

def save_soil_moisture(Folder):
    """
    The moisture index is ideal for finding water stress in plants. 
    It uses the short-wave and near infrared to generate an index of moisture content. 
    In general, wetter vegetation have higher values. But lower moisture index values suggests plants are 
    under stress from insufficient moisture.
    """

    b8a = rio.open(Folder+get_band(Folder,"8A"))
    b11 = rio.open(Folder+get_band(Folder,"11"))

    nir = b8a.read()
    swir1 = b11.read()

    nmi = (nir.astype(float) - swir1.astype(float))/(nir+swir1)
        # Write the NDVI image
    meta = b8a.meta
    meta.update(driver='GTiff')
    meta.update(dtype=rio.float32)
    meta.update(crs=b8a.crs)
    meta.update(transform=b8a.transform)
    meta.update(width=b8a.width, height=b8a.height)

    with rio.open('NMI.tif', 'w', **meta) as dst:
        dst.write(nmi.astype(rio.float32))

        
def save_ndwi(Folder):
    # Open b4 and b8
    b4 = rio.open(Folder+get_band(Folder,"03"))
    b8 = rio.open(Folder+get_band(Folder,"08"))

    # read Red(b4) and NIR(b8) as arrays
    green = b4.read()
    nir = b8.read()

    # Calculate ndvi
    ndwi = (green.astype(float)-nir.astype(float))/(green+nir)

    # Write the NDVI image
    meta = b4.meta
    meta.update(driver='GTiff')
    meta.update(dtype=rio.float32)

    with rio.open('Agriculture.tiff','w',driver='Gtiff', width=b4.width, height=b4.height,crs=b4.crs, 
            count=3,transform=b4.transform, dtype=rio.float32) as dst:
        dst.write(ndwi.astype(rio.float32))

def save_agriculture(Folder):

    b2 = rio.open(Folder+get_band(Folder,"02"))
    b8 = rio.open(Folder+get_band(Folder,"08"))
    b11 = rio.open(Folder+get_band(Folder,"11"))
    
    b2.count
    #number of raster columns
    b2.width
    #number of raster rows
    b2.height
    # #plot band 
    #type of raster byte
    b2.dtypes[0]
    #raster sytem of reference
    b2.crs
    #raster transform parameters
    b2.transform

    blue = b2.read(1)
    nir = b8.read(1)
    swir1 = b11.read(1)

    #Adjust the bands to a normalized range between 0 and 1, then back to a 0-255 range.
    blue = rio.plot.adjust_band(blue)*255
    nir = rio.plot.adjust_band(nir)*255
    swir1 = rio.plot.adjust_band(swir1)*255

    #Clip it!
    blue = np.clip((blue), 1, 255).astype(np.uint8)
    nir = np.clip((nir), 1, 255).astype(np.uint8)
    swir1 = np.clip((swir1), 1, 255).astype(np.uint8)

    with rio.open('Agriculture.tiff','w',driver='Gtiff', width=b2.width, height=b2.height,crs=b2.crs, 
            count=3,transform=b2.transform, dtype=rio.uint8) as false_rgb:
        false_rgb.write(swir1,1)
        false_rgb.write(nir,2)
        false_rgb.write(blue,3)
        false_rgb.close()




if __name__ == "__main__":
        
    subfolders = [ f.path for f in os.scandir("./") if f.is_dir() ]

    # Open Bands 4, 3 and 2 with rio
    home_folder=choose_data(newest=True)
    data_folder = home_folder+".SAFE/" + "GRANULE/"
    data_folder += next(os.walk(data_folder))[1][0] + "/IMG_DATA/"



    select = ""
    while(select != "q"):
        print("Done.")
        print("Select an image to view:")
        print("1) Regular (RGB)")
        print("2) NDVI (Vegetation)")
        print("3) NDWI (Standing Water")
        print("4) Soild Moisture")
        print("5) Agriculture False Colour")
        
        if select=="1":
            save_rgb(data_folder)
        elif select == "2":
            save_nir(data_folder)
        elif select =="3":
            save_ndwi(data_folder)
        elif select == "4":
            save_soil_moisture(data_folder)
        elif select == "5":
            save_agriculture(data_folder)

        select = input()
        


    # src = rio.open("RGB.tiff")
    # show(src.read(), transform=src.transform)
    #multiple band representation
    #export true color image
    # red = rio.open('./red.tiff', 'w', driver="Gtiff", width=b4.width, height=b4.height,dtype=b4.dtypes[0],crs=b4.crs,transform=b4.transform,count=3) 
    # red.write(b4.read(1)/10000,1)
    # red.close()
    # trueColor = rio.open('./SentinelTrueColor2.tiff','w',driver='Gtiff',
    #                          width=b4.width, height=b4.height,
    #                          count=3,
    #                          crs=b4.crs,
    #                          transform=b4.transform,
    #                          dtype="float64"
    #                          )
    # trueColor.write((b4.read(1)/10000),1) #blue

    # trueColor.write((b3.read(1)/10000),2) #green
    # trueColor.write((b4.read(1)/10000),3) #red
    # trueColor.close()
    # Create an RGB image 

    # meta = b4.meta
    # meta.update(driver='GTiff')
    # meta.update(dtype=rio.float32)



    # nReserve_proj = nReserve.to_crs({'init': 'epsg:32633'})

    # with rio.open("RGB.tiff") as src:
    #     out_image, out_transform = rio.mask.mask(src, nReserve_proj.geometry,crop=True)
    #     out_meta = src.meta.copy()
    #     out_meta.update({"driver": "GTiff",
    #                  "height": out_image.shape[1],
    #                  "width": out_image.shape[2],
    #                  "transform": out_transform})
        
    # with rio.open("RGB_masked.tif", "w", **out_meta) as dest:
    #     dest.write(out_image)

    # Open b4 and b8

    # def view_ndvi():
    #     # Open b4 and b8
    #     b4 = rio.open(Folder+'/T33TTG_20190605T100039_B04_10m.jp2')
    #     b8 = rio.open(Folder+'/T33TTG_20190605T100039_B08_10m.jp2')

    #     # read Red(b4) and NIR(b8) as arrays
    #     red = b4.read()
    #     nir = b8.read()

    #     # Calculate ndvi
    #     ndvi = (nir.astype(float)-red.astype(float))/(nir+red)

    #     # Write the NDVI image
    #     meta = b4.meta
    #     meta.update(driver='GTiff')
    #     meta.update(dtype=rio.float32)

    #     with rio.open('NDVI.tif', 'w', **meta) as dst:
    #         dst.write(ndvi.astype(rio.float32))
