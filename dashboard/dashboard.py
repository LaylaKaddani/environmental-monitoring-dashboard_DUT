import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Capteurs")
        self.root.geometry("1200x800")

        # Variables
        self.data = None
        self.current_frame = None

        # Barre latérale
        self.create_sidebar()

        # Page d'accueil par défaut
        self.show_home_page()

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="black", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        buttons = [
            ("Accueil", self.show_home_page),
            ("Affichage", self.show_display_menu),
            ("Support", self.show_support_page),
            ("Manuel d'utilisation", self.show_manual_page),
            ("A propos", self.show_about_page),
            ("Quitter", self.quit_app),
        ]

        for text, command in buttons:
            button = tk.Button(
                sidebar, text=text, font=("Arial", 12), bg="blue", fg="white",
                activebackground="red", activeforeground="white", command=command
            )
            button.pack(fill=tk.X, pady=5, padx=10)

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_home_page(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            self.current_frame, text="Bienvenue sur le Dashboard des Capteurs",
            font=("Arial", 24), bg="white", fg="black"
        )
        title_label.pack(pady=20)

        description_label = tk.Label(
            self.current_frame,
            text="Utilisez la barre latérale pour naviguer entre les différentes pages.",
            font=("Arial", 14), bg="white", fg="gray"
        )
        description_label.pack(pady=10)

    def show_display_menu(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        display_label = tk.Label(
            self.current_frame, text="Menu d'Affichage", font=("Arial", 18), bg="white", fg="black"
        )
        display_label.pack(pady=10)

        buttons = [
            ("Graphique - Temperature", lambda: self.show_graph_page("temperature", "Temperature (C)", "red")),
            ("Graphique - Humidite", lambda: self.show_graph_page("humidity", "Humidite (%)", "blue")),
            ("Graphique - Lumiere", lambda: self.show_graph_page("light", "Intensite lumineuse", "orange")),
            ("Graphique - Eau", lambda: self.show_graph_page("water", "Detection d'eau", "green")),
            ("4 Graphes separes", self.show_four_graphs_page),
            ("Graphique combine", self.show_combined_graph_page),
            ("Tableau CSV", self.show_csv_page),
        ]

        for text, command in buttons:
            button = tk.Button(
                self.current_frame, text=text, font=("Arial", 12), bg="black", fg="white",
                activebackground="red", activeforeground="white", command=command
            )
            button.pack(fill=tk.X, pady=5, padx=10)

    def show_graph_page(self, column, ylabel, color):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        if self.data is None or column not in self.data.columns:
            messagebox.showerror("Erreur", f"Les donnees pour {ylabel} ne sont pas disponibles.")
            return

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self.data[column], label=ylabel, color=color)
        ax.set_title(ylabel)
        ax.set_xlabel("Echantillons")
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=self.current_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def show_four_graphs_page(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        if self.data is None:
            messagebox.showerror("Erreur", "Aucune donnee n'est chargee.")
            return

        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        graphs = [
            ("temperature", "Temperature (C)", "red"),
            ("humidity", "Humidite (%)", "blue"),
            ("light", "Intensite lumineuse", "orange"),
            ("water", "Detection d'eau", "green"),
        ]

        for i, (column, ylabel, color) in enumerate(graphs):
            row, col = divmod(i, 2)
            if column in self.data.columns:
                axs[row, col].plot(self.data[column], label=ylabel, color=color)
                axs[row, col].set_title(ylabel)
                axs[row, col].grid(True, linestyle="--", alpha=0.7)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.current_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def show_combined_graph_page(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        if self.data is None:
            messagebox.showerror("Erreur", "Aucune donnee n'est chargee.")
            return

        fig, ax = plt.subplots(figsize=(10, 5))
        graphs = [
            ("temperature", "Temperature", "red"),
            ("humidity", "Humidite", "blue"),
            ("light", "Intensite lumineuse", "orange"),
            ("water", "Detection d'eau", "green"),
        ]

        for column, label, color in graphs:
            if column in self.data.columns:
                ax.plot(self.data[column], label=label, color=color)

        ax.set_title("Graphique combine")
        ax.set_xlabel("Echantillons")
        ax.set_ylabel("Valeurs")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=self.current_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def show_csv_page(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        load_button = tk.Button(
            self.current_frame, text="Charger un fichier CSV", font=("Arial", 12),
            bg="blue", fg="white", command=self.load_csv
        )
        load_button.pack(pady=10)

        self.tree = ttk.Treeview(self.current_frame, columns=("temperature", "humidity", "light", "water"), show="headings")
        self.tree.heading("temperature", text="Temperature (C)")
        self.tree.heading("humidity", text="Humidite (%)")
        self.tree.heading("light", text="Intensite lumineuse")
        self.tree.heading("water", text="Detection d'eau")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if not file_path:
            return

        try:
            self.data = pd.read_csv(file_path)
            self.update_table()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier CSV : {e}")

    def update_table(self):
        if self.data is None:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in self.data.iterrows():
            self.tree.insert("", tk.END, values=(row["temperature"], row["humidity"], row["light"], row["water"]))

    def show_support_page(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(self.current_frame, text="Support - Formulaire de contact", font=("Arial", 18), bg="white", fg="black")
        label.pack(pady=20)

        form_frame = tk.Frame(self.current_frame, bg="white")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nom :", bg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(form_frame, text="Email :", bg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(form_frame, text="Message :", bg="white", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="nw")

        name_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        email_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        message_entry = tk.Text(form_frame, font=("Arial", 12), width=40, height=5)

        name_entry.grid(row=0, column=1, pady=5)
        email_entry.grid(row=1, column=1, pady=5)
        message_entry.grid(row=2, column=1, pady=5)

        submit_button = tk.Button(
            self.current_frame, text="Envoyer", font=("Arial", 12), bg="blue", fg="white",
            command=lambda: messagebox.showinfo("Support", "Message envoye avec succes !")
        )
        submit_button.pack(pady=10)

    def show_manual_page(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        manual_text = """Ce tableau de bord vous permet :
        - D'afficher des graphiques des donnees de capteurs.
        - De charger des fichiers CSV.
        - D'explorer les donnees via des graphiques combines et separes.
        
        Navigation :
        - Utilisez la barre laterale pour acceder aux fonctionnalites.
        - Consultez \"Support\" pour des questions ou problemes.
        """
        label = tk.Label(self.current_frame, text="Manuel d'Utilisation", font=("Arial", 18), bg="white", fg="black")
        label.pack(pady=20)

        text_box = tk.Text(self.current_frame, font=("Arial", 12), wrap="word", bg="white", fg="black")
        text_box.insert("1.0", manual_text)
        text_box.configure(state="disabled")
        text_box.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def show_about_page(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        about_text = """Dashboard - Capteurs
        Version : 1.0
        Developpe par : Layla Kaddani
        Contact : ESTO.kaddani@ump.ac.ma

        Ce tableau de bord a ete concu pour afficher et analyser les donnees de capteurs 
        tels que la temperature, l'humidite, la lumiere, et l'eau.
        Merci d'utiliser notre application !
        """
        label = tk.Label(self.current_frame, text="À propos de ce Dashboard", font=("Arial", 18), bg="white", fg="black")
        label.pack(pady=20)

        text_box = tk.Text(self.current_frame, font=("Arial", 12), wrap="word", bg="white", fg="black")
        text_box.insert("1.0", about_text)
        text_box.configure(state="disabled")
        text_box.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def quit_app(self):
      self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
             
