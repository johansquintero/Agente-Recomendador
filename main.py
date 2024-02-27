from Recommendation import CoreRecommendation
import requests, pandas as pd

"""
def get_products(api_url):
    try:
        response = requests.get(api_url)
        return response.json()  
    except Exception as e:
        print(e)
        return None

   #formatea un objeto de producto para volver los metadatos simples
   #ya que los rating estaban almacenados dentro de otro objeto

def format_product_save(product):
    return {
         'id':product['id'],
         'title': product['title'],
         'price': product['price'],
         'category': product['category'],
         'rating_rate': product['rating']['rate'],
         'rating_count': product['rating']['count'],
        }

api_url = 'https://fakestoreapi.com/products'

products = get_products(api_url = 'https://fakestoreapi.com/products')#end point de la api a obtener los datos)
formated_products = [format_product_save(product=product) for product in products]

recommender = CoreRecommendation()

recommender.init_components("products",formated_products)

user = {
  "user_id": "12345",
  "name": "John Smith",
  "age": 30,
  "gender": "male",
  "location": "Mexico City",
  "interests": ["technology", "travel", "sports"],
  "purchase_history": [
    {
      "product_id": "P1",
      "name": "Smartphone",
      "category": "Technology",
      "price": 500,
      "purchase_date": "2023-10-15"
    },
    {
      "product_id": "P2",
      "name": "Trip to Paris",
      "category": "Travel",
      "price": 2000,
      "purchase_date": "2023-08-20"
    }
  ],
  "preferences": {
    "category": ["Technology", "Travel"],
    "platform": ["iOS", "Android"],
    "language": "Spanish"
  }
}
print(recommender.get_recommendation(user=user))
"""

books = pd.read_csv("../dataset_books/Books2.csv")
books = books.fillna('')
books.drop(columns=["isbn13","thumbnail","subtitle"],axis=1,inplace=True)
books["id"] = books.index + 1
books_dict = books.to_dict(orient='records')


recommender = CoreRecommendation()

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