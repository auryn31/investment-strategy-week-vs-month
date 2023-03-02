import csv
import datetime


years = 10
start_date = datetime.date.today() - datetime.timedelta(days=365*years)
end_date = datetime.date.today()

allWeeks = []
allMonth = []
# Loop through each month and get the first day
current_date = start_date.replace(day=1)
while current_date <= end_date:
    allMonth.append(current_date)
    current_date = current_date + datetime.timedelta(days=32)
    current_date = current_date.replace(day=1)

# Loop through each week and get the first day (Monday) of the week
current_date = start_date - datetime.timedelta(days=start_date.weekday())
while current_date <= end_date:
    allWeeks.append(current_date)
    current_date = current_date + datetime.timedelta(days=7)

def is_same_day(date1, date2):
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day


currentStockAmountMonth = 0.0
buyPriceMonth = 1000
lastPrice = 0.0
sumPriceMonth = years * 12 * buyPriceMonth
currentStockAmountWeek = 0.0
buyPriceWeek = 250
sumPriceWeek = sumPriceMonth

allPrices = []
allDates = []

with open('./msci_day.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count > 0:
            if line_count == 1:
                lastPrice = float(row[1].replace(",", ""))
            date = datetime.datetime.strptime(row[0], "%m/%d/%Y")
            price = float(row[1].replace(",", ''))
            allPrices.append(price)
            allDates.append(date.date())
        line_count += 1

def find_nearest_date_index(date_list, target_date):
    return min(range(len(date_list)), key=lambda i: abs(date_list[i] - target_date))

for month in allMonth:
    index = find_nearest_date_index(allDates, month)
    price = allPrices[index]
    if sumPriceMonth > 0:
        currentStockAmountMonth += buyPriceMonth / price  
        sumPriceMonth -= buyPriceMonth

for week in allWeeks:
    index = find_nearest_date_index(allDates, week)
    price = allPrices[index]
    if sumPriceWeek > 0:
        currentStockAmountWeek += buyPriceWeek / price  
        sumPriceWeek -= buyPriceWeek

print(f'Price if you buy every month on the first')
print(f'CurrentStockAmount {currentStockAmountMonth}')
print(f'Current Price ${lastPrice}')
print(f'Money left ${sumPriceMonth}')
print(f'CurrentValue ${round(currentStockAmountMonth * lastPrice, 2)}')
print()
print(f'Price if you buy every week on the first')
print(f'CurrentStockAmount {currentStockAmountWeek}')
print(f'Current Price ${lastPrice}')
print(f'Money left ${sumPriceWeek}')
print(f'CurrentValue ${round(currentStockAmountWeek * lastPrice, 2)}')
print(f'Difference {round(( currentStockAmountWeek  / currentStockAmountMonth   - 1) * 100, 2)}%')

