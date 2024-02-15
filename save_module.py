import os
import json
from datetime import date, datetime


def save(save_objects):
    time = datetime.now()
    file_name = str(date.today()) + '_' + str(time.hour) + str(time.minute) + str(time.second)
    with open('saves/save_' + file_name + '.sav', 'w', encoding='utf-8') as save_file:
        save_data = []
        for obj in save_objects:
            object_data = {'Class_name': type(obj).__name__, 'Position': obj.get_position()}
            save_data.append(object_data)
        json.dump(save_data, save_file)


def load_save():
    save_files = [i for i in os.walk('saves')][0][2]
    if not save_files:
        return
    nums = [int(''.join(''.join(i[5:-4].split('-')).split('_'))) for i in save_files]
    with open(f'saves/{save_files[nums.index(max(nums))]}', 'r', encoding='utf-8') as save_file:
        objects = []
        file = save_file.read()
        data = json.loads(file)
        for i in data:
            obj = i['Class_name'] + '(' + '*' + str(i['Position']) + ')'
            objects.append(obj)
        return objects
