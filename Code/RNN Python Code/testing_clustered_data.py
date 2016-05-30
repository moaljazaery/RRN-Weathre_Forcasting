from rnn import *
from parse_data import *


out_path = './data/models_summary/'
HIDDEN_LAYERS = 10
PAST_DAYS = 7
TESTING_PERCENTAGE = 0.1
n_epochs = 300
normalization = 'zcore'

n_in = 18
n_out = 2

print("Hidden Lyers ", HIDDEN_LAYERS)
print("PAST_DAYS ", PAST_DAYS)
print("TESTING_PERCENTAGE ", TESTING_PERCENTAGE)
print("Epochs Num ", n_epochs)
print("Normalization ", normalization)

Experiment_KEY = 'Hidden_' + str(HIDDEN_LAYERS) + '_DAYS_' + str(PAST_DAYS) + '_nepoch_' + str(
    n_epochs) + '_normalization_' + str(normalization) + '_features_' + str(n_in)
print(Experiment_KEY)

cluster_subset = [1, 5, 11, 19]
airports_clusters = get_clusters()

tst_indexes = get_test_indexes()
airports, airports_data = parse_data(normalization=normalization)
real_test_data = get_real_test_target(tst_indexes)
airports_clusters_data = {}
airports_all_data = {'features_trn': [], 'targets_trn': [], 'features_tst': [], 'targets_tst': [],
                     'targets_tst_real': []}
for air_id in airports:
    cluster_id = airports_clusters[air_id]
    if cluster_id in cluster_subset:
        data = []
        for rec in airports_data[air_id]:
            data.append(rec)

        features_trn, targets_trn, features_tst, targets_tst, targets_tst_real = divide_to_sequence(data, tst_indexes,
                                                                                                    feature_num=n_in,
                                                                                                    PAST_DAYS=PAST_DAYS,
                                                                                                    real_test_data=real_test_data)

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

err_maxtemp_clusters = 0
err_mintemp_clusters = 0
err_clusters_count = 0
for cluster_id in cluster_subset:
    print("cluster no:" + str(cluster_id))
    model = MetaRNN()
    model.load(out_path + "/clusters/" + Experiment_KEY + '/cluster_' + str(cluster_id) + '_obj.save')
    features_trn = airports_clusters_data[cluster_id]['features_trn']
    targets_trn = airports_clusters_data[cluster_id]['targets_trn']
    features_tst = airports_clusters_data[cluster_id]['features_tst']
    targets_tst = airports_clusters_data[cluster_id]['targets_tst']
    targets_tst_real = airports_clusters_data[cluster_id]['targets_tst_real']

    counter = 0

    if (len(features_tst) > 0):
        for one_seq in features_tst:
            guess = model.predict(one_seq)
            from denrmalization import *

            if normalization == 'minmax':
                prediction = minmax(guess[-1][0], temp_max_min, temp_max_max)
            else:
                prediction = zscore(guess[-1][0], temp_max_mean, temp_max_sigma)

            real = float(targets_tst_real[counter][0])
            err_maxtemp_clusters += abs(prediction - real)

            if normalization == 'minmax':
                prediction = minmax(guess[-1][1], temp_min_min, temp_min_max)
            else:
                prediction = zscore(guess[-1][1], temp_min_mean, temp_min_sigma)
            real = float(targets_tst_real[counter][1])
            err_mintemp_clusters += abs(prediction - real)
            counter += 1
            err_clusters_count += 1
all_error_min = err_mintemp_clusters / err_clusters_count
all_error_max = err_maxtemp_clusters / err_clusters_count

print(all_error_min)
print(all_error_max)