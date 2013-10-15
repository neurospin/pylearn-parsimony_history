# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:32:00 2013

@author:  Tommy Löfstedt
@email:   tommy.loefstedt@cea.fr
@license: TBD.
"""

import numpy as np
from grad import grad_L1
from grad import grad_L2
from grad import grad_TV
from utils import bisection_method

__all__ = ['load']


def load(l, k, g, beta, M, e, snr=None, shape=None):
    """Returns data generated such that we know the exact solution.

    The data generated by this function is fit to the Linear regression + L1 +
    L2  + Total variation function, i.e. to:

        f(b) = (1 / 2).|Xb - y|² + l.|b|_1 + (k / 2).|b|² + g.TV(b),

    where |.|_1 is the L1 norm, |.|² is the squared L2 norm and TV is the
    total variation penalty.

    Parameters
    ----------
    l : The L1 regularisation parameter.

    k : The L2 regularisation parameter.

    g : The total variation regularisation parameter.

    beta : The regression vector to generate data from.

    M : The matrix to use when building data. This matrix carries the desired
            correlation structure of the generated data. The generated data
            will be a column-scaled version of this matrix.

    e : The error vector e = Xb - y. This vector carries the desired
            distribution of the residual.

    snr : Signal-to-noise ratio between model and residual.

    shape : The underlying dimension of the regression vector, beta. E.g. the
            beta may represent an underlying 3D image. In that case the shape
            is a three-tuple with dimensions (Z, Y, X). If shape is not
            provided, the shape is set to (p,) where p is the dimension of
            beta.

    Returns
    -------
    X : The generated X matrix.

    y : The generated y vector.

    beta : The regression vector with the correct snr.
    """
    l = float(l)
    k = float(k)
    g = float(g)

    if shape == None:
        shape = (beta.shape[0],)

    if snr != None:
        def f(x):
            X, y = _generate(l, k, g, x * beta, M, e, shape)

            print "norm(beta) = ", np.linalg.norm(beta)
            print "norm(Xbeta) = ", np.linalg.norm(np.dot(X, beta))
            print "norm(e) = ", np.linalg.norm(e)

            print "snr = %.5f = %.5f = |X.b| / |e| = %.5f / %.5f" \
                   % (snr, np.linalg.norm(np.dot(X, x * beta)) \
                                           / np.linalg.norm(e),
                      np.linalg.norm(np.dot(X, x * beta)), np.linalg.norm(e))

            return (np.linalg.norm(np.dot(X, x * beta)) / np.linalg.norm(e)) \
                        - snr

        snr = bisection_method(f, low=0.0, high=snr, maxiter=30)

        beta = beta * snr

    X, y = _generate(l, k, g, beta, M, e, shape)

    return X, y, beta


def _generate(l, k, g, beta, M, e, shape):

    p = np.prod(shape)

    gradL1 = grad_L1(beta)
    gradL2 = grad_L2(beta)
    gradTV = grad_TV(beta, shape)

    alpha = -(l * gradL1 + k * gradL2 + g * gradTV)
    alpha = np.divide(alpha, np.dot(M.T, e))

    X = np.zeros(M.shape)
    for i in xrange(p):
        X[:, i] = M[:, i] * alpha[i, 0]

    y = np.dot(X, beta) - e

    return X, y