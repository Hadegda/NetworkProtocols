from Tester import Tester
from GoBackNProtocol import GoBackNProtocol
from SelectiveRepeatProtocol import SelectiveRepeatProtocol
from utils import make_plot

if __name__ == "__main__":
    goBackNProtocol = GoBackNProtocol()
    goBackNTester = Tester(goBackNProtocol)

    selectiveRepeatProtocol = SelectiveRepeatProtocol()
    selectiveRepeatTester = Tester(selectiveRepeatProtocol)

    wind = 10  # window size
    wind_array = [4 * i for i in range(1, 10)]  # array of window size
    num_packages = 1000  # packages count
    num_packages_array = [300 * i for i in range(1, 10)]  # array of packages counts
    pLoss = 0.4  # probability package loss
    pLoss_array = [0.06 * i for i in range(1, 10)]  # array of probabilities package loss

    time_gbn = []  # performance of Go back N
    time_sr = []  # performance of Selective repeat

    nTests = 1  # number of every test repeats

    for num in num_packages_array:
        print("packSize = %d" % num)
        time_gbn.append(goBackNTester.testRun(wind, num, pLoss, nTests))
        time_sr.append(selectiveRepeatTester.testRun(wind, num, pLoss, nTests))

    make_plot(num_packages_array, time_gbn, time_sr, "Count of packages")

    time_gbn.clear()
    time_sr.clear()

    for w in wind_array:
        print("winSize = %d" % w)
        time_gbn.append(goBackNTester.testRun(w, num_packages, pLoss, nTests))
        time_sr.append(selectiveRepeatTester.testRun(w, num_packages, pLoss, nTests))

    make_plot(wind_array, time_gbn, time_sr, "Size of window")

    time_gbn.clear()
    time_sr.clear()

    for p in pLoss_array:
        print("pLoss = %f" % p)
        time_gbn.append(goBackNTester.testRun(wind, num_packages, p, nTests))
        time_sr.append(selectiveRepeatTester.testRun(wind, num_packages, p, nTests))

    make_plot(pLoss_array, time_gbn, time_sr, "probability of package loss")
