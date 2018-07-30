import os
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import matplotlib.pyplot as plt
import numpy as np

class Timer:
    """
    A simple timer to use during training.
    """
    def __init__(self):
        self.time0 = time.time()

    def elapsed(self):
        time1 = time.time()
        elapsed = time1 - self.time0
        self.time0 = time1
        return elapsed
#
# def plot(corpus, model, fig, ax, step, sent=2):
#     words = Variable(torch.LongTensor([corpus.train.words[sent]]))
#     tags = Variable(torch.LongTensor([corpus.train.tags[sent]]))
#     heads = Variable(torch.LongTensor([corpus.train.heads[sent]]))
#     labels = Variable(torch.LongTensor([corpus.train.labels[sent]]))
#     # Disable dropout.
#     model.eval()
#     S_arc, S_lab = model(words, tags)
#     # Turn dropout back on.
#     model.train()
#     # Plot the gold adjacency matrix, if does not yet exist.
#     if not os.path.exists('img/gold.pdf'):
#         # Make a 0/1 gold adjacency matrix.
#         n = words.size(1)
#         G = np.zeros((n, n))
#         heads = heads.squeeze().data.numpy()
#         G[heads, np.arange(n)] = 1.
#         im = ax.imshow(G, vmin=0, vmax=1)
#         fig.colorbar(im)
#         plt.savefig('img/gold.pdf'.format(step))
#         plt.cla()
#         plt.clf()
#     # Plot the predicted adjacency matrix
#     A = F.softmax(S_arc.squeeze(0), dim=0)
#     fig, ax = plt.subplots()
#     im = ax.imshow(A.data.numpy(), vmin=0, vmax=1)
#     fig.colorbar(im)
#     plt.savefig('img/a.{}.pdf'.format(step))
#     plt.cla()
#     plt.clf()
