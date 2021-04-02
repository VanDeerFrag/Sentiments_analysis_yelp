import pandas as pd
import numpy as np

def json_maker(activity_field: str, location: str, df_businesses: pd.DataFrame, df_reviews: pd.DataFrame):

    """
    Function that returns a dictionary that contains the information we want to send
    to the API.
    PARAMETERS:
        activity_field: str => the field of activity that we want to survey
        location: str => the location of the search
        df_business: pd.DataFrame => dataframe containing a list of all businesses
            on Yelp
        df_reviews: pd.DataFrame => dataframe containing a list of all the reviews
            found on Yelp
    RETURNS:
        json_result: dict => a dictionary containing the json we want to send through
            the API
    """

    if len(df_reviews) == 0:
        return []

    # count the number of businesses
    number_businesses = len(df_businesses)

    # count the number of reviews
    number_reviews = len(df_reviews)

    # count the number of positive/negative comments
    number_positive_reviews = df_reviews["predicted_sentiment"].value_counts()["POSITIVE"]
    number_negative_reviews = df_reviews["predicted_sentiment"].value_counts()["NEGATIVE"]

    # count the number of businesses without reviews

    # count the number of businesses that have more positive reviews than negative reviews

    df_reviews["predicted_sentiment"] = df_reviews["predicted_sentiment"].astype("category")

    df_TEMP = df_reviews.groupby(["id_business", "predicted_sentiment"]).count()["review"]

    def business_rating_from_predicted_sentiment(id_business):
        if id_business not in df_reviews["id_business"].unique():
            rating = np.nan
        else:
            rating = 100 * df_TEMP[id_business, "POSITIVE"] / (df_TEMP[id_business, "POSITIVE"] + df_TEMP[id_business, "NEGATIVE"])
        return rating

    df_businesses["prediction_rating"] = df_businesses["id_business"].map(business_rating_from_predicted_sentiment)

    number_positively_rated_businesses = df_businesses.loc[df_businesses["prediction_rating"] > 50]["prediction_rating"].count()
    number_negatively_rated_businesses = df_businesses.loc[df_businesses["prediction_rating"] < 50]["prediction_rating"].count()

    # add a list of the businesses addresses with their ratios of positive reviews (for a map)

    return {
        "activity_field": activity_field,
        "location": location,
        "number_businesses": int(number_businesses),
        "number_reviews": int(number_reviews),
        "number_positive_reviews": int(number_positive_reviews),
        "number_negative_reviews": int(number_negative_reviews),
        "number_positively_rated_businesses": int(number_positively_rated_businesses),
        "number_negatively_rated_businesses": int(number_negatively_rated_businesses)
    }