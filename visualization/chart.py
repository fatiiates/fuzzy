import csv
from typing import List, Mapping
from matplotlib import pyplot as plt
import plotly.graph_objects as go


CSV_FILE = "data.csv"


def ReadCSVAsAMap(filename: str, sort: bool = True) -> Mapping[str, List[float]]:
    file = open(filename)
    csvr = csv.reader(file)
    headers = next(csvr)
    data = {}
    for header in headers:
        data[header] = []

    for row in csvr:
        for i, col in enumerate(row):
            data[headers[i]].append(float(col))

    if not sort:
        return data 

    for key in data:
        data[key].sort()

    return data


def ShowBoxPlot() -> None:

    data = ReadCSVAsAMap(CSV_FILE)

    for key in data:
        fig = go.Figure()
        fig.add_trace(go.Box(y=data[key], name=key,
                             marker_color='indianred'))

        fig.show()


def median(data: List[float]) -> float:
    if len(data) % 2 == 1:
        return data[int(len(data)/2)]
    else:
        return (data[int(len(data)/2) - 1] + data[int(len(data)/2)]) / 2


def calcBoxMetrics(data: List[float]) -> List[float]:
    res = []
    res.append(median(data))
    res.append(data[0])  # lowest
    res.append(data[len(data) - 1])  # biggest

    if len(data) % 2 == 1:
        res.append(median(data[:int(len(data)/2)]))  # q1
        res.append(median(data[int(len(data)/2) + 1:]))  # q3
    else:
        res.append(median(data[:len(data)/2]))  # q1
        res.append(median(data[len(data)/2:]))  # q3

    return res


def getBoxPlotMetrics(data: Mapping[str, List[float]]) -> List[List[float]]:
    res = []
    for key in data:
        res.append(calcBoxMetrics(data[key]))

    return res


def drawResultGraphWithMamdaniMethod(method_results_filename: str):
    data = ReadCSVAsAMap(CSV_FILE, False)

    data = data["If"]
    result = []

    f = open(method_results_filename, 'r')
    
    for line in f.readlines():
        result.append(float(line))

    zipped = zip(data, result)
    zipped = sorted(zipped)

    tuples = zip(*zipped)
    list1, list2 = [ list(tuple) for tuple in  tuples]
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.yaxis.tick_left()

    plt.plot(list1, 'b')
    plt.plot(list2, 'r')
    plt.ylabel("Prediction graph")
    plt.show()

class ThreePaneChart:

    def __init__(self, result: List[float]) -> None:
        if len(result) < 3:
            raise Exception("Metriklerde en az 3 veri olmalıdır")

        self.median = result[0]
        self.lowest = result[1]
        self.biggest = result[2]

    def lowMembershipFunction(self, x: float) -> float:
        if x <= self.lowest:
            return 1
        elif x > self.median:
            return 0
        else:
            return -x/(self.median-self.lowest) + self.median/(self.median-self.lowest)

    def middleMembershipFunction(self, x: float) -> float:
        if x <= self.lowest or x > self.biggest:
            return 0
        elif x > self.lowest and x <= self.median:
            return x/(self.median-self.lowest) - self.lowest/(self.median-self.lowest)
        elif x > self.median and x <= self.biggest:
            return -x/(self.biggest-self.median) + self.biggest/(self.biggest-self.median)

        return 0

    def highMembershipFunction(self, x: float) -> float:
        if x <= self.median:
            return 0
        elif x > self.biggest:
            return 1
        else:
            return x/(self.biggest-self.median) - self.median/(self.biggest-self.median)

    @staticmethod
    def Draw() -> None:

        data = ReadCSVAsAMap(CSV_FILE)

        metrics = getBoxPlotMetrics(data)

        for metric, key in zip(metrics, data):
            low_y = []
            mid_y = []
            high_y = []
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')

            ax.yaxis.tick_left()

            t = ThreePaneChart(metric)

            # plot the function
            x = data[key]
            x = [x[0]/2] + x + [x[len(x)-1]+x[0]/2]

            for i in x:
                low_y.append(t.lowMembershipFunction(i,))
                low_y = [None if i == 0 else i for i in low_y]

                mid_y.append(t.middleMembershipFunction(i))
                mid_y = [None if i == 0 else i for i in mid_y]

                high_y.append(t.highMembershipFunction(i))
                high_y = [None if i == 0 else i for i in high_y]

            plt.plot(x, low_y, 'r')
            plt.plot(x, mid_y, 'g')
            plt.plot(x, high_y, 'b')
            plt.ylabel(key)

        plt.show()


class FivePaneChart(ThreePaneChart):

    def __init__(self, result: List[float]) -> None:
        if len(result) < 3:
            raise Exception("Metriklerde en az 5 veri olmalıdır")

        self.median = result[0]
        self.lowest = result[1]
        self.biggest = result[2]
        self.q1 = result[3]
        self.q3 = result[4]
        self.IQR = self.q3 - self.q1

    def veryLowMembershipFunction(self, x: float) -> float:
        if x <= self.q1 - 3*self.IQR:
            return 1
        elif x >= self.q1 - 3*self.IQR and x <= self.q1 - 1.5*self.IQR:
            return (self.q1 - (x + 1.5*self.IQR))/1.5*self.IQR
        elif x >= self.q1 - 1.5*self.IQR:
            return 0

    def lowMembershipFunction(self, x: float) -> float:
        if x <= self.q1 - 3*self.IQR:
            return 0
        elif x >= self.q1 - 3*self.IQR and x <= self.q1 - 1.5*self.IQR:
            return (x - (self.q1 - 3*self.IQR))/1.5*self.IQR
        elif x >= self.q1 - 1.5*self.IQR and x <= self.q1:
            return (self.q1 - x)/1.5*self.IQR
        elif x >= self.q1:
            return 0

        return self.median

    def middleMembershipFunction(self, x: float) -> float:
        if x <= self.q1 - 1.5*self.IQR:
            return 0
        elif x >= self.q1 - 1.5*self.IQR and x <= self.q1:
            return (x - (self.q1 - 1.5*self.IQR))/1.5*self.IQR
        elif x >= self.q1 and x <= self.q3:
            return 1
        elif x >= self.q3 and x <= self.q3 + 1.5*self.IQR:
            return ((self.q3 + 1.5*self.IQR) - x)/1.5*self.IQR
        elif x >= self.q3 + 1.5*self.IQR:
            return 0

        return self.median

    def highMembershipFunction(self, x: float) -> float:
        if x <= self.q3:
            return 0
        elif x >= self.q3 and x <= self.q3 + 1.5*self.IQR:
            return (x - self.q3)/1.5*self.IQR
        elif x >= self.q3 + 1.5*self.IQR and x <= self.q3 + 3*self.IQR:
            return ((self.q3 + 3*self.IQR) - x)/1.5*self.IQR
        elif x >= self.q3 + 3*self.IQR:
            return 0

        return self.median

    def veryHighMembershipFunction(self, x: float) -> float:
        if x <= self.q3 + 1.5*self.IQR:
            return 0
        elif x >= self.q3 + 1.5*self.IQR and x <= self.q3 + 3*self.IQR:
            return (x - (self.q3 + 1.5*self.IQR))/1.5*self.IQR
        elif x >= self.q3 + 3*self.IQR:
            return 1

        return self.median

    @staticmethod
    def Draw() -> None:

        data = ReadCSVAsAMap(CSV_FILE)

        metrics = getBoxPlotMetrics(data)

        for metric, key in zip(metrics, data):
            very_low_y = []
            low_y = []
            mid_y = []
            high_y = []
            very_high_y = []
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')

            ax.yaxis.tick_left()

            f = FivePaneChart(metric)

            # plot the function
            x = data[key]
            x = [x[0]/2] + x + [x[len(x)-1]+x[0]/2]

            for i in x:
                very_low_y.append(f.veryLowMembershipFunction(i))
                very_low_y = [None if i == 0 else i for i in very_low_y]

                low_y.append(f.lowMembershipFunction(i))
                low_y = [None if i == 0 else i for i in low_y]

                mid_y.append(f.middleMembershipFunction(i))
                mid_y = [None if i == 0 else i for i in mid_y]

                high_y.append(f.highMembershipFunction(i))
                high_y = [None if i == 0 else i for i in high_y]

                very_high_y.append(f.highMembershipFunction(i))
                very_high_y = [None if i == 0 else i for i in very_high_y]

            plt.plot(x, very_low_y, 'p')
            plt.plot(x, low_y, 'r')
            plt.plot(x, mid_y, 'g')
            plt.plot(x, high_y, 'b')
            plt.plot(x, very_high_y, 'y')

            plt.ylabel(key)

        plt.show()
