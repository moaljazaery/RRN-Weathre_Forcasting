from rnn import *
from parse_data import *

logging.basicConfig(level=logging.INFO)


out_path = './data/models/'
PAST_DAYS = 10
TESTING_PERCENTAGE = 0.1
normalization = 'zcore'


n_in = 18
n_out = 2

# normalization='zcore'

print("PAST_DAYS ", PAST_DAYS)
print("TESTING_PERCENTAGE ", TESTING_PERCENTAGE)
print("Normalization ", normalization)

cluster_subset=[1,5,11,19]
airports_clusters = get_clusters()
err_counter = 0
err_mintmp = 0
err_maxtmp = 0
tst_indexes = get_test_indexes()
airports, airports_data = parse_data(normalization=normalization)
real_test_data=get_real_test_target(tst_indexes)
airports_clusters_data = {}
airports_all_data = {'features_trn': [], 'targets_trn': [], 'features_tst': [], 'targets_tst': [],'targets_tst_real':[]}
air_count=0
for air_id in airports:
    cluster_id = airports_clusters[air_id]
    if cluster_id in cluster_subset:
        air_count+=1
        data = []
        for rec in airports_data[air_id]:
            data.append(rec)

        features_trn, targets_trn, features_tst, targets_tst ,targets_tst_real = divide_to_sequence(data, tst_indexes, feature_num=n_in,
                                                                                  PAST_DAYS=PAST_DAYS,real_test_data=real_test_data)

        if airports_clusters_data.get(cluster_id, 0) == 0:
            airports_clusters_data[cluster_id] = {}
            airports_clusters_data[cluster_id]['features_trn'] = []
            airports_clusters_data[cluster_id]['targets_trn'] = []
            airports_clusters_data[cluster_id]['features_tst'] = []
            airports_clusters_data[cluster_id]['targets_tst'] = []
            airports_clusters_data[cluster_id]['targets_tst_real'] = []

        for rec in features_trn:
            airports_clusters_data[cluster_id]['features_trn'].append(rec)
            airports_all_data['features_trn'].append(rec)
        for rec in targets_trn:
            airports_clusters_data[cluster_id]['targets_trn'].append(rec)
            airports_all_data['targets_trn'].append(rec)
        for rec in features_tst:
            airports_clusters_data[cluster_id]['features_tst'].append(rec)
            airports_all_data['features_tst'].append(rec)
        for rec in targets_tst:
            airports_clusters_data[cluster_id]['targets_tst'].append(rec)
            airports_all_data['targets_tst'].append(rec)
        for rec in targets_tst_real:
            airports_clusters_data[cluster_id]['targets_tst_real'].append(rec)
            airports_all_data['targets_tst_real'].append(rec)

        a=[]
        b=[]
        import itertools
        for feat in features_trn:
            a.append(list(itertools.chain(*feat)))

        for tar in targets_trn:
            b.append(tar[-1])
        from sklearn import linear_model
        model = linear_model.LinearRegression()
        model.fit(a, b)
        a=[]
        b=[]
        for feat in features_tst:
            a.append(list(itertools.chain(*feat)))

        counter = 0
        if (len(features_tst) > 0):
            for one_seq in a:
                guess = model.predict([one_seq])
                from denrmalization import *

                prediction = zscore(guess[0][0], temp_max_mean, temp_max_sigma)
                real = float(targets_tst_real[counter][0])
                err_maxtmp += abs(prediction - real)

                prediction = zscore(guess[0][1], temp_min_mean, temp_min_sigma)
                real = float(targets_tst_real[counter][1])
                err_mintmp += abs(prediction - real)
                err_counter += 1
                counter += 1

print("Airports' models error ")
all_error_min = err_mintmp / err_counter
all_error_max = err_maxtmp / err_counter
print(all_error_min)
print(all_error_max)

#
# Train regression model for all the data
#
features_trn = airports_all_data['features_trn']
targets_trn = airports_all_data['targets_trn']
features_tst = airports_all_data['features_tst']
targets_tst = airports_all_data['targets_tst']
targets_tst_real = airports_all_data['targets_tst_real']

a=[]
b=[]
import itertools
for feat in features_trn:
    a.append(list(itertools.chain(*feat)))

for tar in targets_trn:
    b.append(tar[-1])



from sklearn import linear_model
model = linear_model.LinearRegression()

model.fit(a, b)

a=[]
b=[]
for feat in features_tst:
    a.append(list(itertools.chain(*feat)))

# for tar in ta:
#     b.append(tar[-1])

counter = 0
err_mintmp = 0
err_maxtmp = 0
if (len(features_tst) > 0):
    for one_seq in a:
        guess = model.predict([one_seq])
        from denrmalization import *

        prediction = zscore(guess[0][0], temp_max_mean, temp_max_sigma)
        real = float(targets_tst_real[counter][0])
        err_maxtmp += abs(prediction - real)

        prediction = zscore(guess[0][1], temp_min_mean, temp_min_sigma)
        real = float(targets_tst_real[counter][1])
        err_mintmp += abs(prediction - real)
        counter += 1
all_error_min = err_mintmp / counter
all_error_max = err_maxtmp / counter

print("All Data Model Error")
print(all_error_min)
print(all_error_max)