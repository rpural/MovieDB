# MovieDB
Catalog of movies owned on DVD and Bluray.

![Alt text](Screenshot.png?raw=true "Main Screen")

I collect movies; it's an addiction of sorts. At the time of this update, I have almost 1,200 DVDs and Bluray discs. Keeping track of them all began to
take its toll. While in a store, we would see a film, read the description, not remember seeing it, and buy it. We'd get home, and (you guessed it) 
already had a copy. I needed a way to quickly look up a title to see if it was already in the collection at home.

Keeping them in their original cases
became impractical, so I moved them to special notebooks, with 20 pages each that hold four discs, so 80 discs per book. I'm currently in to book 18, and just bought six new books.

So, on to the application. In today's form, it is a Python GUI program that allows entry and editing movies within a database, and reporting, so that I
can transfer the report on to my phone and have it handy for use in a store. 

Once I'm happy with the for interface and look, the ultimate goal will
be to rewrite the app in Swift (iPhone / Mac user) and be able to dynamically update the list from anywhere.

The program displays the list of movies, read from an Sqlite3 database, sorted by either Title, or by Book and Page numbers, refering to the location of the movie in my library. The Media column contains D for DVD, B for Bluray, 4 for 4k Bluray, 3 for 3D Bluray, and E for extras and special features. When editing an entry, actors and a description can also be entered. Three printed reports can be generated: Sorted by Title, Sorted by Title with actors and description, and Sorted by Book and Page where the DVD / Bluray can be found.

The program uses the pyqt5 or Pyside2 libraries to build the displays, and FPDF for reporting.
