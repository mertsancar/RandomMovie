import httpx
from bs4 import BeautifulSoup
import json
import webbrowser
import random
import tkinter.messagebox as MessageBox
from tkinter import *
from tkinter import Tk, Canvas, Frame, BOTH


class MainPage:
    
    def __init__(self):
        global root
        scraper = Scraper()
        root = Tk()
        root.title("Watch Random Movie")
        root.geometry("540x360")
        root.config(bg="black")
        root.iconbitmap("movie.ico")
        root.resizable(False, False)

        def getMovie():                    
            movieData = scraper.getMoviesData() 
            global randomMovie
            randomMovie = random.choice(movieData)
            movieName = randomMovie.get("title")
            movieRate = randomMovie.get("rate")
            LabelmovieTitle.config(text="Title: {}".format(movieName))
            LabelmovieRate.config(text="Rate: {}".format(movieRate))
            
            ButtongoPage = Button(root, text="Go IMDB ", bg="black", fg="yellow", font=("Arial",13), command=goPage)
            ButtongoPage.place(x=225, y=300)

        def goPage():
            webbrowser.open('https://www.imdb.com/{}'.format(randomMovie.get("url")))

        #Labels
        LabelAppTitle = Label(root, text="Random Movie",bg="black" ,fg="yellow", font = ("Arial",23,"bold"))
        LabelAppTitle.place(x=160, y=20)

        LabelmovieTitle = Label(root, text="Title: ",bg="black", fg="yellow", font=("Arial",15))
        LabelmovieTitle.place(x=80, y=120)
        
        LabelmovieRate = Label(root, text="Rate: ",bg="black", fg="yellow", font=("Arial",15))
        LabelmovieRate.place(x=80, y=170)

        #Button
        ButtongetMovie = Button(root, text="Get Movie", bg="black", fg="yellow", font=("Arial",13), command=getMovie)
        ButtongetMovie.place(x=225, y=260)

        root.mainloop()
        
class Scraper:
    
    def __init__(self):
        self.db = Database()
        self.top250Movies = self.db.readfromDB()
        if not self.top250Movies:
            response = self.getPage("https://www.imdb.com/chart/top/")
            self.parseHTML(response)
            self.saveData(self.top250Movies)
                
    def getPage(self, url):
        response = httpx.get(url)
        return response
           
    def parseHTML(self, response):
        soup = BeautifulSoup(response.content, "html.parser")
        tableTop250Movie = soup.find( "tbody" ,{"class":"lister-list"}).findAll("tr")
        if tableTop250Movie == None:
            print("Something Wrong at parseHTML")

        id = 0
        for movie in tableTop250Movie:
            movieDetails = {}                
            movieURL = movie.find("td",{"class":"titleColumn"}).a.get("href")
            movieTitle = movie.find("td",{"class":"titleColumn"}).a.text
            movieRate = movie.find("td",{"class":"ratingColumn imdbRating"}).text                 
            movieDetails["id"] = id
            movieDetails["url"] = movieURL
            movieDetails["title"] =  movieTitle 
            movieDetails["rate"] = movieRate.replace("\n","")              
            self.top250Movies.append(movieDetails)
            id += 1
        
    def saveData(self, moviesData):
        self.db.writeToDB(moviesData)
    
    def getMoviesData(self):
        return self.top250Movies
            
class Database:

     def readfromDB(self):         
         try:        
            with open('movies.json') as f:
                  data = json.load(f)         
            return data
        
         except:
             return []

     def writeToDB(self, database):
        with open('movies.json', 'w') as outfile:
            json.dump(database, outfile, indent=4)
         
                 
if __name__ == "__main__":
    main = MainPage()

    