import os
import re
import time

import pandas as pd
from pdfminer.high_level import extract_text

feature_description_SI = ["ОПИСАНИЕ ТИПА СРЕДСТВА ИЗМЕРЕНИЙ", "ОПИСАНИЕ ТИПА СРЕДСТВ ИЗМЕРЕНИЙ"]
feature_meaning_SI = ['Назначение средства измерений', 'Назначение и область применения']
feature_big_description = ['Описание средства измерений']

ed_izmer = ['Бк/м3', 'дБ', 'дБм', 'МОм', 'МПа', 'кЭ', 'НВ',
            'кА/м', 'т/ч', 'кг/ч', 'м3/ч', 'дм3/ч',
            'мА', 'м2', 'м3', 'см2', 'см3', 'дм3', 'Ом', 'Па'
                                                         'нм2', 'нм3', 'кН', 'имп./кВт∙ч', 'СФФ'
                                                                                           'мм', 'см', 'нм', 'угл', 'т',
            'c', 'А', 'м', 'кВ']
ed_izmer2 = [['температур', '°C']]

letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
          'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
          'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л' 'М', 'Н',
          'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь',
          'Э', 'Ю', 'Я']


def read_floder(floder_name):
    listdir = os.listdir(floder_name)
    listdir.sort()
    listdir = listdir[1:]
    # l_files = len(listdir)
    # print(l_files)
    listdir = listdir[::-1]
    return listdir


def del_hole(text_for_fix):
    for i in range(len(text_for_fix)):
        text_for_fix[i] = text_for_fix[i].strip()
    return text_for_fix


def per_name_and_letter(name):
    l = len(name)
    min_ind = l
    per = list(set(name[1:]) & set(letter))
    ind_list = []
    for i in range(len(per)):
        ind_list.append(name[1:].index(per[i]) + 1)
    if len(per) != 0:
        min_ind = min(ind_list)
    return min_ind, l


def count_hole_name(name_SI):
    l = len(name_SI)
    count = 0
    for i in range(l):
        if name_SI[i] == ' ':
            count = i
    return count, l


def create_text(file_path):
    PD_empty = pd.DataFrame()
    t0 = time.time()
    text = extract_text(file_path)
    text1 = text.split('\n')
    text1 = del_hole(text1)
    text2 = text.split()
    text3 = ' '.join(text2)
    T = 'СФФ' in text2
    # print(text3)

    # название и тип СИ
    description_SI = None
    per_description_SI = list(set(text1) & set(feature_description_SI))
    per_meaning_SI = list(set(text1) & set(feature_meaning_SI))
    if per_description_SI != [] and per_meaning_SI != []:
        index_description_SI = text1.index(per_description_SI[0]) + 2
        index_meaning_SI_start = text1.index(per_meaning_SI[0])
        description_SI = text1[index_description_SI:index_meaning_SI_start]
        description_SI = ' '.join(description_SI)

    # назначение СИ
    meaning_SI = None
    per_meaning_SI = list(set(text1) & set(feature_meaning_SI))
    per_feature_big_description = list(set(text1) & set(feature_big_description))
    if per_meaning_SI != [] and per_feature_big_description != []:
        index_meaning_SI = text1.index(per_meaning_SI[0]) + 2
        index_meaning_SI_end = text1.index(per_feature_big_description[0])
        meaning_SI = text1[index_meaning_SI:index_meaning_SI_end]
        meaning_SI = ' '.join(meaning_SI)

    # еденицы измерений
    izmer = None
    for izmer_i in range(len(ed_izmer)):
        t1 = ed_izmer[izmer_i]
        match_izmer = re.search(f'{t1}', f'{text2}')
        if match_izmer != None and len(t1) > 1:
            if len(t1) == 2:
                match_izmer2 = ed_izmer[izmer_i] in text2
                if match_izmer2 == True:
                    izmer = match_izmer[0]
                    break
            else:
                izmer = match_izmer[0]
                break
    if izmer == None and description_SI != None:
        for izmer_i in range(len(ed_izmer2)):
            T = ed_izmer2[izmer_i][0] in description_SI
            if T == True:
                izmer = ed_izmer2[izmer_i][1]
                break

    # погрешность
    pogresh = None
    type_pogresh = ['абсолютн', 'относительн']
    match_pogresh = re.search('±\d{1,9}\S\d{1,9}', f'{text2}')
    for tp_i in type_pogresh:
        match_type_pogresh = re.search(f'{tp_i}', f'{text2}')
        if match_type_pogresh != None:
            type_pogresh = match_type_pogresh[0]
            break
    if len(type_pogresh) == 2:
        type_pogresh = None

    match_pogresh2 = re.search('±\d{1,9}', f'{text2}')
    if match_pogresh != None:
        pogresh = match_pogresh[0][1:]
    elif match_pogresh2 != None:
        pogresh = match_pogresh2[0][1:]

    # дата утверждения
    date = None
    match_date = re.search('от\s«\d{1,2}»\D{3,10}\s20\d\d', f'{text1}')
    if match_date != None:
        date = match_date[0]

    # производитель
    # maker = None
    # match_maker = re.search('Изготовитель\D{2,500}\s\D{2,4} «\D{3,30}»', f'{text3}')
    # if match_maker != None:
    #     maker = match_maker[0]
    #     match_maker = re.search('\s\D{2,4} «\D{3,30}»', f'{maker}')
    #     if match_maker != None:
    #         maker = match_maker[0]
    #         maker = maker.strip()
    # maker2 = None
    # text4 = re.sub('\d', 'w', text3)
    # match_maker = re.search('Изготовитель\D{2,200}\sг.\s\D{2,20},', f'{text4}')
    # if match_maker != None:
    #     maker2 = match_maker[0]
    #     match_maker = re.search('г.\D{2,20},', f'{maker2}')
    #     if match_maker != None:
    #         maker2 = match_maker[0]
    # if maker != None:
    #     maker = maker + ' ' + maker2
    # # elif maker2 != None and maker == None:
    # #     maker = 'ИП ' + maker2
    # elif maker == None:
    match_maker = re.search('Изготовитель', f'{text1}')
    maker = None
    if match_maker != None:
        ind_maker = text1.index('Изготовитель')
        maker = text1[ind_maker + 2] + ' ' + text1[ind_maker + 3]

    # номер файла и номер в гос реестре
    f_name = file_path
    match_number_gos = re.search('-\d{1,50}-\d\d', f'{f_name}')
    number_gos = match_number_gos[0][1:]

    new_row = pd.DataFrame({'Номер_в_госреестре': [number_gos],
                            'Наименование_СИ': [description_SI],
                            'Eденица_измерения_СИ': [izmer],
                            'Погрешностиь_СИ': [pogresh],
                            'Дата_утверждения_СИ': [date],
                            'Производитель_СИ': [maker],
                            'Наименование_файла_с_описанием': [f_name],
                            'Тип_погрешности': [type_pogresh],
                            'Назначение_СИ': [meaning_SI]})

    PD_empty = PD_empty.append(new_row, ignore_index=True)
    print(round(time.time() - t0, 3), f_name)
    t0 = time.time()

    return PD_empty


if __name__ == '__main__':
    PD = pd.DataFrame()
    DIR = read_floder('pdfone/BD/DS/ds/')
    BD = create_text(DIR, 'pdfone/BD/DS/ds/', PD)
    BD.to_csv('pdfone/file.csv')
