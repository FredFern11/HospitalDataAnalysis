import matplotlib.pyplot as plt
import numpy
import pandas
import seaborn
from matplotlib import pyplot
from pandas import DataFrame


def merge():
    # set the maximum number of a dataframe's columns to 8
    pandas.set_option("display.max_columns", 8)

    # retrieve the data from the CVS files
    generalData = pandas.read_csv("test/general.csv")
    prenatalData = pandas.read_csv("test/prenatal.csv")
    sportData = pandas.read_csv("test/sports.csv")

    # standarized name of the columns
    newColumns = ["index", "hospital", "gender", "age", "height", "weight", "bmi", "diagnosis", "blood_test", "ecg",
                  "ultrasound", "mri", "xray", "children", "months"]

    # standarize the columns names
    prenatalData.columns = newColumns
    sportData.columns = newColumns

    # merge the 3 tables into a single one
    dataFrame = pandas.concat([generalData, prenatalData, sportData], ignore_index=True)
    dataFrame.drop(dataFrame.columns[0], axis=1, inplace=True)
    dataFrame.drop(dataFrame.columns[14], axis=1, inplace=True)

    return dataFrame


def clean(dataFrame: DataFrame) -> DataFrame:
    # change all the null values to female (pregnancy)
    dataFrame["gender"] = dataFrame["gender"].fillna("f")

    # convert all the masculine genders to "m" and the feminine genders to "f"
    for i in range(len(dataFrame.index)):
        if dataFrame.loc[i, "gender"] == "man" or dataFrame.loc[i, "gender"] == "male":
            dataFrame.loc[i, "gender"] = "m"
        else:
            dataFrame.loc[i, "gender"] = "f"

    # change all the null values to 0
    dataFrame = dataFrame.fillna(0)

    # delete all the rows that have 0 as a hospital name (null row)
    for i in range(len(dataFrame.index)):
        if dataFrame.loc[i, "hospital"] == 0: dataFrame = dataFrame.drop(index=i)

    dataFrame = dataFrame.reset_index()

    return dataFrame


def save(dataFrame) -> None:
    # writes the data frame to a file
    f = open("test/test.csv", "w")
    f.write(dataFrame.to_csv())


def stats(dataFrame):
    # the hospital with the most patient
    popHospital = str(dataFrame["hospital"].mode()[0])
    # the number of patient having a stomach-related issue
    nbrGeneral = sum(dataFrame["hospital"].values == "general")
    stomachCount = 0
    disloCount = 0
    for j in range(len(dataFrame)):
        if dataFrame.loc[j, "hospital"] == "general" and dataFrame.loc[j, "diagnosis"] == "stomach":
            stomachCount += 1

        elif dataFrame.loc[j, "hospital"] == "sports" and dataFrame.loc[j, "diagnosis"] == "dislocation":
            disloCount += 1

    stomachRatio = str(round(stomachCount / nbrGeneral, 3))
    # the share of patient having a dislocation-related issue
    nbrSport = sum(dataFrame["hospital"].values == "sports")
    disloRatio = str(round(disloCount / nbrSport, 3))
    # difference in the median ages accross the hospitals
    ageMedian = dataFrame["age"].groupby(dataFrame["hospital"]).median()
    diffMedian = str(int(ageMedian["general"] - ageMedian["sports"]))
    # hospital with the most patients blood tested
    bloodTest = dataFrame["blood_test"]
    hospitalList = dataFrame["hospital"]
    results = {"general": 0, "prenatal": 0, "sports": 0}

    for i in range(len(dataFrame)):
        if bloodTest[i] == "t":
            if hospitalList[i] == "general":
                results["general"] += 1
            elif hospitalList[i] == "prenatal":
                results["prenatal"] += 1
            elif hospitalList[i] == "sports":
                results["sports"] += 1

    maxHospital = max(results, key=results.get)
    nbrBloodTest = str(results[maxHospital])


def histogram(dataFrame: DataFrame):
    pyplot.hist(dataFrame["age"], bins=[0, 15, 35, 55, 70, 80])
    pyplot.xlabel("age")
    pyplot.ylabel("number of patient")
    pyplot.title("age of patients")
    pyplot.show()


def pieChart(dataFrame: DataFrame):
    cold = sum(dataFrame["diagnosis"].values == "cold")
    stomach = sum(dataFrame["diagnosis"].values == "stomach")
    dislocation = sum(dataFrame["diagnosis"].values == "dislocation")
    heart = sum(dataFrame["diagnosis"].values == "heart")
    sprain = sum(dataFrame["diagnosis"].values == "sprain")
    fracture = sum(dataFrame["diagnosis"].values == "fracture")
    pregnancy = sum(dataFrame["diagnosis"].values == "pregnancy")

    data = [cold, stomach, dislocation, heart, sprain, fracture, pregnancy]
    labels = ["cold", "stomach", "dislocation", "heart", "sprain", "fracture", "pregnancy"]

    pyplot.pie(x=data, labels=labels)
    pyplot.show()


def violin(dataFrame: DataFrame):
    seaborn.violinplot(x=dataFrame["hospital"], y=dataFrame["height"])
    plt.show()


def visualize(dataFrame: DataFrame):
    histogram(dataFrame)
    pieChart(dataFrame)


def run() -> None:
    # the dataframe representing the hospital
    data = clean(merge())
    visualize(data)
    save(data)
    violin(data)
    print("The answer to the 1st question: 15-35" + "\n" +
          "The answer to the 2nd question: pregnancy" + "\n" +
          "The answer to the 3rd question: Because some values don't make sens")


run()
