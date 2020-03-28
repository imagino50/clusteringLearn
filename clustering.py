# Module imports

# Third party imports
import hdbscan
import time


def detectCluster(inputDataFrame):
    # Compute DBSCAN
    #hdb_t1 = time.time()
    clusterer =  hdbscan.HDBSCAN(min_cluster_size=3, allow_single_cluster=False, prediction_data=True).fit(inputDataFrame)
    #hdb_elapsed_time = time.time() - hdb_t1
    #print('Elapsed time to cluster: %.4f s' % hdb_elapsed_time)
    return clusterer 

def predict(hdb, test_points):
	test_labels, strengths = hdbscan.approximate_predict(hdb, test_points)
	return test_labels, strengths

def printHDBSCAN(hdb, inputDataFrame, index_feature):
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_hdb = len(set(hdb.labels_)) - (1 if -1 in hdb.labels_ else 0)
    #hdb_netw = list(hdb.condensed_tree_.to_networkx().nodes(data=True))
    #hdb_pd = hdb.condensed_tree_.to_pandas()
    #hdb_np = hdb.condensed_tree_.to_numpy()
    #hdb_nps = hdb.single_linkage_tree_.to_pandas()
    #hdb_nps_cluster = hdb.single_linkage_tree_.get_clusters(0.023, min_cluster_size=2)
    
    print('\n**** HDBSCAN Results ****')
    print("index_feature {}".format(index_feature))

    print("InputDataFrame :")
    print(inputDataFrame)

    print('Estimated number of clusters: %d' % n_clusters_hdb)

    print("hdb_labels : Cluster labels for each point in the dataset:")
    print(hdb.labels_)

    print("hdb_probabilities : The strength with which each sample is a member of its assigned cluster: ")
    print(hdb.probabilities_)

    print("hdb.cluster_persistence_ : A score of how persistent each cluster is:")
    print(hdb.cluster_persistence_)

    #print("hdb_exemplars : most representative points of the cluster: {}".format(hdb.exemplars_))
    #print("hdb_netw : condensed_tree_ NetworkX directed graph : {}".format(hdb_netw))
    #print("hdb_pd : condensed_tree_ Panda DataFrame: {}".format(hdb_pd))
    #print("hdb_np : condensed_tree_ numpy record array: {}".format(hdb_np))
    #print("hdb_nps : single_linkage_tree_ Pandas record array : {}".format(hdb_nps))
    #print("hdb_nps_cluster : single_linkage_tree_ clusters  : {}".format(hdb_nps_cluster))
    print('**** HDBSCAN Results ****\n')
    #print('Silhouette Coefficient: %0.3f' % metrics.silhouette_score(inputDataFrame, hdb_labels))