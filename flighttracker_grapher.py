import csv
from matplotlib import pyplot as plt
import matplotlib
import random

class ResultReader():
    def __init__(self):

        with open('Results.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            rows_list = []


            count = 0
            for row in readCSV:
                for index, item in enumerate(row):
                    if count < 1:
                        rows_list.append([item, []])
                    else:
                        rows_list[index][1].append(row[index])
                #print(count)
                count += 1
            print("Rows list: ", rows_list)


            self.dates= []
            self.example_prices_all = []
            self.output_dict = {}
            for index, item in enumerate(rows_list):
                if index > 1:
                    example_prices = []
                    for i in rows_list[index][1]:
                        if len(i) > 2:
                            string = i[1:-1]
                            num = int(string)
                        else: num = 0
                        example_prices.append(num)
                    # print(example_prices)
                    self.example_prices_all.append([rows_list[index][0],example_prices])
                    self.dates.append(rows_list[index][0])

            print("Actual Dates", self.dates)



            example_dates = []
            for i in rows_list[0][1]:
                if i[4] == '/':
                    string = i[2:4]
                elif i[6] == '/':
                    #print("1st: ",i[2:6])
                    string = i[2:6]
                    #print("2nd: ",string)
                num = float(string)
                example_dates.append(num)
            print("Example Prices All: ", self.example_prices_all)
            print("Example Dates: ", example_dates)



            font = {'family': 'normal',
                    'weight': 'bold',
                    'size': 5}

            matplotlib.rc('font', **font)

            print("Dates: {}".format(example_dates))
            self.dates_dict = {}

            for index,item in enumerate(example_dates):
                self.dates_dict[index] = item
            print("Dates dictionary: {}".format(self.dates_dict))
            # self.plotting()
            self.output()

    def output(self):
        # Initialise the output
        for index, item in enumerate(self.example_prices_all):
            self.output_dict[index] = [[],[]]

        # Populate the output
        for index, item in enumerate(self.example_prices_all):
            # print("index: ", index)
            tempDates = []
            tempPrices = []
            # print(item[1])

            emptyflag = 1
            for ind, ite in enumerate(item[1]):
                if ite != 0:
                    tempDates.append(self.dates_dict[ind])
                    tempPrices.append(ite)
                    emptyflag = 0

            if emptyflag == 1:
                break
                # raise Exception("Sorry there is an empty to date to be removed: {}".format(self.dates_dict[index]))
            self.output_dict[index] = [tempDates, tempPrices]
        print("Output Dictionary", self.output_dict)
        return self.output_dict

    def plotting(self):
        for i in self.example_prices_all:
            tempDates = []
            tempPrices = []
            for ind, ite in enumerate(i[1]):
                if ite != 0:
                    tempDates.append(self.dates_dict[ind])
                    tempPrices.append(ite)

            plt.plot(tempDates, tempPrices, label = i[0])

        #     for x, y in zip(example_dates, i[1]):
        #         label = i[0]
        #
        #         plt.annotate(label,  # this is the text
        #                      (x, y),  # this is the point to label
        #                      textcoords="offset points",  # how to position the text
        #                      xytext=(random.randrange(0,20,10), 0),  # distance from text to points (x,y)
        #                      ha='center')  # horizontal alignment can be left, right or center
        #
        # plt.plot(example_dates, example_prices)
        # plt.legend()
        plt.show()



if __name__ == "__main__":
    Reader = ResultReader()
    Reader.plotting()
    output = Reader.output()




