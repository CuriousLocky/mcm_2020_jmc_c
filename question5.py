from tools import *

category_names = [
    "hair_dryer",
    "microwave",
    "pacifier"
]

tsv_folder_path = ".\\tsv_files\\"
result_folder_path = ".\\question5\\"

for category_name in category_names:
    review_list = read_reviews_from_tsv(tsv_folder_path+category_name+".tsv")
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

    with open(result_folder_path+category_name+".txt", "w+") as f:

        for i in range(5):
            f.write("star %d :\n" %(i+1))
            for k in range(min(10, len(key_words_by_star[i]))):
                f.write("{}\t{}\n".format(key_words_by_star[i][k][0], key_words_by_star[i][k][1]))
            f.write("\n")