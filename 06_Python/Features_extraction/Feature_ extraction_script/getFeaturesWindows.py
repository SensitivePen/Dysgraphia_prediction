import math
import pandas as pd
import kinematicFeatures
import tiltFeatures


#window is a dataframe consisting of tip, top accX,Y,Z; tilt-azimuth, tilt-altitude
def createFeatures(window):

    #we get tilt and kinematic features
    tiltDataFrame = tiltFeatures.tiltFeatures(window)
    kinematicDataFrame = kinematicFeatures.kinematicFeatures(window)

    featuresByWindowDF = pd.concat([tiltDataFrame, kinematicDataFrame], axis=1, join="inner")


    return featuresByWindowDF

X = []

def passThroughWindow(data, dataWindow, overlapRatio):

    lenDat_ = len(data)
    i = 0
    featuresByWindowDF = pd.DataFrame([])

    # Window rolling
    while i < (lenDat_ - 1):
        indStart_ = i
        indStop_ = indStart_ + dataWindow
        if (indStop_ >= lenDat_):
            indStop_ = lenDat_ - 1
        if (indStop_ - indStart_ >= 1):

            # Create window of raw data and pass it to the feature creator
            window = data[indStart_:indStop_]

            #get the featuresByWindow with the features creator
            featuresByWindowDF = featuresByWindowDF.append(createFeatures(window))

            #We define a rolling window that overlapps with the old window
            i += math.floor(dataWindow / overlapRatio)
    return featuresByWindowDF







