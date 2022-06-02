import csv
from tkinter import W
from typing import List, Mapping, Tuple
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def ShowBoxPlot(data: Mapping[str,List[float]]) -> None:

    for key in data:
        fig = go.Figure()
        fig.add_trace(go.Box(y=data[key], name=key,
                    marker_color = 'indianred'))

        fig.show()

def median(data: List[float]) -> float:
    if len(data) % 2 == 1:
        return data[int(len(data)/2)]
    else:
        return (data[int(len(data)/2) - 1] + data[int(len(data)/2)]) / 2

def calcBoxMetrics(data: List[float]) -> List[float]:
    res = []
    res.append(median(data))
    if len(data) % 2 == 1:
        res.append(median(data[:int(len(data)/2)])) # q1
        res.append(median(data[int(len(data)/2) + 1:])) # q3
    else:
        res.append(median(data[:len(data)/2])) # q1
        res.append(median(data[len(data)/2:])) # q3
    
    res.append(data[0]) # lowest
    res.append(data[len(data) - 1]) # biggest
    return res

def getBoxPlotMetrics(data: Mapping[str,List[float]]) -> List[List[float]]:
    res = []
    for key in data:
        res.append(calcBoxMetrics(data[key]))

    return res

def DrawMemFunctions(data: Mapping[str,List[float]]) -> None:
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

        # plot the function
       
        x = data[key]
        x = [x[0]/2] + x + [x[len(x)-1]+x[0]/2]

        for i in x:
            low_y.append(lowMembershipFunction(i,metric[3],metric[0]))
            low_y = [None if i == 0 else i for i in low_y]

            mid_y.append(middleMembershipFunction(i,metric[3], metric[4],metric[0]))
            mid_y = [None if i == 0 else i for i in mid_y]
            
            high_y.append(highMembershipFunction(i,metric[4],metric[0]))
            high_y = [None if i == 0 else i for i in high_y]
        
        plt.plot(x,low_y, 'r')
        plt.plot(x,mid_y, 'g')
        plt.plot(x,high_y, 'b')
        plt.show()


def removeZeros(x: List[float],y: List[float]) -> Tuple[List[float],List[float]]:
    direction = 1
    index = 0
    for i in range(len(y)):
        if y[i] == 0:
            index = 0

def lowMembershipFunction(x: float,lowest: float, median: float) -> float:
    if x <= lowest:
        return 1
    elif x > median:
        return 0
    else:
        return -x/(median-lowest) + median/(median-lowest)


def middleMembershipFunction(x: float, lowest: float, biggest: float, median: float) -> float:
    if x <= lowest or x > biggest:
        return 0
    elif x > lowest and x <= median:
        return x/(median-lowest) - lowest/(median-lowest)
    elif x > median and x <= biggest:
        return -x/(biggest-median) + biggest/(biggest-median)

    return 0

def highMembershipFunction(x: float, biggest: float, median: float) -> float:
    if x <= median:
        return 0
    elif x > biggest:
        return 1
    else:
        return x/(biggest-median) - median/(biggest-median)


def ReadCSV(filename: str) -> Mapping[str,List[float]]:
    file = open(filename)
    type(file)
    csvr = csv.reader(file)
    headers = next(csvr)
    data = {}
    for header in headers:
        data[header] = []

    for row in csvr:
        for i, col in enumerate(row):
            data[headers[i]].append(float(col))
    
    for key in data:
        data[key].sort()

    return data

if __name__ == '__main__':

    data = ReadCSV("data.csv")
    
    # ShowBoxPlot(data)
    DrawMemFunctions(data)
