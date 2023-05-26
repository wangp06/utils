from pyproj import Proj
import cartopy.crs as ccrs
import numpy as np
    
def trans_lcc_to_utm(lon_array,lat_array, zone):
    '''
    using cartopy to transform lcc to utm
    '''
    latlon = ccrs.PlateCarree()
    utm = ccrs.UTM(zone)
    UTM_array = utm.transform_points(latlon, np.array(lon_array), np.array(lat_array))

    utm_x =[]
    utm_y = []
    for i in range(UTM_array.shape[0]):
        utm_x.append(UTM_array[i][0]/1000)
        utm_y.append(UTM_array[i][1]/1000)

    return utm_x,utm_y

def transform_utm_into_lat_lon(utm_x, utm_y, zone, hemisphere):
    '''using the pyproj to transform utm to lcc'''
    # verify the hemisphere
    h_north = False
    h_south = False
    if (hemisphere == 'N'):
        h_north = True
    elif (hemisphere == 'S'):
        h_south = True
    else:
        print("Unknown hemisphere: " + hemisphere)
    proj_in = Proj(proj = 'utm', zone = zone, ellps = 'WGS84', south = h_south, north = h_north, errcheck = True)
    Lon = [];Lat = []
    for i in range(len(utm_y)):
        lon, lat = proj_in(utm_x[i], utm_y[i], inverse = True)
        # just printing the floating point number with 6 decimal points will round it
        lon = np.floor(lon * 1000000) / 1000000
        lat = np.floor(lat * 1000000) / 1000000
        Lon.append(lon);Lat.append(lat)
    return Lon, Lat

if __name__ == '__main__':
    lon = [120.874, 121.908]; lat = [30.634, 31.549] #经纬度
    xx = [605514.0,1555514.0]; yy = [3693392.1,4603392.1] #UTM坐标，单位m
    #时区计算方式:zone = int(lonmin/6)+31 ,lonmin,经度数组的最小值
    UTM_x, UTM_y = trans_lcc_to_utm(lon, lat, 51)
    LON, LAT = transform_utm_into_lat_lon(xx, yy, 48, 'N')