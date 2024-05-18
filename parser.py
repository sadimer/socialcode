# -*- coding: utf-8 -*-
import os
import re
import pymorphy2
from conditions import Conditions

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)

morph = pymorphy2.MorphAnalyzer()

# Регулярное выражение для поиска имен в тексте
name_pattern = re.compile(r'\b[А-ЯЁ][а-яё]+|\b[А-ЯЁ]+\b')


def normalize_name(word):
    parsed_word = morph.parse(word)[0]
    return parsed_word.normal_form


def extract_and_normalize_names(text):
    names = name_pattern.findall(text)
    normalized_names = [normalize_name(name) for name in names]
    return normalized_names


def check_txt(element):
    if ".txt" in element:
        return True
    return False


def parsing(path):
    segmenter = Segmenter()

    morph_vocab = MorphVocab()

    emb = NewsEmbedding()

    ner_tagger = NewsNERTagger(emb)

    files_in_path = []

    for i in path:
        for j in os.listdir(i):
            if check_txt(j):
                files_in_path.append(i + "/" + j)

    payer_list = []
    skip = 0
    payer = {}

    for filename in files_in_path:
        with open(filename, "r+", encoding='cp1251') as file_content:
            contents = file_content.readlines()

        for string in contents:
            string = (string.replace('\n', '')).split("=")
            if 'Плательщик' in string:
                doc = Doc(string[1])
                doc.segment(segmenter)
                doc.tag_ner(ner_tagger)
                for span in doc.spans:
                    if (span.type == PER):
                        payer['ФИО'] = span.text

                if ("фонд борьбы с лейкемией" in string[1].lower()):
                    skip = 1
                payer['Плательщик'] = string[1]

            if ('ПлательщикСчет' in string) and (skip == 0):
                payer['ПлательщикСчет'] = string[1]

            if ('ПлательщикИНН' in string) and (skip == 0):
                payer['ПлательщикИНН'] = string[1]

            if ('ПлательщикРасчСчет' in string) and (skip == 0):
                payer['ПлательщикРасчСчет'] = string[1]

            if ('ПлательщикКорсчет' in string) and (skip == 0):
                payer['ПлательщикКорсчет'] = string[1]

            if ('ПлательщикБИК' in string) and (skip == 0):
                payer['ПлательщикБИК'] = string[1]

            if ('ПлательщикБанк1' in string) and (skip == 0):
                payer['ПлательщикБанк1'] = string[1]

            if ('НазначениеПлатежа' in string) and (skip == 0):
                payer['НазначениеПлатежа'] = string[1]

            if ('Сумма' in string) and (skip == 0):
                payer['Сумма'] = string[1]

            if 'КонецДокумента' in string[0]:
                if (skip == 0):
                    payer_list.append(payer)
                payer = {}
                skip = 0

    for payer in payer_list:
        names_patients = extract_and_normalize_names(payer.get('НазначениеПлатежа'))
        doc = Doc(payer.get('НазначениеПлатежа'))
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)
        for span in doc.spans:
            if (span.type == PER):
                span.normalize(morph_vocab)
                names_patients.extend(re.split(" .+? ", span.normal))
        payer["Пациент"] = names_patients

    for payer in payer_list:
        cond = Conditions(payer)
        for condition in cond.statements:
            if condition[1]:
                payer['Тип'] = condition[0]

    return payer_list
