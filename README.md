# <u> Market research by sentiment analysis </u>


![img](https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Ffondation-valentin-ribet.org%2Fwp-content%2Fuploads%2F2016%2F12%2Flogo-simplon.gif&f=1&nofb=1.png)
 

# Context :

## We are data scientists team in a market research service company. 

 This API providing an overview of the feelings that users have towards potential competing companies.

## Method :

The first step consists to track establishment data like the reviews and rating stars, in fonction of the field of activity and the geographical area. 

From this we can predict sentiment analysis for géneral and specific customers.

# Requirement :

- You'll need Python 3.8.8 and 
- It's recommended to install it in a Virtual environment

```bash
$ sudo apt install python3.8.8

$ pip install requirements.txt
```


# How to use the API :

- You can use the command line : <u> uvicorn API:app </u> in your terminal to start the API.
- Go to the url "http://localhost:8000/?activity_field=Restaurants&location=Reims", after replacing "Restaurants" and "Reims" with desired activity field and location.

```python
#------------- User settings ------------------------------------------------#

# url : http://127.0.0.1:8000
# command line : uvicorn API:app --reload

#-----------------------------------------------------------------------------#

```

# Resources

## Useful link :

[TheophileBlard github documentation ](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert)

[FastAPi documentation](https://fastapi.tiangolo.com/tutorial/first-steps/)

[BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

[Matplotlib documentation](https://matplotlib.org/)

[Pandas documentation ](https://pandas.pydata.org/docs/)


# ToDo 

- Incorporate interactive map with sentiment area arround the choosen. 

- Create new set of weights for camenBERT model from specific datasets.

