import csv
import tkinter as tk
from tkinter import ttk
import datetime
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

CAR_STATUS_INDEX = 3
CAR_MODEL_INDEX = 1
CAR_RENTED_COUNT_INDEX = 5

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


def renderMostRentedCarsChart(root):
    chartData = {};

    for carRow in rentedCars():
        carName = carRow[CAR_MODEL_INDEX]
        carRentedCount = carRow[CAR_RENTED_COUNT_INDEX]

        chartData[carName] = int(carRentedCount)

    print(chartData)

    models = chartData.keys()
    popularity = chartData.values()

    # create a figure
    figure = Figure(figsize=(16, 9), dpi=100)

    # create FigureCanvasTkAgg object
    figure_canvas = FigureCanvasTkAgg(figure, root)

    # create the toolbar
    NavigationToolbar2Tk(figure_canvas, root)

    # create axes
    axes = figure.add_subplot()

    # create the barchart
    axes.bar(models, popularity)
    axes.set_title('Most Rented Cars')
    axes.set_ylabel('Popularity')

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)


def main():
    # Create window
    root = tk.Tk()

    # Provide Window Size
    root.geometry("1000x1000")

    # App Title
    tk.Label(text="Car Rental Admin Dashboard",
             height=2,
             width=30,
             font=("Courier", 25)).pack()

    # Rented Cars Section
    tk.Label(text="Rented Cars").pack()
    tk.Label(text="{rentedCarsCount}".format(
        rentedCarsCount=rentedCarsCount())).pack()

    # Most Rented Cars Chart
    renderMostRentedCarsChart(root)

    # Run app
    root.mainloop()

if __name__ == "__main__":
    main()
