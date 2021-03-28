from numpy import random
import matplotlib.pyplot as plot

def rand_is_corrupted(p):
    return random.rand() < p


def make_plot(data, time_gbn, time_sr, xLabel):
    plot.plot(data, time_gbn, 'r', label="Go back N")
    plot.plot(data, time_sr, 'b', label="Selective repeat")
    plot.xlabel(xLabel)
    plot.ylabel('time')
    plot.legend(loc='upper left')
    plot.grid(True)
    plot.show()