from './zkDist/distance' import zkDistance
from './zkSort/sort.py' import zkSort
from './zkMaxLabel/maxLabel.py' import zkmaxLabel


def main():
    df = pd.read_csv('train.csv')
    datapoint = [6,3]

    zkDistProof, witness_path = zkDistance(df, datapoint)

    witness_path = './zkDist/' + witness_path
    zkSortProof = zkSort(witness_path)

    zkmaxLabelProof, witness_path = zkmaxLabel(witness_path)
