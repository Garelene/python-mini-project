import csv
import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

matplotlib.use('TkAgg')

CAR_STATUS_INDEX = 3
CAR_MODEL_INDEX = 1
CAR_RENTED_COUNT_INDEX = 5
LARGEFONT = ("Verdana", 35)
MEDIUMFONT = ("Verdana", 20)

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1000x1000")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, Dashboard, MostPopularCarsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = ttk.Label(self, text="Login", font=LARGEFONT)
        title.grid(row=0, column=1)

        userNameLabel = ttk.Label(self, text="Username", font=MEDIUMFONT)
        userNameLabel.grid(row=1, column=1)

        userNameInputBox = ttk.Entry(self)
        userNameInputBox.grid(row=2, column=1)

        passwordLabel = ttk.Label(self, text="Password", font=MEDIUMFONT)
        passwordLabel.grid(row=3, column=1)

        passwordInputBox = ttk.Entry(self)
        passwordInputBox.grid(row=4, column=1)

        submitButton = ttk.Button(
            self,
            text="Login",
            command=lambda: controller.show_frame(Dashboard))
        submitButton.grid(row=5, column=1)

class Dashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = ttk.Label(self, text="Dashboard", font=LARGEFONT)
        title.grid(row=0, column=1, padx=10, pady=10)

        rentedCarsText = ttk.Label(self, text="Rented Cars", font=MEDIUMFONT)
        rentedCarsText.grid(row=1, column=1, padx=10, pady=10)

        rentedCarsCountText = ttk.Label(self, text="{rentedCarsCount}".format(
        rentedCarsCount=rentedCarsCount()))
        rentedCarsCountText.grid(row=2, column=1, padx=10, pady=10)

        mostPopularCarsPageButton = ttk.Button(
            self,
            text="Most Popular Cars",
            command=lambda: controller.show_frame(MostPopularCarsPage))
        mostPopularCarsPageButton.grid(row=3, column=1)



class MostPopularCarsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = ttk.Label(self, text="Most Populars Cars", font=LARGEFONT)
        title.grid(row=0, column=1, padx=10, pady=10)

        chartData = {}

        for carRow in rentedCars():
            carName = carRow[CAR_MODEL_INDEX]
            carRentedCount = carRow[CAR_RENTED_COUNT_INDEX]

            chartData[carName] = int(carRentedCount)

        models = chartData.keys()
        popularity = chartData.values()

        # create a figure
        figure = Figure(figsize=(5, 3), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(models, popularity)
        axes.set_title('Most Rented Cars')
        axes.set_ylabel('Popularity')

        figure_canvas.get_tk_widget().grid(row=1, column=1)

        backButton = ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame(Dashboard))
        backButton.grid(row=2, column=1)



def users():
    rows = []

    with open("users.csv", 'r') as file:
        csvreader = csv.reader(file)

        # Skip headers
        next(csvreader)
        for row in csvreader:
            rows.append(row)

    return rows


def cars():
    rows = []

    with open("cars.csv", 'r') as file:
        csvreader = csv.reader(file)

        # Skip headers
        next(csvreader)

        for row in csvreader:
            rows.append(row)

    return rows


def rentedCars():
    return filter(getRentedCars, cars())


def getRentedCars(carRow):
    carStatus = carRow[CAR_STATUS_INDEX]

    if carStatus == "Rented":
        return True
    else:
        return False


def rentedCarsCount():
    return len(list(rentedCars()))


def averageRentalDuration():
    rented_cars = list(rentedCars())
    total_duration = 0

    # get the date for today
    current_date = datetime.date.today()

    for car in rented_cars:
        # calculate duration
        start_date = datetime.datetime.strptime(car[4], "%Y/%m/%d").date()
        duration = (current_date - start_date).days
        total_duration += duration

    if rentedCarsCount() > 0:
        return total_duration / rentedCarsCount()
    else:
        return 0

if __name__ == "__main__":
    app = App()
    app.mainloop()
