from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bs4 import BeautifulSoup
import requests
from customtkinter import * 
import tkinter as tk


class MyApp:
    def __init__(self):
        self.app = CTk()
        self.app.geometry("600x400")
        self.app.resizable(0,0)

        side_img_data = Image.open("side-img.png")
        email_icon_data = Image.open("url-icon.png")
        

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
        

        CTkLabel(master=self.app, text="", image=side_img).pack(expand=True, side="left")

        frame = CTkFrame(master=self.app, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Welcome !", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(30, 0))
        

        CTkLabel(master=frame, text="  Enter the URL :", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(40, 10), padx=(29, 0))
        self.link_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.link_entry.pack(anchor="w", padx=(29, 0))
       

        CTkButton(master=frame,command=self.on_submit, text="Analyse", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225).pack(anchor="w", pady=(25, 0), padx=(29, 0))
        
        self.app.mainloop()

    def on_submit(self):
        link = self.link_entry.get()
        comments = self.get_comments(link)
        sentiment = self.analyse_sentiments(comments)
        self.show_results(sentiment)

   
    def get_comments(self, link):
        response = requests.get(link)
        if response.status_code == 200:
            page_content = response.content
            soup = BeautifulSoup(page_content, 'html.parser')
            comments = soup.find_all('span', {'data-hook': 'review-body'})
            return [comment.text for comment in comments]
        else:
            print(f"Failed to retrieve page: {response.status_code}")
            return []

    def analyse_sentiments(self, comments):
        bien_mots = ['perfect','excellent','prettiest', 'good', 'super', 'fantastic', 'wonderful', 'incredible', 'great', 'awesome', 'outstanding', 'impressive', 'brilliant', 'terrific', 'amazing', 'lovely', 'pleasing','love','happy','interesting','Nice','Durable','Cute',' Beautiful','Well-Made',' best','comfortable','great quality'  ]
        mal_mots = ['allergic','difficult','bad', 'terrible', 'horrible', 'disappointing', 'poor', 'embarrassing', 'awful', 'dreadful', 'lousy', 'subpar', 'inferior', 'unsatisfactory', 'regrettable', 'ghastly', 'horrendous', 'atrocious']
        neutre_mots = ['average', 'acceptable', 'passable', 'correct', 'neutral', 'ok', 'fair', 'mediocre', 'ordinary', 'commonplace', 'undistinguished', 'adequate', 'satisfactory', 'decent', 'tolerable']

        sentiments = []
        for comment in comments:
            bien_count = sum(word in comment for word in bien_mots)
            mal_count = sum(word in comment for word in mal_mots)
            neutre_count = sum(word in comment for word in neutre_mots)

            total = bien_count + mal_count + neutre_count
            bien_pct = bien_count / total if total else 0
            mal_pct = mal_count / total if total else 0
            neutre_pct = neutre_count / total if total else 0
            if bien_pct >= max(mal_pct, neutre_pct):
                sentiments.append('bien')
            elif mal_pct >= max(bien_pct, neutre_pct):
                sentiments.append('mal')
            else:
                sentiments.append('neutre')

        return sentiments

    def show_results(self, sentiments):
        results_window = tk.Toplevel(self.app)
        results_window.title('Résultats de l\'analyse des sentiments')
        side_frame = tk.Frame(results_window, bg='orange')
        side_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        sentiment_counts = {sentiment: sentiments.count(sentiment) for sentiment in set(sentiments)}

        main_frame = tk.Frame(results_window)
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.create_bar_chart(sentiment_counts, main_frame)
        self.create_pie_chart(sentiment_counts, main_frame)
        self.create_line_chart(sentiment_counts, main_frame)

       
        summary_frame = tk.Frame(results_window)
        summary_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

       
        summary_label = tk.Label(summary_frame, text="Résumé des résultats", font=("Arial Bold", 14))
        summary_label.pack()

        
        for sentiment, count in sentiment_counts.items():
            summary_text = f'Le nombre de commentaires {sentiment} est {count}.'
            summary_label = tk.Label(summary_frame, text=summary_text)
            summary_label.pack()

        self.display_sentiments(sentiments, results_window)


    def create_bar_chart(self, sentiment_counts, results_window):
        figure1 = plt.Figure(figsize=(4,3), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, results_window)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        ax1.bar(sentiment_counts.keys(), sentiment_counts.values())
        ax1.set_title('Bar Chart')

    def create_pie_chart(self, sentiment_counts, results_window):
        figure2 = plt.Figure(figsize=(5,3), dpi=100) 
        ax2 = figure2.add_subplot(111)
        pie2 = FigureCanvasTkAgg(figure2, results_window)
        pie2.get_tk_widget().pack()
        ax2.pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct='%1.1f%%')
        ax2.set_title('Pie Chart')

        # Calculer les pourcentages
        total = sum(sentiment_counts.values())
        percentages = {sentiment: (count / total) * 100 for sentiment, count in sentiment_counts.items()}

        # Créer un cadre pour les pourcentages
        percentage_frame = tk.Frame(results_window)
        percentage_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # Afficher les pourcentages dans l'interface graphique
        for sentiment, percentage in percentages.items():
            percentage_text = f'Le pourcentage de commentaires {sentiment} est {percentage:.2f}%'
            percentage_label = tk.Label(percentage_frame, text=percentage_text)
            percentage_label.pack()


    def create_line_chart(self, sentiment_counts, results_window):
        figure3 = plt.Figure(figsize=(5,3), dpi=100)
        ax3 = figure3.add_subplot(111)
        line3 = FigureCanvasTkAgg(figure3, results_window)
        line3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        ax3.plot(list(sentiment_counts.keys()), list(sentiment_counts.values()))
        ax3.set_title('Line Chart')


    def display_sentiments(self, sentiments, results_window):
        for i, sentiment in enumerate(sentiments):
            label = tk.Label(results_window, text=f'Commentaire {i+1}: {sentiment}')
            label.pack()

my_app = MyApp()
