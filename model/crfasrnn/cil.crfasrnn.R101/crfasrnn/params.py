"""
MIT License

Copyright (c) 2019 Sadeep Jayasumana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class DenseCRFParams(object):
    """
    Parameters for the DenseCRF model
    """

    def __init__(
        self,
        alpha=40.0, # default=160.0
        beta=1.7500746997459924,	# default=3.0
        gamma=4.461952267619522,	# default=3.0
        spatial_ker_weight=3.7606425465775133,	# trainable in crfasrnn
        bilateral_ker_weight=1.6835678682669473,	# trainable in crfasrnn
    ):
        """
        Default values were taken from https://github.com/sadeepj/crfasrnn_keras. More details about these parameters
        can be found in https://arxiv.org/pdf/1210.5644.pdf

        Args:
            alpha:                  Bandwidth for the spatial component of the bilateral filter
            beta:                   Bandwidth for the color component of the bilateral filter
            gamma:                  Bandwidth for the spatial filter
            spatial_ker_weight:     Spatial kernel weight
            bilateral_ker_weight:   Bilateral kernel weight
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.spatial_ker_weight = spatial_ker_weight
        self.bilateral_ker_weight = bilateral_ker_weight
