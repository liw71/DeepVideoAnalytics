import numpy as np
import logging
from scipy import spatial
from collections import namedtuple


IndexRange = namedtuple('IndexRange',['start','end'])




class BaseRetriever(object):

    def __init__(self,name):
        self.name = name
        self.net = None
        self.loaded_entries = {}
        self.index, self.files, self.findex = None, {}, 0
        self.support_batching = False

    def load_index(self,numpy_matrix,entries):
        temp_index = [numpy_matrix, ]
        for i, e in enumerate(entries):
            self.files[self.findex] = e
            self.findex += 1
        if self.index is None:
            self.index = np.atleast_2d(np.concatenate(temp_index).squeeze())
            logging.info(self.index.shape)
        else:
            self.index = np.concatenate([self.index, np.atleast_2d(np.concatenate(temp_index).squeeze())])
            logging.info(self.index.shape)

    def nearest(self, vector=None, n=12):
        dist = None
        results = []
        if self.index is not None:
            # logging.info("{} and {}".format(vector.shape,self.index.shape))
            dist = spatial.distance.cdist(vector,self.index)
        if dist is not None:
            ranked = np.squeeze(dist.argsort())
            for i, k in enumerate(ranked[:n]):
                temp = {'rank':i+1,'algo':self.name,'dist':float(dist[0,k])}
                temp.update(self.files[k])
                results.append(temp)
        return results # Next also return computed query_vector