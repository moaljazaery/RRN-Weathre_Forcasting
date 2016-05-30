from rnn import *
from parse_data import *

logging.basicConfig(level=logging.INFO)


out_path = './data/models_summary/'
HIDDEN_LAYERS = 25
PAST_DAYS = 10
TESTING_PERCENTAGE = 0.1
n_epochs = 1200

normalization = 'zcore' #or minmax

n_in = 18
n_out = 2

# normalization='zcore'

Experiment_KEY = 'Hidden_'+str(HIDDEN_LAYERS)+'_DAYS_'+str(PAST_DAYS)+'_nepoch_'+str(n_epochs)+'_normalization_'+str(normalization)+'_features_'+str(n_in)
print(Experiment_KEY)

print("Hidden Lyers ", HIDDEN_LAYERS)
print("PAST_DAYS ", PAST_DAYS)
print("TESTING_PERCENTAGE ", TESTING_PERCENTAGE)
print("Epochs Num ", n_epochs)
print("Normalization ", normalization)

#
# init and read the data
#

cluster_subset=[1,5,11,19]
airports_clusters = get_clusters()
tst_indexes = get_test_indexes()
airports, airports_data = parse_data(normalization=normalization)
real_test_data=get_real_test_target(tst_indexes)
airports_clusters_data = {}
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

        #
        # train RNN models for each airport data alone
        #
        if not os.path.isfile(out_path+"/airports/"+Experiment_KEY + '_' + str(air_id) + '_obj.save'):
            model = MetaRNN(n_in=n_in, n_hidden=HIDDEN_LAYERS, n_out=n_out,
                            learning_rate=0.005, learning_rate_decay=0.999,
                            n_epochs=n_epochs, activation='tanh')

            model.fit(features_trn, targets_trn, validation_frequency=1000)
            directory = out_path + "/airports/" + Experiment_KEY + "/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            model.save(directory, str(air_id) + '_obj.save')

#
# train RNN model for each cluster alone
#
for cluster_id in cluster_subset:
    print("cluster no:" + str(cluster_id))
    model = MetaRNN(n_in=n_in, n_hidden=HIDDEN_LAYERS, n_out=n_out,
                    learning_rate=0.001, learning_rate_decay=0.999,
                    n_epochs=n_epochs, activation='tanh')
    features_trn = airports_clusters_data[cluster_id]['features_trn']
    targets_trn = airports_clusters_data[cluster_id]['targets_trn']
    features_tst = airports_clusters_data[cluster_id]['features_tst']
    targets_tst = airports_clusters_data[cluster_id]['targets_tst']

    model.fit(features_trn, targets_trn, validation_frequency=1000)
    directory = out_path + "/clusters/"+Experiment_KEY+"/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    model.save(directory, 'cluster_' + str(cluster_id) + '_obj.save')


#
# train RNN model for the whole data
#
features_trn = airports_all_data['features_trn']
targets_trn = airports_all_data['targets_trn']
features_tst = airports_all_data['features_tst']
targets_tst = airports_all_data['targets_tst']

model = MetaRNN(n_in=n_in, n_hidden=HIDDEN_LAYERS, n_out=n_out,
                learning_rate=0.001, learning_rate_decay=0.999,
                n_epochs=n_epochs, activation='tanh')

model.fit(features_trn, targets_trn, validation_frequency=1000)

model.save(out_path + "/all_data/", Experiment_KEY + '_obj.save')
