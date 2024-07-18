
import requests
from bs4 import BeautifulSoup
import pandas as pd
print('Libraries imported successfully')


required_fields = ['Type Of Traveller', 'Seat Type', 'Route',	'Date Flown',	'Seat Comfort',	'Cabin Staff Service', 'Ground Service', 'Value For Money']
customer_ratings = []
review_date = []
review_text = []
type_of_traveler = []
seat_type = []
route = []
date_flown = []
seat_comfort_rating = []
cabin_Staff_service = []
ground_service =[]
value_for_money = []

url = "https://www.airlinequality.com/airline-reviews/british-airways/?sortby=post_date%3ADesc&pagesize=100"
no_of_pages = 36
for page_no in range(1,no_of_pages+1):
  url = f"https://www.airlinequality.com/airline-reviews/british-airways/page/{page_no}/?sortby=post_date%3ADesc&pagesize=100"
  data = requests.get(url)

  soup = BeautifulSoup(data.content, "html.parser")

  reviews_container = soup.findAll('article', attrs = {'itemprop':'review'})



  for review in reviews_container:

    reviews_info = {}

    rating_val = review.find('span', attrs = {'itemprop':'ratingValue'})
    if rating_val is not None:
      rating_val = rating_val.get_text(strip=True)

    date = review.find('time', attrs = {'itemprop':'datePublished'}).get_text(strip=True)
    reviewbody = review.find('div', attrs = {'itemprop':'reviewBody'}).get_text(strip=True)

    customer_ratings.append(rating_val)
    review_date.append(date)
    review_text.append(reviewbody)

    for i in review.find('table', attrs = {'class':'review-ratings'}).findAll('tr'):
      data_header_span,data_value_span = i.findAll('td')

      data_header = data_header_span.get_text(strip=True)

      if data_header in required_fields:
        if len(data_value_span)>1:
          rating_stars = data_value_span.findAll('span',attrs = {'class': 'star fill'})
          max_rating = rating_stars[len(rating_stars)-1]
          data_value = max_rating.get_text(strip=True)
        else:
          data_value = data_value_span.get_text(strip=True)

        reviews_info[data_header] = data_value

    type_of_traveler.append(reviews_info.get('Type Of Traveller'))
    seat_type.append(reviews_info.get('Seat Type'))
    route.append(reviews_info.get('Route'))
    date_flown.append(reviews_info.get('Date Flown'))
    seat_comfort_rating.append(reviews_info.get('Seat Comfort'))
    cabin_Staff_service.append(reviews_info.get('Cabin Staff Service'))
    ground_service.append(reviews_info.get('Ground Service'))
    value_for_money.append(reviews_info.get('Value For Money'))

df = pd.DataFrame({'Customer Rating(out of 10)':customer_ratings, 'Review Date':review_date, 'Review':review_text , 'Type_of_traveler':type_of_traveler,'Seat_type':seat_type,'Route':route,'Date_flown':date_flown,
             'Seat_comfort':seat_comfort_rating,'Cabin_Staff_service':cabin_Staff_service,'Ground_service':ground_service,
             'Value_for_money':value_for_money})

df.to_csv('british_airways_reviews.csv', index=False)

print('Data saved to csv file')