import pickle

filename = 'data/2023-01-30_11.00.00_png_ultra.svo_cpc.npy'

with open(filename, 'rb') as f:
    b = pickle.load(f)

for arr in b:
    if(arr[3] != 0):
        print(arr)

print(b)