from csv import DictWriter, DictReader
from time import sleep, strftime
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
import datetime

class FlightTracker():
    def __init__(self):

        today = datetime.date.today()
        todays_date = today.strftime("%d/%m")
        print("BEGINING TRACKING EVENT ({})".format(todays_date))
        next1 = today + datetime.timedelta(2)
        self.cost_dict = {}
        self.cost_dict['Date'] = [todays_date]

        iterations = 8

        for i in range(iterations):
            next1 = next1 + datetime.timedelta(4)
            ndate1 = next1.strftime("%Y-%m-%d")
            self.informationExtractor(ndate1)
            sleep(randint(10, 20))

        for key in self.cost_dict.keys():
            if len(self.cost_dict[key]) > 1:
                self.cost_dict[key] = self.Average(self.cost_dict[key])

        date_ex = ["{}/6".format(i) for i in range(12, 31)]
        date_ex.extend(["{}/7".format(i) for i in range(1, 15)])
        date_ex.insert(0,'Date')
        print("Date ex: ", date_ex)
        costs_list = []
        for key in date_ex:
            try:
                costs_list.append([key, self.cost_dict[key]])
            except KeyError:
                print(f"'{key}' is unknown.")

        print(costs_list)

        self.CSV_Write(date_ex)


    def informationExtractor(self, date):
        chromedriver_path = '/Users/Jacklswalsh/PycharmProjects/Research_Tool/FlightTracker/chromedriver'
        driver = webdriver.Chrome(executable_path=chromedriver_path)  # This will open the Chrome window
        kayak = 'https://www.kayak.co.uk/flights/LON-YYZ/' + date + '-flexible?sort=duration_a&fs=airlines=~AC;st\
        ops=~0'
        driver.get(kayak)
        sleep(24)

        try:
            xp_popup_close = '//button[contains(@id,"accept") and contains(@class,"Common-Widgets-Button-StyleJam\
            Button")]'
            driver.find_elements_by_xpath(xp_popup_close)[0].click()
        except: pass
        sleep(randint(4, 8))

        try:
            xp_popup_close = '//button[contains(@id,"covid-loading-dialog-close") and contains(@class,"Button-No-\
            Standard-Style close darkIcon large")]'
            driver.find_elements_by_xpath(xp_popup_close)[0].click()
        except: pass
        sleep(randint(2, 6))

        xp_dates = '//div[@class="section date"]'
        dates = driver.find_elements_by_xpath(xp_dates)
        dates_list = [value.text[0:4] for value in dates]
        for index, j in enumerate(dates_list):
            if '/7' in j: dates_list[index] = j[:-1]
        for item in dates_list:
            self.cost_dict[item] = []

        xp_prices = '//div[@class="Common-Booking-MultiBookProvider good-provider featured-provider cheapest multi-row Theme-featured-large"]/a[@class="booking-link "]/span[@class="price option-text"]//span[@class="price-text"]'
        prices = driver.find_elements_by_xpath(xp_prices)
        prices_list = [price.text.replace('£','') for price in prices if price.text != '']
        prices_list = list(map(int, prices_list))


        print(" Dates: ", len(dates_list), "\n","Prices: ", len(prices_list))
        while len(prices_list) != len(dates_list):
            if len(prices_list) < len(dates_list):
                dates_list.pop(0)
            elif len(prices_list) > len(dates_list):
                prices_list.pop(0)

        if len(dates_list) == len(prices_list):
            for i, element in enumerate(dates_list):
                self.cost_dict[element].append(prices_list[i])

        print(self.cost_dict)
        sleep(6)
        driver.quit()
        return

    def Average(self, lst):
        return sum(lst) / len(lst)

    def CSV_Write(self, date_ex):
        dictionary_full = {}
        for item in date_ex:
            dictionary_full[item] = []
            if item in self.cost_dict.keys():
                dictionary_full[item] = self.cost_dict[item]
        print("Log >> Results >> ", dictionary_full)

        with open('Results.csv', 'a', newline='') as f:
            csv_writer = DictWriter(f, fieldnames=date_ex)
            csv_writer.writerow(dictionary_full)


tracker = FlightTracker()