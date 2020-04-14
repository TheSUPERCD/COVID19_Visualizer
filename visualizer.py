import pandas as pd
import matplotlib.pyplot as plt
import pickle as pkl
import sys

if len(sys.argv) > 1:
    countryName = str(sys.argv[1])
else:
    print('Please provide the name of the country whose data you want to view as a command line argument.')
    sys.exit(1)

data_csv = pd.read_csv('.\\COVID19_dataset\\train.csv')
dataset = data_csv.to_numpy()
data_points = len(dataset)

global_data = []
country_data = []
country_temp = dataset[0,2]
confirmed_temp = []
fatalities_temp = []
province_temp = dataset[0,1]

for i in range(data_points):
    if dataset[i,2] == country_temp:
        if str(dataset[i,1]) == str(province_temp):
            confirmed_temp.append(dataset[i,4])
            fatalities_temp.append(dataset[i,5])
        else:
            if str(province_temp) == 'nan':
                country_data.append(('None', confirmed_temp, fatalities_temp))
            else:
                country_data.append((province_temp, confirmed_temp, fatalities_temp))
            province_temp = dataset[i,1]
            confirmed_temp = []
            fatalities_temp = []
    else:
        if str(province_temp) == 'nan':
                country_data.append(('None', confirmed_temp, fatalities_temp))
        else:
            country_data.append((province_temp, confirmed_temp, fatalities_temp))
        global_data.append((country_temp, country_data))
        province_temp = dataset[i,1]
        country_temp = dataset[i,2]
        country_data = []
        confirmed_temp = []
        fatalities_temp = []

with open('processedData.pkl', 'wb+') as f:
    pkl.dump(global_data, f)

with open('processedData.pkl', 'rb') as f:
    world = pkl.load(f)

for country in world:
    if country[0] == countryName:
        for province in country[1]:
            plt.figure(province[0])
            plt.semilogy(province[1], basey=10)
            plt.semilogy(province[2], basey=10)
            plt.grid('on')
            plt.xlabel('Days--->')
            plt.ylabel('Number of people--->')
            plt.legend(('Infected', 'Died'), loc='upper left')
            if province[0] != 'None':
                plt.title('Effects of COVID-19 in ' + province[0] + ' province of ' + country[0])
            else:
                plt.title('Effects of COVID-19 in ' + country[0])
        
        plt.show()
        break