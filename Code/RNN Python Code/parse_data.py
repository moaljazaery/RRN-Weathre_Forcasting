from datetime import date


def get_clusters():
    airports_clusters = {}
    with open("./data/air_cluster.csv") as airports_cluster:
        data = airports_cluster.readlines()
        for line in data:
            line = line.replace("\n", "")
            line = line.split(",")
            airports_clusters[line[0]] = int(line[1])
    return airports_clusters


#
# One time function
#

# def gen_new_test_data(TESTING_PERCENTAGE=0.1):
#     test = []
#     with open("./data/output.csv") as airports_file:
#         data = airports_file.readlines()
#         for line in data:
#             line = line.replace("\n", "")
#             features = line.split(',')
#             air_id = features[0]
#             if (features[1] != "6-31-2015" and features[1] != "9-31-2015"):
#                 r_num = random.uniform(0, 1)
#                 if r_num < TESTING_PERCENTAGE:
#                     test.append(str(air_id) + '_' + features[1])
#     with open('data/data_test_index.txt', 'w') as f:
#         for test_rec in test:
#             f.write(test_rec + "\n")


def get_test_indexes():
    test_indexes = []
    test_file = open("./data/data_test_index.txt")
    test_lines = test_file.readlines()
    for test_index in test_lines:
        test_index = test_index.replace("\n", "")
        test_indexes.append(test_index)
    return test_indexes


def parse_data(normalization='minmax'):
    airports_data = {}
    airports = []

    with open("./data/normalized_" + normalization + ".csv") as airports_file:
        data = airports_file.readlines()
        for line in data[1:]:
            line = line.replace("\n", "")
            features = line.split(',')
            air_id = features[0]
            if features[1] != "6-31-2015" and features[1] != "9-31-2015":
                if air_id not in airports:
                    airports.append(air_id)
                if airports_data.get(air_id, 0) == 0:
                    airports_data[air_id] = []
                airports_data[air_id].append(features)

    return airports, airports_data

def get_real_test_target(test_indexes):
    out = {}

    with open("./data/output.csv") as airports_file:
        data = airports_file.readlines()
        for line in data[1:]:
            line = line.replace("\n", "")
            features = line.split(',')
            is_testing = ((features[0] + '_' + features[1]) in test_indexes)
            if features[1] != "6-31-2015" and features[1] != "9-31-2015" and is_testing:
                out[features[0] + '_' + features[1]]=features[5:7]
    return out

def divide_to_sequence(data, test_indexes, feature_num=18, PAST_DAYS=7 , real_test_data=[]):
    features_trn = []
    features_tst = []
    targets_trn = []
    targets_tst = []
    target_tst_real = []
    start = 0
    days = PAST_DAYS
    end = start + days
    while end < len(data):
        sequence_start = data[start]
        sequence_end = data[end]
        is_testing = ((sequence_end[0] + '_' + sequence_end[1]) in test_indexes)
        d0 = date(int(sequence_end[4]), int(sequence_end[3]), int(sequence_end[2]))
        d1 = date(int(sequence_start[4]), int(sequence_start[3]), int(sequence_start[2]))
        delta = d0 - d1
        day_difference = delta.days
        if day_difference == days:
            sequence = [row[5:5 + feature_num] for row in data[start:end]]
            tmp = []
            for row in sequence:
                tmp_row = [float(i) for i in row]
                tmp.append(tmp_row)
            if is_testing:
                features_tst.append(tmp)
            else:
                features_trn.append(tmp)

            seq_target = [row[5:7] for row in data[start + 1:end + 1]]
            tmp = []
            for row in seq_target:
                tmp_row = [float(i) for i in row]
                tmp.append(tmp_row)
            if is_testing:
                targets_tst.append(tmp)
                target_tst_real.append(real_test_data[data[end][0]+'_'+data[end][1]])
            else:
                targets_trn.append(tmp)

            start += 1
            end = start + days
        else:
            start += 1
            end += 1
    return features_trn, targets_trn, features_tst, targets_tst,target_tst_real
