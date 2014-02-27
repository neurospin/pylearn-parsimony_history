# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 09:21:23 2014

@author:  Tommy Löfstedt
@email:   lofstedt.tommy@gmail.com
@license: BSD 3-clause.
"""
import unittest
from nose.tools import assert_less

import numpy as np

from tests import TestCase


class TestLinearRegression(TestCase):

    def test_linear_regression_overdetermined(self):

        from parsimony.functions.losses import LinearRegression
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        np.random.seed(42)

        n, p = 100, 50

        alpha = 1.0
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        X = np.random.multivariate_normal(mean, Sigma, n)

        start_vector = start_vectors.RandomStartVector(normalise=True)
        beta_star = start_vector.get_vector((p, 1))

        e = 0.01 * np.random.randn(n, 1)

        y = np.dot(X, beta_star) + e

        eps = 1e-8
        max_iter = 2000
        gd = explicit.GradientDescent(eps=eps, max_iter=max_iter)
        linear_regression = LinearRegression(X, y, mean=False)
        beta_start = start_vector.get_vector((p, 1))

        beta_parsimony = gd.run(linear_regression, beta_start)

        mse = (np.linalg.norm(beta_parsimony - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-5, "The found regression vector is not correct.")

        f_parsimony = linear_regression.f(beta_parsimony)
        f_star = linear_regression.f(beta_star)
        err = abs(f_parsimony - f_star)
#        print "err:", err
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_underdetermined(self):

        from parsimony.functions.losses import LinearRegression
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        np.random.seed(42)

        n, p = 50, 100

        alpha = 1.0
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        X = np.random.multivariate_normal(mean, Sigma, n)

        start_vector = start_vectors.RandomStartVector(normalise=True)
        beta_star = start_vector.get_vector((p, 1))

        e = 0.01 * np.random.randn(n, 1)

        y = np.dot(X, beta_star) + e

        eps = 1e-8
        max_iter = 1000
        gd = explicit.GradientDescent(eps=eps, max_iter=max_iter)
        linear_regression = LinearRegression(X, y, mean=False)
        beta_start = start_vector.get_vector((p, 1))

        beta_parsimony = gd.run(linear_regression, beta_start)

        mse = (np.linalg.norm(beta_parsimony - beta_star) ** 2.0) / p
#        print "mse:", mse
#        assert mse < 1e-2
        assert_less(mse, 1e-2, "The found regression vector is not correct.")

        f_parsimony = linear_regression.f(beta_parsimony)
        f_star = linear_regression.f(beta_star)
        err = abs(f_parsimony - f_star)
#        print "err:", err
#        assert abs(f_parsimony - f_star) < 1e-2
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_determined(self):

        from parsimony.functions.losses import LinearRegression
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        np.random.seed(42)

        n, p = 50, 50

        alpha = 1.0
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        X = np.random.multivariate_normal(mean, Sigma, n)

        start_vector = start_vectors.RandomStartVector(normalise=True)
        beta_star = start_vector.get_vector((p, 1))

        e = 0.01 * np.random.randn(n, 1)

        y = np.dot(X, beta_star) + e

        eps = 1e-8
        max_iter = 1000
        gd = explicit.GradientDescent(eps=eps, max_iter=max_iter)
        linear_regression = LinearRegression(X, y, mean=False)
        beta_start = start_vector.get_vector((p, 1))

        beta_parsimony = gd.run(linear_regression, beta_start)

        mse = (np.linalg.norm(beta_parsimony - beta_star) ** 2.0) / p
        print "mse:", mse
#        assert mse < 1e-4
        assert_less(mse, 1e-4, "The found regression vector is not correct.")

        f_parsimony = linear_regression.f(beta_parsimony)
        f_star = linear_regression.f(beta_star)
        err = abs(f_parsimony - f_star)
        print "err:", err
#        assert err < 1e-2
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l1(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_gl as l1_l2_gl
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        n, p = 50, 100

        alpha = 1.0
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta[beta < 0.1] = 0.0

        l = 0.618
        k = 0.0
        g = 0.0

        A = np.eye(p)
        A = [A, A, A]
        snr = 100.0
        X, y, beta_star = l1_l2_gl.load(l, k, g, beta, M, e, A, snr=snr)

        eps = 1e-8
        max_iter = 12000
        fista = explicit.FISTA(eps=eps, max_iter=max_iter)
        linear_regression = LinearRegression(X, y, mean=False)
        l1 = L1(l=l)
        function = CombinedFunction()
        function.add_function(linear_regression)
        function.add_prox(l1)

        beta_start = start_vector.get_vector((p, 1))

        beta_parsimony = fista.run(function, beta_start)

        mse = (np.linalg.norm(beta_parsimony - beta_star) ** 2.0) / p
#        print "mse:", mse
#        assert mse < 1e-4
        assert_less(mse, 1e-2, "The found regression vector is not correct.")

        f_parsimony = function.f(beta_parsimony)
        f_star = function.f(beta_star)
        err = abs(f_parsimony - f_star)
#        print "err:", err
#        assert abs(f_parsimony - f_star) < 1e-2
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l2(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L2
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_gl as l1_l2_gl
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        n, p = 30, 50

        alpha = 1.0
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta[beta < 0.1] = 0.0

        l = 0.0
        k = 0.618
        g = 0.0

        A = np.eye(p)
        A = [A, A, A]
        snr = 100.0
        X, y, beta_star = l1_l2_gl.load(l, k, g, beta, M, e, A, snr=snr)

        eps = 1e-8
        max_iter = 1000

        fista = explicit.FISTA(eps=eps, max_iter=max_iter)
        beta_start = start_vector.get_vector((p, 1))

        function = CombinedFunction()
        function.add_function(LinearRegression(X, y, mean=False))
        function.add_penalty(L2(k))
        beta_penalty = fista.run(function, beta_start)

        function = CombinedFunction()
        function.add_function(LinearRegression(X, y, mean=False))
        function.add_prox(L2(k))
        beta_prox = fista.run(function, beta_start)

        function = CombinedFunction()
        function.add_function(RidgeRegression(X, y, k))
        beta_rr = fista.run(function, beta_start)

        mse = (np.linalg.norm(beta_penalty - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_prox - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_rr - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_parsimony = function.f(beta_penalty)
        err = abs(f_parsimony - f_star)
#        print "err:", err
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

        f_prox = function.f(beta_prox)
        err = abs(f_prox - f_star)
#        print "err:", err
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

        f_rr = function.f(beta_rr)
        err = abs(f_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_tv(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        import parsimony.functions.nesterov.tv as tv
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_tv as l1_l2_tv
        import parsimony.datasets.simulated.l1_l2_tvmu as l1_l2_tvmu
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        px = 4
        py = 4
        pz = 4
        shape = (pz, py, px)
        n, p = 50, np.prod(shape)

        alpha = 0.9
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta = np.sort(beta, axis=0)
#        beta[beta < 0.1] = 0.0

        l = 0.0
        k = 0.0
        g = 1.618

        A, _ = tv.A_from_shape(shape)
        snr = 20.0
        eps = 1e-8
        max_iter = 2000

        X, y, beta_star = l1_l2_tv.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                        A=A, snr=snr)

        mus = [5e-2, 5e-4, 5e-6, 5e-8]
        fista = explicit.FISTA(eps=eps, max_iter=max_iter / len(mus))
        beta_start = start_vector.get_vector((p, 1))

        beta_nonsmooth = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            beta_nonsmooth = fista.run(function, beta_nonsmooth)

        mu_min = mus[-1]
        X, y, beta_star = l1_l2_tvmu.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                          A=A, mu=mu_min, snr=snr)

        beta_smooth = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            beta_smooth = fista.run(function, beta_smooth)

        mse = (np.linalg.norm(beta_nonsmooth - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_parsimony = function.f(beta_nonsmooth)
        err = abs(f_parsimony - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_rr = function.f(beta_smooth)
        err = abs(f_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_gl(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        import parsimony.functions.nesterov.gl as gl
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_gl as l1_l2_gl
        import parsimony.datasets.simulated.l1_l2_glmu as l1_l2_glmu
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        n, p = 60, 90
        groups = [range(0, 2 * p / 3), range(p / 3, p)]
        weights = [1.5, 0.5]

        A = gl.A_from_groups(p, groups=groups, weights=weights)

        alpha = 0.9
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta = np.sort(beta, axis=0)
#        beta[beta < 0.1] = 0.0

        l = 0.0
        k = 0.0
        g = 1.618

        snr = 20.0
        eps = 1e-8
        max_iter = 2600

        X, y, beta_star = l1_l2_gl.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                        A=A, snr=snr)

        mus = [5e-2, 5e-4, 5e-6, 5e-8]
        fista = explicit.FISTA(eps=eps, max_iter=max_iter / len(mus))
        beta_start = start_vector.get_vector((p, 1))

        beta_nonsmooth = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            beta_nonsmooth = fista.run(function, beta_nonsmooth)

        mu_min = mus[-1]
        X, y, beta_star = l1_l2_glmu.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                          A=A, mu=mu_min, snr=snr)

        beta_smooth = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            beta_smooth = fista.run(function, beta_smooth)

        mse = (np.linalg.norm(beta_nonsmooth - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_parsimony = function.f(beta_nonsmooth)
        err = abs(f_parsimony - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_rr = function.f(beta_smooth)
        err = abs(f_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l1_l2(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_gl as l1_l2_gl
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        n, p = 30, 50

        alpha = 1.0
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta[beta < 0.1] = 0.0

        l = 0.618
        k = 1.0 - l
        g = 0.0

        A = np.eye(p)
        A = [A, A, A]
        snr = 100.0
        X, y, beta_star = l1_l2_gl.load(l, k, g, beta, M, e, A, snr=snr)

        eps = 1e-8
        max_iter = 1000

        fista = explicit.FISTA(eps=eps, max_iter=max_iter)
        beta_start = start_vector.get_vector((p, 1))

        function = CombinedFunction()
        function.add_function(LinearRegression(X, y, mean=False))
        function.add_penalty(L2(k))
        function.add_prox(L1(l))
        beta_penalty = fista.run(function, beta_start)

        function = CombinedFunction()
        function.add_function(RidgeRegression(X, y, k))
        function.add_prox(L1(l))
        beta_rr = fista.run(function, beta_start)

        mse = (np.linalg.norm(beta_penalty - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_rr - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_parsimony = function.f(beta_penalty)
        err = abs(f_parsimony - f_star)
#        print "err:", err
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

        f_rr = function.f(beta_rr)
        err = abs(f_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-2, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l1_tv(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        import parsimony.functions.nesterov.tv as tv
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_tv as l1_l2_tv
        import parsimony.datasets.simulated.l1_l2_tvmu as l1_l2_tvmu
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        px = 4
        py = 4
        pz = 4
        shape = (pz, py, px)
        n, p = 50, np.prod(shape)

        alpha = 0.9
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta = np.sort(beta, axis=0)
#        beta[beta < 0.1] = 0.0

        l = 0.618
        k = 0.0
        g = 1.618

        A, _ = tv.A_from_shape(shape)
        snr = 20.0
        eps = 1e-8
        max_iter = 1200

        X, y, beta_star = l1_l2_tv.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                        A=A, snr=snr)

        mus = [5e-2, 5e-4, 5e-6, 5e-8]
        fista = explicit.FISTA(eps=eps, max_iter=max_iter / len(mus))
        beta_start = start_vector.get_vector((p, 1))

        beta_nonsmooth = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_prox(L1(l))
            beta_nonsmooth = fista.run(function, beta_nonsmooth)

        mu_min = mus[-1]
        X, y, beta_star = l1_l2_tvmu.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                          A=A, mu=mu_min, snr=snr)

        beta_smooth = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_prox(L1(l))
            beta_smooth = fista.run(function, beta_smooth)

        mse = (np.linalg.norm(beta_nonsmooth - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_parsimony = function.f(beta_nonsmooth)
        err = abs(f_parsimony - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_rr = function.f(beta_smooth)
        err = abs(f_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l1_gl(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        import parsimony.functions.nesterov.gl as gl
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_gl as l1_l2_gl
        import parsimony.datasets.simulated.l1_l2_glmu as l1_l2_glmu
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        n, p = 60, 90
        groups = [range(0, 2 * p / 3), range(p / 3, p)]
        weights = [1.5, 0.5]

        A = gl.A_from_groups(p, groups=groups, weights=weights)

        alpha = 0.9
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta = np.sort(beta, axis=0)
#        beta[beta < 0.1] = 0.0

        l = 0.618
        k = 0.0
        g = 1.618

        snr = 20.0
        eps = 1e-8
        max_iter = 3500

        X, y, beta_star = l1_l2_gl.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                        A=A, snr=snr)

        mus = [5e-2, 5e-4, 5e-6, 5e-8]
        fista = explicit.FISTA(eps=eps, max_iter=max_iter / len(mus))
        beta_start = start_vector.get_vector((p, 1))

        beta_nonsmooth = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_prox(L1(l))
            beta_nonsmooth = fista.run(function, beta_nonsmooth)

        mu_min = mus[-1]
        X, y, beta_star = l1_l2_glmu.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                          A=A, mu=mu_min, snr=snr)

        beta_smooth = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_prox(L1(l))
            beta_smooth = fista.run(function, beta_smooth)

        mse = (np.linalg.norm(beta_nonsmooth - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_parsimony = function.f(beta_nonsmooth)
        err = abs(f_parsimony - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_rr = function.f(beta_smooth)
        err = abs(f_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l2_tv(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        import parsimony.functions.nesterov.tv as tv
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_tv as l1_l2_tv
        import parsimony.datasets.simulated.l1_l2_tvmu as l1_l2_tvmu
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        px = 4
        py = 4
        pz = 4
        shape = (pz, py, px)
        n, p = 50, np.prod(shape)

        alpha = 0.9
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta = np.sort(beta, axis=0)
#        beta[beta < 0.1] = 0.0

        l = 0.0
        k = 0.618
        g = 1.618

        A, _ = tv.A_from_shape(shape)
        snr = 20.0
        eps = 1e-8
        max_iter = 800

        X, y, beta_star = l1_l2_tv.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                        A=A, snr=snr)

        mus = [5e-2, 5e-4, 5e-6, 5e-8]
        fista = explicit.FISTA(eps=eps, max_iter=max_iter / len(mus))
        beta_start = start_vector.get_vector((p, 1))

        beta_nonsmooth_penalty = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_penalty(L2(k))
            beta_nonsmooth_penalty = \
                    fista.run(function, beta_nonsmooth_penalty)

        beta_nonsmooth_prox = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_prox(L2(k))
            beta_nonsmooth_prox = fista.run(function, beta_nonsmooth_prox)

        beta_nonsmooth_rr = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(RidgeRegression(X, y, k))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            beta_nonsmooth_rr = fista.run(function, beta_nonsmooth_rr)

        mu_min = mus[-1]
        X, y, beta_star = l1_l2_tvmu.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                          A=A, mu=mu_min, snr=snr)

        beta_smooth_penalty = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_penalty(L2(k))
            beta_smooth_penalty = \
                    fista.run(function, beta_smooth_penalty)

        beta_smooth_prox = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_prox(L2(k))
            beta_smooth_prox = fista.run(function, beta_smooth_prox)

        beta_smooth_rr = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(RidgeRegression(X, y, k))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            beta_smooth_rr = fista.run(function, beta_smooth_rr)

        mse = (np.linalg.norm(beta_nonsmooth_penalty - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-5, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_nonsmooth_prox - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-5, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_nonsmooth_rr - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-5, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_nonsmooth_penalty = function.f(beta_nonsmooth_penalty)
        err = abs(f_nonsmooth_penalty - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_nonsmooth_prox = function.f(beta_nonsmooth_prox)
        err = abs(f_nonsmooth_prox - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_nonsmooth_rr = function.f(beta_nonsmooth_rr)
        err = abs(f_nonsmooth_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l2_gl(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        import parsimony.functions.nesterov.gl as gl
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_gl as l1_l2_gl
        import parsimony.datasets.simulated.l1_l2_glmu as l1_l2_glmu
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        n, p = 60, 90
        groups = [range(0, 2 * p / 3), range(p / 3, p)]
        weights = [1.5, 0.5]

        A = gl.A_from_groups(p, groups=groups, weights=weights)

        alpha = 0.9
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta = np.sort(beta, axis=0)
#        beta[beta < 0.1] = 0.0

        l = 0.0
        k = 0.618
        g = 1.618

        snr = 20.0
        eps = 1e-8
        max_iter = 900

        X, y, beta_star = l1_l2_gl.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                        A=A, snr=snr)

        mus = [5e-2, 5e-4, 5e-6, 5e-8]
        fista = explicit.FISTA(eps=eps, max_iter=max_iter / len(mus))
        beta_start = start_vector.get_vector((p, 1))

        beta_nonsmooth_penalty = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_penalty(L2(k))
            beta_nonsmooth_penalty = fista.run(function,
                                               beta_nonsmooth_penalty)

        beta_nonsmooth_prox = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_prox(L2(k))
            beta_nonsmooth_prox = fista.run(function, beta_nonsmooth_prox)

        beta_nonsmooth_rr = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(RidgeRegression(X, y, k))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            beta_nonsmooth_rr = fista.run(function, beta_nonsmooth_rr)

        mu_min = mus[-1]
        X, y, beta_star = l1_l2_glmu.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                          A=A, mu=mu_min, snr=snr)

        beta_smooth_penalty = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_penalty(L2(k))
            beta_smooth_penalty = fista.run(function, beta_smooth_penalty)

        beta_smooth_prox = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_prox(L2(k))
            beta_smooth_prox = fista.run(function, beta_smooth_prox)

        beta_smooth_rr = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(RidgeRegression(X, y, k))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            beta_smooth_rr = fista.run(function, beta_smooth_rr)

        mse = (np.linalg.norm(beta_nonsmooth_penalty - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_nonsmooth_prox - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_nonsmooth_rr - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth_penalty - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth_prox - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth_rr - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-3, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_nonsmooth_penalty = function.f(beta_nonsmooth_penalty)
        err = abs(f_nonsmooth_penalty - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_nonsmooth_prox = function.f(beta_nonsmooth_prox)
        err = abs(f_nonsmooth_prox - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_nonsmooth_rr = function.f(beta_nonsmooth_rr)
        err = abs(f_nonsmooth_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_smooth_penalty = function.f(beta_smooth_penalty)
        err = abs(f_smooth_penalty - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_smooth_prox = function.f(beta_smooth_prox)
        err = abs(f_smooth_prox - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_smooth_rr = function.f(beta_smooth_rr)
        err = abs(f_smooth_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l1_l2_tv(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        import parsimony.functions.nesterov.tv as tv
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_tv as l1_l2_tv
        import parsimony.datasets.simulated.l1_l2_tvmu as l1_l2_tvmu
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        px = 4
        py = 4
        pz = 4
        shape = (pz, py, px)
        n, p = 50, np.prod(shape)

        alpha = 0.9
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta = np.sort(beta, axis=0)
#        beta[beta < 0.1] = 0.0

        l = 0.618
        k = 1.0 - l
        g = 1.618

        A, _ = tv.A_from_shape(shape)
        snr = 20.0
        eps = 1e-8
        max_iter = 600

        X, y, beta_star = l1_l2_tv.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                        A=A, snr=snr)

        mus = [5e-2, 5e-4, 5e-6, 5e-8]
        fista = explicit.FISTA(eps=eps, max_iter=max_iter / len(mus))
        beta_start = start_vector.get_vector((p, 1))

        beta_nonsmooth_penalty = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_penalty(L2(k))
            function.add_prox(L1(l))
            beta_nonsmooth_penalty = \
                    fista.run(function, beta_nonsmooth_penalty)

        beta_nonsmooth_rr = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(RidgeRegression(X, y, k))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_prox(L1(l))
            beta_nonsmooth_rr = fista.run(function, beta_nonsmooth_rr)

        mu_min = mus[-1]
        X, y, beta_star = l1_l2_tvmu.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                          A=A, mu=mu_min, snr=snr)

        beta_smooth_penalty = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_penalty(L2(k))
            function.add_prox(L1(l))
            beta_smooth_penalty = \
                    fista.run(function, beta_smooth_penalty)

        beta_smooth_rr = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(RidgeRegression(X, y, k))
            function.add_penalty(tv.TotalVariation(l=g, A=A, mu=mu,
                                                   penalty_start=0))
            function.add_prox(L1(l))
            beta_smooth_rr = fista.run(function, beta_smooth_rr)

        mse = (np.linalg.norm(beta_nonsmooth_penalty - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-5, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_nonsmooth_rr - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-5, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_nonsmooth_penalty = function.f(beta_nonsmooth_penalty)
        err = abs(f_nonsmooth_penalty - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_nonsmooth_rr = function.f(beta_nonsmooth_rr)
        err = abs(f_nonsmooth_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

    def test_linear_regression_l1_l2_gl(self):

        from parsimony.functions.losses import LinearRegression
        from parsimony.functions.losses import RidgeRegression
        from parsimony.functions.penalties import L1
        from parsimony.functions.penalties import L2
        import parsimony.functions.nesterov.gl as gl
        from parsimony.functions import CombinedFunction
        import parsimony.datasets.simulated.l1_l2_gl as l1_l2_gl
        import parsimony.datasets.simulated.l1_l2_glmu as l1_l2_glmu
        import parsimony.algorithms.explicit as explicit
        import parsimony.start_vectors as start_vectors

        start_vector = start_vectors.RandomStartVector(normalise=True)

        np.random.seed(42)

        n, p = 60, 90
        groups = [range(0, 2 * p / 3), range(p / 3, p)]
        weights = [1.5, 0.5]

        A = gl.A_from_groups(p, groups=groups, weights=weights)

        alpha = 0.9
        Sigma = alpha * np.eye(p, p) \
              + (1.0 - alpha) * np.random.randn(p, p)
        mean = np.zeros(p)
        M = np.random.multivariate_normal(mean, Sigma, n)
        e = np.random.randn(n, 1)

        beta = start_vector.get_vector((p, 1))
        beta = np.sort(beta, axis=0)
#        beta[beta < 0.1] = 0.0

        l = 0.618
        k = 1.0 - l
        g = 1.618

        snr = 20.0
        eps = 1e-8
        max_iter = 1400

        X, y, beta_star = l1_l2_gl.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                        A=A, snr=snr)

        mus = [5e-2, 5e-4, 5e-6, 5e-8]
        fista = explicit.FISTA(eps=eps, max_iter=max_iter / len(mus))
        beta_start = start_vector.get_vector((p, 1))

        beta_nonsmooth_penalty = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_penalty(L2(k))
            function.add_prox(L1(l))
            beta_nonsmooth_penalty = fista.run(function,
                                               beta_nonsmooth_penalty)

        beta_nonsmooth_rr = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(RidgeRegression(X, y, k))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_prox(L1(l))
            beta_nonsmooth_rr = fista.run(function, beta_nonsmooth_rr)

        mu_min = mus[-1]
        X, y, beta_star = l1_l2_glmu.load(l=l, k=k, g=g, beta=beta, M=M, e=e,
                                          A=A, mu=mu_min, snr=snr)

        beta_smooth_penalty = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(LinearRegression(X, y, mean=False))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_penalty(L2(k))
            function.add_prox(L1(l))
            beta_smooth_penalty = fista.run(function, beta_smooth_penalty)

        beta_smooth_rr = beta_start
        for mu in mus:
            function = CombinedFunction()
            function.add_function(RidgeRegression(X, y, k))
            function.add_penalty(gl.GroupLassoOverlap(l=g, A=A, mu=mu,
                                                      penalty_start=0))
            function.add_prox(L1(l))
            beta_smooth_rr = fista.run(function, beta_smooth_rr)

        mse = (np.linalg.norm(beta_nonsmooth_penalty - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-4, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_nonsmooth_rr - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-4, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth_penalty - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-4, "The found regression vector is not correct.")

        mse = (np.linalg.norm(beta_smooth_rr - beta_star) ** 2.0) / p
#        print "mse:", mse
        assert_less(mse, 1e-4, "The found regression vector is not correct.")

        f_star = function.f(beta_star)

        f_nonsmooth_penalty = function.f(beta_nonsmooth_penalty)
        err = abs(f_nonsmooth_penalty - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_nonsmooth_rr = function.f(beta_nonsmooth_rr)
        err = abs(f_nonsmooth_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_smooth_penalty = function.f(beta_smooth_penalty)
        err = abs(f_smooth_penalty - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

        f_smooth_rr = function.f(beta_smooth_rr)
        err = abs(f_smooth_rr - f_star)
#        print "err:", err
        assert_less(err, 1e-3, "The found regression vector does not give " \
                               "the correct function value.")

if __name__ == "__main__":
    unittest.main()