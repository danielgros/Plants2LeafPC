import numpy as np
import open3d as o3d
import pandas as pd
import sys

'''
Read and transform the dataframe
'''
#  Read the csv with the weather metadata with Pandas
dataset_path = sys.argv[1]
dataset = pd.read_csv(dataset_path)
print(dataset.head())

# Transform the DateTime column into a datetime format
#dataset['DateTime']=  pd.to_datetime(dataset['DateTime'], format='%d/%m/%Y %H:%M')
# Extract only the months and multiply them by an arbitrary 10 factor for easier visualization and separation
#dataset['Months'] = dataset['DateTime'].dt.month*10
# Transform the Temperature, Humidity and the new Months columns to a numpy array
dataset_scatter = dataset[['x_coor', 'y_coor','z_coor']].to_numpy()
first = True
prev_idx = -1
while(True):
	idx= int(input("Enter Index:"))
	if first:
		print(dataset_scatter[idx])
		first = False
	else:
		print(dataset_scatter[idx])
		print("Euclidean distance: ", np.linalg.norm(dataset_scatter[idx] - dataset_scatter[prev_idx]))
	prev_idx = idx
