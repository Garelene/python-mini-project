import csv
import datetime
import tkinter as tk
from tkinter import ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')

CAR_STATUS_INDEX = 3
CAR_MODEL_INDEX = 1
CAR_RENTED_COUNT_INDEX = 5
LARGEFONT = ("Roboto", 35)
MEDIUMFONT = ("Roboto", 20)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("700x700")

        # Styles
        style = ttk.Style()
        style.theme_use('alt')
        style.configure(
            'TButton',
            background='red',
            foreground='white',
            width=20,
            borderwidth=1,
            focusthickness=3,
            focuscolor='none',
            fontsize='Roboto',
        )
        style.map('TButton', background=[('active', 'red')])
        style.configure('TLabel', background='#ececec')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, Dashboard, MostPopularCarsPage, BookingsPerDay):
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

        def validateLogin(username, password):
            for user in users():
                userUsername = user[3]
                userPassword = user[4]
                if username.get() == userUsername and password.get(
                ) == userPassword:
                    return True

        title = ttk.Label(self, text="Login", font=LARGEFONT)
        title.grid(row=0, column=1)

        userNameLabel = ttk.Label(self, text="Username", font=MEDIUMFONT)
        userNameLabel.grid(row=1, column=1, padx=10, pady=10)

        username = tk.StringVar()
        userNameInputBox = ttk.Entry(self, textvariable=username)
        userNameInputBox.grid(row=2, column=1, padx=10, pady=10)

        passwordLabel = ttk.Label(self, text="Password", font=MEDIUMFONT)
        passwordLabel.grid(row=3, column=1, padx=10, pady=10)

        password = tk.StringVar()
        passwordInputBox = ttk.Entry(self, textvariable=password)
        passwordInputBox.grid(row=4, column=1, padx=10, pady=10)

        def handleSubmit():
            isValid = validateLogin(username, password)

            if isValid:
                controller.show_frame(Dashboard)
            else:
                errorMessage = ttk.Label(self,
                                         text="Wrong Username or Password",
                                         font=MEDIUMFONT)
                errorMessage.grid(row=6, column=1, padx=10, pady=10)

        submitButton = ttk.Button(self,
                                  text="Login",
                                  command=lambda: handleSubmit(),
                                  style='Kim.TButton')
        submitButton.grid(row=5, column=1)


class Dashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = ttk.Label(self, text="Dashboard", font=LARGEFONT)
        title.grid(row=0, column=1, padx=10, pady=10)

        rentedCarsText = ttk.Label(self, text="Rented Cars", font=MEDIUMFONT)
        rentedCarsText.grid(row=1, column=1, padx=10, pady=10)
        rentedCarsCountText = ttk.Label(
            self,
            text="{rentedCarsCount}".format(rentedCarsCount=rentedCarsCount()))
        rentedCarsCountText.grid(row=2, column=1, padx=10, pady=10)

        rentalDurationText = ttk.Label(self,
                                       text="Average Rental Duration",
                                       font=MEDIUMFONT)
        rentalDurationText.grid(row=1, column=2, padx=10, pady=10)
        averageRentalDurationText = ttk.Label(
            self,
            text="{averageRentalDuration}".format(
                averageRentalDuration=averageRentalDuration()))
        averageRentalDurationText.grid(row=2, column=2, padx=10, pady=10)

        mostPopularCarsPageButton = ttk.Button(
            self,
            text="Most Popular Cars",
            command=lambda: controller.show_frame(MostPopularCarsPage))
        mostPopularCarsPageButton.grid(row=3, column=1)

        bookingsPerDayButton = ttk.Button(
            self,
            text="Bookings Per Day",
            command=lambda: controller.show_frame(BookingsPerDay))
        bookingsPerDayButton.grid(row=3, column=2)


class MostPopularCarsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = ttk.Label(self, text="Most Populars Cars", font=LARGEFONT)
        title.grid(row=0, column=1, padx=10, pady=10)

        chartData = {}

        for rentalRow in rentals():
            carName = rentalRow[1]

            if carName in chartData.keys():
                chartData[carName] += 1
            else:
                chartData[carName] = 1

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

        figure_canvas.get_tk_widget().grid(row=1, column=1, padx=10, pady=10)

        backButton = ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame(Dashboard))
        backButton.grid(row=2, column=1, padx=10, pady=10)


class BookingsPerDay(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = ttk.Label(self,
                          text="Number of Bookings Per Day",
                          font=LARGEFONT)
        title.grid(row=0, column=1, padx=10, pady=10)

        chartData = {}

        for rentalRow in rentals():
            bookedAtDate = rentalRow[6]

            if bookedAtDate in chartData.keys():
                chartData[bookedAtDate] += 1
            else:
                chartData[bookedAtDate] = 1

        bookingDates = chartData.keys()
        popularity = chartData.values()

        # create a figure
        figure = Figure(figsize=(5, 3), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(bookingDates, popularity)
        axes.set_title('Booking Per Day')
        axes.set_ylabel('Number of Bookings')

        figure_canvas.get_tk_widget().grid(row=1, column=1, padx=10, pady=10)

        backButton = ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame(Dashboard))
        backButton.grid(row=2, column=1, padx=10, pady=10)


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


def rentals():
    rows = []

    with open("rentals.csv", 'r') as file:
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
    totalDuration = 0

    for rentalRow in rentals():
        pickUpDate = datetime.datetime.strptime(rentalRow[3],
                                                "%Y/%m/%d").date()
        dropOffDate = datetime.datetime.strptime(rentalRow[4],
                                                 "%Y/%m/%d").date()
        duration = (dropOffDate - pickUpDate).days
        totalDuration += duration

    if len(rentals()) > 0:
        return totalDuration / len(rentals())
    else:
        return 0


if __name__ == "__main__":
    app = App()
    app.mainloop()
