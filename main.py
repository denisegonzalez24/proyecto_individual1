from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import pandas as pd
import ast
from funciones_main import score_titulo , cantidad_filmaciones_mes , cantidad_filmaciones_dia, votos_titulo , get_actor, get_director
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


#creo la app FastApi
app = FastAPI(title = "Consultas peliculas")

#http://127.0.0.1:8000
@app.get("/")
def index():
    return {"messsage" : "hola, este es mi proyecto"}

#defino mi dataframe
df =pd.read_csv(r'D:\Denise_Estudio\henry\PI\datos\movies_data.csv')

#consultas

@app.get("/score_titulo")
def get_score_titulo(titulo: str):
    resultado = score_titulo(titulo, df)
    return resultado
   
#funcion para obtener filmaciones por mes
@app.get("/filmaciones_mes")
def get_cantidad_filmaciones_mes( mes ):
   resultado = cantidad_filmaciones_mes (mes , df)
   return resultado
    
#funcion para obtener filmaciones por dia
@app.get("/filmaciones_dia")
def get_cantidad_filmaciones_dia( dia ):
    return cantidad_filmaciones_dia(dia , df)


#funcion para obtener cantidad de votos por titulo
@app.get("/votos_titulo")
def get_votos_titulo(titulo):
    return votos_titulo(titulo , df)

#funcion para obtener el éxito de un actor medido a través del retorno 
@app.get("/actor")
def get_get_actor(nombre_actor: str):
    return get_actor(nombre_actor , df)
       
    
#función para obtener detalles de las películas de un director
@app.get("/director")
def get_get_director(nombre_director):
    return get_director(nombre_director , df)


#funcion para recomendar peliculas ingresando el nombre (detallado en el archivo 'modelo_machine_learning.ipynb')
muestra = pd.read_csv(r'D:\Denise_Estudio\henry\PI\datos\muestra.csv')

valid_columns = ['title', 'genres_clean', 'companies_names', 'director', 'overview']
muestra = muestra.fillna("")

muestra['combined'] = muestra['genres_clean'] + ' ' + muestra['companies_names'] + ' ' + muestra['director'] 

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(muestra['combined'])

cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

def recomendacion_movie(title: str):
    title = title.lower()
    if title not in muestra['title'].values:
        return {'mensaje': 'No hay datos de la pelicula'}
    
    idx = muestra[muestra['title'] == title].index[0]
    sim_cosine = list(enumerate(cosine_similarity[idx]))
    sim_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True)
    sim_ind = [i for i, _ in sim_scores[1:6]]
    sim_movies = muestra['title'].iloc[sim_ind].values.tolist()
    return {f'peliculas recomendados para {title}': list(sim_movies)}

print(recomendacion_movie('toy story'))