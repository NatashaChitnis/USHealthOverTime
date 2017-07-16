#Import External Modules:
#import csv module to process files
import csv
#import matplotlib to plot line graphs
import matplotlib.pyplot as plt
import numpy as np
#import itemgetter to acquire the second value of each tuple in a list of tuples
from operator import itemgetter


def ranking_obesity(places, obesity_over_five_years):
	#Dictionary Comprehension to create {location : 2015_obesity_value}:
	obesity_rankings_dict = {place:float(obesity_over_five_years[i][4]) for i,place in enumerate(places)}
	sorted_dict = sorted(obesity_rankings_dict.items(), key=itemgetter(1))
	print "The following is a ranking of the least to most obese states (including the \
	national overall average and DC) in the country:"
	i = 1
	for element in sorted_dict:
		print "%d." % i , element[0]
		i += 1

#Opening csv files as file input and creating lists from csv readers:
def create_reader_list(filename):
	readerlist = list(csv.reader(open(filename))) 
	return readerlist


def display_state_obesity_trend(places, obesity_over_five_years, fruits_over_three_years, veggies_over_three_years, index, user_state):
	years = [2011, 2012, 2013, 2014, 2015]
	fruits_veggies_years = [2011, 2013, 2015]
 	min_y_axis = float(min(min(obesity_over_five_years[index]), min(fruits_over_three_years[index]), min(veggies_over_three_years[index]))) - 2
 	max_y_axis = float(max(max(obesity_over_five_years[index]), max(fruits_over_three_years[index]), max(veggies_over_three_years[index]))) + 2
 	#plt.axis sets the min and max of the x and y axes, with an argument of a list [xmin, xmax, ymin, ymax]
 	plt.axis([2010, 2016, min_y_axis, max_y_axis])
 	#plt.xticks sets the location and labels of the xticks
 	plt.xticks(years, ['2011', '2012', '2013', '2014', '2015'])
 	plt.yticks(np.arange(min_y_axis-1, max_y_axis+1, 1.0))
 	plt.xlabel("Year")
 	plt.ylabel("Rate of Obesity/Eating Preference(%)")
 	plt.title("Rate of Obesity Correlated with Eating Preferences in %s from 2011-2015" % user_state)
 	plt.figure(1)
 	plt.plot(years,obesity_over_five_years[index], 'ro', label="% Obese Adults")
 	plt.plot(fruits_veggies_years, fruits_over_three_years[index], 'bs', label="% Adults Eating\n <1 Fruit/Day")
 	plt.plot(fruits_veggies_years, veggies_over_three_years[index], 'g^', label="% Adults Eating\n <1 Veggie/Day")
	legend = plt.legend()
	for label in legend.get_texts():
		label.set_fontsize('small')
 	plt.show()
 	ranking_obesity(places, obesity_over_five_years)


def reader_list_overarching_call(list_of_filenames, init_list):
	for item in xrange(len(list_of_filenames)):
		init_list.append(create_reader_list(list_of_filenames[item]))


def create_prelim_all_vals_lists(all_vals_per_year, csv_list_reader):
	for i in xrange(1,53):
		for j in xrange(len(all_vals_per_year)):
			all_vals_per_year[j].append(csv_list_reader[j][i][14])


def every_state_natl_all_years_list_to_graph(init_list, all_years):
	for k in xrange(52):
		init_list.append([]) #creates 51 lists inside empty list
		#in each of 51 lists, we want the rates of obesity from 2011-2015/rates of eating preferences from 2011-2015
		for j in xrange(len(all_years)):
			init_list[k].append(all_years[j][k])


#Error checking using try/except:
try:
	list_of_obesity_readers_conv_to_lists = []
	list_of_fruits_readers_conv_to_lists = []
	list_of_veggies_readers_conv_to_lists = []
	list_of_veggies_csvs = ["2011_Less_Than_One_Veggie.csv", "2013_Less_Than_One_Veggie.csv", "2015_Less_Than_One_Veggie.csv"]
	list_of_fruits_csvs = ["2011_Less_Than_One_Fruit.csv", "2013_Less_Than_One_Fruit.csv", "2015_Less_Than_One_Fruit.csv"]
	list_of_obesity_csvs = ["2011_Obesity.csv", "2012_Obesity.csv", "2013_Obesity.csv", "2014_Obesity.csv", "2015_Obesity.csv"]
	#each item in the initially empty list will be a reader in list format for the corresponding files:
	reader_list_overarching_call(list_of_obesity_csvs, list_of_obesity_readers_conv_to_lists)
	reader_list_overarching_call(list_of_fruits_csvs, list_of_fruits_readers_conv_to_lists)
	reader_list_overarching_call(list_of_veggies_csvs, list_of_veggies_readers_conv_to_lists)
except IOError:
	print "Error: Cannot find or open one of the files."

places = []
#List Comprehension to generate a list of five lists/three lists:
obesity_all_years = [[] for i in xrange(5)]
fruits_all_years = [[] for i in xrange(3)]
veggies_all_years = [[] for i in xrange(3)]

for i in xrange(1,53):
	places.append(list_of_obesity_readers_conv_to_lists[3][i][5])
create_prelim_all_vals_lists(obesity_all_years, list_of_obesity_readers_conv_to_lists)
create_prelim_all_vals_lists(fruits_all_years, list_of_fruits_readers_conv_to_lists)
create_prelim_all_vals_lists(veggies_all_years, list_of_veggies_readers_conv_to_lists)

national_and_each_state_obesity_over_five_years = []
national_and_each_state_fruits_over_three_years = []
national_and_each_state_veggies_over_three_years = []


user_state = raw_input("Please enter the state for which you want the rate of\
 obesity (by percent) for 2011-2015 OR enter 'National' to see the trend for\
 the country as a whole OR 'District of Columbia' for Washington D.C.: ")
#Error checking using try/except:
try:
	index = places.index(user_state) #Each state is unique; needs to be found only once
	every_state_natl_all_years_list_to_graph(national_and_each_state_obesity_over_five_years, obesity_all_years)
	every_state_natl_all_years_list_to_graph(national_and_each_state_fruits_over_three_years, fruits_all_years)
	every_state_natl_all_years_list_to_graph(national_and_each_state_veggies_over_three_years, veggies_all_years)
	display_state_obesity_trend(places, national_and_each_state_obesity_over_five_years, national_and_each_state_fruits_over_three_years, national_and_each_state_veggies_over_three_years, index, user_state)

except ValueError:
	print "Error: That state is not part of the United States of America."
