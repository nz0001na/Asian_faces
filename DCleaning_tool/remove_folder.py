import os
import csv
import shutil


list_path = 'F:/zn_Chinese_Celebrities/code_DataCleaning/DCleaning_tool/remove_list.csv'
remove_list = []
if (os.path.exists(list_path)):
    t = csv.reader(open(list_path))
    for row in t:
        remove_list.append(row[0])


original_path = 'K:/NaZhang/4 Chinese_Celeb/[20170904]ChineseCeleb_part_I_cleaning/original_images/6_google_2/'
# get all original subjects
# subjects = []
# if (os.path.exists(original_path)):
#     subjects = os.listdir(original_path)

count = 0
n = len(remove_list)
for i in range(0, n):
    delete_sub = original_path + remove_list[i]
    if (os.path.exists(delete_sub)):
        # os.removedirs(delete_sub)
        shutil.rmtree(delete_sub)
        count = count + 1
        print remove_list[i]
print 'count = ' + str(count)
print 'done'