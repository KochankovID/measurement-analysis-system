import os
import re
from datetime import datetime

import pandas as pd
from pdfminer.high_level import extract_text

# feature_description_SI = [
#     "ОПИСАНИЕ ТИПА СРЕДСТВА ИЗМЕРЕНИЙ",
#     "ОПИСАНИЕ ТИПА СРЕДСТВ ИЗМЕРЕНИЙ",
# ]
# feature_meaning_SI = [
#     "Назначение средства измерений",
#     "Назначение и область применения",
# ]
# feature_big_description = ["Описание средства измерений"]

# ed_izmer = [
#     "Бк/м3",
#     "дБ",
#     "дБм",
#     "МОм",
#     "МПа",
#     "кЭ",
#     "НВ",
#     "кА/м",
#     "т/ч",
#     "кг/ч",
#     "м3/ч",
#     "дм3/ч",
#     "мГц",
#     "МГц",
#     "мА",
#     "м2",
#     "м3",
#     "см2",
#     "см3",
#     "дм3",
#     "Ом",
#     "Па",
#     "мл",
#     "Н∙м",
#     "импульс",
#     "об./кВт•час",
#     "А/м",
#     "МСм/м",
#     "нм2",
#     "нм3",
#     "кН",
#     "имп./кВт∙ч",
#     "СФФ",
#     "НКПР",
#     "кг",
#     "км/ч",
#     "м/с",
#     "мм",
#     "см",
#     "нм",
#     "угл",
#     "т",
#     "c",
#     "А",
#     "В",
#     "м",
#     "кВ",
#     "%",
# ]
ed_izmer2 = [
    ["температур", "°C"],
    ["Термом", "°C"],
    ["термом", "°C"],
    ["импульс", "имп"],
]

countries = [
    "Абхазия",
    "Австралия",
    "Австрия",
    "Азад-Кашмир",
    "Азербайджан",
    "Албания",
    "Алжир",
    "Ангола",
    "Андорра",
    "Антигуа и Барбуда",
    "Аргентина",
    "Армения",
    "Аруба",
    "Афганистан",
    "Багамские Острова",
    "Бангладеш",
    "Барбадос",
    "Бахрейн",
    "Белиз",
    "Белоруссия",
    "Белорусь",
    "Бельгия",
    "Бенин",
    "Болгария",
    "Боливия",
    "Босния и Герцеговина",
    "Ботсвана",
    "Бразилия",
    "Бруней",
    "Буркина-Фасо Бурунди",
    "Бутан",
    "Вануату",
    "Ватикан",
    "Великобритания",
    "Венгрия",
    "Венесуэла",
    "Восточный",
    "Тимор Вьетнам",
    "Великобритания",
    "Габон",
    "Гаити",
    "Гайана",
    "Гамбия",
    "Гана",
    "Германия",
    "Гватемала",
    "Гвинея",
    "Гвинея-Бисау",
    "Германия",
    "Гондурас",
    "Гонконг",
    "Государство Палестина",
    "Гренада",
    "Гренландия",
    "Греция",
    "Грузия",
    "Дания",
    "Демократическая Республика Конго",
    "Джибути",
    "Доминика",
    "Доминиканская Республика Египет",
    "Замбия",
    "Зимбабве",
    "Израиль",
    "Индия",
    "Индонезия",
    "Иордания",
    "Ирак",
    "Иран",
    "Ирландия",
    "Исландия",
    "Испания",
    "Италия",
    "Й̆емен",
    "Кабо-Верде",
    "Казахстан",
    "Камбоджа",
    "Камерун",
    "Канада",
    "Катар",
    "Кения",
    "Кипр",
    "Киргизия",
    "Кирибати",
    "Китай",
    "КНДР",
    "Колумбия",
    "Коморские Острова",
    "Косово",
    "Коста-Рика",
    "Кот-д’Ивуар",
    "Куба",
    "Кувейт",
    "Кюрасао",
    "Лаос",
    "Латвия",
    "Лесото",
    "Либерия",
    "Ливан",
    "Ливия",
    "Литва",
    "Лихтенштейн",
    "Люксембург",
    "Маврикий",
    "Мавритания",
    "Мадагаскар",
    "Македония",
    "Малави",
    "Малайзия",
    "Мали",
    "Мальдивы",
    "Мальта",
    "Марокко",
    "Маршалловы Острова",
    "Мексика",
    "Микронезия",
    "Мозамбик",
    "Молдавия",
    "Монако",
    "Монголия",
    "Мьянма",
    "Нагорно-Карабахская Республика",
    "Намибия",
    "Науру",
    "Непал",
    "Нигер",
    "Нигерия",
    "Нидерланды",
    "Никарагуа",
    "Ниуэ",
    "Новая Зеландия",
    "Норвегия",
    "Объединённые Арабские Эмираты",
    "ОАЭ",
    "Оман",
    "Острова Кука",
    "Пакистан",
    "Палау",
    "Панама",
    "Папуа",
    "Новая Гвинея",
    "Парагвай",
    "Перу",
    "Польша",
    "Португалия",
    "Пуэрто-Рико",
    "Республика Конго",
    "Россия",
    "Руанда",
    "Румыния",
    "Сальвадор",
    "Самоа",
    "Сан-Марино",
    "Сан-Томе и Принсипи",
    "Саудовская Аравия",
    "Сахарская Арабская Демократическая Республика Свазиленд",
    "Северный Кипр",
    "Сейшельские Острова",
    "Сенегал",
    "Сент-Винсент и Гренадины",
    "Сент-Китс и Невис",
    "Сент-Люсия",
    "Сербия",
    "Сингапур",
    "Синт-Мартен",
    "Сирия",
    "Словакия",
    "Словения",
    "Соединённые Штаты Америки",
    "США",
    "Соломоновы Острова",
    "Сомали",
    "Судан",
    "Суринам",
    "Сьерра-Леоне",
    "Таджикистан",
    "Таиланд",
    "Танзания",
    "Того",
    "Тонга",
    "Тринидад и Тобаго",
    "Тувалу",
    "Тунис",
    "Туркмения",
    "Турция",
    "Уганда",
    "Узбекистан",
    "Украина",
    "Уругвай",
    "Фареры",
    "Фиджи",
    "Филиппины",
    "Финляндия",
    "Франция",
    "Хорватия",
    "Центральноафриканская Республика Чад",
    "Черногория",
    "Чехия",
    "Чили",
    "Швейцария",
    "Швеция",
    "Шри-Ланка",
    "Эквадор",
    "Экваториальная Гвинея",
    "Эритрея",
    "Эстония",
    "Эфиопия",
    "Южная Корея",
    "Южная Осетия",
    "Южно-Африканская Республика",
    "Южный Судан",
    "Ямайка",
    "Япония",
]

months = dict(
    ЯНВ="01",
    ФЕВ="02",
    МАР="03",
    АПР="04",
    МАЙ="05",
    ИЮН="06",
    ИЮЛ="07",
    АВГ="08",
    СЕН="09",
    ОКТ="10",
    НОЯ="11",
    ДЕК="12",
)


def del_hole(text_for_fix):
    for i in range(len(text_for_fix)):
        text_for_fix[i] = text_for_fix[i].strip()
    return text_for_fix


def create_text(file_path, regex_settings):
    PD_empty = pd.DataFrame()

    f_name = os.path.basename(file_path)

    text = extract_text(file_path)

    text1 = text.split("\n")
    text1 = del_hole(text1)
    text2 = text.split()

    # название и тип СИ
    description_SI = None
    per_description_SI = list(set(text1) & set([i[0] for i in regex_settings.type_description]))
    per_meaning_SI = list(set(text1) & set([i[0] for i in regex_settings.meaning]))
    if per_description_SI != [] and per_meaning_SI != []:
        index_description_SI = text1.index(per_description_SI[0]) + 2
        index_meaning_SI_start = text1.index(per_meaning_SI[0])
        description_SI = text1[index_description_SI:index_meaning_SI_start]
        description_SI = " ".join(description_SI)

    # назначение СИ
    meaning_SI = None
    per_meaning_SI = list(set(text1) & set([i[0] for i in regex_settings.meaning]))
    per_feature_big_description = list(set(text1) & set([i[0] for i in regex_settings.description]))
    if per_meaning_SI != [] and per_feature_big_description != []:
        index_meaning_SI = text1.index(per_meaning_SI[0]) + 2
        index_meaning_SI_end = text1.index(per_feature_big_description[0])
        meaning_SI = text1[index_meaning_SI:index_meaning_SI_end]
        meaning_SI = " ".join(meaning_SI)

    # еденицы измерений
    ed_izmer = [i[0] for i in regex_settings.measurement_unit]
    izmer = None
    for izmer_i in range(len(ed_izmer)):
        t1 = ed_izmer[izmer_i]
        match_izmer = re.search("." + f"{t1}" + ".", f"{text2}")
        if match_izmer != None and len(t1) > 1:
            if len(t1) == 2:
                match_izmer2 = ed_izmer[izmer_i] in text2
                if match_izmer2 == True:
                    izmer = t1
                    break
            else:
                izmer = t1
                break
    if izmer == None and description_SI != None:
        for izmer_i in range(len(ed_izmer2)):
            T = ed_izmer2[izmer_i][0] in description_SI
            if T == True:
                izmer = ed_izmer2[izmer_i][1]
                break

    # погрешность
    pogresh = None
    type_pogresh = ["абсолютн", "относительн"]
    match_pogresh = re.search("±\d{1,9},\d{1,9}", f"{text2}")
    for tp_i in type_pogresh:
        match_type_pogresh = re.search(f"{tp_i}", f"{text2}")
        if match_type_pogresh != None:
            type_pogresh = match_type_pogresh[0]
            break
    if len(type_pogresh) == 2:
        type_pogresh = None

    match_pogresh2 = re.search("±\d{1,9}", f"{text2}")
    if match_pogresh != None:
        pogresh = float(match_pogresh[0][1:].replace(",", "."))
    elif match_pogresh2 != None:
        pogresh = float(match_pogresh2[0][1:].replace(",", "."))

    # дата утверждения
    date = None
    match_date = re.search("от\s«\d{1,2}»\D{3,10}\s20\d\d", f"{text1}")
    match_date2 = re.search("от\s\d{2}.\d{2}.20\d\d", f"{text1}")
    if match_date != None:
        date = match_date[0][3:]
        month = match_date[0][7: len(match_date[0]) - 4].split()[0][:3]
        month = month.upper()
        if month[:2] == "МА":
            month = "05"
        else:
            month = months[month]
        date = date.replace("«", "")
        date = date.replace("»", "")
        date = date.split()
        date[1] = month
        date = "".join(date)
        date = datetime.strptime(date, "%d%m%Y")
        date = str(date.date())
    elif match_date2 != None:
        date = match_date2[0][3:]
        date = datetime.strptime(date, "%d.%m.%Y")
        date = str(date.date())

    # номер файла и номер в гос реестре
    match_number_gos = re.search("-\d{1,50}-\d\d", f"{f_name}")
    number_gos = match_number_gos[0][1:]

    # производитель
    match_maker = re.search("Изготовитель", f"{text1}")
    maker = None
    if match_maker != None:
        T = match_maker[0] in text1
        if T == True:
            ind_maker = text1.index(match_maker[0])
            maker = text1[ind_maker: ind_maker + 5]
            maker = maker[1:]
            maker = " ".join(maker)
        else:
            maker = None
    country_maker = None
    if maker != None:
        country_maker = list(set(maker.split()) & set(countries))
        if country_maker != []:
            country_maker = country_maker[0]
        else:
            country_maker = "Россия"

    new_row = pd.DataFrame(
        {
            "Номер_в_госреестре": [number_gos],
            "Наименование_СИ": [description_SI],
            "Eденица_измерения_СИ": [izmer],
            "Погрешностиь_СИ": [pogresh],
            "Дата_утверждения_СИ": [date],
            "Производитель_СИ": [maker],
            "Наименование_файла_с_описанием": [f_name],
            "Тип_погрешности": [type_pogresh],
            "Назначение_СИ": [meaning_SI],
            "Страна_производитель": [country_maker],
        }
    )
    PD_empty = PD_empty.append(new_row, ignore_index=True)

    return PD_empty


if __name__ == "__main__":
    BD = create_text("../../data_parser/files/2022-84826-22.pdf")
    print(BD)
