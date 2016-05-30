
def get_intellicast_forcast_error():
    all_data = {}
    with open("./data/output.csv") as airports_file:
        data = airports_file.readlines()
        for line in data[1:]:
            line = line.replace("\n", "")
            features = line.split(',')
            if features[1] != "6-31-2015" and features[1] != "9-31-2015":
                all_data[features[0] + '_' + features[1]] = features[5:7]
    c=0
    with open("./data/all_Intellicast.csv") as airports_file:
        data = airports_file.readlines()
        for line in data[1:]:
            line = line.replace("\n", "")
            features = line.split(',')
            inc= ((features[0] + '_' + features[1]) in all_data)
            if features[1] != "6-31-2015" and features[1] != "9-31-2015" and inc:
                error_max= abs(float(features[5]) - float(all_data[features[0] + '_' + features[1]][0]))
                error_min= abs(float(features[6]) - float(all_data[features[0] + '_' + features[1]][1]))
                c+=1
    return error_min/c , error_max/c


print( get_intellicast_forcast_error())