# Module: tools.py
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

def read_reviews_from_tsv(file_path):
    import csv
    from datetime import datetime
    review_list = []
    with open(file_path, encoding="UTF-8") as fd:
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
    return review_list

def load_stop_word_list(file_path='.\\stop_words.txt'):
    from sklearn.feature_extraction import text
    import re
    stop_word_list = []
    with open(file_path) as fd:
        lines = fd.readlines()
        for line in lines:
            words = re.split("['\t-]", line.strip())
            for stop_word in words:
                stop_word_list.append(stop_word)
    stop_word_list = text.ENGLISH_STOP_WORDS.union(stop_word_list)
    return stop_word_list

def gen_key_word_dict_list(string_list, max_key_words=10, stop_word_list=[]):
    from sklearn.feature_extraction import text
    import numpy as np
    if stop_word_list == []:
        stop_word_list = text.ENGLISH_STOP_WORDS
    vectorizer = text.TfidfVectorizer(stop_words=stop_word_list)
    transformer = text.TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(string_list))
    words = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    result_list = []
    for w in weight:
        temp_dict = {}
        loc = np.argsort(-w)
        for i in range(max_key_words):
            if w[loc[i]] <= 0:
                break
            temp_dict[words[loc[i]]] = w[loc[i]]
        result_list.append(temp_dict)
    return result_list

def combine_key_word_dicts(key_word_dict_list, priority_list=[]):
    if len(priority_list) < len(key_word_dict_list):
        for i in range(len(priority_list), len(key_word_dict_list)):
            priority_list.append(1) 
    if len(priority_list) > len(key_word_dict_list):
        for i in range(len(key_word_dict_list), len(priority_list)):
            priority_list.pop()
    result_dict = {}
    for i in range(len(key_word_dict_list)):
        key_word_dict = key_word_dict_list[i]
        for key_word in key_word_dict.keys():
            if not key_word in result_dict.keys():
                result_dict[key_word] = key_word_dict[key_word] * priority_list[i]
            else:
                result_dict[key_word] += key_word_dict[key_word] * priority_list[i]
    return result_dict

def gen_sorted_key_word_list(key_word_dict):
    result_list = list(key_word_dict.items())
    result_list.sort(reverse=True, key=lambda tup: tup[1])
    return result_list 

def remove_dup_key_word(ori_key_word_lists):
    key_words_lists = []+ori_key_word_lists
    for i in range(len(key_words_lists)):
        i_delete_namelist = []
        for k in range(i):
            k_delete_namelist = []
            for key_word in key_words_lists[i]:
                for prev_key_word in key_words_lists[k]:
                    if key_word[0] == prev_key_word[0]:
                        i_delete_namelist.append(key_word)
                        k_delete_namelist.append(prev_key_word)
                        break
            for delete_word in k_delete_namelist:
                key_words_lists[k].remove(delete_word)

        if i == len(key_words_lists)-1:
            for delete_word in i_delete_namelist:
                key_words_lists[i].remove(delete_word)

    return key_words_lists