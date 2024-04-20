import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import random
import yaml
import sys, os

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(base_dir, "config.yml")

# ---------- Configurations ----------
# API URLs
cat_api_url = "https://api.thecatapi.com/v1/images/search"
dog_api_url = "https://api.thedogapi.com/v1/images/search"
fox_api_url = "https://randomfox.ca/floof"
duck_api_url = "https://random-d.uk/api/v2/random"

# Desired image size
desired_img_size = (500, 500)

# default image
with open(config_path, "r") as file:
    data = yaml.safe_load(file)

default_img = data["default img"]
# -----------------------------------

def create_window():
    window = tk.Tk()
    window.title("Cat Generator")
    window.geometry("820x600")
    window.resizable(False, False)
    window.configure(bg="black")

    # ---------- Menu functions ----------

    title = None
    api_url = None
    api_desc = None
    api_docs = None
    api_web = None

    def create_API_settings_window(animal):
        global title, api_url, api_desc, api_docs, api_web

        API_window = tk.Toplevel(window)
        API_window.title("API Settings")
        API_window.geometry("310x180")
        API_window.resizable(False, False)

        title = tk.Label(API_window, text="", font=("Arial", 20))
        api_url = tk.Label(API_window, text="")
        api_desc = tk.Label(API_window, text="")
        api_docs = tk.Label(API_window, text="")
        api_web = tk.Label(API_window, text="")

        title.place(relx=0.5, anchor='n')
        api_url.place(x=10, y=40)
        api_desc.place(x=10, y=70)
        api_docs.place(x=10, y=100)
        api_web.place(x=10, y=130)

        _API_settings_config(animal)

        API_window.mainloop()

    def _API_settings_config(animal):
        global title, api_url, api_desc, api_docs, api_web

        if animal == "cat":
            title.configure(text="Cat API")
            api_url.configure(text=f"API URL: {cat_api_url}")
            api_desc.configure(text="Description: The Cat API provides random cat images.")
            api_docs.configure(text="API Documentation: https://docs.thecatapi.com/")
            api_web.configure(text="API Website: https://thecatapi.com/")
        elif animal == "dog":
            title.configure(text="Dog API")
            api_url.configure(text=f"API URL: {dog_api_url}")
            api_desc.configure(text="Description: The Dog API provides random dog images.")
            api_docs.configure(text="API Documentation: https://thedogapi.com/")
            api_web.configure(text="API Website: https://thedogapi.com/")
        elif animal == "fox":
            title.configure(text="Fox API")
            api_url.configure(text=f"API URL: {fox_api_url}")
            api_desc.configure(text="Description: The Fox API provides random fox images.")
            api_docs.configure(text="API Documentation: https://randomfox.ca/")
            api_web.configure(text="API Website: https://randomfox.ca/")
        elif animal == "duck":
            title.configure(text="Duck API")
            api_url.configure(text=f"API URL: {duck_api_url}")
            api_desc.configure(text="Description: The Duck API provides random duck images.")
            api_docs.configure(text="API Documentation: https://duckapi.com/")
            api_web.configure(text="API Website: https://duckapi.com/")

    def _save_default_img(choise):
        with open(config_path, "r") as file:
            data = yaml.safe_load(file)

        data["default img"] = str(choise)

        with open(config_path, "w") as file:
            yaml.dump(data, file)

    # ---------- Menu Creation ----------

    # creating menu
    menu = tk.Menu(window)
    # adding menu to window
    window.config(menu=menu)
    # creating "settings" tab in menu
    settings = tk.Menu(menu)
    # adding "settings" tab to menu
    menu.add_cascade(label="Settings", menu=settings)

    # creating "API settings" tab in "settings" tab
    API_settings = tk.Menu(settings)
    API_settings.add_command(label="Cat API info", command=lambda: create_API_settings_window("cat"))
    API_settings.add_command(label="Dog API info", command=lambda: create_API_settings_window("dog"))
    API_settings.add_command(label="Fox API info", command=lambda: create_API_settings_window("fox"))
    API_settings.add_command(label="Duck API info", command=lambda: create_API_settings_window("duck"))



    # adding "API settings" tab to "settings" tab
    settings.add_cascade(label="API Settings", menu=API_settings)

    # creating "Image settings" tab in "settings" tab
    Image_settings = tk.Menu(settings)

    # creating "Default Image" tab in "Image settings" tab
    default_img_setting = tk.Menu(Image_settings)
    default_img_setting.add_command(label="Cat", command=lambda: _save_default_img("cat"))
    default_img_setting.add_command(label="Dog", command=lambda: _save_default_img("dog"))
    default_img_setting.add_command(label="Fox", command=lambda: _save_default_img("fox"))
    default_img_setting.add_command(label="Duck", command=lambda: _save_default_img("duck"))

    # adding "Default Image" tab to "Image settings" tab
    Image_settings.add_cascade(label="Default Image", menu=default_img_setting)

    # adding "Image settings" tab to "settings" tab
    settings.add_cascade(label="Image Settings", menu=Image_settings)



    canvas = tk.Canvas(window, width=desired_img_size[0], height=desired_img_size[1], highlightthickness=0)
    canvas.place(x=50, y=50)

    def generate_cat():
        response = requests.get(cat_api_url)
        data = response.json()
        cat_url = data[0]["url"]

        response = requests.get(cat_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        img = img.resize(desired_img_size, Image.LANCZOS)

        global photo
        photo = ImageTk.PhotoImage(img)

        canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    def generate_dog():
        response = requests.get(dog_api_url)
        data = response.json()
        dog_url = data[0]["url"]

        response = requests.get(dog_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        img = img.resize(desired_img_size, Image.LANCZOS)

        global photo
        photo = ImageTk.PhotoImage(img)

        canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    def generate_fox():
        response = requests.get(fox_api_url)
        data = response.json()
        fox_url = data["image"]

        response = requests.get(fox_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        img = img.resize(desired_img_size, Image.LANCZOS)

        global photo
        photo = ImageTk.PhotoImage(img)

        canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    def generate_duck():
        response = requests.get(duck_api_url)
        data = response.json()
        duck_url = data["url"]

        response = requests.get(duck_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        img = img.resize(desired_img_size, Image.LANCZOS)

        global photo
        photo = ImageTk.PhotoImage(img)

        canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    def generate_random():
        choise = random.choice([cat_api_url, dog_api_url, fox_api_url, duck_api_url])
        response = requests.get(choise)
        data = response.json()
        if choise == fox_api_url:
            url = data["image"]
        elif choise == duck_api_url:
            url = data["url"]
        else:
            url = data[0]["url"]

        response = requests.get(url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        
        img = img.resize(desired_img_size, Image.LANCZOS)

        global photo
        photo = ImageTk.PhotoImage(img)

        canvas.create_image(0, 0, image=photo, anchor=tk.NW)

        
    if default_img == "cat":
        generate_cat()
    elif default_img == "dog":
        generate_dog()
    elif default_img == "fox":
        generate_fox()
    elif default_img == "duck":
        generate_duck()

    # button event functions
    def on_enter_cat(e):
        Cat_button["bg"] = "red"

    def on_leave_cat(e):
        Cat_button["bg"] = "cyan"

    def on_enter_dog(e):
        Dog_button["bg"] = "red"

    def on_leave_dog(e):
        Dog_button["bg"] = "green"

    def on_enter_fox(e):
        Fox_button["bg"] = "red"

    def on_leave_fox(e):
        Fox_button["bg"] = "orange"

    def on_enter_duck(e):
        Duck_button["bg"] = "red"
    
    def on_leave_duck(e):
        Duck_button["bg"] = "yellow"

    def on_enter_random(e):
        Random_button["bg"] = "red"

    def on_leave_random(e):
        Random_button["bg"] = "blue"


    Cat_button = tk.Button(
        window, 
        text="Generate a Cat", 
        bg="cyan", 
        fg="black", 
        height=2, 
        width=14, 
        activebackground="gray", 
        activeforeground="white",
        font=("Arial", 20),
        command=generate_cat
    )

    Dog_button = tk.Button(
        window, 
        text="Generate a Dog", 
        bg="green", 
        fg="black", 
        height=2, 
        width=14, 
        activebackground="gray", 
        activeforeground="white",
        font=("Arial", 20),
        command=generate_dog
    )

    Fox_button = tk.Button(
        window, 
        text="Generate a Fox", 
        bg="orange", 
        fg="black", 
        height=2, 
        width=14, 
        activebackground="gray", 
        activeforeground="white",
        font=("Arial", 20),
        command=generate_fox
    )

    Duck_button = tk.Button(
        window, 
        text="Generate a Duck", 
        bg="yellow", 
        fg="black", 
        height=2, 
        width=14, 
        activebackground="gray", 
        activeforeground="white",
        font=("Arial", 20),
        command=generate_duck
    )

    Random_button = tk.Button(
        window,
        text="Generate Random",
        bg="blue",
        fg="black",
        height=2,
        width=14,
        activebackground="gray",
        activeforeground="white",
        font=("Arial", 20),
        command=generate_random
    )


    # event handling
    Cat_button.bind("<Enter>", on_enter_cat)
    Cat_button.bind("<Leave>", on_leave_cat)

    Dog_button.bind("<Enter>", on_enter_dog)
    Dog_button.bind("<Leave>", on_leave_dog)

    Fox_button.bind("<Enter>", on_enter_fox)
    Fox_button.bind("<Leave>", on_leave_fox)

    Duck_button.bind("<Enter>", on_enter_duck)
    Duck_button.bind("<Leave>", on_leave_duck)

    Random_button.bind("<Enter>", on_enter_random)
    Random_button.bind("<Leave>", on_leave_random)


    Cat_button.place(x=570, y=50)
    Dog_button.place(x=570, y=150)
    Fox_button.place(x=570, y=250)
    Duck_button.place(x=570, y=350)
    Random_button.place(x=570, y=450)

    window.mainloop()

create_window()