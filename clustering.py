# Module imports

# Third party imports
import hdbscan
import pandas as pd
import time


def detectCluster(eventList, min_cluster_size):

    # Build Input coordinates
    # https://stackoverflow.com/questions/34997174/how-to-convert-list-of-model-objects-to-pandas-dataframe
    inputDataFrame = pd.DataFrame(columns=['x', 'y'])
    x, y = map(list, zip(*((e.x, e.y) for e in eventList)))
    coordinatesList = [list(el) for el in zip(x, y)]
    inputDataFrame = pd.DataFrame(coordinatesList, columns=['x', 'y'])

    #hdb_t1 = time.time()
    # https://hdbscan.readthedocs.io/en/latest/basic_hdbscan.html#
    # Compute DBSCAN
    clusterer =  hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, prediction_data=True).fit(inputDataFrame)
    #hdb_elapsed_time = time.time() - hdb_t1
    #print('Elapsed time to cluster: %.4f s' % hdb_elapsed_time)
    return clusterer 

def predict(hdb, test_points):
	test_labels, strengths = hdbscan.approximate_predict(hdb, test_points)
	return test_labels, strengths

def printHDBSCAN(inputDataFrame, clusterer):
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_hdb = len(set(clusterer.labels_)) - (1 if -1 in clusterer.labels_ else 0)
    #hdb_netw = list(hdb.condensed_tree_.to_networkx().nodes(data=True))
    #hdb_pd = hdb.condensed_tree_.to_pandas()
    #hdb_np = hdb.condensed_tree_.to_numpy()
    #hdb_nps = hdb.single_linkage_tree_.to_pandas()
    #hdb_nps_cluster = hdb.single_linkage_tree_.get_clusters(0.023, min_cluster_size=2)
    
    print('\n**** HDBSCAN Results ****')

    print("InputDataFrame :")
    print(inputDataFrame)

    print('Estimated number of clusters: %d' % n_clusters_hdb)

    print("hdb_labels : Cluster labels for each point in the dataset:")
    print(clusterer.labels_)

    print("hdb_probabilities : The strength with which each sample is a member of its assigned cluster: ")
    print(clusterer.probabilities_)

    print("hdb.cluster_persistence_ : A score of how persistent each cluster is:")
    print(clusterer.cluster_persistence_)

    #print("hdb_exemplars : most representative points of the cluster: {}".format(hdb.exemplars_))
    #print("hdb_netw : condensed_tree_ NetworkX directed graph : {}".format(hdb_netw))
    #print("hdb_pd : condensed_tree_ Panda DataFrame: {}".format(hdb_pd))
    #print("hdb_np : condensed_tree_ numpy record array: {}".format(hdb_np))
    #print("hdb_nps : single_linkage_tree_ Pandas record array : {}".format(hdb_nps))
    #print("hdb_nps_cluster : single_linkage_tree_ clusters  : {}".format(hdb_nps_cluster))
    print('**** HDBSCAN Results ****\n')
    #print('Silhouette Coefficient: %0.3f' % metrics.silhouette_score(inputDataFrame, hdb_labels))