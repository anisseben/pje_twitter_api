from app import api
from tkinter import * 



def search(my_entry,nbr_Tweet):

    tweets_result = Tk()
    tweets_result.grid_columnconfigure(1, weight=1)
    Label(tweets_result, text="Tweet", anchor="w").grid(row=0, column=0, sticky="ew")
    Label(tweets_result, text="Negative", anchor="w").grid(row=0, column=1, sticky="ew")
    Label(tweets_result, text="Positive", anchor="w").grid(row=0, column=2, sticky="ew")
    Label(tweets_result, text="Neutre", anchor="w").grid(row=0, column=3, sticky="ew")

    search = my_entry.get()
    nbr = nbr_Tweet.get()
    r = api.search_tweets(search,count=nbr)
    row = 1
    for item in r:

        name_label = Label(tweets_result, text=item._json["text"], anchor="w")
        name_label.grid(row=row, column=0, sticky="ew")

        negative_bouton= Button(tweets_result, text="-", command=lambda: classify("-"))
        positive_bouton= Button(tweets_result, text="+", command=lambda: classify("+"))
        neutre_bouton= Button(tweets_result, text="=", command=lambda: classify("="))
        negative_bouton.grid(row=row, column=1, sticky="ew")
        positive_bouton.grid(row=row, column=2, sticky="ew")
        neutre_bouton.grid(row=row, column=3, sticky="ew")

        print(item._json["text"])
        row+=1
        
    tweets_result.mainloop()
    

def classify(sentiment):
    print(sentiment)


# Interface Graphic :

fenetre = Tk()

label = Label(fenetre, text="Twitter Sentiments")
label.pack()
 
my_entry = Entry(fenetre)
nbr_Tweet = Entry(fenetre)
bouton= Button(fenetre, text="Search", command=lambda: search(my_entry,nbr_Tweet))


etiquette = Label(fenetre, text='search :')
etiquette.pack()

my_entry.pack()

etiquette = Label(fenetre, text='count :')
etiquette.pack()
nbr_Tweet.pack()
bouton.pack(side=TOP, padx=50, pady=10)


#fenetre.mainloop()