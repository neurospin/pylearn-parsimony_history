# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:41:13 2013

Copyright (c) 2013-2014, CEA/DSV/I2BM/Neurospin. All rights reserved.

@author:  Tommy Löfstedt
@email:   lofstedt.tommy@gmail.com
@license: BSD 3-clause.
"""
import numpy as np
#import parsimony.estimators as estimators
#import parsimony.algorithms.proximal as proximal
#from parsimony.utils.resampling import k_fold
#
#import parsimony.utils.maths as maths
#
#import parsimony.estimators as estimators
#import parsimony.algorithms.nipals as nipals
#import parsimony.algorithms.gradient as gradient

#X = np.random.rand(10, 15)
#Y = np.random.rand(10, 5)
#w = np.random.rand(15, 1)
#c = np.random.rand(5, 1)
#
#f = -np.dot(w.T, np.dot(X.T, np.dot(Y, c)))
#df = -np.dot(X.T, np.dot(Y, c))
#
#f2 = -np.dot((w - df).T, np.dot(X.T, np.dot(Y, c)))


import parsimony.estimators as estimators
import parsimony.algorithms.nipals as nipals
import parsimony.algorithms.multiblock as multiblock
import numpy as np
np.random.seed(42)

n, p = 16, 10
X = np.random.rand(n, p)
y = np.random.rand(n, 1)
plsr = estimators.SparsePLSRegression(l=[3.0, 0.0], K=1,
                                      algorithm=nipals.SparsePLSR(),
                                      algorithm_params=dict(max_iter=100))
error = plsr.fit(X, y).score(X, y)
print plsr.W
print plsr.C
print "error = ", error

np.random.seed(42)

X = np.random.rand(n, p)
y = np.random.rand(n, 1)
plsr = estimators.SparsePLSRegression(l=[0.1, 0.0], K=1,
                                 algorithm=multiblock.MultiblockFISTA(),
                                 algorithm_params=dict(max_iter=100))
error = plsr.fit(X, y).score(X, y)
print plsr.W
#print np.linalg.norm(plsr.W) ** 2.0
print plsr.C
print "error = ", error


#import parsimony.estimators as estimators
#import parsimony.algorithms.nipals as nipals
#import parsimony.algorithms.multiblock as multiblock
#import numpy as np
#np.random.seed(42)
#
#n, p = 16, 10
#X = np.random.rand(n, p)
#y = np.random.rand(n, 1)
#plsr = estimators.PLSRegression(K=4, algorithm=nipals.PLSR(),
#                                algorithm_params=dict(max_iter=100))
#error = plsr.fit(X, y).score(X, y)
#print "error = ", error
## error =  0.0222345224457
#
#np.random.seed(42)
#
#X = np.random.rand(n, p)
#y = np.random.rand(n, 1)
#plsr = estimators.PLSRegression(K=4,
#                                algorithm=multiblock.MultiblockFISTA(),
#                                algorithm_params=dict(outer_iter=10,
#                                                      max_iter=100))
#error = plsr.fit(X, y).score(X, y)
#print "error = ", error
## error =  0.0222345224457

#K = 10
#M, N, Q = 10, 10, 1
#
#np.random.seed(42)
#
#X = np.random.rand(M, N)
#Y = np.random.rand(M, Q)
#X_orig = np.copy(X)
#Y_orig = np.copy(Y)
#
##plsr = estimators.PLSRegression(K=K, algorithm=nipals.PLSR(),
##                                algorithm_params=dict(max_iter=100))
##plsr.fit(X, Y)
##print plsr.beta
##err = np.sum((np.dot(X, plsr.beta) - Y_orig) ** 2.0) / float(n)
##print "error = ", err
##
##np.random.seed(42)
##
##lr = estimators.LinearRegression(algorithm=gradient.GradientDescent(),
##                                 algorithm_params=dict(max_iter=1000),
##                                 mean=True)
##lr.fit(X, Y)
##print lr.beta
##err = np.sum((np.dot(X, lr.beta) - Y_orig) ** 2.0) / float(n)
##print "error = ", err
##
##print plsr.beta / maths.norm(plsr.beta)
##print lr.beta / maths.norm(lr.beta)
#
#W = np.zeros((N, K))
#T = np.zeros((M, K))
#C = np.zeros((Q, K))
#U = np.zeros((M, K))
#P = np.zeros((N, K))
#
#for k in range(K):
#    maxi = np.argmax(np.sum(Y ** 2.0, axis=0))
#    u = Y[:, [maxi]]
#    w = np.dot(X.T, u)
##    w = np.random.rand(N, 1)
#    w /= maths.norm(w)
#    for i in range(1000):
#        c = np.dot(Y.T, np.dot(X, w))
#        w = np.dot(X.T, np.dot(Y, c))
#        w /= maths.norm(w)
#
#    t = np.dot(X, w)
#    c = np.dot(Y.T, t) / np.dot(t.T, t)
#    u = np.dot(Y, c) / np.dot(c.T, c)
#
#    p = np.dot(X.T, t) / np.dot(t.T, t)
#
#    X = X - np.dot(t, p.T)
##    d = np.dot(t.T, u) / np.dot(t.T, t)
##    Y = Y - np.dot(t * d, c.T)
#
#    W[:, [k]] = w
#    T[:, [k]] = t
#    C[:, [k]] = c
#    U[:, [k]] = u
#    P[:, [k]] = p
#
#Ws = np.dot(W, np.linalg.inv(np.dot(P.T, W)))
#B = np.dot(Ws, C.T)
#
#Yhat = np.dot(X_orig, B)
##Yhat = np.dot(T, C.T)
#
#err = np.sum((Yhat - Y_orig) ** 2.0)  # / float(n)
#print err


#for k in range(K):
#    w = np.random.rand(N, 1)
#    w /= maths.norm(w)
#    for i in range(1000):
#        c = np.dot(Y.T, np.dot(X, w))
#        w = np.dot(X.T, np.dot(Y, c))
#        w /= maths.norm(w)
#
#    t = np.dot(X, w)
#    c = np.dot(Y.T, t)  # / np.dot(t.T, t)
#    c /= maths.norm(c)
#    u = np.dot(Y, c)  # / np.dot(c.T, c)
#
#    p = np.dot(X.T, t) / np.dot(t.T, t)
#
#    W[:, [k]] = w
#    T[:, [k]] = t
#    C[:, [k]] = c
#    U[:, [k]] = u
#    P[:, [k]] = p
#
#    X = X - np.dot(t, p.T)
#    d = np.dot(t.T, u) / np.dot(t.T, t)
#    Y = Y - np.dot(t * d, c.T)
#
#    print np.linalg.norm(np.dot(X.T, t))
#    print np.linalg.norm(np.dot(X, w))
#
##    print "corr:", maths.corr(t, u)
#    print "cov:", np.dot(t.T, u)
#
#Ws = np.dot(W, np.linalg.inv(np.dot(P.T, W)))
#
#beta = np.dot(Ws, C.T)
#print beta

#for k in range(K):
#    #Yhat = np.dot(X_orig, beta)
#    Yhat = np.dot(T[:, :k], C[:, :k].T)
#
#    n, p = X.shape
#    err = np.sum((Yhat - Y_orig) ** 2.0) / float(n)
#    print "error = ", err


#n = 32
#p = 48
#
#np.random.seed(42)
#X = np.random.randn(n, p)
#y = np.random.randn(n, 1)
#l = 0.3
#en = estimators.ElasticNet(l,
#                           algorithm=proximal.FISTA(),
#                           algorithm_params=dict(max_iter=1000),
#                           mean=False)
#
#ssy = np.sum(y ** 2.0)
#for l in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
#
#    np.random.seed(42)
#    en = estimators.ElasticNet(l, alpha=2.0,
#                               algorithm=proximal.FISTA(),
#                               algorithm_params=dict(max_iter=1000),
#                               mean=False)
#    err = 0.0
#    for train, test in k_fold(n, K=7):
#
#        Xtr = X[train, :]
#        ytr = y[train, :]
#        Xte = X[test, :]
#        yte = y[test, :]
#
#        yhat = en.fit(Xtr, ytr).predict(Xte)
#
##        yhat = np.dot(Xte, en.beta)
#
#        err += np.sum(yhat ** 2.0) / ssy
#
#    Q2 = 1.0 - err
#    print "l = %.2f, R2 = %.2f" % (l, Q2)

#import time
#
#import numpy as np
#
#from parsimony.functions.penalties import RGCCAConstraint
#
#np.random.seed(0)
#
#n = 100
#p = 1000
#tau = 0.5
#c = 1.5
#
#X = np.random.randn(n, p)
#x = np.random.rand(p, 1)
#c = RGCCAConstraint(c=c, tau=tau, X=X)
#
#t = time.time()
#y = c.proj(x)
#print "time:", time.time() - t

#n = 25
#p = 500
#tau = 0.5
#c = 1.0
#
#X = np.loadtxt("X.txt", delimiter=',')
#x = np.loadtxt("a.txt", delimiter=',').reshape((p, 1))
#c = RGCCAConstraint(c=c, tau=tau, X=X)
#
#t = time.time()
#y = c.proj(x)
#print "time:", time.time() - t

#import numpy as np
#import cPickle as pickle
#from parsimony.functions.penalties import RGCCAConstraint
#
#np.random.seed(42)
#
#result = {}
#
#for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
#    for p in [501, 1001, 5000, 10000, 50000, 100000, 250000, 500000]:
#        if p < n:
#            continue
#        for c in [0.1, 0.5, 1.0, 5.0, 10.0, 50.0]:
#            for tau in [0.1, 0.3, 0.5, 0.7, 0.9]:
#                for m in xrange(5):
#                    print n, p, c, tau
#                    X = np.random.rand(n, p)
#                    rgcca = RGCCAConstraint(c=c, tau=tau, X=X)
#                    x = np.random.rand(p, 1) * 2.0 * c - c
#                    y, low_start, high_start = rgcca.proj(x)
#                    result[(n, p, c, tau, m)] = (low_start, high_start)
#
#    with open("RGCCAproj_test.p", "wb") as pfile:
#        pickle.dump(result, pfile)


#import time
#import sys
#
#import numpy as np
#import matplotlib.pyplot as plot
#import scipy.sparse as sparse
#
#import parsimony.functions.penalties as penalties
#import parsimony.functions.multiblock.losses as mb_losses
#import parsimony.algorithms as algorithms
#import parsimony.utils.maths as maths
#import parsimony.utils.consts as consts
#import parsimony.functions.nesterov.gl as gl
#import parsimony.functions.nesterov.tv as tv
#import parsimony.start_vectors as start_vectors
#
#import parsimony.datasets.simulated as simulated
#
#from parsimony.functions import *
#
#import parsimony.datasets.simulated.grad as grad
#
##__all__ = ["__test__"]
##__test__ = False
#
#seed = 42
#np.random.seed(seed)

#
#import numpy as np
#import parsimony.estimators as estimators
#import parsimony.algorithms.explicit as explicit
#import parsimony.functions.nesterov.tv as tv
#shape = (1, 4, 4)
#num_samples = 10
#num_ft = shape[0] * shape[1] * shape[2]
#
#np.random.seed(42)
#X = np.random.rand(num_samples, num_ft)
#y = np.random.rand(num_samples, 1)
#l = 0.1  # L1 coefficient
#k = 0.9  # Ridge coefficient
#g = 1.0  # TV coefficient
#mu = 1e-5
#A, n_compacts = tv.A_from_shape(shape)
#lr = estimators.LinearRegression_L1_L2_TV(l, k, g, A, mu=mu,
#                                      algorithm=explicit.FISTA(max_iter=1000))
#lr = lr.fit(X, y)
#error = lr.score(X, y)
#print "error = ", error
##error =  0.87958672586
#lr = estimators.LinearRegression_L1_L2_TV(l, k, g, A, mu=mu,
#                                       algorithm=explicit.ISTA(max_iter=1000))
#lr = lr.fit(X, y)
#error = lr.score(X, y)
#print "error = ", error
##error =  1.07391299463


#eps = 0.001
#maxit = 20000
#mu = 1e-6
#k = 0.6
#l = 0.4
#g = 0.9
#
#px = 100
#py = 1
#pz = 1
#shape = (pz, py, px)
#p = 1 + px * py * pz  # Must be even!
#n = 60
#alpha = 1.0
#Sigma = alpha * np.eye(p, p) + (1.0 - alpha) * np.random.randn(p, p)
#mean = np.zeros(p)
#M = np.random.multivariate_normal(mean, Sigma, n)
#X = np.hstack((np.ones((n, 1)), np.random.randn(n, p - 1)))
#betastar = np.concatenate((np.zeros(((p - 1) / 2, 1)),
#                           np.random.randn(round((p - 1) / 2.0), 1)))
#betastar = np.sort(np.abs(betastar), axis=0)
#betastar = np.concatenate((np.random.rand(1, 1), betastar))
##betastar = np.array([[2.0],[0.5]])
#
#print X.shape
#print betastar.shape
#
#y = np.dot(X, betastar)
##m = np.mean(y)
##y[y < m] = 0.0
##y[y >= m] = 1.0
##print y
#
#A, n_compacts = tv.A_from_shape(shape)
##A = gl.A_from_groups(px, [range(0, int(px / 2.0)),
##                          range(int(px / 2.0), px)])
#Al1 = sparse.eye(p - 1, p - 1)
#
#beta_start = start_vectors.RandomStartVector(normalise=False)
#beta_start = beta_start.get_vector((p, 1))
#
#
#
###rr = RR_L1_GL(X, y, k, l, g, A=A, mu=mu, penalty_start=0)
##rr = RR_SmoothedL1TV(X, y, k, l, g, Atv=A, Al1=Al1, mu=mu,
##                     penalty_start=0)
##
##print maths.norm(betastar - beta_start)
##
##ista = algorithms.ISTA(output=True, max_iter=maxit)
##t = time.time()
##beta, output = ista(rr, beta_start)
###print time.time() - t
##
##print maths.norm(betastar - beta)
#
#
##rr = RR_L1_TV(X, y, k, l, g, A=A, mu=mu, penalty_start=0)
##rr = RR_L1_GL(X, y, k, l, g, A=A, mu=mu, penalty_start=1)
#rr = RR_SmoothedL1TV(X, y, k=0.01, l=l, g=g, Atv=A, Al1=Al1, mu=mu,
#                     penalty_start=1)
##rr = RLR_L1_TV(X, y, k, l, g, A=A, mu=mu, weights=None, penalty_start=1)
#
#print maths.norm(betastar - beta_start)
#print maths.norm(np.dot(X, betastar) - np.dot(X, beta_start))
#
##ista = algorithms.ISTA(output=True, max_iter=maxit)
#ista = algorithms.ExcessiveGapMethod(output=True, max_iter=maxit)
#t = time.time()
#beta, output = ista(rr, beta_start)
##print time.time() - t
#print beta
#
#print maths.norm(betastar - beta)
#print maths.norm(np.dot(X, betastar) - np.dot(X, beta))
#
#
#
##rr = RR_L1_TV(X, y, k, l, g, A=A, mu=mu, penalty_start=1)
##rr = RR_L1_GL(X, y, k, l, g=0.9, A=A, mu=mu, penalty_start=1)
#rr = RR_SmoothedL1TV(X, y, k, l=0.0, g=g, Atv=A, Al1=Al1,
#                     mu=mu, penalty_start=1)
##rr = RLR_L1_TV(X, y, k, l, g=0.9, A=A, mu=mu, weights=None, penalty_start=1)
#
#print maths.norm(betastar - beta_start)
#print maths.norm(np.dot(X, betastar) - np.dot(X, beta_start))
#
##ista = algorithms.ISTA(output=True, max_iter=maxit)
#ista = algorithms.ExcessiveGapMethod(output=True, max_iter=maxit)
#t = time.time()
#beta, output = ista(rr, beta_start)
##print time.time() - t
#print beta
#
#print maths.norm(betastar - beta)
#print maths.norm(np.dot(X, betastar) - np.dot(X, beta))
#
#
#
##rr = RR_L1_TV(X, y, k, l, g, A=A, mu=mu, penalty_start=1)
##rr = RR_L1_GL(X, y, k, l, g=0.9, A=A, mu=mu, penalty_start=1)
#rr = RR_SmoothedL1TV(X, y, k, l, g=0.0, Atv=A, Al1=Al1,
#                     mu=mu, penalty_start=1)
##rr = RLR_L1_TV(X, y, k, l, g=0.9, A=A, mu=mu, weights=None, penalty_start=1)
#
#print maths.norm(betastar - beta_start)
#print maths.norm(np.dot(X, betastar) - np.dot(X, beta_start))
#
##ista = algorithms.ISTA(output=True, max_iter=maxit)
#ista = algorithms.ExcessiveGapMethod(output=True, max_iter=maxit)
#t = time.time()
#beta, output = ista(rr, beta_start)
##print time.time() - t
#print beta
#
#print maths.norm(betastar - beta)
#print maths.norm(np.dot(X, betastar) - np.dot(X, beta))
#
#
#
##rr = RR_L1_TV(X, y, k, l, g, A=A, mu=mu, penalty_start=1)
##rr = RR_L1_GL(X, y, k, l, g=0.9, A=A, mu=mu, penalty_start=1)
#rr = RR_SmoothedL1TV(X, y, k, l=0.0, g=0.0, Atv=A, Al1=Al1,
#                     mu=mu, penalty_start=1)
##rr = RLR_L1_TV(X, y, k, l, g=0.9, A=A, mu=mu, weights=None, penalty_start=1)
#
#print maths.norm(betastar - beta_start)
#print maths.norm(np.dot(X, betastar) - np.dot(X, beta_start))
#
##ista = algorithms.ISTA(output=True, max_iter=maxit)
#ista = algorithms.ExcessiveGapMethod(output=True, max_iter=maxit)
#t = time.time()
#beta, output = ista(rr, beta_start)
##print time.time() - t
#print beta
#
#print maths.norm(betastar - beta)
#print maths.norm(np.dot(X, betastar) - np.dot(X, beta))



#mx = np.mean(X)
#my = np.mean(y)
#X -= mx
#y -= my
##rr = RR_L1_GL(X, y, k, l, g, A=A, mu=mu, penalty_start=0)
#rr = RR_SmoothedL1TV(X, y, k, l, g, Atv=A, Al1=Al1, mu=mu,
#                     penalty_start=0)
#
#print maths.norm(betastar - beta_start)
#
#ista = algorithms.ISTA(output=True, max_iter=maxit)
#t = time.time()
#beta, output = ista(rr, beta_start)
##print time.time() - t
#
#print maths.norm(betastar - beta)



#beta_star = np.random.rand(p, 1)
#px = 30
#py = 20
#w_star = np.vstack((np.zeros((int(px / 3.0), 1)),
#                    np.ones((int(px / 3.0), 1)),
#                    np.zeros((int(px / 3.0), 1))))
#c_star = np.random.rand(py, 1)
#print w_star.T
#px = w_star.shape[0]
#n = 10
#
#l = 0.5
#k = 0.5
#g = 0.11
#shape = (1, 1, px)
#
#Sigma = np.eye(px, px)
#mean = np.zeros(px)
#M = np.random.multivariate_normal(mean, Sigma, n)
#
#e = np.random.randn(n, 1)
#
#Agl = gl.A_from_groups(px, [range(0, int(px / 3.0)),
#                            range(int(px / 3.0), int(2.0 * px / 3.0)),
#                            range(int(2.0 * px / 3.0), px)])
##import scipy.sparse as sparse
##np.set_printoptions(threshold=100000, linewidth=100000)
##print sparse.vstack(Agl).toarray()
##Atv, n_compacts = tv.A_from_shape(shape)
#
#snr = 20.0
#
#mu = 1e-6
#
##X, y, beta_star = simulated.l1_l2_tvmu.load(l, k, g, beta_star, M, e, Atv, mu, snr)
##X, y, beta_star = simulated.l1_l2_tv.load(l, k, g, beta_star, M, e, Atv, snr)
##X, y, beta_star = simulated.l1_l2_glmu.load(l, k, g, beta_star, M, e, Agl, mu, snr)
#X, y, w_star = simulated.l1_l2_gl.load(l, k, g, w_star, M, e, Agl, snr)
#
#c_star = np.random.randn(py, 1)
#c_star = c_star / maths.norm(c_star)
#Y = np.dot(y, c_star.T)
#
##constraintX_1 = functions.L1(c=2.0)
#constraintX = penalties.RGCCAConstraint(c=k, tau=1.0, X=X, unbiased=True)
##constraintX = functions.CombinedProjectionOperator([constraintX_1,
##                                                    constraintX_2])
#
##constraintY_1 = functions.L1(c=2.0)
#constraintY = penalties.RGCCAConstraint(c=k, tau=1.0, X=Y, unbiased=True)
##constraintY = functions.CombinedProjectionOperator([constraintY_1,
##                                                    constraintY_2])
#
#f = []
#fmu = []
#b = []
#start_vector_x = start_vectors.RandomStartVector()
#start_vector_y = start_vectors.RandomStartVector()
#errs = [-0.1, -0.08, -0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, 0.08, 0.1]
#for er in errs:
#
#    funcX = mb_losses.LatentVariableCovariance([X, Y], unbiased=True)
#    funcY = mb_losses.LatentVariableCovariance([Y, X], unbiased=True)
#
#    gl = gl.GroupLassoOverlap(l=g + er, A=Agl, mu=mu)
#
#    function = mb_losses.GeneralisedMultiblock([X, Y], [[[gl], funcX],
#                                                        [funcY, []]])
#
#    function.add_constraint(constraintX, 0)
#    function.add_constraint(constraintY, 1)
#
#    algorithm = algorithms.MultiblockProjectedGradientMethod(outer_iter=10,
#                                                             max_iter=100000,
#                                                             output=True)
#
#    w_x = start_vector_x.get_vector((X.shape[1], 1))
#    w_y = start_vector_y.get_vector((Y.shape[1], 1))
#
#    w, output = algorithm(function, [w_x, w_y])
#
#    start_vector_x = start_vectors.IdentityStartVector(w[0])
#    start_vector_y = start_vectors.IdentityStartVector(w[1])
#
#    f.append(abs(function.f(w) - function.f([w_star, c_star])) \
#            / abs(function.f([w_star, c_star])))
##    fmu.append(abs(function.fmu(beta, mu) - function.fmu(beta_star, mu)) \
##              / function.fmu(beta_star, mu))
#    b.append((maths.norm(w_x - w_star) / maths.norm(w_star)) + \
#             (maths.norm(w_y - c_star) / maths.norm(c_star)))
#    print "er :", er
#    print "f  :", f[-1]
##    print "fmu:", fmu[-1]
#    print "b  :", b[-1]
#    print
#    sys.stdout.flush()
#
#plot.subplot(2, 1, 1)
#plot.plot(errs, f)
##plot.subplot(3, 1, 2)
##plot.plot(errs, fmu)
#plot.subplot(2, 1, 2)
#plot.plot(errs, b)
#plot.show()
#
##var_x = 30
##var_y = 20
##n = 10
##
###Sigma = np.eye(var_x, var_x)
###mean = np.zeros(var_x)
###X = np.random.multivariate_normal(mean, Sigma, n)
###beta_star = np.vstack([np.random.randn(var_x / 3, 1) * 0.01 + 0.0,
###                       np.random.randn(var_x / 3, 1) * 0.01 + 1.0,
###                       np.random.randn(var_x / 3, 1) * 0.01 + 0.0])
###y = np.dot(X, beta_star)  # + np.random.randn(X.shape[0], 1) * 0.001
###
###Agl = gl.A_from_groups(var_x, [#range(0, var_x/3),
###                               range(var_x/3, 2 * var_x / 3),
###                               range(2 * var_x/3, var_x)])
###f = functions.RR_L1_GL(X, y, k=0.0, l=0.9, g=10.0, A=Agl, mu=0.00001)
###
###start_vector = start_vectors.RandomStartVector()
###beta_start = start_vector.get_vector((var_x, 1))
###
###algorithm = algorithms.ISTA(output=True, eps=consts.TOLERANCE,
###                            max_iter=100000, min_iter=1)
###beta, info = algorithm(f, beta_start)
###
###f_star = f.f(beta_star)
###
###plot.figure()
###plot.plot(beta_star, 'g')
###plot.plot(beta, 'r')
###plot.title("Weight vectors")
###plot.show()
###
###plot.figure()
###plot.plot(info["f"], 'g')
###plot.plot([0, len(info["f"])], [f_star, f_star])
###plot.yscale("log")
###plot.title("Convergence")
###plot.show()
##
##X = np.random.randn(10, var_x)
##Y = np.random.rand(10, var_y)
##mX = np.mean(X)
##mY = np.mean(Y)
##X = X - mX
##Y = Y - mY
##constraintX_1 = functions.L1(c=2.0)
##constraintX_2 = functions.RGCCAConstraint(c=1.0, tau=1.0, X=X, unbiased=True)
##constraintX = functions.CombinedProjectionOperator([constraintX_1,
##                                                    constraintX_2])
##
##constraintY_1 = functions.L1(c=2.0)
##constraintY_2 = functions.RGCCAConstraint(c=1.0, tau=1.0, X=Y, unbiased=True)
##constraintY = functions.CombinedProjectionOperator([constraintY_1,
##                                                    constraintY_2])
##
##w = (np.random.rand(var_x, 1) * 2.0) - 1.0
##w = constraintX.proj(w)
##c = (np.random.rand(var_y, 1) * 2.0) - 1.0
##c = constraintY.proj(c)
##
##Agl = gl.A_from_groups(var_x, [range(0, var_x/2), range(var_x/2, var_x)])
##gl = functions.GroupLassoOverlap(l=0.5, A=Agl, mu=0.00001)
##
##Atv, n_compacts = tv.A_from_shape((1, 1, var_y))
##tv = functions.TotalVariation(l=0.1, A=Atv, mu=0.00001)
##
##funcX = functions.LatentVariableCovariance([X, Y], unbiased=True)
##funcY = functions.LatentVariableCovariance([Y, X], unbiased=True)
##
##function = functions.GeneralisedMultiblock([X, Y], [[[gl], funcX],
##                                                    [funcY, []]])
##function.add_constraint(constraintX, 0)
##function.add_constraint(constraintY, 1)
##
##algorithm = algorithms.MultiblockProjectedGradientMethod(outer_iter=25,
##                                                         max_iter=2000,
##                                                         output=True)
##
##(w_mb, output_mb) = algorithm(function, [w, c])
##
##print "Done!"
##sys.stdout.flush()
##
###for i in xrange(30):
###    for j in xrange(5000):
###        w = w - 0.01 * funcX.grad([w, c], 0)
###    w = w / maths.norm(w)
###    for j in xrange(5000):
###        c = c - 0.01 * funcY.grad([c, w], 0)
###    c = c / maths.norm(c)
##
###for i in xrange(500):
###    w = np.dot(X.T, np.dot(Y, c))
####    w = w / maths.norm(w)
###    w = constraintX.proj(w)
####    print "l1:", maths.norm1(w), \
####        ", l2:", maths.norm(w)
###
###    c = np.dot(Y.T, np.dot(X, w))
####    c = c / maths.norm(c)
###    c = constraintY.proj(c)
##
##print "l1:", maths.norm1(w), \
##    ", l2:", maths.norm(w)
##print "l1:", maths.norm1(c), \
##    ", l2:", maths.norm(c)
###w = -w
##
###    c = np.dot(Y.T, np.dot(X, w))
###    c = c / maths.norm(c)
####    c = constraintY.proj(c)
###    w = np.dot(X.T, np.dot(Y, c))
####    if i == its - 1:
####        print "norm: ", maths.norm(w)
####    w = constraintX.proj(w)
###    w = w / maths.norm(w)
##
##print w
##print w_mb[0]
##print "f(w)    : ", function.f([w, c])
##print "f(w_mb) : ", function.f(w_mb)
##print "cov     : ", funcX.f([w, c])
##print "cov mb  : ", funcX.f(w_mb)
##print "corr    : ", maths.corr(np.dot(X, w), np.dot(Y, c))
##print "corr mb : ", maths.corr(np.dot(X, w_mb[0]), np.dot(Y, w_mb[1]))
###print out[1]
###print c
##
##plot.figure()
##plot.plot(w, 'g')
##plot.plot(c, '-.g')
##plot.plot(w_mb[0], 'r')
##plot.plot(w_mb[1], '-.r')
##plot.title("Weight vectors")
##plot.show()
##
##plot.figure()
##plot.plot(np.dot(X, w), 'g')
##plot.plot(np.dot(Y, c), '-.g')
##plot.plot(np.dot(X, w_mb[0]), 'r')
##plot.plot(np.dot(Y, w_mb[1]), '-.r')
##plot.title("Score vectors")
##plot.show()
##
##plot.figure()
##plot.plot(output_mb['f'])
##plot.title("Convergence")
##plot.show()
##
##
###import numpy as np
###import parsimony.utils as utils
####from parsimony import *
###import parsimony.models as models
###import parsimony.preprocess as preprocess
###import parsimony.start_vectors as start_vectors
###import parsimony.loss_functions as loss_functions
###import parsimony.algorithms as algorithms
###import parsimony.data.simulated.lasso as lasso
###import parsimony.data.simulated.ridge as ridge
###import parsimony.data.simulated.l1_l2 as l1_l2
###import parsimony.data.simulated.l1_l2_2D as l1_l2_2D
###import parsimony.data.simulated.ridge_2D as ridge_2D
###import parsimony.data.simulated.lasso_2D as lasso_2D
####import parsimony.data.simulated.l2_2D as l2_2D
###import parsimony.data.simulated.l1_tv as l1_tv
###import parsimony.data.simulated.l1_l2_tv as l1_l2_tv
###import parsimony.data.simulated.l1_l2_tv_2D as l1_l2_tv_2D
####import multiblock.start_vectors as start_vectors
####import multiblock.prox_ops as prox_ops
####import multiblock.schemes as schemes
####from sklearn.datasets import load_linnerud
###from time import time
###
###import matplotlib.pyplot as plot
###import matplotlib.cm as cm
####import pylab
###import copy
###
###
###def test_lasso():
###
###    np.random.seed(42)
###
###    eps = 0.01
###    maxit = 10000
###
###    px = 100
###    py = 1
###    pz = 1
###    p = px * py * pz  # Must be even!
###    n = 60
###    X = np.random.randn(n, p)
###    betastar = np.concatenate((np.zeros((p / 2, 1)),
###                               np.random.randn(p / 2, 1)))
###    betastar = np.sort(np.abs(betastar), axis=0)
###    y = np.dot(X, betastar)
###
###
###    print "LinearRegression"
###    lr = models.LinearRegression()
###    lr.set_max_iter(maxit)
###    lr.set_tolerance(eps)
###    lr.fit(X, y)
###    computed_beta = lr.beta
###
###    plot.subplot(3, 1, 1)
###    plot.plot(betastar[:, 0], '-', computed_beta[:, 0], '*')
###    plot.title("Linear regression")
###
###
###
###    print "LASSO"
###    l = 20.0
###    lasso = models.LASSO(l)
###    lasso.set_max_iter(maxit)
###    lasso.set_tolerance(eps)
###
###    lasso.fit(X, y)
###    computed_beta = lasso.beta
###
###    plot.subplot(3, 1, 2)
###    plot.plot(betastar[:, 0], '-', computed_beta[:, 0], '*')
###    plot.title("LASSO")
###
###
###
###    print "LinearRegressionTV"
###    gamma = 0.01
###    lrtv = models.LinearRegressionTV(gamma, (pz, py, px), mu=0.01)
###    lrtv.set_max_iter(maxit)
###    lrtv.set_tolerance(eps)
###    cr = models.ContinuationRun(lrtv, [1.0, 0.1, 0.01, 0.001, 0.0001])
###
###    cr.fit(X, y)
###    computed_beta = cr.beta
###
###    plot.subplot(3, 1, 3)
###    plot.plot(betastar[:, 0], '-', computed_beta[:, 0], '*')
###    plot.title("Linear regression + TV")
###
###
###
####    print "LinearRegressionL1TV"
####    gamma = 0.01
####    l = 1.0
####    lrl1tv = models.LinearRegressionL1TV(l, gamma, (pz, py, px), mu=0.01)
####    lrl1tv.set_max_iter(maxit)
####    lrl1tv.set_tolerance(eps)
####    cr = models.ContinuationRun(lrtv, [1.0, 0.1, 0.01, 0.001, 0.0001])
####
####    cr.fit(X, y)
####    computed_beta = cr.beta
####
####    plot.subplot(4, 1, 4)
####    plot.plot(betastar[:, 0], '-', computed_beta[:, 0], '*')
####    plot.title("Linear regression + TV + L1")
###
###    plot.show()
###
###
###def test_lasso_tv():
###    np.random.seed(42)
###
###    x = np.arange(-10, 10, 1)
###    y = np.arange(-10, 10, 1)
###    nrows, ncols = len(x), len(y)
###    px = ncols
###    py = nrows
###    pz = 1
###    p = nrows * ncols
###    n = 70
###    mask = np.zeros((nrows, ncols))
###    beta = np.zeros((nrows, ncols))
###    for i in xrange(nrows):
###        for j in xrange(ncols):
####            if (((x[i] - 3) ** 2 + (y[j] - 3) ** 2 > 8) &
####                ((x[i] - 3) ** 2 + (y[j] - 3) ** 2 < 25)):
####                mask[i, j] = 1
###
###            if ((x[i] - 3) ** 2 + (y[j] - 3) ** 2 < 25):
###                mask[i, j] = 1
###
###            if (((x[i] + 1) ** 2 + (y[j] - 5) ** 2 > 5) &
###                ((x[i] + 1) ** 2 + (y[j] - 5) ** 2 < 16)):
###                mask[i, j] = 1
###
###            if (y[j] > 1) & (x[i] > 3) & (y[j] + x[i] < 10):
###                beta[i, j] = (x[i] - 3) ** 2 + (y[j] - 3) ** 2 + 25
###
####    beta = np.random.rand(nrows, ncols)
####    beta = np.sort(np.abs(beta), axis=0)
####    beta = np.sort(np.abs(beta), axis=1)
###
###    beta1D = beta.reshape((p, 1))
###    mask1D = mask.reshape((p, 1))
###
####    u = np.random.randn(p, p)
###    u = np.eye(p, p)
###    sigma = np.dot(u.T, u)
###    mean = np.zeros(p)
###
###    X = np.random.multivariate_normal(mean, sigma, n)
###    y = np.dot(X, beta1D)
###
###    eps = 0.01
###    maxit = 50000
###
###    num_mus = 1
###    mus = [0] * num_mus
###    mus[0] = 10.0
####    mus[1] = 0.01
####    mus[2] = 0.0001
####    mus[3] = 0.000001
####    mus[4] = 0.00000001
###
###    lr = models.LinearRegression()
###    lr.set_max_iter(maxit)
###    lr.set_tolerance(eps)
###    lr.fit(X, y)
###    computed_beta = lr.beta
###
###    plot.subplot(3, 3, 1)
###    plot.plot(beta1D[:, 0], '-', computed_beta[:, 0], '*')
###    plot.title("Linear regression")
###
###    plot.subplot(3, 3, 2)
###    plot.imshow(beta, interpolation='nearest', cmap=cm.gist_rainbow)
###
###    plot.subplot(3, 3, 3)
###    plot.imshow(np.reshape(computed_beta, (pz, py, px))[0, :, :],
###                interpolation='nearest', cmap=cm.gist_rainbow)
###
###
###
###    l = 1.0
###    l1 = models.LASSO(l)
###    l1.set_max_iter(maxit)
###    l1.set_tolerance(eps)
###    l1.fit(X, y)
###    computed_beta = l1.beta
###
###    plot.subplot(3, 3, 4)
###    plot.plot(beta1D[:, 0], '-', computed_beta[:, 0], '*')
###    plot.title("LASSO")
###
###    plot.subplot(3, 3, 5)
###    plot.imshow(beta, interpolation='nearest', cmap=cm.gist_rainbow)
###
###    plot.subplot(3, 3, 6)
###    plot.imshow(np.reshape(computed_beta, (pz, py, px))[0, :, :],
###                interpolation='nearest', cmap=cm.gist_rainbow)
###
###
###    gamma = 10.0
###    lrtv = models.LinearRegressionTV(gamma, (pz, py, px), mu=mus[0])
###    lrtv.set_max_iter(maxit)
###    lrtv.set_tolerance(eps)
###    lrtv.fit(X, y)
###    computed_beta = lrtv.beta
###
###    plot.subplot(3, 3, 7)
###    plot.plot(beta1D[:, 0], '-', computed_beta[:, 0], '*')
###    plot.title("Linear regression + TV")
###
###    plot.subplot(3, 3, 8)
###    plot.imshow(beta, interpolation='nearest', cmap=cm.gist_rainbow)
###
###    plot.subplot(3, 3, 9)
###    plot.imshow(np.reshape(computed_beta, (pz, py, px))[0, :, :],
###                interpolation='nearest', cmap=cm.gist_rainbow)
###
###    plot.show()
###
###
###def test_tv():
###
###    np.random.seed(42)
###
###    x = np.arange(-10, 10, 1)
###    y = np.arange(-10, 10, 1)
###    nrows, ncols = len(x), len(y)
###    px = ncols
###    py = nrows
###    pz = 1
###    p = nrows * ncols
###    n = 70
###    mask = np.zeros((nrows, ncols))
###    beta = np.zeros((nrows, ncols))
###    for i in xrange(nrows):
###        for j in xrange(ncols):
####            if (((x[i] - 3) ** 2 + (y[j] - 3) ** 2 > 8) &
####                ((x[i] - 3) ** 2 + (y[j] - 3) ** 2 < 25)):
####                mask[i, j] = 1
###
###            if ((x[i] - 3) ** 2 + (y[j] - 3) ** 2 < 25):
###                mask[i, j] = 1
###
###            if (((x[i] + 1) ** 2 + (y[j] - 5) ** 2 > 5) &
###                ((x[i] + 1) ** 2 + (y[j] - 5) ** 2 < 16)):
###                mask[i, j] = 1
###
###            if (y[j] > 1) & (x[i] > 3) & (y[j] + x[i] < 10):
###                beta[i, j] = (x[i] - 3) ** 2 + (y[j] - 3) ** 2 + 25
###
####    beta = np.random.rand(nrows, ncols)
####    beta = np.sort(np.abs(beta), axis=0)
####    beta = np.sort(np.abs(beta), axis=1)
###
###    beta1D = beta.reshape((p, 1))
###    mask1D = mask.reshape((p, 1))
###
###    r = 0.0
###    u = r * np.random.randn(p, p)
###    u += (1.0 - r) * np.eye(p, p)
###    sigma = np.dot(u.T, u)
###    mean = np.zeros(p)
###
####    pylab.imshow(beta, extent=(x.min(), x.max(), y.max(), y.min()),
####               interpolation='nearest', cmap=cm.gist_rainbow)
####    pylab.show()
####
####    pylab.imshow(mask, extent=(x.min(), x.max(), y.max(), y.min()),
####               interpolation='nearest', cmap=cm.gist_rainbow)
####    pylab.show()
###
###    X = np.random.multivariate_normal(mean, sigma, n)
###    y = np.dot(X, beta1D)
###
####    px = 1
####    py = 300
####    pz = 1
####    p = px * py * pz  # Must be even!
####    n = 50
####    X = np.random.randn(n, p)
####    betastar = np.concatenate((np.zeros((p / 2, 1)),
####                               np.random.randn(p / 2, 1)))
####    beta1D = np.sort(np.abs(betastar), axis=0)
####    y = np.dot(X, beta1D)
###
###    eps = 0.001
###    maxit = 100000
###
###    gamma = 5.0
###    l = 0.1
###    en_lambda = 0.95
###
###    num_mus = 1
###    mus = [0] * num_mus
###    mus[0] = 0.1  # 2.0 * eps / (p - 1.0)
####    mus[1] = 0.01
####    mus[2] = 0.0001
####    mus[3] = 0.000001
####    mus[4] = 0.00000001
####    for k in xrange(0, num_mus - 1):
####        tau = 2.0 / (float(k) + 3.0)
####        mus[k + 1] = (1.0 - tau) * mus[k]
###
####    r = 0
####    for i in xrange(X.shape[1]):
####        r = max(r, abs(utils.cov(X[:, [i]], y)))
####    mus = [r * 0.5 ** i for i in xrange(num_mus)]
###
###    total_start = time()
###    init_start = time()
###
###    mask1D = mask1D.flatten().astype(int).tolist()
###    preprocess_mask = preprocess.Mask(mask1D)
####    X = preprocess_mask.process(X)
###
###    lrtv = models.LinearRegressionTV(gamma, (pz, py, px), mu=mus[0])#,
###                                     #mask=mask1D)
###    lrtv.set_max_iter(maxit)
###    lrtv.set_tolerance(eps)
###    method = lrtv
####    cr = models.ContinuationRun(lrtv, mus)
####    method = cr
###
####    rrtv = RidgeRegressionTV(1.0 - en_lambda, gamma, (pz, py, px), mask=mask1D)
####    rrtv.set_max_iter(maxit)
####    rrtv.set_tolerance(eps)
####    method = rrtv
###
###    print "Init time:", (time() - init_start)
###
###    method.fit(X, y)
###    computed_beta = method.beta
####    computed_beta = preprocess_mask.revert(method.beta.T).T
###
###    alg = method.get_algorithm()
###    print "Algorithm:", alg
###    print "Total time:", (time() - total_start)
###    print "Total iterations:", alg.iterations, "(%d)" % len(alg.f)
###    print "Error:", alg.f[-1]
###
####    from scipy import fftpack
####    ft = fftpack.fft(alg.f)
####    n = ft.shape[0]
####    k = 20000
####    if n % 2 != 0:
####        n += 1  # Must be even
####    test = np.array(ft)
####    test[k:n / 2] = 0
####    test[n / 2:-k] = 0
####    ift = fftpack.ifft(test).real
####    from scipy.interpolate import UnivariateSpline
####    x = range(len(alg.f))
####    y = np.log10(alg.f)
####    spline = UnivariateSpline(x, y, s=1)
####    smooth = spline(x)
###
####    y = (alg.f[30000:])
####    n = len(y)
###
####    k = 10
####    if n % k != 0:
####        n -= n % k
####    y = y[:n]
####    x = range(n)
####    print "len: ", n
####
####    from scipy.interpolate import UnivariateSpline
####    spline = UnivariateSpline(x, y, s=5e-16, k=1)
####    smooth = spline(x)
###
####    smooth = [0] * n
####    for i in xrange(0, n, k):
####        X = np.reshape(np.array(x[i:i + k]), (k, 1))
####        X = np.hstack((np.ones((k, 1)), X))
####        b = np.dot(np.linalg.pinv(X), y[i:i + k])
####        smooth[i:i + k] = np.dot(X, b)
###
####    for i in xrange(n):
####        left = max(0, i - k)
####        right = min(i + k, n - 1) + 1
####        smooth[i] = sum(y[left:right]) / (right - left)
####        print "i:", i
####        print "left:", left
####        print "right:", right
####        print "values:", y[left:right]
####        print "sum:", sum(y[left:right])
####        print "denom:", (right - left)
####        print
####    F = np.array(y)
####    S = np.array(smooth)
####    d = np.min(F)
####    F /= d
####    S /= d
####    y = F.tolist()
####    smooth = S.tolist()
####
####    print "alg.f[i]:", y[-1]
####    i = len(y) - 1
####    while y[i] == y[-1]:
####        i -= 1
####    print "alg.f[i]:", y[i]
####    print "diff:", (y[i] - y[-1])
####
####    fig = plot.figure()
####    ax = fig.add_subplot(1, 1, 1)
####    ax.plot(x, y, '-b', x, smooth, '-r')
#####    ax.plot(x, y, '-b')
####    plot.title("f: " + str(alg.f[-1]))
####    plot.show()
###
####    return
###
###    plot.subplot(2, 2, 1)
###    plot.plot(beta1D[:, 0], '-', computed_beta[:, 0], '*')
###    plot.title("Iterations: " + str(alg.iterations))
###
###    plot.subplot(2, 2, 3)
###    plot.plot(alg.f, '-b')
###    plot.title("f: " + str(alg.f[-1]))
###
###    plot.subplot(2, 2, 2)
###    plot.imshow(beta,  # , extent=(x.min(), x.max(), y.max(), y.min()),
###                interpolation='nearest', cmap=cm.gist_rainbow)
###
###    plot.subplot(2, 2, 4)
###    plot.imshow(np.reshape(computed_beta, (pz, py, px))[0, :, :],# + mask,
###                # extent=(x.min(), x.max(), y.max(), y.min()),
###                interpolation='nearest', cmap=cm.gist_rainbow)
###    plot.show()
###
###
###def test_logistic_regression():
###
###    import numpy as np
###
###    n = 200
###    p = 50
###    # generate a Gaussian dataset
###    x = np.random.randn(n, p)
###    # generate a beta with "overlapping groups" of coefficients
###    beta1 = beta2 = beta3 = np.zeros((p, 1))
###    beta1[0:20] = np.random.randn(20, 1)
###    beta2[15:35] = np.random.randn(20, 1)
###    beta3[27:50] = np.random.randn(23, 1)
###    beta = beta1 + beta2 + beta3
###
###    # compute X beta
###    combi = np.dot(x, beta)
###
###    # compute the class of each individual
###    proba = 1 / (1 + np.exp(-combi))
###    y = np.zeros((n, 1))
###    for i in xrange(n):
###        y[i] = np.random.binomial(1, proba[i], 1)
###
###
###def test_data():
###
####    vector = start_vectors.GaussianCurveVector(normalise=False)
####
####    M = 100
####    N = 100
####    n_points = 5
####
####    means = np.random.rand(1, 2)
####    for i in xrange(1, n_points):
#####        p = np.random.rand(1, 2)
#####        while np.any(np.sqrt(np.sum((means - p) ** 2.0, axis=1))
#                    < max(0.2, (1.0 / n_points))):
#####            p = np.random.rand(1, 2)
#####        print np.sqrt(np.sum((means - p) ** 2.0, axis=1))
#####        means = np.vstack((means, p))
####
#####        det = 0.0
#####        p_best = 0
#####        for j in xrange(100):
#####            p = np.random.rand(1, 2)
#####            Ap = np.vstack((means, p))
#####            det_curr = abs(np.linalg.det(np.dot(Ap.T, Ap)))
#####            if det_curr > det:
#####                p_best = p
#####                det = det_curr
#####        print det
#####        means = np.vstack((means, p_best))
####
#####    while abs(np.linalg.det(np.dot(means.T, means))) < 0.15:
#####        means = np.random.rand(n_points, 2)
####
####        dist = 0.0
####        p_best = 0
####        for j in xrange(20):
####            p = np.random.rand(1, 2)
####            dist_curr = np.min(np.sqrt(np.sum((means - p) ** 2.0, axis=1)))
####            if dist_curr > dist:
####                p_best = p
####                dist = dist_curr
####            if dist_curr > 0.3:
####                break
####        means = np.vstack((means, p_best))
####
####    means[means < 0.05] = 0.05
####    means[means > 0.95] = 0.95
####    means[:, 0] *= M
####    means[:, 1] *= N
####    means = means.tolist()
#####    means = [[0.3 * M, 0.3 * N], [0.7 * M, 0.7 * N]]
####
####    covs = [0] * n_points
####    for i in xrange(n_points):
####        S1 = np.diag((np.abs(np.diag(np.random.rand(2, 2))) * 0.5) + 0.5)
####
####        S2 = np.random.rand(2, 2)
####        S2 = (((S2 + S2.T) / 2.0) - 0.5) * 0.9  # [0, 0.45]
####        S2 = S2 - np.diag(np.diag(S2))
####
####        S = S1 + S2
####
####        S /= np.max(S)
####
####        S *= float(min(M, N))
####
####        covs[i] = S.tolist()
####
#####    d = min(M, N)
#####    covs = [[[1.0*M, 0.2*d], [0.2*d, 1.0*N]],
#####            [[1.0*M, -0.2*d], [-0.2*d, 1.0*N]]]
####
####    size=[M, N]
####    dims = 2
####    p = size[0] * size[1]
#####    S = 2.0 * (np.random.rand(dims, dims) - 0.5)
#####    S = np.dot(S.T, S) / 2.0
#####    for i in xrange(dims):
#####        if abs(S[i, i]) < 0.5:
#####            if S[i, i] > 0:
#####                S[i, i] = 0.5
#####            else:
#####                S[i, i] = -0.5
#####    S = (p ** (1.0 / dims)) * S / np.max(S)
#####    X = vector.get_vector(shape=(p, 1), dims=dims)
####    X = np.zeros((p, 1))
####    for i in xrange(n_points):
####        X = X + vector.get_vector(size=size, dims=dims,
####                                  mean=means[i], cov=covs[i])
####
####    X = np.reshape(X, size)
###
###    dims = 2
###    size = [100, 100]
###    vector = start_vectors.GaussianCurveVectors(num_points=3, normalise=False)
###
###    w = vector.get_vector(size=size, dims=dims)
###    X = np.reshape(w, size)
###
###    cmap = cm.hot  # cm.RdBu
###    if dims == 1:
###        plot.plot(X, '-')
###    elif dims == 2:
###        plot.imshow(X, interpolation='nearest', cmap=cmap)
###    elif dims == 3:
###        m = np.max(X)
###        for i in xrange(X.shape[0]):
###            plot.subplot(X.shape[0], 1, i)
###            plot.imshow(X[i, :, :], interpolation='nearest', vmin=0.0, vmax=m,
###                        cmap=cmap)
####            plot.set_cmap('hot')
###    plot.show()
###
###
###def create_data(
###        grp_desc =[range(100), range(100,200), range(200,300), range(300,400),
#                      range(400,1000)],
###        grp_cors = [0.8, 0, 0.8, 0, 0],
###        grp_assoc = [0.5, 0.5, 0.3, 0.3, 0],
###        grp_firstonly = [True, False, True, False, False],
###        n = 100,
###        labelswapprob = 0,
###        basehaz = 0.2,
###        intercept = 0):
###    """
###    create data with X : n x p observations with groups of variables
###    with intra-group correlation (grp_cors) and effect on the outcome(betas).
###     the outcome is logistic and potentially noisy (intercept, labelswapprob)
###    """
###    p = sum([len(i) for i in grp_desc])
###    X = np.zeros( (n, p) )
###    y = np.zeros( n )
###    sigma = np.zeros( (p,p) )
###    betas = np.zeros( p )
###
###    for b,c,a,o in zip(grp_desc, grp_cors, grp_assoc, grp_firstonly):
###       #print b[0]
###       sigma[b[0]:(b[-1]+1), b[0]:(b[-1]+1)] = c
###       sigma[b[0]:(b[-1]+1), b[0]:(b[-1]+1)] += (1.0 - c) * np.eye(len(b),len(b))
###       #print sigma
###       center = np.zeros(len(b))
###       X[:,b] = np.random.multivariate_normal(center, sigma[b[0]:(b[-1]+1),
#                                                 b[0]:(b[-1]+1)], n)
###       if o:
###           betas[b[0]] = a
###       else:
###           betas[b[0]:(b[-1]+1)] = a
###
###    predlin = np.dot(X, betas)
###
###    p = 1./(1. + np.exp(-(predlin + intercept)))
###    for i in xrange(n):
###        y[i] = np.random.binomial(1, p[i], 1)
###
###    return X, y, betas, grp_desc, sigma
###
###
###if __name__ == "__main__":
####    test_tv()
####    test_lasso()
####    test_lasso_tv()
####    test_data()
###
####    from pylab import *
####    from numpy import outer
####    rc('text', usetex=False)
####    a=outer(arange(0,1,0.01),ones(10))
####    figure(figsize=(10,5))
####    subplots_adjust(top=0.8,bottom=0.05,left=0.01,right=0.99)
####    maps=[m for m in cm.datad if not m.endswith("_r")]
####    maps.sort()
####    l=len(maps)+1
####    for i, m in enumerate(maps):
####        subplot(1,l,i+1)
####        axis("off")
####        imshow(a,aspect='auto',cmap=get_cmap(m),origin="lower")
####        title(m,rotation=90,fontsize=10)
####    show()
###
####    pz = 2
####    py = 2
####    px = 3
####    p = px * py * pz
#####    beta = np.ones((pz * py * px, 1))
#####    X = np.reshape(xrange(p), (pz, py, px))
####    X = np.ones((5, pz * py * px))
####    print X
####    lrtv = models.LinearRegressionTV(10.0, (pz, py, px), mu=10.0)
####    beta = lrtv.get_start_vector().get_vector(X)
#####    print lrtv._tv.grad(beta).T
####    Ax, Ay, Az = lrtv.get_g().A()
####    print Ax.todense()
####    print Ay.todense()
####    print Az.todense()
####
####    mu = 0.1
####    asx = Ax.dot(beta) / mu
####    asy = Ay.dot(beta) / mu
####    asz = Az.dot(beta) / mu
####
####    print asx
####    print asy
####    print asz
####
####    print "norm: ", np.sqrt(asx ** 2.0 + asy ** 2.0 + asz ** 2.0)
####
####    # Apply projection
####    asx, asy, asz = lrtv.get_g().projection((asx, asy, asz))
####
####    print asx
####    print asy
####    print asz
###
###
####    import pickle
####    O = pickle.load(open("/home/tl236864/objs.pickle"))
####    y = O[0]
####    X = O[1]
####    groups = O[2]
####
####    for i in xrange(len(groups) - 1, -1, -1):
####        if len(groups[i]) == 0:
####            del groups[i]
####            print "group %d deleted!" % (i,)
####
####    gamma = 1.0
####    mu = 0.01
####    weights = [1.0] * len(groups)
####
####    lr = loss_functions.LogisticRegressionError()
####    gl = loss_functions.GroupLassoOverlap(gamma, X.shape[1], groups, mu,
####                                          weights)
####    combo = loss_functions.CombinedNesterovLossFunction(lr, gl)
####
####    algorithm = algorithms.ISTARegression(combo)
####    algorithm._set_tolerance(0.01)
####    algorithm._set_max_iter(1000)
####    lr.set_data(X, y)
####    beta = algorithm.run(X, y)
###
####    # Test group lasso!!
####    import scipy
####
####    np.random.seed(42)
####
####    p = 40
####    betastar = np.zeros((p, 1)).ravel()
#####    betastar = [0., 0., 0., 0., 0., .5, .7, 1., .6, .7, 0., 0., 0., 0., 0.]
#####    groups = [[5, 6, 7, 8, 9]]
#####    groups = [range(p / 3), range(p / 3, 2 * p / 3), range(2 * p / 3, p)]
####    groups = [range(p / 3, 2 * p / 3), range(p)]
####    betastar[groups[0]] = 1
####
####    p = len(betastar)
####    n = 20
####
####    r = 0.0
####    u = r * np.random.randn(p, p)
####    u += (1.0 - r) * np.eye(p, p)
####    sigma = np.dot(u.T, u)
####    mean = np.zeros(p)
####
####    X = np.random.multivariate_normal(mean, sigma, n)
####    y = np.reshape(np.dot(X, betastar), (n, 1))
####
#####    eps = 0.0001
####    gamma = 1.0
#####    weights = [1.0] * len(groups)
####
#####    lrgl = models.LinearRegressionGL(gamma, p, groups)
####    lrgl = models.LinearRegressionTV(gamma, (1, 1, p))
####    cont = models.ContinuationRun(lrgl,
####                                  mus=[10, 1.0, 0.1, 0.01, 0.001, 0.0001])
####    cont.set_tolerance(0.00001)
####    cont.set_max_iter(10000)
#####    lrgl.set_data(X, y)
#####    lrgl.set_mu(lrgl.compute_mu(eps))
####    cont.fit(X, y)
####
####    alg = cont.get_algorithm()
####    print cont.get_transform()
####    print alg.iterations
####
####    plot.subplot(2, 1, 1)
####    plot.plot(betastar, '-g', cont.beta, '*r')
####
####    plot.subplot(2, 1, 2)
####    plot.plot(alg.f)
####    plot.title("Iterations: " + str(alg.iterations))
####
####    plot.show()
###
###
####    #  Test Logistic Group Lasso ==========
####    np.random.seed(42)
####    X, y, betas, groups, sigma = create_data()
####    #    eps = 0.0001
####    gamma = 10.
####    #    weights = [1.0] * len(groups)
####    p = len(betas)
####    lrgl = models.LogisticRegressionGL(gamma,p, groups, mu=None, weights=None)
####    cont = models.ContinuationRun(lrgl,
####                                 tolerances=[ 0.1, 0.01, 0.001, 0.0001])
####    #    lrgl.set_tolerance(eps)
####    cont.set_max_iter(1000)
####    #    lrgl.set_data(X, y)
####    #    lrgl.set_mu(lrgl.compute_mu(eps))
####    cont.fit(X, y)
####
####    alg = cont.get_algorithm()
####    print cont.get_transform()
####    print alg.iterations
####
####    plot.subplot(2, 1, 1)
####    plot.plot(betas, '-g', cont.beta, '*r')
####
####    plot.subplot(2, 1, 2)
####    plot.plot(alg.f)
####    plot.title("Iterations: " + str(alg.iterations))
####
####    plot.show()
####
####    # Test group lasso!!
####    import scipy
####
####    return
###
###
####    np.random.seed(42)
####
####    maxit = 10000
####
####    px = 100
####    py = 1
####    pz = 1
####    p = px * py * pz  # Must be even!
####    n = 60
####    X = np.random.randn(n, p)
####    betastar = np.concatenate((np.zeros((p / 2, 1)),
####                               np.random.randn(p / 2, 1)))
####    betastar = np.sort(np.abs(betastar), axis=0)
####    y = np.dot(X, betastar)
####
####    m = models.NesterovProximalGradientMethod()
####
####    gamma = 1.0
####    shape = [pz, py, px]
####    mu = 0.01
####    tv = loss_functions.TotalVariation(gamma, shape, mu)
####    lr = loss_functions.LinearRegressionError()
####    combo = loss_functions.CombinedNesterovLossFunction(lr, tv)
####
####    m.set_g(combo)
####    combo.set_data(X, y)
####
####    D = tv.num_compacts() / 2.0
####    print "D:", D
#####    _A = tv.Lipschitz(mu) * mu
####    A = tv.Lipschitz(1.0)
#####    assert abs(_A - A) < 0.0000001
####    l = lr.Lipschitz()
####
#####    import scipy.sparse as sparse
#####    A_ = sparse.vstack(tv.A()).todense()
#####    L, V = np.linalg.eig(np.dot(A_.T, A_))
#####    print max(L)
####
####    print "A:", A
####    print "l:", l
####
####    def mu_plus(eps):
####        return (-2.0 * D * A + np.sqrt((2.0 * D * A) ** 2.0 + 4.0 * D * l *
#                    eps * A)) / (2.0 * D * l)
####
####    def eps_plus(mu):
####        return ((2.0 * mu * D * l + 2.0 * D * A) ** 2.0 - 
#                    (2.0 * D * A) ** 2.0) / (4.0 * D * l * A)
####
####    m.algorithm._set_tolerance(m.compute_tolerance(mu))
####    beta = m.algorithm.run(X, y)
####
####    for eps in [1000000.0, 100000.0, 10000.0, 1000.0, 100.0, 10.0, 1.0, 0.1,
#                    0.01, 0.001]:
####        print "eps: %.7f -> mu: %.7f -> eps: %.7f" % (eps, mu_plus(eps),
#                                                          eps_plus(mu_plus(eps)))
####        print "eps: %.7f -> mu: %.7f -> eps: %.7f" % (eps, m.compute_mu(eps),
#                                          m.compute_tolerance(m.compute_mu(eps)))
####        print "D * mu = %.7f" % (D * mu)
###
####    mu1 = []
####    mu2 = []
####    eps = []
####    for _eps in xrange(1, 1000):
####        eps.append(_eps / 1000.0)
####
#####        mu1.append(mu_plus(eps[-1]))
#####        mu2.append(m.compute_mu(eps[-1]))
####        mu1.append(eps_plus(eps[-1]))
####        mu2.append(m.compute_tolerance(eps[-1]))
####
####    plot.plot(eps, mu1, '-r')
####    plot.plot(eps, mu2, '-g')
####    plot.show()
####    print mu1[-10:]
####    print mu2[-10:]
###
####    eps = 0.01
####    mu = mu_plus(eps)
####
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_mu(eps), mu, time() - s)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_tolerance(mu), eps, time() - s)
####    print
####
####    eps = 0.3
####    mu = mu_plus(eps)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_mu(eps), mu, time() - s)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_tolerance(mu), eps, time() - s)
####    print
####
####    eps = 1.0
####    mu = mu_plus(eps)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_mu(eps), mu, time() - s)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_tolerance(mu), eps, time() - s)
####    print
####
####    mu = 0.00149
####    eps = eps_plus(mu)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_tolerance(mu), eps, time() - s)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_mu(eps), mu, time() - s)
####    print
####
####    mu = 0.01949
####    eps = eps_plus(mu)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_tolerance(mu), eps, time() - s)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_mu(eps), mu, time() - s)
####    print
####
####    mu = 0.03975
####    eps = eps_plus(mu)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_tolerance(mu), eps, time() - s)
####    s = time()
####    print "%.5f = %.5f? (%f s)" % (m.compute_mu(eps), mu, time() - s)
####    print
###
####    # Testing the new continuation
####    np.random.seed(42)
####
####    eps = 0.00001
####    maxit = 5
####    cont_maxit = 100
####    gamma = 0.0
####    l = 0.6
####    k = 1.0 - l
####
####    px = 1000
####    py = 1
####    pz = 1
####    p = px * py * pz  # Must be even!
####    n = 100
####    X = np.random.randn(n, p)
####    betastar = np.concatenate((np.zeros((p / 2, 1)),
####                               np.random.randn(p / 2, 1)))
####    betastar = np.sort(np.abs(betastar), axis=0)
####    y = np.dot(X, betastar)
####
#####    Sigma = 0.999 * np.ones((p, p)) + 0.001 * np.eye(p)
#####    Mu = np.zeros(p)
#####    M = np.random.multivariate_normal(Mu, Sigma, n)
#####    e = np.random.randn(n, 1)
#####    e = e / np.sqrt(np.sum(e ** 2.0))
#####    X, y, betastar = l1_l2_tv.load(l, k, gamma, density=0.5, snr=100.0,
#####                                   M=M, e=e)
#####    start_vector = start_vectors.IdentityStartVector(betastar \
#####                                + 0.001 * np.random.randn(*betastar.shape))
####
####    start = time()
####    m = models.RidgeRegressionL1TV(l, k, gamma, shape=(pz, py, px),
####                                   compress=False)  # , mu=0.01)
####    m.set_tolerance(eps)
####    m.set_max_iter(maxit)
#####    m.set_max_iter(5000000)
#####    m.set_start_vector(start_vector)
#####    c = m
####    c = models.Continuation(m, cont_maxit)
####    c.fit(X, y)
####    computed_beta = c._beta
####    print "time: ", (time() - start)
####
####    print "f: ", c.get_algorithm().f[-1]
####    print "its: ", c.get_algorithm().iterations
####
####    plot.subplot(2, 2, 1)
####    plot.plot(betastar[:, 0], '-', computed_beta[:, 0], '*')
####    plot.subplot(2, 2, 2)
####    plot.plot(c.get_algorithm().f)
####    plot.title("Continuation")
####
####    start = time()
####    m = models.RidgeRegressionL1TV(l, k, gamma, shape=(pz, py, px),
####                                   compress=False)
####    m.set_tolerance(eps)
####    m.set_max_iter(cont_maxit)
####    cr = models.ContinuationRun(m, mus=[0.5 ** i for i in range(1, maxit + 1)])
####    cr.fit(X, y)
####    computed_beta = cr._beta
####    print "time: ", (time() - start)
####
####    print "f: ", cr.get_algorithm().f[-1]
####    print "its: ", cr.get_algorithm().iterations
####
####    plot.subplot(2, 2, 3)
####    plot.plot(betastar[:, 0], '-', computed_beta[:, 0], '*')
####    plot.subplot(2, 2, 4)
####    plot.plot(cr.get_algorithm().f)
####    plot.title("Continuation Run")
####
####    plot.show()
###
###
###
####     # Relevant tests for Lasso for the paper!
####    lambdas = [3.00, 3.25, 3.50, 3.75, 4.00]
####    for i in xrange(len(lambdas)):
####        lambd = float(lambdas[i])
#####        lambd = float(0.25)
####        #    gamma = 131.2457
####        #    lambd = float(0.75)
####        #    gamma = 131.2457
####        density = float(0.5)  # Fraction of non-zero values. Must be \in [0, 1]
####        snr = float(1.0)  # ~SNR
####        n = 25
####        p = 50
####        ps = int(round(p * density))  # <= p
####        #    P = (np.random.randn(n, p) - 0.5) * 2.0
####        #    P = np.random.randn(n, p)
####        Sigma = 0.8 * np.ones((p, p)) + 0.2 * np.eye(p)
####        Mu = np.zeros(p)
####        P = np.random.multivariate_normal(Mu, Sigma, n)
####        e = np.random.randn(n, 1)
####        #    e = np.random.rand(n, 1)
####        e = e / np.sqrt(np.sum(e ** 2.0))
####
####        X, y, beta = lasso.load(lambd, density, snr, P, e)
####
####        tolerance = 0.00005
####        maxit = 20000
####
####        v = []
####        x = []
####        scale = 100.0
####        a = max(0, int(round(lambd * scale - scale / 2.0)))
####        b = int(round(lambd * scale + scale / 2.0))
####        for l in xrange(a, b):
####            l = l / float(scale)
####            lr = models.Lasso(l)
####            lr.set_tolerance(tolerance)
####            lr.set_max_iter(maxit)
####            lr.fit(X, y)
####            v.append(np.sum((beta - lr._beta) ** 2.0))
####            x.append(l)
####            print "l = %.2f => %f" % (l, v[-1])
####
####        plot.subplot(len(lambdas), 1, i + 1)
####        plot.plot(x, v, '-g')
####        plot.title("l: %.2f, min: %.2f" % (lambd, x[np.argmin(v)]))
####        plot.axis([a / scale, b / scale, min(v), max(v)])
####    plot.show()
###
####    # Relevant tests for EN + TV for the paper!
####    gammas = [1.50, 2.00, 2.50]
####    for i in xrange(len(gammas)):
####        lambd = float(1.00)
####        gamma = float(gammas[i])  # float(1.142)
####        density = float(0.5)  # Fraction of non-zero values. Must be \in [0, 1]
####        snr = float(10.0)  # ~SNR
####        n = 25
####        p = 50
####        ps = int(round(p * density))  # <= p
####        #    P = (np.random.randn(n, p) - 0.5) * 2.0
####        #    P = np.random.randn(n, p)
####        Sigma = 0.8 * np.ones((p, p)) + 0.2 * np.eye(p)
####        Mu = np.zeros(p)
####        P = np.random.multivariate_normal(Mu, Sigma, n)
####        e = np.random.randn(n, 1)
####        #    e = np.random.rand(n, 1)
####        e = e / np.sqrt(np.sum(e ** 2.0))
####
####        np.random.seed(42)
####        X, y, beta = l1_l2_tv.load(lambd, 1.0 - lambd, gamma, density, snr, P, e)
####
####        tolerance = 0.00001
####        maxit = 25000
####        mu = 0.00001
####
####        v = []
####        x = []
####        scale = 50.0
####        value = gamma
####        a = max(0, int(round(value * scale - scale / 2.0)))
####        b = int(round(value * scale + scale / 2.0))
####        start_vector = start_vectors.RandomStartVector()
####        for val in xrange(a, b):
####            l = lambd
####            g = val / float(scale)
####            axis = g
####            lr = models.ElasticNetTV(l, g, shape=[1, 1, p], mu=mu)
####            lr.set_start_vector(start_vector)
####            lr.set_tolerance(tolerance)
####            lr.set_max_iter(maxit)
####            lr.fit(X, y)
####            start_vector = start_vectors.IdentityStartVector(lr._beta)
####            v.append(np.sum((beta - lr._beta) ** 2.0))
####            x.append(axis)
####            print "true = %.2f => %f" % (axis, v[-1])
####
####        plot.subplot(len(gammas), 1, i + 1)
####        plot.plot(x, v, '-g')
####        plot.title("true: %.2f, min: %.2f" % (value, x[np.argmin(v)]))
####        plot.axis([a / scale, b / scale, min(v), max(v)])
####    plot.show()
###
###
####     # Test to find SNR for Lasso
####    l = 3.14159
####    density = float(0.5)  # Fraction of non-zero values. Must be \in [0, 1]
####    snr = float(100)  # 100 = |X.b| / |e|
####    n = 200
####    p = 1000
####    ps = int(round(p * density))  # <= p
####    #    M = (np.random.randn(n, p) - 0.5) * 2.0
####    #    M = np.random.randn(n, p)
####    Sigma = 0.8 * np.ones((p, p)) + 0.2 * np.eye(p)
####    Mu = np.zeros(p)
####    M = np.random.multivariate_normal(Mu, Sigma, n)
####    e = np.random.randn(n, 1)
####    #    e = np.random.rand(n, 1)
####    norm_e = np.sqrt(np.sum(e ** 2.0))
####    e = e / norm_e
####
#####    seed = np.random.randint(2000000000)
#####
#####    low = 0.0
#####    high = 1.0
#####    for i in xrange(30):
#####        print "low:", low, "high:", high
#####        np.random.seed(seed)
#####        X, y, beta = lasso.load(l, density, high, M, e)
#####        val = np.sqrt(np.sum(np.dot(X, beta) ** 2.0) / np.sum(e ** 2.0))
#####        if val > snr:
#####            break
#####        else:
#####            low = high
#####            high = high * 2.0
#####
#####    def f(x):
#####        np.random.seed(seed)
#####        X, y, beta = lasso.load(l, density, x, M, e)
#####        return np.sqrt(np.sum(np.dot(X, beta) ** 2.0) / np.sum(e ** 2.0)) - snr
#####
#####    bm = algorithms.BisectionMethod(max_iter=20)
#####    bm.run(utils.AnonymousClass(f=f), low, high)
#####
#####    np.random.seed(seed)
####    X, y, beta = lasso.load(l, density, snr, M, e)
####    print "snr = %.5f = %.5f = |X.b| / |e| = %.5f / %.5f" \
####            % (snr, np.linalg.norm(np.dot(X, beta) / np.linalg.norm(e)),
####               np.linalg.norm(np.dot(X, beta)), np.linalg.norm(e))
####
#####    tolerance = 0.00005
#####    maxit = 20000
#####
#####    lr = models.Lasso(l)
#####    lr.set_tolerance(tolerance)
#####    lr.set_max_iter(maxit)
#####    lr.fit(X, y)
#####
#####    plot.subplot(len(lambdas), 1, i + 1)
#####    plot.plot(x, v, '-g')
#####    plot.title("l: %.2f, min: %.2f" % (lambd, x[np.argmin(v)]))
#####    plot.axis([a / scale, b / scale, min(v), max(v)])
#####    plot.show()
###
###
###
####     # Test to find SNR for EN + TV
####    tolerance = 0.0001
####    maxit = 50000
####    mu = 0.000001
####    alg = algorithms.FISTARegression()
####
####    vals = [0.50, 1.5, 2.50, 3.5, 4.50, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5]
#####    vals = [6.00]
####    for i in xrange(len(vals)):
####        l = 2.71828
####        k = 0.61803
#####        gamma = 3.14159
####        gamma = vals[i]
####        value = gamma  # Ändra här också!
####
####        density = float(0.5)  # Fraction of non-zero values. Must be \in [0, 1]
####        snr = float(100)  # 100 = |X.b| / |e|
####        n = 5
####        p = 10
####        ps = int(round(p * density))  # <= p
####        #    M = (np.random.randn(n, p) - 0.5) * 2.0
####        #    M = np.random.randn(n, p)
####        Sigma = 0.9 * np.ones((p, p)) + 0.1 * np.eye(p)
####        Mu = np.zeros(p)
####        M = np.random.multivariate_normal(Mu, Sigma, n)
####        e = np.random.randn(n, 1)
####        #    e = np.random.rand(n, 1)
####        norm_e = np.sqrt(np.sum(e ** 2.0))
####        e = e / norm_e
####
####        X, y, beta = l1_l2_tv.load(l, k, gamma, density, snr, M, e)
####
####        v = []
####        x = []
####        scale = 101.0
####        start_vector = start_vectors.RandomStartVector()
####        a = max(0, value - 0.5)
####        b = value + 0.5
####        for val in np.linspace(a, b, scale):
####            l_ = l
####            k_ = k
####            g_ = val
####
####            model = models.RidgeRegressionL1TV(l_, k_, g_, shape=[1, 1, p],
####                                               mu=mu, compress=False,
####                                               algorithm=alg)
####            model.set_start_vector(start_vector)
####            model.set_tolerance(tolerance)
####            if val == a:
####                model.set_max_iter(maxit * 10)
####            else:
####                model.set_max_iter(maxit)
####            model.fit(X, y)
####            start_vector = start_vectors.IdentityStartVector(model._beta)
####            v.append(np.sum((beta - model._beta) ** 2.0))
####            x.append(val)
####            print "true = %.2f => %.7f" % (val, v[-1])
####
####        plot.subplot(len(vals), 1, i + 1)
####        plot.plot(x, v, '-g')
####        plot.title("true: %.2f, min: %.2f" % (value, x[np.argmin(v)]))
####        plot.axis([a, b, min(v), max(v)])
####    plot.show()
###
###
###
###    # Testing the new continuation
###    np.random.seed(42)
###
###    tolerance = 0.00001
###    maxit = 50000
###    mu = 0.0001
###    alg = algorithms.FISTARegression()
###
###    l = 0.61803
###    k = 0.0  # 2.71828
###    gamma = 1.314159
###    opt = gamma
###
###    px = 6
###    py = 6
###    p = px * py
###    n = 25
###
###    alpha = 1.0
###    Sigma = alpha * np.eye(p) + (1.0 - alpha) * np.ones((p, p))
###    Mu = np.zeros(p)
###    M = np.random.multivariate_normal(Mu, Sigma, n)
###    e = np.random.randn(n, 1)
###
####    X, y, beta = lasso.load(l, density=0.7, snr=100.0, M=M, e=e)
####    X, y, beta = ridge.load(k, density=0.7, snr=100.0, M=M, e=e)
####    X, y, beta = l1_tv.load(l, gamma, density=0.7, snr=100.0, M=M, e=e)
####    X, y, beta = ridge_2D.load(k, density=0.7, snr=100.0, M=M, e=e,
####                               shape=(py, px))
####    X, y, beta = lasso_2D.load(l, density=0.7, snr=100.0, M=M, e=e,
####                               shape=(py, px))
####    X, y, beta = l1_l2.load(l, k, density=0.7, snr=100.0, M=M, e=e)
####    X, y, beta = l1_l2_2D.load(l, k, density=0.7, snr=100.0, M=M, e=e,
####                               shape=(py, px))
###    X, y, beta = l1_l2_tv.load(l, k, gamma, density=0.50, snr=100.0,
###                               M=M, e=e)
###
###    num_lin = 51
###    vals = np.maximum(0.0, np.linspace(opt - 0.25, opt + 0.25, num_lin))
###    v = []
###    x = []
###    f = []
###    start_vector = start_vectors.RandomStartVector()
###    best_vec = 0
###    best_val = float("inf")
###    opt_vec = 0
###    for i in range(len(vals)):
###        val = vals[i]
####        model = models.Lasso(val, algorithm=alg)
####        model = models.RidgeRegression(val, algorithm=alg)
####        model = models.LinearRegressionTV(val, shape=(1, 1, p), mu=mu,
####                                          algorithm=alg)
###        model = models.LinearRegressionL1TV(l, val, shape=(1, 1, p), mu=mu,
###                                            algorithm=alg)
####        model = models.LinearRegressionL1L2(l, val, algorithm=alg)
####        model = models.RidgeRegressionL1TV(l, k, val,
####                                           shape=[1, py, px],
####                                           mu=mu, compress=False,
####                                           algorithm=alg)
###        model.set_start_vector(start_vector)
###        model.set_tolerance(tolerance)
###        if i == 0:
###            model.set_max_iter(maxit * 2)
###        else:
###            model.set_max_iter(maxit)
###        model.fit(X, y)
####        c = models.ContinuationRun(model, mus=[0.1, 0.01, 0.001, 0.0001, 0.00001])
####        c.fit(X, y)
###        beta_ = model._beta
###        f_ = model.algorithm.f
###        start_vector = start_vectors.IdentityStartVector(beta_)
###
###        curr_val = np.sum((beta - beta_) ** 2.0)
###        v.append(curr_val)
###        x.append(val)
###        f.append(f_)
###        print "true = %.2f => %.7f" % (val, v[-1])
###
###        if curr_val < best_val:
###            best_val = curr_val
###            best_vec = copy.deepcopy(beta_)
###
###        if abs(val - opt) < (max(vals) - min(vals)) / num_lin:
###            print "Sparar beta vid ", val
###            opt_vec = copy.deepcopy(beta_)
###
###    plot.subplot(2, 1, 1)
###    plot.plot(x, v, '-b')
###    plot.title("true: %.2f, min: %.2f" % (opt, x[np.argmin(v)]))
###    plot.subplot(2, 1, 2)
###    plot.plot(beta, '-g', opt_vec, '-r', best_vec, '-b')
###    plot.show()