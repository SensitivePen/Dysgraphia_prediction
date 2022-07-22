import getFeaturesWindows
import pandas as pd
import ML_Model_AND_Evaluation

# Put the path of the directory where the data is located (keep the r before the string)
#path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\06_Python\Features_extraction\Data\goodata\Openclose'
# path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands'
#path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\testing_files\test1\test_1_tilt_on_paper.csv'
# subjectLabels = pd.read_excel(r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands\Data_summary.xlsx',header=0)
# jen path
# path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands'
# subjectLabels = pd.read_excel(r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands\Data_summary_children.xlsx',header=0)

path = r'../../../09_Data_probands'

# 09_Data_probands/Data_summary_children.xlsx

def runfeaturesextract(subjectLabels):
    total_df = pd.DataFrame()

    #filter the database to only include the desired scope
    #subjectLabels = subjectLabels[subjectLabels['Dataset']==datasetScope]


    # Go through the file indexing all existing files
    for ind in subjectLabels.index:

        #print subjects that will be used for the model
        #print(subjectLabels[scope][ind])

        #some probands do not have data -> skip
        try:
            # DataFrame Creation with the Data by looking up the link in the excel file corresponding to proband
            reference = '/' + subjectLabels['Dataset'][ind] + '/' + subjectLabels[scope][ind] + '.csv'
            link = path + reference
            #link = path + start & end
            start, end = subjectLabels[f'Start_{scope}'][ind], subjectLabels[f'End_{scope}'][ind]


            raw_df = pd.read_csv(link)
            raw_df = raw_df.loc[start:end,:]
            raw_df = raw_df.reset_index()

            df = raw_df[['time', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 'psi', 'theta', 'normAccel', 'normMag','normGyr']]

            #When the length of the df changes, also change "getFeaturesFromFile.py"
            df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ','psi','theta','normAccel','normMag','normGyr']

            #topDF - we only use the acceleration data and the calculated psi & theta angles for the prediction
            totalDF = df[["time", "accX", 'accY', 'accZ','normAccel','psi','theta']]
            totalDF = totalDF.rename(columns={'accX': "accX_Top", 'accY': "accY_Top", 'accZ': "accZ_Top"})


            # Pass subject's dataframe through window
            featuresByWindowDF = getFeaturesWindows.passThroughWindow(totalDF, windowSize, overlapRatio)

            #Insert label of subject
            featuresByWindowDF.insert(0, 'subjectLabel', subjectLabels['Dataset'][ind] + "_" + subjectLabels['Subject'][ind])

            #Insert BHK scores of subject - insert command for insertion at specific space
            featuresByWindowDF.insert(1, 'BHK_speed', subjectLabels['Speed_score'][ind])
            featuresByWindowDF.insert(2, 'BHK_quality', subjectLabels['Quality_score'][ind])

            #Insert classification labels of subject
            featuresByWindowDF.insert(3, 'Class_binary', subjectLabels['Classification_binary'][ind])
            featuresByWindowDF.insert(4, 'Class_three', subjectLabels['Classification_three'][ind])

            #Add Age and Gender to the features
            featuresByWindowDF["Age"] = subjectLabels["Age"][ind]
            featuresByWindowDF["Gender"] = int(subjectLabels["Gender (0=boys)"][ind])

            pd.set_option('display.max_columns', None)

            total_df = pd.concat([total_df,featuresByWindowDF], axis=0)

        except TypeError:
            pass
    return total_df


if __name__ == "__main__":

    # window=[200,300,400,500,600]
    window=[300]
    over=[1]

    for windowInd in window:
        for overInd in over:
            print(windowInd)
            print(overInd)

            path = r"../../../09_Data_probands/"
            subjectLabels = pd.read_excel(path + 'Data_summary_all.xlsx', header=0)

            # define windowsize
            windowSize = windowInd

            #define the overlapping ratio meaning: windowStart += math.floor(dataWindow / overlapRatio)
            # 1 is resulting in no overlap
            # 2 results in 50% overlap
            overlapRatio = overInd

            #define scope: 'Link_loops'/'Link_sentences'
            scope = 'Link_loops'

            #define scope of Dataset
            datasetScope = 'Children'

            #extract features by window
            total_df = runfeaturesextract(subjectLabels)

            #export
            total_df.to_excel("Data_summary.xlsx")

            #run model pipeline and predict
            ML_Model_AND_Evaluation.pipeline(total_df)