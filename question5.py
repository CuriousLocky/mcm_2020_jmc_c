from tools import *

review_list = read_reviews_from_tsv(".\\tsv_files\\hair_dryer.tsv")
star_list = [[] for i in range(5)]
for review in review_list:
    star_list[review.star_rating-1].append(review)
stop_word_list = load_stop_word_list()
key_words_by_star = []
for i in range(5):
    review_body_list = [review.review_body for review in star_list[i]]
    priority_list = [review.priority for review in star_list[i]]
    key_word_dict_list = gen_key_word_dict_list(review_body_list, 20, stop_word_list)
    combined_dict = combine_key_word_dicts(key_word_dict_list)
    sorted_word_list = gen_sorted_key_word_list(combined_dict)
    key_words_by_star.append(sorted_word_list)

    key_words_by_star = remove_dup_key_word(key_words_by_star)

for i in range(5):
    print("\nstar %d :" %(i+1))
    for k in range(5):
        print("{}\t{}".format(key_words_by_star[i][k][0], key_words_by_star[i][k][1]))