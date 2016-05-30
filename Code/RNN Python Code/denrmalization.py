from __future__ import division
import math
import csv

temp_max_mean=   83.0358963578
temp_min_mean=  60.7109040875
temp_avg_mean=  72.1225454099
temp_dep_mean=  1.74964280645
temp_hdd_mean=  1.79568167473
temp_cdd_mean=  8.93318781121
water_mean=  0.118031140919
Snow_mean=  0.000979428531782
snow_depth_mean=  0.0499701786984
wind_speed_avg_mean = 7.16709240452
wind_speed_max_mean= 17.6919828636
wind_dir_mean= 193.354635219
sunshine_min_mean=  373.130671506
sunshine_percent_mean=  37.114213198
sky_cover_mean=  3.15486579429
weather_type_mean=  26.0728058331
wind_highest_speed_mean=  25.0287976896
wind_highest_dir_mean=  194.057370902
temp_max_sigma=   11.3946206303
temp_min_sigma=  11.3053504855
temp_avg_sigma=  10.5574198077
temp_dep_sigma=  5.51593475796
temp_hdd_sigma=  4.60647631426
temp_cdd_sigma=  8.55075319869
water_sigma=  0.360292065315
Snow_sigma=  0.0667633770642
snow_depth_sigma=  7.90059067265
wind_speed_avg_sigma = 3.36565059886
wind_speed_max_sigma= 6.51239702782
wind_dir_sigma=  95.6387712393
sunshine_min_sigma=  286.45803876
sunshine_percent_sigma=  33.9492701717
sky_cover_sigma = 2.92997326034
weather_type_sigma=  145.268425937
wind_highest_speed_sigma=  17.9919668708
wind_highest_dir_sigma=  95.6507483657

temp_max_min=   -27.0
temp_min_min=  -47.0
temp_avg_min=  -34.0
temp_dep_min=  -77.0
temp_hdd_min=  0.0
temp_cdd_min=  0.0
water_min=  0.0
Snow_min=  0.0
snow_depth_min=  0.0
wind_speed_avg_min = 0.0
wind_speed_max_min= 0.0
wind_dir_min=  0.0
sunshine_min_min=  0.0
sunshine_percent_min=  0.0
sky_cover_min=  0.0
weather_type_min=  1.0
wind_highest_speed_min=  0.0
wind_highest_dir_min=  0.0
temp_max_max=   119.0
temp_min_max=  96.0
temp_avg_max=  105.0
temp_dep_max=  26.0
temp_hdd_max=  99.0
temp_cdd_max=  1212.1
water_max=  9.91
Snow_max=  11.2
snow_depth_max=  1854.9
wind_speed_avg_max = 76.0
wind_speed_max_max= 330.0
wind_dir_max=  360.0
sunshine_min_max=  909.0
sunshine_percent_max=  100.0
sky_cover_max=  110.0
weather_type_max=  12468.0
wind_highest_speed_max=  360.0
wind_highest_dir_max=  999.0


def minmax(arg,min,max):
     result = ((arg + 1)/2)*(max-min) + min 
     return result

def zscore(arg, mean,sigma):
     result = arg*sigma + mean
     return result

#example
# print(minmax(0.004, temp_max_min, temp_max_max))
# print(zscore(0.17, temp_max_mean,temp_max_sigma))

