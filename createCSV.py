import sqlite3
import csv

def save2CSV(data):
    with open('data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Link', 'Name', 'Price', 'Rentier-Name', "Rentier-Company", 'Location', 'Date', 'DateOfUnlisting'])
        writer.writerows(data)


con = sqlite3.connect("offers.db")
cur = con.cursor()
save2CSV(cur.execute("SELECT Id, Link, Name, Price, RentierName, RentierCompany, Location, Date, DateOfUnlisting FROM offers"))    
