from rnn import *
from parse_data import *

out_path = './data/models_summary/'
HIDDEN_LAYERS = 25
PAST_DAYS = 10
TESTING_PERCENTAGE = 0.1
n_epochs = 1200
normalization = 'zcore'
n_in = 18
n_out = 2

Experiment_KEY = 'Hidden_'+str(HIDDEN_LAYERS)+'_DAYS_'+str(PAST_DAYS)+'_nepoch_'+str(n_epochs)+'_normalization_'+str(normalization)+'_features_'+str(n_in)
print(Experiment_KEY)


print("Hidden Lyers ", HIDDEN_LAYERS)
print("PAST_DAYS ", PAST_DAYS)
print("TESTING_PERCENTAGE ", TESTING_PERCENTAGE)
print("Epochs Num ", n_epochs)
print("Normalization ", normalization)

cluster_subset=[1,5,11,19]
airports_clusters = get_clusters()

tst_indexes = get_test_indexes()
airports, airports_data = parse_data(normalization=normalization)
real_test_data=get_real_test_target(tst_indexes)
airports_clusters_data = {}
err_counter = 0
err_mintmp = 0
err_mintmp_linear = 0
err_maxtmp = 0
err_maxtmp_linear = 0
airports_all_data = {'features_trn': [], 'targets_trn': [], 'features_tst': [], 'targets_tst': [],'targets_tst_real':[]}
for air_id in airports:
    cluster_id = airports_clusters[air_id]
    if cluster_id in cluster_subset:
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
        lin_model = linear_model.LinearRegression()
        lin_model.fit(a, b)

        a=[]
        b=[]
        for feat in features_tst:
            a.append(list(itertools.chain(*feat)))

        model=MetaRNN()
        model.load(out_path+"/airports/"+ Experiment_KEY + '/' + str(air_id) + '_obj.save')
        counter = 0

        if (len(features_tst) > 0):
            for one_seq in features_tst:
                guess = model.predict(one_seq)
                guess_lin = lin_model.predict([a[counter]])
                from denrmalization import *
                if normalization == 'minmax':
                    prediction = minmax(guess[-1][0], temp_max_min, temp_max_max)
                    prediction_lin = minmax(guess_lin[0][0], temp_max_min, temp_max_max)
                else:
                    prediction = zscore(guess[-1][0], temp_max_mean, temp_max_sigma)
                    prediction_lin = zscore(guess_lin[0][0], temp_max_mean, temp_max_sigma)

                real = float(targets_tst_real[counter][0])
                err_maxtmp += abs(prediction-real)
                err_maxtmp_linear += abs(prediction_lin-real)

                if normalization == 'minmax':
                    prediction = minmax(guess[-1][1], temp_min_min, temp_min_max)
                    prediction_lin = minmax(guess_lin[0][1], temp_min_min, temp_min_max)
                else:
                    prediction = zscore(guess[-1][1], temp_min_mean, temp_min_sigma)
                    prediction_lin = zscore(guess_lin[0][1], temp_min_mean, temp_min_sigma)

                real = float(targets_tst_real[counter][1])
                err_mintmp += abs(prediction - real)
                err_mintmp_linear += abs(prediction_lin - real)
                counter += 1
                err_counter += 1

print("RNN Error")
error_max = err_maxtmp / err_counter
error_min = err_mintmp / err_counter

print(error_min)
print(error_max)

print("Linear Error")

error_max = err_maxtmp_linear / err_counter
error_min = err_mintmp_linear / err_counter

print(error_min)
print(error_max)
