import glob
import re
import csv
#for August list all airport
directory_path='/Users/quranworks/PycharmProjects/Weather/data/'
out_path='/Users/quranworks/PycharmProjects/Weather/data/output/'
meta_data=[]
meta_data.append({"month":5,"data_folder":"Jun_1_2015"})
meta_data.append({"month":6,"data_folder":"Jun_30_2015"})
meta_data.append({"month":7,"data_folder":"Aug_1_2015"})
meta_data.append({"month":8,"data_folder":"Sep_1_2015"})
meta_data.append({"month":9,"data_folder":"Oct_1_2015"})
meta_data.append({"month":10,"data_folder":"Oct_4_2015"})
header="airport,date,day,month,year,temp_max,temp_min,temp_avg,temp_dep,temp_hdd,temp_cdd,water," \
       "Snow,snow_depth,wind_speed_avg,wind_speed_max,wind_dir,sunshine_min,sunshine_percent,sky_cover,weather_type,wind_highest_speed,wind_highest_dir"
year=2015
airport_file_ext='_daily.txt'
all_data=[]

for meta in meta_data:
    folder_name=meta['data_folder']
    month=meta['month']
    out_data_rows=[]
    full_directory_path=directory_path+folder_name+'/'
    airports_files=glob.glob(full_directory_path+'*'+airport_file_ext)
    for airport_file in airports_files:
        airport_name=airport_file.replace(full_directory_path,"")
        airport_name=airport_name.replace(airport_file_ext,"")
        if len(airport_name) ==3:
            with open(airport_file) as f:
                lines = f.readlines()
                line_is_header=True
                for line in lines:
                    line=line.replace('        ',' M ')
                    line=line.replace('\n','')
                    line=re.sub(' +', ' ', line)
                    if line_is_header:
                        line_is_header=False
                        continue
                    data_fields=line.split(" ")
                    day=data_fields[1]
                    out_data_row=[airport_name,str(month)+'-'+str(day)+'-'+str(year),str(day),str(month),str(year)]+data_fields[2:]
                    out_data_rows.append(','.join(out_data_row))


    import os

    out_path_file=os.path.join(out_path,str(month)+'-'+str(year)+'.csv')

    f = open(out_path_file, 'w+')
    content="\n".join(out_data_rows)
    f.write(header+"\n"+content)  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    all_data.append(content)

out_path_file=os.path.join(out_path,'all.csv')
f = open(out_path_file, 'w+')
f.write(header+"\n"+"\n".join(all_data))  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it