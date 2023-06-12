from fastapi import FastAPI
import uvicorn 
import pandas as pd
import numpy as np


url='https://drive.google.com/file/d/1rDsPP32O5ZUKapVXgIlQe4K0tqW8YhgC/view?usp=sharing'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2] 
df_movies_recomendation=pd.read_csv(url)
#df_movies_recomendation=pd.read_csv('D:\SoyHenry\Proyecto Integrador 1\Movies-Recomendation-ML\movies_actors_directors.csv')
app=FastAPI()


# Endpoint 1: cantidad_filmaciones_mes
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    df_movies_recomendation['release_date'] = pd.to_datetime(df_movies_recomendation['release_date'])
    df_movies_recomendation['mes'] = df_movies_recomendation['release_date'].dt.month_name(locale='es_ES')
    cantidad = df_movies_recomendation[df_movies_recomendation['mes'] == mes.capitalize()].shape[0]

    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"

# Endpoint 2: cantidad_filmaciones_dia
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    df_movies_recomendation['release_date'] = pd.to_datetime(df_movies_recomendation['release_date'])
    df_movies_recomendation['dia'] = df_movies_recomendation['release_date'].dt.day_name(locale='es_ES')
    cantidad = df_movies_recomendation[df_movies_recomendation['dia'] == dia.capitalize()].shape[0]
    return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}"

# Endpoint 3: score_titulo
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    movie = df_movies_recomendation[df_movies_recomendation['title'] == titulo]
    title = movie['title'].values[0]
    anio = movie['release_year'].values[0]
    score = movie['popularity'].values[0]
    return f"La película {title} fue estrenada en el año {anio} con un score/popularidad de {score}"

# Endpoint 4: votos_titulo
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    movie = df_movies_recomendation[df_movies_recomendation['title'] == titulo]
    titulo = movie['title'].values[0]
    cantidad_votos = movie['vote_count'].values[0]
    promedio_votos = movie['vote_average'].values[0]
    if cantidad_votos < 2000:
        return "La película no cumple con la condición mínima de 2000 valoraciones"
    else:
        # Ejemplo de retorno
        return f"La película {titulo}  cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {promedio_votos}"

# Endpoint 5: get_actor
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    actor_movies = df_movies_recomendation[df_movies_recomendation['casts_extracted'].str.contains(nombre_actor, case=False, na=False)]
    cantidad = actor_movies.shape[0]
    retorno = actor_movies['return'].sum()
    promedio = retorno / cantidad
    return f"El actor {nombre_actor} ha participado de {cantidad} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno} con un promedio de {promedio} por filmación"

# Endpoint 6: get_director
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    try:
        director_movies = df_movies_recomendation[df_movies_recomendation['directors_extracted'].str.contains(nombre_director, case=False, na=False)]
        éxito = director_movies['return'].sum()
        películas = []

        for _, movie in director_movies.iterrows():
            película = {
                'título': movie.get('title', 'Información no disponible'),
                'fecha_lanzamiento': movie['release_date'].strftime('%Y-%m-%d') if isinstance(movie.get('release_date'), pd.Timestamp) else 'Información no disponible',
                'retorno_individual': movie.get('return', 'Información no disponible'),
                'costo': movie.get('budget', 'Información no disponible'),
                'ganancia': movie.get('revenue', 'Información no disponible')
            }

            películas.append(película)

        return {
            'éxito': éxito,
            'películas': películas
        }
    except (SyntaxError, TypeError, ValueError):
        return {
            'message': 'No se cuenta con esta información'
        }



# ML
@app.get('/recomendacion/{titulo}')
def recommendation(title):
    # Filter movies that match the provided title
    movie = df_movies_recomendation[df_movies_recomendation['title'] == title]

    if movie.empty:
        return "Movie not found in the database."

    # Get the genre and directors of the movie
    genre = movie['genres_extracted'].values[0]
    directors = movie['directors_extracted'].values[0]

    # Perform recommendations based on genre and same directors
    genre_recommendations = df_movies_recomendation[df_movies_recomendation['genres_extracted'] == genre]['title']
    director_recommendations = df_movies_recomendation[df_movies_recomendation['directors_extracted'].apply(lambda x: any(director in x for director in directors))]['title']

    # Combine and remove duplicates from recommendations
    recommendations = pd.concat([genre_recommendations, director_recommendations]).drop_duplicates()

    # Exclude the original movie from recommendations
    recommendations = recommendations[recommendations != title]

    return {'lista recomendada': recommendations.tolist()[:5]}  # Return the first 5 recommendations









if __name__ == "__main__":
    
    uvicorn.run ("main:app", host="0.0.0.0", port=8000, reload=True) 