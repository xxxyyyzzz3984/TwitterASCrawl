import json
import os.path

result1_root = '../search_results/1116-0712pm_fine/'
result2_root = '../search_results/1121-0542pm_fine/'
result_files = ['a_result.js', 'b_result.js', 'c_result.js', 'd_result.js', 'e_result.js', 'f_result.js', 'g_result.js',
                'h_result.js', 'i_result.js', 'j_result.js', 'k_result.js', 'l_result.js', 'm_result.js', 'n_result.js',
                'o_result.js', 'p_result.js', 'q_result.js', 'r_result.js', 's_result.js', 't_result.js', 'u_result.js',
                'v_result.js', 'w_result.js', 'x_result.js', 'y_result.js', 'z_result.js']

min_words_possible = 14
max_words_possible = 24

users = []

for result_file in result_files:
    result_file_path = result1_root + result_file
    if not os.path.exists(result_file_path):
        continue
    with open(result_file_path) as f:
        for line in f:
            try:
                each_tweet_info = json.loads(line)
                if min_words_possible <= len(each_tweet_info['content']) <= max_words_possible:
                    users.append(each_tweet_info['username'].encode('utf-8'))
                    each_tweet_info.clear()

            except Exception, e:
                print str(e)

        f.close()

first_dataset = set(users)

# firsttime_namelist = open("Twitter_Firsttime_NameList.txt", "a")
#
# for user in first_dataset:
#     firsttime_namelist.write(user)
#     firsttime_namelist.write("\n")
# firsttime_namelist.close()
# print "finish"
print 'The number of fist data set ' + str(len(list(first_dataset)))

## second time
#
min_words_possible = 11
max_words_possible = 21

users = []

for result_file in result_files:
    result_file_path = result2_root + result_file
    with open(result_file_path) as f:
        for line in f:
            try:
                each_tweet_info = json.loads(line)
                if min_words_possible <= len(each_tweet_info['content']) <= max_words_possible:
                    users.append(each_tweet_info['username'].encode('utf-8'))
                    each_tweet_info.clear()

            except Exception, e:
                print str(e)

        f.close()

second_dataset = set(users)

print 'The number of fist data set ' + str(len(list(second_dataset)))


whole_list = list(first_dataset) + list(second_dataset)


common_set = set([x for x in whole_list if whole_list.count(x) > 1])

common_list = list(common_set)

print 'The number of total data set is ' + str(len(whole_list))
print 'The number of total data set in common is ' + str(len(common_list))
print 'They are:'
print common_list