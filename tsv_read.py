# prepare:
#     define Review class

import csv
from datetime import datetime
# 1st step:
#     parse the input tsv file to a
#     list of review class objects

class Review:
    def __init__(
        self,
        marketplace,
        customer_id,
        review_id,
        product_id,
        product_parent,
        product_title,
        product_category,
        star_rating,
        helpful_votes,
        total_votes,
        vine,
        verified_purchase,
        review_headline,
        review_body,
        review_date        
    ):
        self.marketplace = marketplace
        self.customer_id = customer_id
        self.review_id = review_id
        self.product_id = product_id
        self.product_parent = product_parent
        self.product_title = product_title
        self.product_category = product_category
        self.star_rating = star_rating
        self.helpful_votes = helpful_votes
        self.total_votes = total_votes
        self.vine = vine
        self.verified_purchase = verified_purchase
        self.review_headline = review_headline
        self.review_body = review_body
        self.review_date = review_date
        self.priority = 1 + 2*helpful_votes - (total_votes-helpful_votes)

review_list = []
with open(".\\tsv_files\\hair_dryer.tsv", encoding="UTF-8") as fd:
    rd = csv.reader(fd, delimiter='\t', quotechar='"')
    temp = 0
    for row in rd:
        if temp<1:
            temp+=1
            continue
        if len(row)!=15:
            print("invalid tsv file")
            exit()
        new_review = Review(
            marketplace = row[0],
            customer_id = row[1],
            review_id = row[2],
            product_id = row[3],
            product_parent = row[4],
            product_title = row[5],
            product_category = row[6],
            star_rating = int(row[7]),
            helpful_votes = int(row[8]),
            total_votes = int(row[9]),
            vine = row[10],
            verified_purchase = row[11],
            review_headline = row[12],
            review_body = row[13],
            review_date = datetime.strptime(row[14], "%m/%d/%Y")
        )
        review_list.append(new_review)

# 2nd step:
#     split review_list to sub-lists based
#     on product_id
class Product:
    def __init__(
        self,
        product_id,
        reviews
    ):
        self.product_id = product_id
        self.reviews = sorted(reviews, key=lambda s:s.review_date)
product_list = []
temp_reviews_dict = {}
for review in review_list:
    if not review.product_id in temp_reviews_dict.keys():
        temp_reviews_dict[review.product_id] = []
    temp_reviews_dict[review.product_id].append(review)
for product_id in temp_reviews_dict.keys():
    product_list.append(
        Product(
            product_id,
            temp_reviews_dict[product_id]
        )
    )


# 3rd step:
#     cut the reviews into pieces, based on
#     the rating trend with time.
#     For example, from xx/xx/xxxx to xx/xx/xxxx,
#     certain product's rating is rising/falling
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import scipy.interpolate as interpolate
for i in range(len(product_list)):
    star_list = gen_star_list(product_list[i].reviews)
    x, y = smooth_graph()

def gen_star_list(review_list):
    result = []
    for review in review_list:
        result.append(review.star_rating)
    return result 

def smooth_graph(ori_x, ori_y):
    result_list = []+ori_y
    window_size = len(ori_y)//10
    sparse_flag = False
    if window_size < 15:
        sparse_flag = True
        window_size = len(ori_y)//4
    if window_size%2==0:
        window_size+=1
    polyorder = 3
    if polyorder>=window_size:
        polyorder = window_size-1
    if(polyorder<0):
        return result_list
    result_list = savgol_filter(result_list, window_size, polyorder)
    result_list = savgol_filter(result_list, window_size, polyorder)
    result_list = savgol_filter(result_list, window_size, polyorder)

    if sparse_flag:
        t,c,k = interpolate.splrep(ori_x, result_list, s=0, k=4)
        new_x_range = np.linspace(min(ori_x), max(ori_x), 3*len(result_list))
        spline = interpolate.BSpline(t, c, k, extrapolate=False)
        return (new_x_range,spline(new_x_range))
    # print("length of 3rd smoothing: "+str(len(temp)))
    # temp = savgol_filter(temp, 161, 3)
    # print("length of 4th smoothing: "+str(len(temp)))
    return (ori_x, ori_y)

#test tf-idf
stop_word_list = []
with open(".\\stop_words.txt") as fd:
    for line in fd:
        stop_word_list.append(line)
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import numpy as np
testlist = []
for review in product_list[0].reviews:
    testlist.append(review.review_body)

vectorizer = TfidfVectorizer(stop_words=stop_word_list)
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(testlist))
words = vectorizer.get_feature_names()
weight = tfidf.toarray()
n = 5

for w in weight:
    loc = np.argsort(-w)
    for i in range(n):
        print (words[loc[i]], w[loc[i]])