import requests as r
from bs4 import BeautifulSoup as bs
from random import randint
from time import sleep
from datetime import datetime

import sqlite3

def get(url):
    sleep(randint(10,500)/1000)
    page = r.get(url)
    return page

def soup(page):
    return bs(page.content, 'html.parser')

class offer:
    def __init__(self, link):
        self.link = link

    def setName(self, name):
        self.name = name
        
    def setPrice(self, price):
        self.price = price
        
    def setRetierName(self, rentierName):
        self.rentierName = rentierName
        
    def setRentierPhone(self, rentierPhone):
        self.rentierPhone = rentierPhone
        
    def setRentierEmail(self, rentierEmail):
        self.rentierEmail = rentierEmail

    def setRentierCompany(self, rentierCompany):
        self.rentierCompany = rentierCompany

    def setDescription(self, description):
        self.description = description

    def setDetails(self, details):
        self.details = details

    def setLocation(self, location):
        self.location = location

    def setDate(self, date):
        self.date = date
    


url = "https://www.sreality.cz/hledani/pronajem/byty,domy"

"""
Datová struktura offeru.

Link, Name, Price, Rentier Name, Rentier Phone, Rentier Email, Rentier Company, Description, Details, Location, Date, DateofUnlisting

"""


def updateDatabase(cur, link, name, price, rentierName, rentierPhone, rentierEmail, rentierCompany, description, details, location, date, dateofUnlisting):
    cur.execute("""INSERT OR IGNORE INTO offers (Link, Name, Price, RentierName, RentierPhone, RentierEmail, RentierCompany, Description, Details, Location, Date, DateOfUnlisting) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (link, name, price, rentierName, rentierPhone, rentierEmail, rentierCompany, description, details, str(location), date, dateofUnlisting, ))

def getOfferDetails(url):
    offer_ = offer(url)
    try:
        offerSoup = soup(get(url))

        #Gets name of the offer

        try:
            name = offerSoup.find_all("h1")[0].text
            offer_.setName(name)
        except:
            offer_.setName("NaN")
            
        #Gets price of the offer
            
        try:
            price = offerSoup.find_all("p", class_="MuiTypography-root MuiTypography-body1 css-1b1ajfd")[0].text
            offer_.setPrice(price)
        except:
            offer_.setPrice("NaN")
            
        # Gets Pronajímatel
        
        try:
            rentierName = offerSoup.find_all("a",class_ = "MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textSecondary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-colorSecondary MuiButton-root MuiButton-text MuiButton-textSecondary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-colorSecondary css-isq4dy")[0].text
            offer_.setRetierName(rentierName)
        except:
            offer_.setRetierName("NaN")
        try:
            rentierPhone = offerSoup.find_all("a", class_ = "MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textSecondary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-colorSecondary MuiButton-root MuiButton-text MuiButton-textSecondary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-colorSecondary css-1q1bqq3")[0].text
            offer_.setRentierPhone(rentierPhone)
        except:
            offer_.setRentierPhone("NaN")
        try:
            rentierEmail = offerSoup.find_all("a", class_="MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textSecondary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-colorSecondary MuiButton-root MuiButton-text MuiButton-textSecondary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-colorSecondary css-1q1bqq3")[1].text
            offer_.setRentierEmail(rentierEmai)
            if rentierEmail == offer_.phone:
                offfer.setRentierEmail("NaN")
        except:
            offer_.setRentierEmail("NaN")
            
        try:
            rentierCompany = offerSoup.find_all("a", class_="MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textSecondary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-colorSecondary MuiButton-root MuiButton-text MuiButton-textSecondary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButton-colorSecondary css-isq4dy")[1].text
            offer_.setRentierCompany(rentierCompany)
        except:
            offer_.setRentierCompany("NaN")
                   
        # Gets Housing description

        try:
            housingDescription = offerSoup.find_all("pre")
            offer_.setDescription(housingDescription[0].text)
            
        except:
            offer_.setDescription("NaN")
        #  Gets Housing details
        
        try:
            housingDetails = offerSoup.find_all("section", class_="css-v4pyck")[0]
            details = housingDetails.find_all("div")[0].text
            offer_.setDetails(details)
        
        except:
            offer_.setDetails("NaN")
        
        # Gets Housing location
        try:
            housingLocation = offerSoup.find_all("section", class_="css-1y11ixe")[0]
            ahrefs = housingLocation.find_all("a")[0].get("href")
            location = ahrefs[ahrefs.find("=")+1:ahrefs.find("&")].split(",")
            if location[0] == "stre" or location[0] == "ward" or location[0] == "muni" or location[0] == "quar":
                offer_.setLocation(ahrefs)
            else:
                offer_.setLocation(location[1] + " " + location[0])
        except:
            offer_.setLocation("NaN")

        
        today = datetime.now().date()
        offer_.setDate(str(today))
        
        return offer_
    except:
        print("Error in getting offer details")

def main():
    con = sqlite3.connect("offers.db")
    updateDelist = con.cursor()
    updateDelist.execute("UPDATE offers SET DateOfUnlisting = 0;")
    con.commit()
    dateOfUnlisting = str(datetime.fromtimestamp(0).date())
    sreality = soup(get(url))
    data = []
    last_page = int(sreality.find_all("li", class_="MuiListItem-root MuiListItem-gutters MuiListItem-padding css-1ydg92w")[-1].text)
    for i in range(1,  last_page):
       offersPage = soup(get(f"https://www.sreality.cz/hledani/pronajem/byty,domy?strana={i}"))
       print(i)
       allOffers = offersPage.find_all("ul", class_="MuiGrid2-root MuiGrid2-container MuiGrid2-direction-xs-row css-1fesoy9")[0]
       allOffers  = allOffers.find_all("a")
       print("----------------------------\n\n\n\n\n\n")
       for offer in allOffers:
            cur = con.cursor()
            ahref = "https://www.sreality.cz" + offer.get("href")
            print(ahref)
            if not cur.execute("SELECT EXISTS(SELECT 1 FROM offers WHERE Link=?);", (ahref,)).fetchone()[0]:
                offer_=(getOfferDetails(ahref))
                updateDatabase(cur, offer_.link, offer_.name, offer_.price, offer_.rentierName, offer_.rentierPhone, offer_.rentierEmail, offer_.rentierCompany, offer_.description, offer_.details, offer_.location, offer_.date, dateOfUnlisting)
                con.commit()
                print("added!")
            else:
                cur.execute(f"UPDATE offers SET DateOfUnlisting = ? WHERE Link = ?;", (dateOfUnlisting,ahref,))
                con.commit()
                print("skipped")
    today = str(datetime.now().date())
    updateDelist.execute("UPDATE offers SET DateOfUnlisting = ? WHERE DateOfUnlisting = ?;", (today,0))
    con.commit()
                
if __name__ == '__main__':
    main() 
