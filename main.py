from Recommendation import CoreRecommendation
import pandas as pd

"""
  Ejemplo de implementacion del sistema
"""
books = pd.read_csv("../dataset_books/Books2.csv")
books = books.fillna('')
books.drop(columns=["isbn13","thumbnail","subtitle"],axis=1,inplace=True)
#un requisito es que los cada elemento tengan un id
books["id"] = books.index + 1
books_dict = books.to_dict(orient='records')#se convierte a diccionario el dataset

#si se cuenta con una api key de openai se agrega en este apartado
openai_api_key = ""
recommender = CoreRecommendation(openai_key=openai_api_key)

recommender.init_components(collection_name="books",resources=books_dict)

user = {
  "user": {
    "id": 234567,
    "name": "Carlos Rodriguez",
    "email": "carlos_rodriguez@email.com",
    "address": {
      "street": "Calle Principal",
      "city": "Barcelona",
      "state": "Spain",
      "postal_code": "08001"
    },
    "preferences": {
      "genres": ["Philosophy","Novels", "History"],
      "favorite_authors": ["Dan Brown", "Ken Follett", "René Descartes"]
    },
    "purchase_history": [
      {
        "book": "The Da Vinci Code",
        "author": "Dan Brown",
        "price": 17.99,
        "purchase_date": "2023-12-12"
      },
      {
        "book": "The Pillars of the Earth",
        "author": "Ken Follett",
        "price": 22.99,
        "purchase_date": "2024-01-05"
      }
    ]
  }
}


print(recommender.get_recommendation(user=user))