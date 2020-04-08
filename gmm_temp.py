from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_sample_image
import matplotlib.pyplot as plt


X = load_sample_image('china.jpg')
old_shape = X.shape
X = X.reshape(-1,3)

# Representation of a Gaussian mixture model probability distribution. 
# This class allows to estimate the parameters of a Gaussian mixture distribution.
gmm = GaussianMixture(covariance_type='full', n_components=5).fit(X)

# Predict the labels for the data samples in X using trained model.
clusters = gmm.predict(X)

# Predict posterior probability of each component given the data.
probs = gmm.predict_proba(Y_sklearn)

clusters = clusters.reshape(old_shape[0], old_shape[1])
imshow(clusters)


