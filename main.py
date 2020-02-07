from classes.weather_api import Weather_api
from classes.news_api import News_api
from classes.random_classes import FullScreenApp
from PIL import Image, ImageTk
from time import strftime, localtime 
from newsapi import NewsApiClient
import Tkinter as tk
import sys

reload(sys)
sys.setdefaultencoding('utf8')

weather_api = Weather_api()
weather = weather_api.get_data()

news_api = News_api()
news = news_api.get_data()

#top_headlines = newsapi.get_top_headlines(category='technology',
#                                          language='en',
#                                          country='us')

#print(weather_api.jprint(weather))

# display time on the label 
def time(): 
    string = strftime('%H:%M:%S %p')
    clock.config(text = string) 
    day_of_week.config(text = strftime("%A", localtime()))
    date.config(text = strftime("%d-%m-%Y", localtime()))
    clock.after(1000, time) 


#configuring the tkinter module
root=tk.Tk()
app=FullScreenApp(root)
root.configure(background='black')

top_frame = tk.LabelFrame(root, background = 'black',borderwidth=0, highlightthickness=0)
top_frame.pack(anchor = 'n',fill="x")

time_clock_frame = tk.LabelFrame(top_frame, background = 'black',borderwidth=0, highlightthickness=0)
time_clock_frame.pack(anchor="n",side="right",padx=5)

# Styling the label widget for clock
clock = tk.Label(time_clock_frame, font = ('arial', 50, 'bold'), background = 'black', foreground = 'white') 
# Placing clock at the centre of the tkinter window 
clock.pack(anchor = 'ne')

#show date
date = tk.Label(time_clock_frame, font = ('arial', 30, 'bold'), background = 'black', foreground = 'white')
date.pack(anchor = 'ne')

#show day of week
day_of_week = tk.Label(time_clock_frame, font = ('arial', 20, 'bold'), 
            background = 'black', 
            foreground = 'white')
day_of_week.pack(anchor = 'ne')

#update da label date;clock;day_of_week

time()


weather_weather_frame = tk.LabelFrame(top_frame, background = 'black',borderwidth=0, highlightthickness=0)
weather_weather_frame.pack(side="left")

weather_frame = tk.LabelFrame(weather_weather_frame, background = 'black',borderwidth=0, highlightthickness=0)
weather_frame.grid(row=0,column=0,padx=(15, 15))
left = tk.Label(weather_frame, text=weather[0], font = ('arial', 50, 'bold'), background = 'black', foreground = 'white')
left.pack(anchor="w")

weather_labels = []
i=1
for w in weather[1]:
    weather_label_inside = []  #0 - image; 1 - temp; 2 - wind; 3 - humidity; 4 - clouds; 5 - rain
    weather_frame = tk.LabelFrame(weather_weather_frame, background = 'black',borderwidth=0, highlightthickness=0)
    weather_frame.grid(row=0,column=i,padx=(5, 5))
    i=i+1
     
    #date = datetime.fromtimestamp(weather[0]['dt'])
    left = tk.Label(weather_frame, font = ('arial', 24, 'bold'), background = 'black', foreground = 'white',text=w[0])
    left.pack()
    img = ImageTk.PhotoImage(Image.open("images/weather_icons_b/"+w[6]+"b.jpg"))
    imgLabel = tk.Label(weather_frame,image=img,borderwidth=0, highlightthickness=0)
    imgLabel.image = img
    imgLabel.pack(anchor = 'n')
    weather_label_inside.append(imgLabel)
    left = tk.Label(weather_frame, font = ('arial', 18), text="Temp: "+ str(w[1]) +"C",background = 'black', foreground = 'white')
    left.pack(anchor="w")
    weather_label_inside.append(left)
    left = tk.Label(weather_frame, font = ('arial', 18), text="wind: "+ str(w[2]) +"km/h",background = 'black', foreground = 'white')
    left.pack(anchor="w")
    weather_label_inside.append(left)
    left = tk.Label(weather_frame, font = ('arial', 18), text="humidity: "+ str(w[3]) +"%",background = 'black', foreground = 'white')
    left.pack(anchor="w")
    weather_label_inside.append(left)
    left = tk.Label(weather_frame, font = ('arial', 18), text="clouds: "+ str(w[4]) +"%",background = 'black', foreground = 'white')
    left.pack(anchor="w")
    weather_label_inside.append(left)
    left = tk.Label(weather_frame, font = ('arial', 18), text="rain: "+ str(w[5]) +"",background = 'black', foreground = 'white')
    left.pack(anchor="w")
    weather_label_inside.append(left)




one_news_counter = 0

def update_news_to_new_source():
    global news
    global news_api

    news_api.generate_url(True)
    news = news_api.get_data()
    print(news_api.get_category())
    counter = 0
    for n in news['articles']:
        news_labels[counter][0].config(text = n['title'])
        news_labels[counter][2].config(text = "       " + str(n['description']))
        news_labels[counter][3].config(text = "Source: " + n['source']['name'])
        news_labels[counter][4].config(text = "Published at: " + n['publishedAt'])
        counter += 1
    

def update_news_content():
    global one_news_counter
    news_labels[(one_news_counter-1)][1].config(height=0)
    if(len(news['articles'])<=one_news_counter):
        update_news_to_new_source()
        one_news_counter = 0
        news_labels[(one_news_counter)][1].config(height=150)
    else:
        news_labels[(one_news_counter)][1].config(height=150)

    one_news_counter = one_news_counter + 1
    all_news_frame.after(30000,update_news_content)


width  = root.winfo_screenwidth()/2
height  = root.winfo_screenheight()-500
news_frame = tk.LabelFrame(root, background = 'black',borderwidth=0, highlightthickness=0,width = width,height=height)
news_frame.pack(anchor="sw",side="bottom", expand=False)
news_frame.pack_propagate(0)


all_news_frame = tk.LabelFrame(news_frame, background = 'black',borderwidth=0, highlightthickness=0)
all_news_frame.pack(anchor="sw",side="bottom", expand=False)
#all_news_frame.after(300000,update_news_to_new_source)  #5 minutos
all_news_frame.after(30000,update_news_content)

news_labels = []
for n in news['articles']:
    news_label_inside = [] #0 - title; 1 - content_container; 2 - content; 3 - source; 4 - date
    new = tk.Label(all_news_frame, font = ('arial', 18), background = 'black', foreground = 'white',justify="left")
    new.pack(anchor = 'w')
    new.config(text = n['title'])
    news_label_inside.append(new)

    one_new_frame = tk.LabelFrame(all_news_frame, background = 'black',borderwidth=0, highlightthickness=0,width = width,height=0)
    one_new_frame.pack(anchor="nw", expand=False)
    one_new_frame.pack_propagate(0)
    news_label_inside.append(one_new_frame)

    news_content = tk.Label(one_new_frame, font = ('arial', 18), background = 'black', foreground = 'white',wraplength=width-60,justify="left")
    news_content.pack(anchor = 'w',padx=(40,0),pady=(10,0))
    news_label_inside.append(news_content)

    news_source = tk.Label(one_new_frame, font = ('arial', 18), background = 'black', foreground = 'white',justify="right")
    news_source.pack(anchor = 'e',pady=(10,0))
    news_label_inside.append(news_source)

    news_date = tk.Label(one_new_frame, font = ('arial', 18), background = 'black', foreground = 'white',justify="right")
    news_date.pack(anchor = 'e')
    news_label_inside.append(news_date)

    news_content.config(text = "       " + n['description'])
    news_source.config(text = "Source: " + n['source']['name'])
    news_date.config(text = "Published at: " + n['publishedAt'])

    if(one_news_counter == 0):
        one_new_frame.config(height=150)
        one_news_counter = one_news_counter + 1


    news_labels.append(news_label_inside)


root.mainloop()




