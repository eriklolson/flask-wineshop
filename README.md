# Full-Stack Ecommerce Project:

## Objectives
My goal was to make a full e-commerce website.  To accomplish this, I created a wine merchant website.   Although a wine merchant has unique product offerings, there are functionalities that are common to many e-commerce sites. This includes:

Public Users
* View products
* Flash messages for user feedback
* Filter products by categories
* View 'excursions' page

Logged-in Users
* Shopping Cart
* Commit orders
* View orders history
* View account info page

## Technologies Used:
* Python
* Flask
* HTML
* CSS
* Bootstrap
* Anaconda Project
* Font Awesome
* Request
* Flexbox
* Docker
* JavaScript
* jQuery
* Postgres
* SQLAlchemy
* Jinja
* Jupyter Notebook
* WTForms & Flask_wtf
* Redis
* Beautiful Soup
* psycopg2 
* NumPy
* Splash
* Pandas
* JSON
* Flask-Migrate
* Regex
* marshmallow & marshmallow_jsonapi
* werkzeug.security
* Flask-Login
* Flask-paginate
* Flask-REST-JSONAPI
* YAML

# Table of Contents
 **Phase A**: *setting up the back-end database*
   1. Data Model
   2. Web Scraper App
      1. Overview
      2. Basic Setup with Beautiful Soup
      3. Scraping JavaScript-generated Elements
      4. Data Cleaning and Manipulation with *Pandas*
   3. Import App

 **Phase B**: *creating the e-commerce app*
   1. Environment
   2. Flask Factory Pattern
   3. Configuration
   4. Database Models
   5. Product Views
       1. Bottles Route
       2. Categories Routes
   6. User Functions
      1. WTForms
      2. Login and Registration Logic
      3. User Session Data with Flask-Session & Redis
      4. Shopping Cart and Orders
   7. Excursions Page
   8. JSON REST API

# **Phase A**: *setting up the back-end database*
## 1. Database Model
As my e-commerce website would have to store user info, order history, product details for each product and more, I made the decision early on to create a relational database on the backend to store this data. I settled on the following database schema to meet my needs.
![Wineshop ER Diagram](https://user-images.githubusercontent.com/58354051/146614422-9c379f66-b848-484e-b33f-74b4188af995.png)

## 2. Web Scraper App
### i. Overview
To supply my back-end database with wine products, I made a web scraper app that extracts the desired product data from a wine seller website, <www.winedeals.com>.  The scraper uses *Beautiful Soup* to extract the data desired from HTML and uses *Pandas* to clean the data collected before saving it to CSV. This project is a mock demonstration of an e-commerce website only. The product data used herein are not for actual use in a business environment.

### ii. Basic Setup with Beautiful Soup
As there was multiple pages to be scraped, it was necessary to define the start, stop, and step ranges of the scraper; doing this via the *NumPy* library's `arrange` function, I set them at 1, 20, and 1, respectively. Then Iinitialized the Python dictionaries into which I would append the data collected.
![](../../../../Pictures/arrange.png)
After this I wrote a for-loop that encompasses the whole of the scraper functionality, `for page in pages:` Within the loop, I first defined the base URL to be scraped as winedeals.com's shopping page; an instance of *Beautiful Soup* using `html.parser` as `soup`; and the HTML element containing all product data I wanted to extract under the variable 'products'.

Then I wrote a nested for-loop to run through my 'products' variable, thereby defining the scope of the scrape within each of the pages. Within the loop, I first defined a variable to save each product's own product page. Then using this link, I defined a subpage along with its own subsoup, the former representing the product page and the latter a *Beautiful Soup* instance of it for parsing. The reason I bothered to scrape these product pages in addition is because it allowed me to scrape data inaccessible from the products browsing page. For instance, I could not scrape the color name except from the individual product pages.

Sometimes I had to resort to using regular expressions or *Regex* to isolate the desired text. For instnace, `region = re.findall(r"(?<=: )[^\]]+", region)`. The expression in quotes uses the negative lookbehind `(?<=:` to find a colon, matching a group before the main expression without including it in the result; and the negated set `[^\]]` as consisting of a "]" character.

I went on to scrape all the data I needed from, from product name to primary grape, and appended the isolated text to the appropriate python dictionary initialized from before. Thus, I appended the year of each wine product to the 'year' dictionary, the region name text to the region name dictionary, and so forth.

### iii. Scraping JavaScript-generated Elements
With *Beautiful Soup* I was able to scrape all the data I desired for each given product with the only exception being the color name. I came to the realization after many failed attempts to extract it from HTML that the element containing this text was generated dynamically through JavaScript, thus inaccessible in HTML. I found a workaround was to use *Splash*, the JavaScript rendering service with an HTTP API. I ran the `Splash` server in a Docker container and passed it to the params of my *Beautiful Soup* scraper. It rendered a static copy of the dynamically loaded page so that I could then access the otherwise inaccessible elements generated by JavaScript.

### iv. Data Cleaning and Manipulation with Pandas
After successfully appending all the desired data to python dictionaries, I saved these to a *Pandas* dataframe 
for the sake of data cleaning and easy conversion/manipulation.

![init_*Pandas*](https://user-images.githubusercontent.com/58354051/146993905-d7217fb8-c1a0-4646-ba8f-e1d71ac82e31.png)

Then I dropped rows with missing values via the *Panda* function called `dropna`. This was necessary to do since I would otherwise get products whose fields sometimes had missing data. Thus *Pandas* let me weed out any products scraped whose fields contained missing data, not wanting any such in my database. 

Even though I had used Python's `.strip` and `.replace` functions before when scraping the data, there would always remain some unwanted characters or spaces. As such, it was necessary to remove these with *Pandas*. I did so in combination with regular expressions or *Regex*. 

Lastly, I simply converted the *Pandas* dataframe to a CSV file so I could view/confirm the results and troubleshoot. Also, the CSV file is a good format to dump the data into, being easy to share and to export. 

## v. Import App
I wrote a simple app in Python to convert my CSV file of scraped data to an SQL table for storing products. This app connected securely to my *Postgres* account via the *SQLAlchemy* and *psycopg2* database URI, being grabbed from a hidden `.env` file. The URI in that file looks like this:`DATABASE_URI=postgresql+psycopg2://postgres:mysecretpassword@localhost:myport/mydatabase`. With the engine created, the app read and converted the CSV file to a *Pandas*  dataframe.  It then edited the data, removing any pesky remaining unwanted characters.  Finally, it saved the dataframe in a *Postgres* table called Bottles.


# **Phase B**: *creating the e-commerce app*

## 1. Environment
For my e-commerce Flask app, wineshop, I opted to use an Anaconda environment over a virtualenv or pipenv due to the anaconda-project feature that it offers. Saving all project dependencies and commands in a single `anaconda-project.yml` file written in YML, it allows for easy sharing of the project across users and machines. The folder where the environment lives is `/env` located in the root directory.

## 2. Flask Factory Pattern
An important principle in designing web applications is *the separation of concerns*. This was the primary motivator
behind my design choice to not write my application in a single file--say app.py--but rather to divide it into
multiple modules. Doing so is called the Flask factory pattern; its basic format is as follows:
<pre><code>~/project
   ├── /app                           # application module
      ├── __init__.py                 # file that creates the application
      ├── models.py                   # file that contains all database models
      ├── forms.py                    # file that contains all forms used by the application
      ├── routes.pys                  # file that contains routes used by the application
      ├── /static                     # file that contains all static assets used by the application
      ├── /templates                  # file that contains all HTML templates used by the application
   ├── /env                           # folder that contains the virtual environment used by the application
   ├── config.py                      # file to specify all configuration variables
   ├── wsgi.py                        # file where the application object is created and pointed to
</code></pre>
The Flask factory pattern file structure can be easily expanded as needed. My project ended up taking this structure:
<pre><code>~/wineshop
   ├── /app                           # application module
      ├── __init__.py                 # file that creates the application
      ├── auth.py                     # file that stores all routes related to user authentication
      ├── models.py                   # file that contains all SQLAlchemy database models
      ├── forms.py                    # file that contains all forms used by the application
      ├── routes.py                   # file that contains routes used by the application
      ├── shop.py                     # file that contains all routes pertaining to shopping cart
      ├── /api                        # Folder that contains all modules related to JSON api
      ├── /static                     # file that contains all static assets used by the application
          ├── /css                    # file that contains all CSS files for each page
          ├── /images                 # file that contains all images used  
          ├── /js                     # file that contains all JavaScript files for each page
      ├── /templates                  # file that contains all HTML templates used
   ├── /Jupyter                       # folder that contains the environment (hidden by .gitignore)
   ├── /env                           # folder for Jupyter notebooks (hidden by .gitignore)
   ├── /migrations                    # folder for records of data migrations (hidden by .gitignore)
   ├── .env                           # file to save sensitive environment variables (hidden by .gitignore)
   ├── .gitignore                     # file to specify files/folders to be excluded from public view
   ├── anaconda-project.yml           # YAML file encapsulates the project for easy sharing
   ├── config.py                      # file to specify configuration variables
   ├── wineshop.py                    # file where the application object is created and pointed to
</code></pre>
*Note: I changed the filename of wsgi.py to wineshop.py, though the functionality of this file is the same.*

The `/app` module holds the whole of my Flask application itself, which is created or initiated in `__init__.py`. For example, I reserved auth.py for all logic related to user authentication; `models.py` for data  models that map onto my database; and `forms.py` for all web forms (and related functions) to be used by my application. Importantly, I put all  HTML templates used in the `/templates` directory and any static assets global to the application in `/static`, with the former containing sub-directories for CSS files, images, and JavaScript files. 

## 3. Configuration
Before I started using the Flask factory pattern, I had all my configuration code in the script where I instantiated the Flask object, like so: 
```python
app.py
_____________________________
from flask import Flask
# Flask app creation
app = Flask(__name__)
# Ugly and confusing tangent of in-line config stuff
app.config['TESTING'] = True
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = 'GDtfDCFYjD' 
```
The problem with this, besides issues of readability, was that there was no way to change the configuration of the Flask instance after being instantiated. There was no way to have different versions of the application based on what I would be doing:  such as development configuration when in development phase, testing configuration when I want to do testing, and production configuration when I would be ready to deploy. Thus, instead of having all my configuration code in the script where I instantiated the Flask object, I made the design choice to put my configuration code in `config.py` located in the project root directory. There, I defined three classes:

- BaseConfig(BaseConfig), which is the base configuration class that contains configurations settings that apply to all the environments. All the other two classes inherit from this class.
-  DevelopmentConfig(BaseConfig), which is the base configuration class that contains configurations settings that apply to all the environments. All the other two classes inherit from this class.
- ProductionConfig(BaseConfig), which contains the configuration settings for the production environment.

This approach allowed me to run the suitable environment for my needs at the time by replacing 'None' with the configuration class name in the following code from `__init__.py`:
```python
__init__.py
_____________________________
def create_app(config_name=None):
    if config_name is None:
        config_name = environ.get('Flask_CONFIG', 'development')
        
``` 
To avoid exposing sensitive environment variables such as Flask's `SECRET_KEY` to GitHub, I set these in a local file called `.env` and grabbed them in `config.py` using the *Python-dotenv* library: 
```python
config.py
_____________________________
from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
FLASK_APP = environ.get('FLASK_APP')
FLASK_ENV = environ.get('FLASK_ENV')
SECRET_KEY = environ.get('SECRET_KEY')
```

## 4. Database Models
Instead of executing expensive SQL queries against my database, I decided to use the ORM *SQLAlchmy*, which allowed me to handle data by modifying objects 
 in code (data classes). With the ORM, I avoided dreaded "context switches" by modifying  objects instead of queries. In `models.py`, I wrote a data model to represent every SQL table in my database, with attributes of the model translating to columns in the SQL table. Whenever I had to alter the model, I persisted the change in the corresponding database table by using *Flask-Migrate*. A record of each migration got automatically saved in the `/migrations` directory.

## 5. Product Views
### i. Bottles Route
I reserved `routes.py` within the app module for view functions that display products to the user. For the `/wine` route, handling the main shopping page, I made a variable, 'bottles', for the products to be viewed by querying the Bottles model. I then paginated this variable so that it would return only six products per page. Further, I defined a seperate variable for each of the several categories a user can filter results, from color name to varietal.  Lastly, I passed these variables to `wine.html`. Within that html, I displayed these variables to the user using *Jinja* syntax.

### ii. Categories Route
To return the correct results that match whatever category the user should click on, I had to write dynamic routes for each category (color, varietal, country, and region).  For example, `@app.route('/color/<color_name>')` receives the dynamic input of the color_name  passed from the HTML page via this href:: 
```jinja
 <form> 
     {% for color in colors %}
    
         <a href="/color/{{ color.color_name }}">{{ color.color_name }}</a>
   
      {% endfor %}
 </form>`
```
With the color name received through this href, it is then used in an *SQLAlchemy* query that filters products where the color_name received equals the same in the Bottles model. This being saved as a variable is then returned in the `results.html` page.

## 6. User Functions
### i. WTForms
When it came to web forms, critical in passing data from the user to the back-end, I debated whether to use HTML 
forms or *WTForms*. What made me settle on the latter was that HTML forms, unlike *WTForms*, have these drawbacks:

- With no direct link between the client-side HTML form and the server-side Flask app, Flask View
has to recreate the form elements from the client-side back again to process them.
- HTML forms provide no CSRF tokens to protect against CSRF (Cross-Site Request Forgery) attacks.
- No automatic validation

Thus, I made the design choice to use *WTForms*. I defined
my `LoginForm` to be later used in my login function as having fields that ask the user for 
username and password. I included *WTForm*'s `DataRequired` validator, which throws an error
if input is missing.

### ii. Login and Registration Logic
Having decided to put all logic related to user authentication in auth.py, 
I wrote my login, logout, and register functions in this file. The login function calls on the `LoginForm` form
from `forms.py` and checks the username and password submitted against the corresponding fields in the User model.
If the username and password submitted match, the user gets loged-in automatically by the `login_user` function 
that comes with the `*Flask-Login* library.
I made the register user function evoke the `RegistrationForm` form. It then takes the password submitted
 and hashes it via the `generate_password_hash` function that comes with the WTF library.
 It also saves the username and email submitted to variables and appends those variables to the user 
 model via *SQLAlchemy*'s `db.session(add)` and `db.session(commit)` method.
### iii. User Session Data with Flask-Session & Redis
A lot of functionality in a web application depends on how users' sessions are managed. I did not want items in a user's cart to remain long after they were abandoned. Nor did I want carts to persist across devices. For these reasons, I determined that I could not rely on Flask's default method of storing session variables, which happens via locally stored browser cookies. Instead, I avoided these issues by using the cloud key/value store *Redis* (leveraging the *Flask-Session* plugin). I used the NoSQL datastore *Redis* to temporarily hold data in memory for users as they navigate my website. With *Flask-Session*, I defined the session type of my web app as *Redis* which connects to a Redis instance in `config.py`. ` 
```python
config.py
_____________________________
SESSION_TYPE = 'Redis'
SESSION_Redis = Redis.from_url(environ.get('SESSION_Redis'))
```
### 4. Shopping Cart and Orders
Again with the *separation of concerns* in mind, I decided to put all routes related to the user's shopping cart 
and committing orders in `shop.py`. There, the `addToCart` route and function handles the adding of items to the
user's shopping cart. It takes the argument `<int:bottles_id>` (i.e., product id) to only return the appropriate 
products from the Bottles model, which is done via an *SQLAlchemy* query. This `addToCart` function also gets the 
quantity to be added from the web-form by using `resquest.form`. Then it checks if the product is already in the
shopping cart by matching the product id received against that in the cart. If there is a match, the 
function adds the quantity received to that already in the cart; it then commits the change via *SQLAlchmy*'s
`db.session.commit()`.

The `/cart` route returns the cart.html page, and, with the function of the same name, displays products
that have been added to the cart. To define the cart variable, I used an *SQLAlchemy* query to join the Bottles
and Cart models on the product id field to access the product name and price from the Bottles model where the
product id is the same as that in cart. Additionally, I added the Stocks model on the product id field to access the
quantity in inventory for each product. In this function I compute the total price of by multiplying the quantity
in cart by the price of product; I then return this total to the HTML page to be rendered through *Jinja*. 

The `create_order` function is responsible for committing sales transactions; it does so while updating the 
inventory quantity in the Stocks model, saving records of individual products sold to the OrderedItems model, 
saving a record of each order in the Order model, and saving transaction info like card number in the 
Transactions model. First this function grabs the needed variables for each product from the Cart, Bottles,
and Stocks models through an *SQLAlchemy* query join statement. Then it checks to see if the quantity to be bought
 exceeds that in inventory, throwing an error message if so. If not, it subtracts the quantity to be bought from
the quantity in inventory and persists the change in database with `db.commit`. It then saves the order date and
order total to the Order model. The OrderedItems model is updated by calling on the `updateOrderedItems` function
as defined in forms.py; it receives the 'order_id' and 'user_id'. Next, it calls on the `updateTransactions` 
function from `forms.py`; it takes the following variables to be saved in the Transactions model: order_id, order_date,
order_total, card_number, card_type.

## 7. Excursions Page
I wrote the excursions page, accessed by the main link of the same name, to demonstrate how the
website could include other elements besides the shopping related. This page shows how articles or blog entries could be incorporated
in the website. It makes use of the image files I saved in `/static/images`. Since this is just for 
demonstration, I did not write the individual blog posts or articles.

## 8. JSON REST API
Although my Flask routes successfully return the products desired from the database, I included a basic skeleton api that can be used as a starting point for more ambitious product filtering if this project were to be expanded on. In `/api`, I used the *Flask-REST-JSONAPI* extension to build a REST web api according to JSON API specification and using `Marshmallow` data abstraction layers. In its current form, the api returns all products in the *Postgres* database at the `/bottles` endpoint and all data for an individual product at the `/bottles/<int:id>` endpoint, with id being that of any individual product. The returned data is in JSON format.


**Edit a file, create a new file, and clone from Bitbucket in under 2 minutes**

When you're done, you can delete the content in this README and update the file with details for others getting started with your repository.

*We recommend that you open this README in another tab as you perform the tasks below. You can [watch our video](https://youtu.be/0ocf7u76WSo) for a full demo of all the steps in this tutorial. Open the video in a new tab to avoid leaving Bitbucket.*

---

## Edit a file

You’ll start by editing this README file to learn how to edit a file in Bitbucket.

1. Click **Source** on the left side.
2. Click the README.md link from the list of files.
3. Click the **Edit** button.
4. Delete the following text: *Delete this line to make a change to the README from Bitbucket.*
5. After making your change, click **Commit** and then **Commit** again in the dialog. The commit page will open and you’ll see the change you just made.
6. Go back to the **Source** page.

---

## Create a file

Next, you’ll add a new file to this repository.

1. Click the **New file** button at the top of the **Source** page.
2. Give the file a filename of **contributors.txt**.
3. Enter your name in the empty file space.
4. Click **Commit** and then **Commit** again in the dialog.
5. Go back to the **Source** page.

Before you move on, go ahead and explore the repository. You've already seen the **Source** page, but check out the **Commits**, **Branches**, and **Settings** pages.

---

## Clone a repository

Use these steps to clone from SourceTree, our client for using the repository command-line free. Cloning allows you to work on your files locally. If you don't yet have SourceTree, [download and install first](https://www.sourcetreeapp.com/). If you prefer to clone from the command line, see [Clone a repository](https://confluence.atlassian.com/x/4whODQ).

1. You’ll see the clone button under the **Source** heading. Click that button.
2. Now click **Check out in SourceTree**. You may need to create a SourceTree account or log in.
3. When you see the **Clone New** dialog in SourceTree, update the destination path and name if you’d like to and then click **Clone**.
4. Open the directory you just created to see your repository’s files.

Now that you're more familiar with your Bitbucket repository, go ahead and add a new file locally. You can [push your change back to Bitbucket with SourceTree](https://confluence.atlassian.com/x/iqyBMg), or you can [add, commit,](https://confluence.atlassian.com/x/8QhODQ) and [push from the command line](https://confluence.atlassian.com/x/NQ0zDQ).