# SmartDine-AI-Powered-Restaurant-Recommendation-System

This repository contains a Flask web application for restaurant recommendations based on user input. Below is an overview of the directory structure and key components:

## Directory Structure:

- **app.py:** This file contains the main backend operations of the website and is used to run the Flask server locally.
- **template :** Contains the HTML files used for different pages of the website.
  - *home.html:* Home page.
  - *search.html:* Search page.
- **static** Contains the CSS file and images used for styling.
  - *home.css:* Styling of the home page.
  - *search.css:* Styling of the search/result page.
  - *background1.jpg:* Background image for web pages.
- **main_rest.csv:** Raw data file.
- **food1.csv:** Cleaned data file.

## Explanation:

The `app.py` script serves as the backend for the web application. It performs the following steps:

1. **Data Preparation:**
   - Loads restaurant data from `main_rest.csv`.
   - Encodes categorical features like 'cuisines' and 'locality'.
   - Scales numerical features like 'average_cost_for_one' using min-max scaling.
   - Trains a k-nearest neighbors (KNN) model on the dataset.

2. **Function Definitions:**
   - `fav(lko_rest1)`: Performs content-based filtering for restaurant recommendations based on highlights.
   - `rest_rec(cost, people=2, min_cost=0, cuisine=[], Locality=[], fav_rest="", lko_rest=lko_rest)`: Filters restaurants based on user preferences.
   - `calc(max_Price, people, min_Price, cuisine, locality)`: Prepares restaurant recommendations for display.

3. **Flask Application:**
   - Sets up routes for handling restaurant search functionality.
   - Renders HTML templates with recommendations based on user input.

## Usage:
To run the application locally:
1. Install dependencies or libraries of the code 
2. Run `app.py`.

## Contributing:
Contributions are welcome! Please feel free to open issues or submit pull requests.

