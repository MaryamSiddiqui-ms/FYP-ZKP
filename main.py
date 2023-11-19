import sys
import pandas as pd
import os

try:
    sys.path.append('./zkDist')
    sys.path.append('./zkSort')
    sys.path.append('./zkMaxLabel')
    
    from distance import zkDistance
    from sort import zkSort
    from maxLabel import zkmaxLabel

except Exception as e:
    print(e)


def main():

    dir_path = os.getcwd()


    df = pd.read_csv('train.csv')
    datapoint = [6,3]
    k = 3

    print(df.head(10))

    zkDistProof, distanceWitness = zkDistance(df, datapoint, dir_path)
    zkSortProof, sortWitness = zkSort(distanceWitness, dir_path)
    zkmaxLabelProof, prediction = zkmaxLabel(sortWitness, k, dir_path)

    print(prediction)

if __name__ == "__main__":
    main()


