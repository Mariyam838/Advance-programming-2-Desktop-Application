#MealDB Explorer Application
#A comprehensive GUI application for exploring recipes using TheMealDB API.
#Features include searching meals by name, ingredients, categories, and region,
# with detailed information display and image support.

#Import requires Libraries
from tkinter import * # Import the Tkinter basic widgets
from tkinter import ttk # Import the Tkinter themed widgets
import tkinter as tk # Import the Tkinter with namespace
from PIL import Image, ImageTk # Import the PIL library for image processing
import requests # Import the requests library for API calls
from io import BytesIO # Import the BytesIO library for image data
from tkinter import messagebox  # Import the messagebox library for displaying messages

class MealDBExplorer:
    # Main application class for the MealDB Explorer.
    # Handles all GUI and API interactions.

    def __init__(self):
        #Initialize the main application window and setup components.
        # Create the main application window
        self.root = Tk()
        # Initialize color scheme
        self.initialize_colors()
        # Set up the main window properties
        self.setup_main_window()
        # Create the welcome search frame
        self.create_welcome_screen()
        #Initialize tab system
        self.setup_tabs()
        #Configure visual styles
        self.configure_styles()

    def initialize_colors(self):
        #Initialize the color scheme for the application.
        self.colors = {
            'primary': '#1A1A2E',     # Dark blue-black 
            'secondary': '#16213E',    # Dark blue 
            'accent': '#0F3460',       # Deep blue 
            'highlight': '#E94560',    # Coral pink 
            'text': '#FFFFFF',         # White for text
            'text_secondary': '#B2B2B2', # Light gray 
            'button': '#E94560',       # Coral pink 
            'button_hover': '#D63655', # Darker coral 
        }
        
    def setup_main_window(self):
        #Configure the main application window and background.
        # Set window title
        self.root.title("Food Fiesta")
        self.root.geometry("900x700")
        # Disable resizing
        self.root.resizable(0, 0)
        self.root.configure(bg=self.colors['primary'])
        
        # Create gradient background
        self.canvas = Canvas(self.root, width=900, height=700, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(0, 0, 900, 700, 
                                   fill=self.colors['primary'],
                                   outline="")
        
    
    def create_welcome_screen(self):
        #Create the welcome screen with a background image and modern styling.
        # Uses a dark overlay to ensure text readability over the background image.

    # Create the main welcome frame
        self.welcome_frame = Frame(self.root)
        self.welcome_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        try:
        # Load and process background image
            image_path = "Bg img.jpg"  # Replace with your image path
            bg_image = Image.open(image_path)
        
        # Calculate proper image scaling to fill the window
            window_ratio = 900/700 #width/height
            image_ratio = bg_image.width/bg_image.height
        # Determine the scaling factor 
            if window_ratio > image_ratio:
                new_width = 900
                new_height = int(900/image_ratio)
            else:
                new_height = 700
                new_width = int(700*image_ratio)
            # Resize the image
            bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a darkened version of the image for better text visibility
            overlay = Image.new('RGBA', bg_image.size, (26, 26, 46, 180))  # Image transparency
            bg_image = Image.alpha_composite(bg_image.convert('RGBA'), overlay)
            # Convert image to PhotoImage for Tkinter
            self.bg_photo = ImageTk.PhotoImage(bg_image)
        
        # Create canvas for background
            self.bg_canvas = Canvas(self.welcome_frame, width=900, height=700, highlightthickness=0)
            self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Add the darkened image to canvas
            self.bg_canvas.create_image(450, 350, image=self.bg_photo)

        except Exception as e:
            messagebox.showerror("Error", f"Error loading background image: {e}")
            # Fallback to solid color if image loading fails
            self.welcome_frame.configure(bg=self.colors['primary'])

    # Create content frame for welcome screen elements
        content_frame = Frame(self.welcome_frame, bg=self.colors['primary'])
        content_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Welcome title with custom font and styling
        title = Label(content_frame,
                 text="Welcome to Foodie Fiesta!",
                 font=("Helvetica", 32, "bold"),
                 fg=self.colors['highlight'],
                 bg=self.colors['primary'])
        title.pack(pady=20)

    # Subtitle with description , custom font and styling
        subtitle = Label(content_frame,
                    text="Discover delicious recipes from around the world!",
                    font=("Helvetica", 16),
                    fg=self.colors['text'],
                    bg=self.colors['primary'])
        subtitle.pack(pady=10)

    # Modern styled start button
        start_button = self.create_button(content_frame,
                                    "Start Exploring",
                                    self.start_exploration)
        start_button.pack(pady=30)

    def configure_styles(self):
        #Configure the visual styles for the application.
        #Set up themed styles for notebook tabs and scrollbars.

        # Configure notebook tabs
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure notebook (tab) styling
        self.style.configure("TNotebook",
                           background=self.colors['primary'],
                           borderwidth=0)
        
        self.style.configure("TNotebook.Tab",
                           font=("Helvetica", 12),
                           padding=[15, 10],
                           background=self.colors['secondary'],
                           foreground=self.colors['text'])
        
        self.style.map("TNotebook.Tab",
                      background=[("selected", self.colors['accent'])],
                      foreground=[("selected", self.colors['text'])])

        # Configure scrollbar styling
        self.style.configure("Custom.Vertical.TScrollbar",
                           background=self.colors['accent'],
                           bordercolor=self.colors['accent'],
                           arrowcolor=self.colors['text'],
                           troughcolor=self.colors['primary'])

    def setup_tabs(self):
        #Create and initialize all application tabs.
        #Each tab is a separate frame that contains the content for that tab.

        # Create notebook with tabs
        self.tab_control = ttk.Notebook(self.root)
        
        # Create individual tab frames
        self.meal_tab = Frame(self.tab_control, bg="#1e3c72")
        self.ingredients_tab = Frame(self.tab_control, bg="#1e3c72")
        self.categories_tab = Frame(self.tab_control, bg="#1e3c72")
        self.random_tab = Frame(self.tab_control, bg="#1e3c72")
        self.area_tab = Frame(self.tab_control, bg="#1e3c72")
        
        # Add tabs to notebook with labels
        self.tab_control.add(self.meal_tab, text="Search Meal")
        self.tab_control.add(self.ingredients_tab, text="Search by Ingredients")
        self.tab_control.add(self.categories_tab, text="Meal Categories")
        self.tab_control.add(self.random_tab, text="Random Meal")
        self.tab_control.add(self.area_tab, text="Filter by Area")

    def create_button(self, parent, text, command):
        #Create a modern styled button with hover effects.
        button = Button(parent,
                       text=text,
                       font=("Helvetica", 12, "bold"),
                       bg=self.colors['button'],
                       fg=self.colors['text'],
                       activebackground=self.colors['button_hover'],
                       activeforeground=self.colors['text'],
                       relief="flat",
                       command=command,
                       padx=20,
                       pady=10,
                       cursor="hand2")

        # Add hover effects
        button.bind("<Enter>", lambda e: button.config(
            background=self.colors['button_hover']))
        button.bind("<Leave>", lambda e: button.config(
            background=self.colors['button']))

        return button

    def fetch_and_display_meal(self, meal_id):
        """Fetch and display details for a specific meal by ID.
        Args:
            meal_id: The unique identifier of the meal to fetch.
        """
        # Fetch meal details from API
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
        try:
            # Send GET request to API
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            meal = data.get("meals", [])
            
            # Display meal details
            if meal:
                self.display_meal_details(meal[0])
            else:
                print("Meal not found")
                
        except Exception as e:
            messagebox.showerror(f"Error fetching meal details: {e}")

    def setup_search_tab(self):
        #Set up the meal search tab with search functionality.
        #Create search input field and results display area.

        # Search input field (Header label)
        Label(self.meal_tab,
              text="Enter Meal Name to see details",
              font=("Helvetica", 18, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=20)

        # Create search entry field
        self.meal_entry = Entry(self.meal_tab,
                              font=("Helvetica", 16),
                              width=30,
                              justify=CENTER)
        self.meal_entry.pack(pady=10)

        # Create search button
        self.create_button(self.meal_tab,
                          "Search Meal",
                          self.search_meal).pack(pady=10)

        # Create display area for search results
        self.meal_frame = Frame(self.meal_tab, bg="#1e3c72")
        self.meal_frame.pack(fill=BOTH, expand=True, pady=10)

        # Create placeholders for meal image and details
        self.meal_image_placeholder = Label(self.meal_frame, bg="#1e3c72")
        self.meal_image_placeholder.pack(side=LEFT, padx=20)

        self.meal_placeholder = Label(self.meal_frame,
                                    text="",
                                    font=("Helvetica", 14),
                                    bg="#1e3c72",
                                    fg="white",
                                    width=50,
                                    height=25,
                                    wraplength=400,
                                    relief="groove",
                                    bd=2,
                                    anchor="nw",
                                    justify="left")
        self.meal_placeholder.pack(side=LEFT, padx=20)

    def setup_ingredients_tab(self):
        #Set up the ingredients search tab.
        #Create search functionality for ingredients.
        Label(self.ingredients_tab,
              text="Enter an Ingredient to see meals",
              font=("Helvetica", 18, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=20)

        # Create search entry field
        self.ingredient_entry = Entry(self.ingredients_tab,
                                    font=("Helvetica", 16),
                                    width=30,
                                    justify=CENTER)
        self.ingredient_entry.pack(pady=10)
        # Create search button
        self.create_button(self.ingredients_tab,
                          "Search by Ingredient",
                          self.search_by_ingredient).pack(pady=10)
        # Create display area for search results
        self.ingredients_placeholder = Frame(self.ingredients_tab,
                                          bg="#1e3c72",
                                          relief="groove",
                                          bd=2)
        self.ingredients_placeholder.pack(fill=BOTH, expand=True, pady=20)

    def setup_categories_tab(self):
        #Set up the meal categories tab.
        Label(self.categories_tab,
              text="Explore Meal Categories",
              font=("Helvetica", 18, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=20)

        self.create_button(self.categories_tab,
                          "Fetch Categories",
                          self.fetch_categories).pack(pady=10)

        self.categories_placeholder = Frame(self.categories_tab,
                                         bg="#1e3c72",
                                         relief="groove",
                                         bd=2)
        self.categories_placeholder.pack(fill=BOTH, expand=True, pady=20)

    def setup_random_tab(self):
        #Set up the random meal tab.
        Label(self.random_tab,
              text="Discover a Random Meal!",
              font=("Helvetica", 18, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=20)

        self.create_button(self.random_tab,
                          "Get Random Meal",
                          self.show_random_meal).pack(pady=10)

        self.random_frame = Frame(self.random_tab, bg="#1e3c72")
        self.random_frame.pack(fill=BOTH, expand=True, pady=10)

        self.random_image_placeholder = Label(self.random_frame, bg="#1e3c72")
        self.random_image_placeholder.pack(side=LEFT, padx=20)

        self.random_placeholder = Label(self.random_frame,
                                      text="",
                                      font=("Helvetica", 14),
                                      bg="#1e3c72",
                                      fg="white",
                                      width=50,
                                      height=25,
                                      wraplength=400,
                                      relief="groove",
                                      bd=2,
                                      anchor="nw",
                                      justify="left")
        self.random_placeholder.pack(side=LEFT, padx=20)

    def setup_area_tab(self):
        #Set up the area filter tab.
        Label(self.area_tab,
              text="Enter Area to see meals",
              font=("Helvetica", 18, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=20)

        self.area_entry = Entry(self.area_tab,
                              font=("Helvetica", 16),
                              width=30,
                              justify=CENTER)
        self.area_entry.pack(pady=10)

        self.create_button(self.area_tab,
                          "Search by Area",
                          self.fetch_meals_by_area).pack(pady=10)

        self.area_placeholder = Frame(self.area_tab,
                                    bg="#1e3c72",
                                    relief="groove",
                                    bd=2)
        self.area_placeholder.pack(fill=BOTH, expand=True, pady=20)

    def start_exploration(self):
        #Transition from welcome screen to main application.
        # Destroys the welcome screen and shows the main application tabs.
        self.welcome_frame.destroy()
        # Position and size the tab control
        self.tab_control.place(x=20, y=20, width=860, height=660)
        # Initialize all tab contents
        self.setup_search_tab()
        self.setup_ingredients_tab()
        self.setup_categories_tab()
        self.setup_random_tab()
        self.setup_area_tab()

    def fetch_meal_data(self, url, name_input=None):
        #Fetch meal data from the API.
        try:
            # Send a GET request to the API
            if name_input:
                url = f"{url}?s={name_input.strip()}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("meals", [])
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")
            return None
        
    def display_meal_details(self, meal_data):
        #Display detailed meal information in a new window.
        # The window will contain the meal name, ingredients, and instructions.

        # Create new window for meal details.
        details_window = Toplevel(self.root)
        details_window.title(meal_data["strMeal"])
        details_window.geometry("800x600")
        details_window.configure(bg="#1e3c72")

        # Create scrollable canvas for content
        canvas = Canvas(details_window, bg="#1e3c72")
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#1e3c72")

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_frame.bind("<Configure>",
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Display meal title
        Label(scrollable_frame,
              text=meal_data["strMeal"],
              font=("Helvetica", 24, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=20)

        # load and display meal image
        try:
            response = requests.get(meal_data["strMealThumb"])
            img = Image.open(BytesIO(response.content))
            img = img.resize((300, 300))
            photo = ImageTk.PhotoImage(img)
            img_label = Label(scrollable_frame, image=photo, bg="#1e3c72")
            img_label.image = photo
            img_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror(f"Error loading image: {e}")

        # Display category and area
        info_frame = Frame(scrollable_frame, bg="#1e3c72")
        info_frame.pack(pady=10)
        
        Label(info_frame,
              text=f"Category: {meal_data.get('strCategory', 'Unknown')}",
              font=("Helvetica", 14),
              fg="white",
              bg="#1e3c72").pack(side=LEFT, padx=10)
        
        Label(info_frame,
              text=f"Area: {meal_data.get('strArea', 'Unknown')}",
              font=("Helvetica", 14),
              fg="white",
              bg="#1e3c72").pack(side=LEFT, padx=10)

        # Display ingredients section
        Label(scrollable_frame,
              text="Ingredients:",
              font=("Helvetica", 16, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=(20, 10))

        ingredients_frame = Frame(scrollable_frame, bg="#1e3c72")
        ingredients_frame.pack()
        # Display ingredients and measurements
        for i in range(1, 21):
            ingredient = meal_data.get(f"strIngredient{i}")
            measure = meal_data.get(f"strMeasure{i}")
            if ingredient and ingredient.strip():
                Label(ingredients_frame,
                      text=f"• {measure} {ingredient}",
                      font=("Helvetica", 12),
                      fg="white",
                      bg="#1e3c72").pack(anchor="w")

        # Display cooking instructions
        Label(scrollable_frame,
              text="Instructions:",
              font=("Helvetica", 16, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=(20, 10))

        Label(scrollable_frame,
              text=meal_data.get("strInstructions"),
              font=("Helvetica", 12),
              fg="white",
              bg="#1e3c72",
              wraplength=700,
              justify=LEFT).pack(padx=20, pady=10)

    def search_meal(self):
        #Handle meal search functionality.
        meal_name = self.meal_entry.get().strip()
        if meal_name:
            meals = self.fetch_meal_data("https://www.themealdb.com/api/json/v1/1/search.php", meal_name)
            if meals:
                self.display_meal_details(meals[0])
            else:
                messagebox.showerror("No meal found", "Please try again.")

    def search_by_ingredient(self):
        #Handle ingredient search functionality.
        ingredient = self.ingredient_entry.get().strip()
        if ingredient:
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                meals = data.get("meals")
                
                # Clear existing results
                for widget in self.ingredients_placeholder.winfo_children():
                    widget.destroy()
                # Handle the case where no meals are found for the ingredient
                if not meals:
                    messagebox.showinfo("No Results", f"No meals found with ingredient: {ingredient}")
                    return
                # Create scrollable frame for results
                canvas = Canvas(self.ingredients_placeholder, bg="#1e3c72")
                scrollbar = ttk.Scrollbar(self.ingredients_placeholder, orient="vertical", command=canvas.yview)
                scrollable_frame = Frame(canvas, bg="#1e3c72")

                canvas.configure(yscrollcommand=scrollbar.set)
                scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

                # Display meal buttons
                for meal in meals:
                    meal_frame = Frame(scrollable_frame, bg="#1e3c72")
                    meal_frame.pack(fill=X, pady=5, padx=10)

                    try:
                        # Load and display meal thumbnail
                        response = requests.get(meal["strMealThumb"]) # Load the image from the URL
                        img = Image.open(BytesIO(response.content)) # Open the image file
                        img = img.resize((50, 50)) # Resize the image to 50x50 pixels
                        photo = ImageTk.PhotoImage(img) # Convert the image to a PhotoImage object
                        img_label = Label(meal_frame, image=photo, bg="#1e3c72") # Create a Label widget with the image
                        img_label.image = photo # Keep a reference to the image to prevent it from being garbage collected
                        img_label.pack(side=LEFT, padx=5) # Pack the image label to the left of the meal frame
                    except Exception as e:
                        print(f"Error loading thumbnail: {e}")  
                        messagebox.showerror("Error", f"Error loading thumbnail: {e}")

                    button = Button(meal_frame,
                                  text=meal["strMeal"],
                                  font=("Helvetica", 12),
                                  bg="#4e8ccf",
                                  fg="white",
                                  command=lambda id=meal["idMeal"]: self.fetch_and_display_meal(id))
                    button.pack(side=LEFT, fill=X, expand=True, padx=5)

                scrollbar.pack(side=RIGHT, fill=Y)
                canvas.pack(side=LEFT, fill=BOTH, expand=True)

            except Exception as e:
                # Handle any exceptions by clearing the placeholder and displaying an error message.
                for widget in self.ingredients_placeholder.winfo_children():
                    widget.destroy()
                Label(self.ingredients_placeholder,
                      text=f"Error: {e}",
                      font=("Helvetica", 16),
                      fg="white",
                      bg="#1e3c72").pack(pady=10)
        else:
            # If no ingredients was entered , display a message enter an ingredient.
            messagebox.showwarning("Input Required", "Please enter an ingredient.")

    def fetch_categories(self):
        #Fetch and display meal categories.
        url = "https://www.themealdb.com/api/json/v1/1/categories.php"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            categories = data.get("categories")
            
            # Clear existing results
            for widget in self.categories_placeholder.winfo_children():
                widget.destroy()

            if not categories: # If no categories were found.
                # Display a message indicating that no categories were found.
                Label(self.categories_placeholder,
                      text="No categories found.",
                      font=("Helvetica", 16),
                      fg="white",
                      bg="#1e3c72").pack(pady=10)
                return

            # Create scrollable frame for categories
            canvas = Canvas(self.categories_placeholder, bg="#1e3c72")
            scrollbar = ttk.Scrollbar(self.categories_placeholder, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg="#1e3c72")

            canvas.configure(yscrollcommand=scrollbar.set)
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            # Display categories in a grid layout.
            row = 0 # Row counter
            col = 0 # Column counter
            for category in categories:
                category_frame = Frame(scrollable_frame, bg="#1e3c72", padx=10, pady=10)
                category_frame.grid(row=row, column=col, sticky="nsew")

                try:
                    # Load and display category thumbnail
                    response = requests.get(category["strCategoryThumb"])
                    img = Image.open(BytesIO(response.content))
                    img = img.resize((100, 100))
                    photo = ImageTk.PhotoImage(img)
                    img_label = Label(category_frame, image=photo, bg="#1e3c72")
                    img_label.image = photo
                    img_label.pack()
                except Exception as e:
                    print(f"Error loading category thumbnail: {e}") 
                    messagebox.showerror("Error", f"Error loading category thumbnail: {e}")
                Label(category_frame,
                      text=category["strCategory"],
                      font=("Helvetica", 12, "bold"),
                      fg="white",
                      bg="#1e3c72").pack(pady=5)

                button = Button(category_frame,
                              text="View Meals",
                              font=("Helvetica", 10),
                              bg="#4e8ccf",
                              fg="white",
                              command=lambda cat=category["strCategory"]: self.fetch_meals_by_category(cat))
                button.pack() # Pack the button into the frame.

                col += 1 # Move to the next column.
                if col > 5:  # Limit columns to 5 per row.
                    col = 0 # Reset to the first column.
                    row += 1 # Move to the next row

            scrollbar.pack(side=RIGHT, fill=Y)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)

        except Exception as e:
            for widget in self.categories_placeholder.winfo_children():
                widget.destroy()
            Label(self.categories_placeholder,
                  text=f"Error: {e}",
                  font=("Helvetica", 16),
                  fg="white",
                  bg="#1e3c72").pack(pady=10)

    def fetch_meals_by_category(self, category):
        #Fetch and display meals for a specific category.
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            meals = data.get("meals", [])
            
            if meals: # If meals exist, create a new window to display them.
                category_window = Toplevel(self.root) # Create a new window.
                category_window.title(f"{category} Meals") # Set the window title.
                category_window.geometry("600x800") # Set the window size.
                category_window.configure(bg="#1e3c72")

                # Create scrollable frame
                canvas = Canvas(category_window, bg="#1e3c72")
                scrollbar = ttk.Scrollbar(category_window, orient="vertical", command=canvas.yview)
                scrollable_frame = Frame(canvas, bg="#1e3c72")

                canvas.configure(yscrollcommand=scrollbar.set)
                scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

                Label(scrollable_frame,
                      text=f"{category} Meals",
                      font=("Helvetica", 20, "bold"),
                      fg="white",
                      bg="#1e3c72").pack(pady=20)

                for meal in meals:
                    meal_frame = Frame(scrollable_frame, bg="#1e3c72")
                    meal_frame.pack(fill=X, pady=5, padx=10)

                    try:
                        response = requests.get(meal["strMealThumb"])
                        img = Image.open(BytesIO(response.content))
                        img = img.resize((50, 50))
                        photo = ImageTk.PhotoImage(img)
                        img_label = Label(meal_frame, image=photo, bg="#1e3c72")
                        img_label.image = photo
                        img_label.pack(side=LEFT, padx=5)
                    except Exception as e:
                        print(f"Error loading meal thumbnail: {e}")

                    button = Button(meal_frame,
                                  text=meal["strMeal"],
                                  font=("Helvetica", 12),
                                  bg="#4e8ccf",
                                  fg="white",
                                  command=lambda id=meal["idMeal"]: self.fetch_and_display_meal(id))
                    button.pack(side=LEFT, fill=X, expand=True, padx=5)

                scrollbar.pack(side=RIGHT, fill=Y)
                canvas.pack(side=LEFT, fill=BOTH, expand=True)

        except Exception as e:
            print(f"Error loading meal thumbnail: {e}")  
            messagebox.showerror("Error", f"Error loading meal thumbnail: {e}")

    def show_random_meal(self):
        #Fetch and display a random meal.
        url = "https://www.themealdb.com/api/json/v1/1/random.php"
        meals = self.fetch_meal_data(url) # Fetch meal data from API
        if meals:
            self.display_meal_details(meals[0]) # Display meal details random meals
        else:
            messagebox.showinfo("No Result", "Error fetching random meal. Please try again.")

    def setup_area_tab(self):
        #Set up the area filter tab with clickable area buttons.
        Label(self.area_tab,
              text="Select an Area to see meals",
              font=("Helvetica", 18, "bold"),
              fg="white",
              bg="#1e3c72").pack(pady=20)

        self.create_button(self.area_tab,
                          "Load Areas",
                          self.fetch_areas).pack(pady=10)

        self.area_placeholder = Frame(self.area_tab,
                                    bg="#1e3c72",
                                    relief="groove",
                                    bd=2)
        self.area_placeholder.pack(fill=BOTH, expand=True, pady=20)

    def fetch_areas(self):
        #Fetch and display all available areas as clickable buttons.
        url = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            areas = data.get("meals", [])

            # Clear existing content
            for widget in self.area_placeholder.winfo_children():
                widget.destroy()

            if not areas:
                Label(self.area_placeholder,
                      text="No areas found.",
                      font=("Helvetica", 16),
                      fg="white",
                      bg="#1e3c72").pack(pady=10)
                return

            # Create scrollable frame for areas.
            canvas = Canvas(self.area_placeholder, bg="#1e3c72")
            scrollbar = ttk.Scrollbar(self.area_placeholder, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg="#1e3c72")

            canvas.configure(yscrollcommand=scrollbar.set)
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            # Create grid layout of area buttons.
            row = 0 # Row counter
            col = 0 # Column counter
            for area in areas:
                area_name = area["strArea"] # Extract area name from dictionary
                area_button = Button(scrollable_frame,
                                   text=area_name,
                                   font=("Helvetica", 14),
                                   bg="#4e8ccf",
                                   fg="white",
                                   width=15,
                                   height=2,
                                   command=lambda a=area_name: self.show_area_meals(a))
                area_button.grid(row=row, column=col, padx=10, pady=10)
                
                col += 1 # Move to the next column
                if col > 3:  #  columns 4 per row
                    col = 0 
                    row += 1

            scrollbar.pack(side=RIGHT, fill=Y)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)

        except Exception as e:
            for widget in self.area_placeholder.winfo_children():
                widget.destroy()
            Label(self.area_placeholder,
                  text=f"Error: {e}",
                  font=("Helvetica", 16),
                  fg="white",
                  bg="#1e3c72").pack(pady=10)

    def show_area_meals(self, area):
        #Display meals for the selected area in a new window.
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={area}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            meals = data.get("meals", [])

            if meals:
                area_window = Toplevel(self.root)
                area_window.title(f"Meals from {area}")
                area_window.geometry("600x800")
                area_window.configure(bg="#1e3c72")

                # Create scrollable frame
                canvas = Canvas(area_window, bg="#1e3c72")
                scrollbar = ttk.Scrollbar(area_window, orient="vertical", command=canvas.yview)
                scrollable_frame = Frame(canvas, bg="#1e3c72")

                canvas.configure(yscrollcommand=scrollbar.set)
                scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

                Label(scrollable_frame,
                      text=f"Meals from {area}",
                      font=("Helvetica", 20, "bold"),
                      fg="white",
                      bg="#1e3c72").pack(pady=20)

                for meal in meals:
                    meal_frame = Frame(scrollable_frame, bg="#1e3c72")
                    meal_frame.pack(fill=X, pady=5, padx=10)

                    try:
                        response = requests.get(meal["strMealThumb"])
                        img = Image.open(BytesIO(response.content))
                        img = img.resize((50, 50))
                        photo = ImageTk.PhotoImage(img)
                        img_label = Label(meal_frame, image=photo, bg="#1e3c72")
                        img_label.image = photo
                        img_label.pack(side=LEFT, padx=5)
                    except Exception as e:
                        print(f"Error fetching meals for area: {e}") 
                        messagebox.showerror("Error", f"Error fetching meals for area: {e}")
                        
                    button = Button(meal_frame,
                                  text=meal["strMeal"],
                                  font=("Helvetica", 12),
                                  bg="#4e8ccf",
                                  fg="white",
                                  command=lambda id=meal["idMeal"]: self.fetch_and_display_meal(id))
                    button.pack(side=LEFT, fill=X, expand=True, padx=5)

                scrollbar.pack(side=RIGHT, fill=Y)
                canvas.pack(side=LEFT, fill=BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")

    def run(self):
        """Start the application."""
        self.root.mainloop()
# Entry point of the application.
if __name__ == "__main__":
    # Create an instance of the application.
    app = MealDBExplorer()
    # Run the application.
    app.run()