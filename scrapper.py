import requests
from bs4 import BeautifulSoup as bs
from time import time, sleep
import pandas as pd
import numpy as np
from tqdm.auto import tqdm



def sleep_progress(sleep_time: int):
    """
    Function that shows a timer while sleeping
    PARAMETERS : sleep_time : int > 0
    RETURNS : None
    """
    
    print(f"sleeping for {sleep_time} seconds ...")
    for i in tqdm(range(sleep_time)):
        sleep(1)
        
        
def scrapper(activity: str, location: str):
    
    """
    Function that returns pandas DataFrames of the businesses and their reviews
    on Yelp.
    
    PARAMETERS:
    
        activity (string): Activity field which we want to scrap
        
        location (string): Geographical location that we want to survey
        
    RETURNS:
    
        df_businesses (pandas.DataFrame): DataFrame that contains informations about
            the businesses on Yelp
            
        df_reviews (pandas.DataFrame): DataFrame that contains the reviews of the
            businesses on Yelp
    """

    # define empty dictionnaries that will hold the data
    data_businesses = {
        "id_business": [],
        "name": [],
        "#_reviews": [],
        "address": [],
        "#_stars":[]
    }

    data_reviews = {
        "id_business": [],
        "review": [],
        "date": [],
        "#_stars": []
    }
    
    # time to sleep between each requests
    sleep_time = 30
    
    # first search page URL
    url = f"https://www.yelp.fr/search?find_desc={activity}&find_loc={location}"

    # declare a new session for the requests package
    session = requests.Session()

    # request the 1st search page to Yelp, until a page with no error is returned
    while True:
        try:
            print("1st search page request ...")
            response = session.get(url)
            if not response.ok:
                if response.status_code == 504:
                    # the request timed out, try again
                    print("response code 504 : timeout")
                    sleep_progress(sleep_time)
                    raise ValueError
                else:
                    # the server returned an unknown error, crash
                    raise KeyboardInterrupt(f"server response error : {response.status_code}")
            print("request successful")
            # create a soup
            soup = bs(response.text, 'html.parser')
            # sleep for 30 seconds
            sleep_progress(sleep_time)

            # get the number of pages of results
            if len(soup.find_all("h3", class_="css-ve950e")) == 1:
                print("not a place")
                number_pages = 0
            elif len(soup.select("ul.undefined:nth-child(1)")[0].find_all("li", class_="border-color--default__09f24__1eOdn")) == 6:
                print("no businesses")
                number_pages = 0
            else:
                print("some businesses")
                number_pages = int(soup.select("div.text-align--center__09f24__1P1jK:nth-child(2) > span:nth-child(1)")[0].get_text().split()[-1])

            print("number of pages:", number_pages)
            
            break
            
        except KeyboardInterrupt:
            raise
        except:
            print("error in requested page, new try ...")

    # for every page available ...
    for current_page_number in range(number_pages):
    # for current_page_number in range(1):
        
        # get the new search page if not the first one (that we already have)
        while True:
            try:
                if current_page_number != 0:
                    url = f"https://www.yelp.fr/search?find_desc={activity}&find_loc={location}&start={current_page_number * 10}"
                    print(f"search page {current_page_number + 1} request ...")
                    response = session.get(url)
                    if not response.ok:
                        if response.status_code == 504:
                            print("response code 504 : timeout")
                            sleep_progress(sleep_time)
                            raise ValueError
                        else:
                            raise KeyboardInterrupt(f"server response error : {response.status_code}")
                    print("request successful")
                    soup = bs(response.text, 'html.parser')
                    sleep_progress(sleep_time)

                # create the soup "businesses" that will hold the information about all the businesses of the page
                businesses = soup.select("ul.undefined:nth-child(1)")[0].find_all("li", class_=True)
                
                break
            
            except KeyboardInterrupt:
                raise
            except:
                print("error in requested page, new try ...")

        print("number_of_businesses:", len(businesses) - 6)
        
        # for each business in the page ...
        for index_business in range(len(businesses) - 6):
    #     for index_business in range(1):
            
            # set business_id
            business_id = current_page_number * 10 + index_business
            print("business_id :", business_id)
            
            # get the business name
            business_name = businesses[index_business + 2].find("a", class_="css-166la90").get_text()
            print("business_name :", business_name)
            
            # get the number of reviews
            try:
                business_number_reviews = int(businesses[index_business + 2].find("span", class_="reviewCount__09f24__EUXPN css-e81eai").get_text())
                print("some reviews")
            except:
                business_number_reviews = 0
                print("no reviews")
    #         print("business_#_reviews :", business_number_reviews)
            
            # get the address
            try:
                business_address = businesses[index_business + 2].find("address", class_="").get_text()
            except:
                business_address = np.nan
                print("no address")
    #         print("business_address :",business_address)
            
            # get the number of stars
            try:
                business_stars = businesses[index_business + 2].find("div", class_=True, role="img").get("aria-label")[0]
            except:
                business_stars = np.nan
                print("no business stars")
    #         print("business_stars :", business_stars)
            
            # save the date in data_businesses
            data_businesses["id_business"].append(business_id)
            data_businesses["name"].append(business_name)
            data_businesses["#_reviews"].append(business_number_reviews)
            data_businesses["address"].append(business_address)
            data_businesses["#_stars"].append(business_stars)
            
            # if there is no reviews, go directly to the next business
            if business_number_reviews == 0:
                continue
            
            # get the hypertext to the business page
            business_url = "https://www.yelp.fr" + businesses[index_business + 2].find("a", class_="css-166la90", href=True).get('href')
    #         business_url = "https://www.yelp.fr/biz/caf%C3%A9-du-palais-reims-4?osq=Restaurants"
    #         print("business_url :", business_url)
            
            # request the business page and create a soup
            while True:
                try:
                    print("business page request ...")
                    response = session.get(business_url + "&sort_by=date_desc")
                    if not response.ok:
                        if response.status_code == 504:
                            print("response code 504 : timeout")
                            sleep_progress(sleep_time)
                            raise ValueError
                        else:
                            raise KeyboardInterrupt(f"server response error : {response.status_code}")
                    print("request successful")
                    business_soup = bs(response.text, 'html.parser')
                    sleep_progress(sleep_time)

                    # get the number of pages of french reviews, if there are any
                    if len(business_soup.select("ul.undefined:nth-child(4)")[0].find_all("li", class_="margin-b5__373c0__2ErL8 border-color--default__373c0__3-ifU")) == 0:
                        print("no french reviews")
                        number_pages_review = 0
                    else:
                        print("some french reviews")
                        number_pages_review = int(business_soup.select(".pagination__373c0__3z4d_ > div:nth-child(2) > span:nth-child(1)")[0].get_text().split()[-1])
                        # print("number of review pages :", number_pages_review)
                    break
                
                except KeyboardInterrupt:
                    raise
                except:
                    print("error in requested page, new try ...")
            
            # we only scrap the first 20 reviews, so the first 2 pages of reviews
            for current_business_page_number in range(min(number_pages_review, 2)):
    #         for current_business_page_number in range(1):
                
                # get the new review page if not the first one (which we already have)
                while True:
                    try:
                        if current_business_page_number != 0:
                            business_url = "https://www.yelp.fr" + businesses[index_business + 2].find("a", class_="css-166la90", href=True).get('href') + f"&start={current_business_page_number * 10}"
                            print(f"review page {current_business_page_number + 1} request ...")
                            response = session.get(business_url + "&sort_by=date_desc")
                            if not response.ok:
                                if response.status_code == 504:
                                    print("response code 504 : timeout")
                                    sleep_progress(sleep_time)
                                    raise ValueError
                                else:
                                    raise KeyboardInterrupt(f"server response error : {response.status_code}")
                            print("request successful")
                            business_soup = bs(response.text, 'html.parser')
                            sleep_progress(sleep_time)

                        # create a soup "reviews" that will hold all the reviews of the page
                        reviews = business_soup.select("ul.undefined:nth-child(4)")[0].find_all("li", class_="margin-b5__373c0__2ErL8 border-color--default__373c0__3-ifU")
                        print("number of reviews :", len(reviews))
                        
                        break
                        
                    except KeyboardInterrupt:
                        raise
                    except:
                        print("error in requested page, new try ...")

                # for each review ...
                for review in reviews:

                    # get the review, by replacing all new line with a space
                    review_text = review.find("p", class_="comment__373c0__1M-px css-n6i4z7").get_text(" ")
        #             print(review_text)

                    # get the publication date
                    review_date = review.find("span", class_="css-e81eai").get_text().split()[-1]
        #             print(review_date)

                    # get the number of stars associated
                    review_stars = review.find("div", class_=True, role="img").get("aria-label").split()[0]
        #             print(review_stars)

                    # save the data in data_reviews
                    data_reviews["id_business"].append(business_id)
                    data_reviews["review"].append(review_text)
                    data_reviews["date"].append(review_date)
                    data_reviews["#_stars"].append(review_stars)

    # create pandas DataFrames from the dictionaries
    df_businesses = pd.DataFrame.from_dict(data_businesses)
    df_reviews = pd.DataFrame.from_dict(data_reviews)

    return df_businesses, df_reviews