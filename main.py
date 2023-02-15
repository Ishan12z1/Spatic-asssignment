import pandas as pd
from geopy.distance import GreatCircleDistance as GCD

#global constants variables as per the conditions 
MINIMUN_EDITS=5
DISTANCE_THRESHOLD=200


# function to find the minimum edit distance between two strings
def minDis(str1,str2):
    m=len(str1)
    n=len(str2)

    # initialize the 2D array with 0ss
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):

            # if str1 is empty, only option is to insert all characters of str2
            if i == 0:
                dp[i][j] = j 

            # if str2 is empty, only option is to insert all characters of str1
            elif j == 0:
                dp[i][j] = i 

            # if last characters of both strings are same, ignore the last characters and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            # if the last characters are not same, consider all three operations on the str1 and find the minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],	 # Insert
                                dp[i-1][j],	 # Remove
                                dp[i-1][j-1]) # Replace

    return dp[m][n]<MINIMUN_EDITS # returns True if minimum edit distance is less than 5

if __name__ == "__main__":
	# read in a csv file into a pandas dataframe
	df=pd.read_csv('dataset.csv')

	# calculate the mean latitude and longitude of all locations
	mean_lat=df['latitude'].mean()
	mean_long=df['longitude'].mean()

	# add two new columns to the dataframe
	df['distance']=None # will be used to store the distance from each location to the mean location
	df['is_similar']=0 # will be used to mark locations that are similar



	# calculate the distance between each location and the mean location, and store the result in the distance column
	for i in range(len(df)):
		df.loc[i, 'distance'] = GCD((df.loc[i, 'latitude'], df.loc[i, 'longitude']), (mean_lat, mean_long)).m


	# sort the dataframe by distance, in ascending order
	df=df.sort_values(by='distance')

	# compare each location to all the other locations that are closer than 200 meters, until a location that is more than 200 meters away is encountered
	for i in df.index:
		lat1=df['latitude'][i]
		long1=df['longitude'][i]
		name1=df['name'][i]
		for j in range(i+1,len(df)):
			lat2=df.loc[j,'latitude']
			long2=df.loc[j,'longitude']
			distance=GCD((lat1,long1),(lat2,long2)).m
			if distance<=DISTANCE_THRESHOLD:
				name2=df.loc[j,'name']
				if minDis(name1,name2):
					df.loc[i,'is_similar']=1
					df.loc[j,'is_similar']=1
			elif distance>400:
				break

	# sort the dataframe by  index  in ascending order
	df=df.sort_index(axis=0)

	# select the columns to include in the output file and save the results to a csv file
	header=['name','latitude','longitude','is_similar']
	df.to_csv('output.csv', index=False,columns=header)
