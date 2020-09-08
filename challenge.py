#Name: Peter Leong
#Shopify Data science challenge

import pandas as pd

shopData = pd.read_csv("2019 Winter Data Science Intern Challenge Data Set - Sheet1.csv")
print(shopData.order_amount.describe())
#this describe statement returns
# count      5000.000000
# mean       3145.128000  <---- the AOV from the original problem
# std       41282.539349   <----  we notice that the standard deviation is very high here
# min          90.000000
# 25%         163.000000
# 50%         284.000000
# 75%         390.000000
# max      704000.000000

#We can sort by the highest order amounts and see how often they appear
large_orders = shopData.groupby(['order_amount']).size().reset_index(name='count').sort_values(by='order_amount', ascending=False)
print(large_orders.head(15))
#it seems the larger order amounts of 704000,77175,51450, and 25725 are repeated multiple times.
# 257        704000     17
# 256        154350      1
# 255        102900      1
# 254         77175      9
# 253         51450     16
# 252         25725     19

#We can take a look at the data for these large_orders
print(shopData.loc[shopData['order_amount'].isin([704000, 77175, 51450, 25725])].sort_values(by='order_amount', ascending=False))
#All of these orders except the 704000 orders seem to be different buyers buying a very expensive pair of shoes from store 78.
#The 70400 orders are all from the same buyer and the same amount every time, also occuring at the same time every time an order is made.
#This leads me to believe that the 704000 orders are from a supplier of some kind.
#One possible way to normalize the data would be to drop the orders from user607 and orders made in shop 78 from the table and re-evaluate the mean from there. However, that could be seen as bias and false reporting.
#I believe a better way to report the data would be to narrow the range we are looking at so that these outliers don't affect the outcome as much.
#We can use the Inter Quartile Range for this.
q1 = shopData['order_amount'].quantile(0.25)
q3 = shopData['order_amount'].quantile(0.75)
iqr = q3 - q1
#Here we trim off anything less than or greater than 1.5 times the IQR
trimmed_shopData = shopData.loc[(shopData['order_amount'] > q1 - 1.5 * iqr) & (shopData['order_amount'] < q3 + 1.5 * iqr)]
print(trimmed_shopData.order_amount.describe())
# count    4859.000000
# mean      293.715374   <---- New AOV
# std       144.453395   <---- std much lower than before
# min        90.000000
# 25%       162.000000
# 50%       280.000000
# 75%       380.000000
# max       730.000000

# a)This would be how I would re-evaluate this data if I was given a suspucious AOV.
# b)Seeing how the mean is greater than the median, the numbers are skewed towards the lower end of the spectrum. Just like with the numbers we trimmed from the original data set, some of the larger numbers skew the mean immensely and the median would make more sense in this case.
# c)I would report the median of the trimmed data set at $280 with a standard deviation of 144.453.


#2a) SELECT COUNT(*) AS SpeedyShipments
# FROM [Orders]
# JOIN [Shippers]
#     ON [Orders].ShipperID = [Shippers].ShipperID
# WHERE [Shippers].ShipperName = 'Speedy Express'
# 54 Total Orders

# 2b) SELECT [Employees].LastName, COUNT(*) AS NumberOfOrders
# FROM [Orders]
# JOIN [Employees]
# ON [Orders].EmployeeID = [Employees].EmployeeID
# GROUP BY [Employees].LastName
# ORDER BY NumberOfOrders DESC
# Limit 1
#Peacock with 40 orders

# 2c) SELECT [Products].ProductName,
#     SUM([OrderDetails].Quantity) AS "NumberOfOrders"
# FROM [Orders]
# JOIN [Customers]
#     ON [Orders].CustomerID = [Customers].CustomerID
# JOIN [OrderDetails]
#     ON [Orders].OrderID = [OrderDetails].OrderID
# JOIN [Products]
#     ON [OrderDetails].ProductID = [Products].ProductID
# WHERE [Customers].Country = 'Germany'
# GROUP BY [OrderDetails].ProductID
# ORDER BY NumberOfOrders DESC
# Limit 1
#Boston Crab Meat with 160 orders
