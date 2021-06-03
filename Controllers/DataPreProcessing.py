import pandas as pd
import numpy as np

class DataPreProcessing():

    def printDF(self):
        print(self.df.head())

    def __init__(self,path):
        self.df = pd.read_csv(path)

    def dropColumn(self,columnName):
        if columnName != "None":
            self.df.drop([columnName],axis = 1, inplace=True)

    def extractYColumn(self,columnName):
        self.Y = self.df[columnName].copy()
        self.df.drop([columnName],axis = 1, inplace=True)

    def getColumns(self):
        return self.df.columns

    def findCategoricalAndDrop(self):
        for column in self.df.columns:
            if (self.df[column].dtype.name == "object" or self.df[column].dtype.name == "category"):
                self.df.drop([column], axis=1, inplace=True)


    def __echelon(self,arr,dim):
        for col in range(dim):
            for row in range(col+1,dim):
                if arr[col][col] == 0:
                    break
                elim_ratio = arr[row][col] / arr[col][col]
                arr[row] = arr[row] - elim_ratio * arr[col]

    def __reducedEchelon(self,arr,dim):
        self.__echelon(arr,dim)
        for col in reversed(range(dim)):
            for row in reversed(range(col)):
                if arr[col][col] == 0:
                    break
                elim_ratio = arr[row][col] / arr[col][col]
                arr[row] = arr[row] - elim_ratio * arr[col]

    def __getBayesList(self,arr,dim):
        self.__reducedEchelon(arr,dim)
        for idx, row in enumerate(arr):
            yield row[-1] / row[idx]

    def doRegression(self):
        innerBayesMatrix = []
        for i in range(len(self.df.columns)):
            jlist = []
            for j in range(len(self.df.columns)):
                sumX = 0
                for k in range(len(self.df[self.df.columns[0]])):
                    sumX = sumX + ((self.df[self.df.columns[i]][k]) * (self.df[self.df.columns[j]][k]))
                jlist.append(sumX)
            innerBayesMatrix.append(jlist)

        firstRow = []
        for i in range(len(self.df.columns)):
            sumX = 0
            for j in range(len(self.df[self.df.columns[i]])):
                sumX = sumX + self.df[self.df.columns[i]][j]
            firstRow.append(sumX)
        concatv = [firstRow] + innerBayesMatrix
        vectorB0 = [len(self.df[self.df.columns[0]])] + firstRow

        BayesMatrix = concatv.copy()
        for i in range(len(vectorB0)):
            BayesMatrix[i] = [vectorB0[i]] + concatv[i]

        yMatrix = []
        for i in range(len(self.df.columns)):
            sumXY = 0
            for j in range(len(self.df[self.df.columns[i]])):
                sumXY = sumXY + (self.df[self.df.columns[i]][j] * self.Y[j])
            yMatrix.append(sumXY)
        YMatrix = [sum(self.Y)] + yMatrix

        GaussMatrix = BayesMatrix.copy()
        for i in range(len(vectorB0)):
            GaussMatrix[i] = BayesMatrix[i] + [YMatrix[i]]

        GaussMatrix = np.array(GaussMatrix, dtype="float32")
        matrixDim = len(GaussMatrix)
        self.BayesList = list(self.__getBayesList(GaussMatrix, matrixDim))

    def predict(self,inputs):
        predictionVal = 0
        for i in range(len(inputs)):
            predictionVal = predictionVal + (inputs[i] * self.BayesList[i + 1])
        predictionVal = predictionVal + self.BayesList[0]
        return predictionVal

