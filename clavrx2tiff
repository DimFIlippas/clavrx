# -*- coding: utf-8 -*-

import glob
import os
import sys
import gdal
import argparse
import numpy as np
import subprocess
from pyhdf.SD import SD, SDC
from geoimread import geoimread
from geoimwrite import geoimwrite

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def remove_by_ext(PathOfImages, extension):
    for root, dirnames, filenames in os.walk(PathOfImages):
        for filename in filenames:
            if filename.endswith(extension):
                os.remove(os.path.join(root, filename))

class Clavrx(object):
        
        def createVrt(self, ):
                
                self.fn_vrt = '.'.join(self.file_name.split('.')[0:-1]) + '.vrt'
                self.gm_vrt = '.'.join(self.gmtco.split('.')[0:-1]) + '.vrt'
                
                # set gdal_translate command and execute
                cmd_fn_vrt = 'gdal_translate -of VRT HDF4_SDS:UNKNOWN:' + os.path.join(self.WorkPath, self.file_name) + \
                                ':' + self.code +' ' + os.path.join(self.WorkPath, self.fn_vrt)
                
                self.res1 = os.system(cmd_fn_vrt)
                
                cmd_gm_vrt = 'gdal_translate -of VRT HDF5:' + os.path.join(self.WorkPath, self.gmtco) + \
                                '://All_Data/VIIRS-MOD-GEO-TC_All/Longitude ' + os.path.join(self.WorkPath, self.gm_vrt)
                
                self.res2 = os.system(cmd_gm_vrt)
                
                rA = gdal.Open(self.fn_vrt)
                self.fn_cols = rA.GetRasterBand(1).ReadAsArray().shape[0]
                
                rB = gdal.Open(self.gm_vrt)
                self.gm_cols = rB.GetRasterBand(1).ReadAsArray().shape[0]
                
                self.scale = str(self.gm_cols / float(self.fn_cols))
                
        def fixVrt(self, ):
                if self.res1 == 0:
                        # open vrt file
                        in_file = open(self.fn_vrt, "rt")
                        # read the entire file into a string variable
                        contents = in_file.read()
                        # find substring that is going to be replaced
                        erase = find_between(contents, "</Metadata>", "<VRTRasterBand")
                        # set substring
                        rplc = """ 
                        <Metadata domain="GEOLOCATION">
                        <MDI key="LINE_OFFSET">1</MDI>
                        <MDI key="LINE_STEP">::scale</MDI>
                        <MDI key="PIXEL_OFFSET">1</MDI>
                        <MDI key="PIXEL_STEP">::scale</MDI>
                        <MDI key="SRS">GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,""" + \
                        """AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],""" + \
                        """UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]</MDI>
                        <MDI key="X_BAND">1</MDI>
                        <MDI key="X_DATASET">HDF5:""" + os.path.join(self.WorkPath, self.gmtco) + """://All_Data/VIIRS-MOD-GEO-TC_All/Longitude</MDI>
                        <MDI key="Y_BAND">1</MDI>
                        <MDI key="Y_DATASET">HDF5:""" + os.path.join(self.WorkPath, self.gmtco) + """://All_Data/VIIRS-MOD-GEO-TC_All/Latitude</MDI>
                        </Metadata>"""
                        rplc = rplc.replace('::scale',self.scale)
                        # replace substring
                        contents = contents.replace(erase, rplc)
                        in_file.close()
                        # write string to vrt file
                        fvrt = open(self.fn_vrt, "w")
                        fvrt.write(contents)
                        fvrt.close()
                
        def Createtif(self, ):
                self.fn_tif = '.'.join(self.file_name.split('.')[0:-1]) + '.tif'
                # set gdalwarp command and execute
                cmd_wr = 'gdalwarp -ot Float32 -geoloc -t_srs EPSG:4326  -overwrite ' + os.path.join(self.WorkPath,self.fn_vrt) + ' ' + os.path.join(self.OutPath,self.fn_tif)
                
                proc   = subprocess.Popen(cmd_wr, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
                stdout,stderr = proc.communicate()
                
                if stderr:
                    self.scale = str(1)
                    self.fixVrt()
                    cmd_wr = 'gdalwarp -co compress=LZW -ot Float32 -geoloc -t_srs "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs" -overwrite ' + os.path.join(self.WorkPath,self.fn_vrt) + ' ' + os.path.join(self.OutPath,self.fn_tif)
                    os.system(cmd_wr)
                else:
                    cmd_wr = 'gdalwarp -co compress=LZW -ot Float32 -geoloc -t_srs "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs" -overwrite ' + os.path.join(self.WorkPath,self.fn_vrt) + ' ' + os.path.join(self.OutPath,self.fn_tif)
                    os.system(cmd_wr)
                    
        def Correcttif(self, ):
            image   = geoimread(os.path.join(self.OutPath,self.fn_tif))
            hdf     = SD(os.path.join(self.WorkPath,self.file_name), SDC.READ)
            hdf_dic = hdf.datasets()
            cld_obj = hdf.select(self.product)
            self.min,self.max  = cld_obj.attributes()['actual_range']
            min = image[0].min()
            max = image[0].max()
            nimage = np.interp(image[0], (min, max), (self.min,self.max))
            geoimwrite(os.path.join(self.OutPath,self.fn_tif),nimage,image[1],image[2],image[3])
            
        def __init__(self,WorkPath,OutPath,product):
            self.WorkPath = WorkPath
            self.OutPath  = OutPath
            self.product  = product
                
def main(argv):
    argparser  = argparse.ArgumentParser()
    
    argparser.add_argument("-w", "--workpath", type=str,required=True, default=None, help="workpath folder")
    argparser.add_argument("-o", "--output"  , type=str,required=True, default=None, help="output path folder")
    argparser.add_argument("-p", "--product" , type=str,required=True, default="cld_height_acha", help="desired product")
    args  = argparser.parse_args(argv[1:])
    
    WorkPath  = args.workpath
    OutPath   = args.output
    product   = args.product
    clavrxObj = Clavrx(WorkPath,OutPath,product)
    
    if clavrxObj.product == 'cld_height_acha':
        clavrxObj.code = '53'
    else:
        print "error product"

    os.chdir(clavrxObj.WorkPath)
    clavrxObj.file_name = ''.join(glob.glob('clavrx_*.hdf'))
    clavrxObj.gmtco     = ''.join(glob.glob('GMTCO*.h5'))
    if clavrxObj.file_name:
        clavrxObj.createVrt()
        clavrxObj.fixVrt()
        clavrxObj.Createtif()
        clavrxObj.Correcttif()
    else:
        exit()
    # Remove xml files
    extension = ['.xml', '.vrt']
    remove_by_ext(clavrxObj.WorkPath, extension[0])
    remove_by_ext(clavrxObj.WorkPath, extension[1])
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))
