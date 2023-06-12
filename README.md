# Movies-Recomendation-ML

Movie Recommendation System
This project aims to create a machine learning model for movie recommendation. It utilizes two datasets, namely credits.csv and movies_datasets.csv,(you can acces them from the followin link : https://drive.google.com/drive/folders/1nvSjC2JWUH48o3pb8xlKofi8SNHuNWeu)  which underwent a series of data processing functions for information extraction and ETL (Extract, Transform, Load) operations. The original datasets contained nested data and various errors, which were addressed during the preprocessing stage. The datasets were merged to create the movies_actors_directors.csv file(https://drive.google.com/file/d/1rDsPP32O5ZUKapVXgIlQe4K0tqW8YhgC/view?usp=sharing), which serves as the project's main database for the API.

Features
Data Extraction and Preprocessing: The project employs functions to extract and preprocess relevant information from the original datasets, addressing nested data and errors.
ETL Operations: The extracted data is transformed and loaded into a consolidated dataset (movies_actors_directors.csv), which serves as the basis for the movie recommendation system.
Movie Recommendation API: The project utilizes the FastAPI framework to create an API for movie recommendations.
Deployment: The API is deployed using the Render platform to make the movie recommendation system accessible.
Exploratory Data Analysis (EDA)
An exploratory data analysis was conducted to identify the most important columns and information for building the machine learning recommendation model.

Getting Started
To get started with the project, follow these steps:

Clone the repository.
Install the required dependencies.
Run the data processing scripts to extract and preprocess the movie data.
Merge the processed datasets to create movies_actors_directors.csv.
Launch the FastAPI server to start using the movie recommendation API.

API Endpoints

The following API endpoints are available:

GET
/cantidad_filmaciones_mes/{mes}
Cantidad Filmaciones Mes
"Enter the month, and the function returns the number of movies historically released in that month"
GET
/cantidad_filmaciones_dia/{dia}
Cantidad Filmaciones Dia
"Enter the day, and the function returns the number of movies historically released on that day.
GET
/score_titulo/{titulo}
Score Titulo
Enter the day, and the function returns the number of movies historically released on that day."
GET
/votos_titulo/{titulo}
Votos Titulo
"Enter the title of a movie, expecting the response to include the title, vote count, and average rating."
GET
/get_actor/{nombre_actor}
Get Actor
"Enter the name of an actor that exists in the dataset, and the function should return their success measured through the return."
GET
/get_director/{nombre_director}
Get Director
"Enter the name of a director that exists in the dataset, and the function should return their success measured through the return."
GET
/recomendacion/{titulo}
Recommendation
"Enter a movie title, and it will recommend similar movies in a list."