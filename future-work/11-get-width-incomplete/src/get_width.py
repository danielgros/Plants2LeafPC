import math
 
# Function to find distance
def euclidian_distance(x1, y1, z1, x2, y2, z2):
      
    d = math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) +
                math.pow(z2 - z1, 2)* 1.0)
    print("Distance is ")
    print(d)


def main():
    print("start")



if __name__ == "__main__":
    main()
