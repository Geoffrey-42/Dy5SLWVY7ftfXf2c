import os
cwd = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
runfile('setup.py')

## Import the raw data into a dataframe
data_path = "data/raw/"
dataframe = pd.read_csv(data_path + "potential-talents - Aspiring human resources - seeking human resources.csv")
print('\nData imported')
dataframe.drop_duplicates(inplace = True, subset = ['job_title', 'location', 'connection'])
dataframe.reset_index(drop = True, inplace = True)
## Remove a non informative feature
dataframe.drop(inplace = True, labels=['id'], axis = 1)
print('''Column 'id' and duplicate rows were removed''')
##

## Display basic information about the dataframe
types = [type(c) for c in dataframe.columns]
print('\nThe dataframe columns and their types are:\n', dict(zip(dataframe.columns, types)))
print(f"\nThe dataframe shape is {dataframe.shape}")
##

print('make_dataset.py was run')