from unittest import result
import numpy as np
from itertools import groupby

class Statistic():
    def __init__(self):
        self.series_list = []
        self.variation_range = []
        self.variants = []
        self.frequency_range = []
        self.relative_frequency_range = []
        self.distribution_function = []
        self.average_sample = []
        self.dispersion = []
        self.deviation = []
        self.corrected_deviation = []

    def setSeriesList(self, seriaesList):
        self.series_list = seriaesList
        self.variation_range = self.variationRange()
        self.variants = self.getVariants()
        self.frequency_range = self.staticalFrequencyRange()
        self.relative_frequency_range = self.statisticalRelativeFrequencyRange()
        self.distribution_function = self.empiricalDistributionFunction()
        self.average_sample = self.averageSample()
        self.dispersion = self.sampleDispersion()
        self.deviation = self.sampleAverageSquareDeviation()
        self.corrected_deviation = self.correctedSampleAverageSquareDeviation()

    #Вариационный ряд
    def variationRange(self):
        return sorted(self.series_list)

    #Получить варианты
    def getVariants(self):
        return [i for i, _ in groupby(self.variation_range)]

    #Статистический ряд частот
    def staticalFrequencyRange(self):       
        return [self.variation_range.count(i) for i in self.variants]

    #Статистияеский ряд относительных частот
    def statisticalRelativeFrequencyRange(self):
        seriesListLenght = len(self.variation_range)
        return [i / seriesListLenght for i in self.frequency_range]

    #Эмпирическая функция распределения
    def empiricalDistributionFunction(self):
        empericalFunction = []
        
        for i in range(0, len(self.relative_frequency_range)):
            empericalFunction.append(np.sum(self.relative_frequency_range[:i], initial=0)) #сумма элементов до
            empericalFunction[i] = round(empericalFunction[i], 4)
        
        empericalFunction.append(np.sum(self.relative_frequency_range, initial=0))
        empericalFunction[-1] = round(empericalFunction[-1], 4)
        return empericalFunction

    #X выбор
    def averageSample(self):
        return sum(self.variation_range) / len(self.variation_range)

    #Выборочная дисперсия
    def sampleDispersion(self):
        seriasLengh = len(self.variation_range)
        avgX = self.average_sample
        return sum((self.variation_range[i] - avgX) ** 2 for i in range(seriasLengh)) / seriasLengh

    #Выборочное среднее квадратическое отклонение
    def sampleAverageSquareDeviation(self):
        result = self.dispersion ** 0.5
        return round(result, 4)

    #Исправленное выборочное среднее квадратическое отклонение
    def correctedSampleAverageSquareDeviation(self):
        despertion = self.dispersion
        n = len(self.variation_range)
        result = (n / (n - 1) * despertion) ** 0.5
        return round(result, 4)