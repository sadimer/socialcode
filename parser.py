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
    Doc,
)

morph = pymorphy2.MorphAnalyzer()

# Регулярное выражение для поиска имен в тексте
name_pattern = re.compile(r"\b[А-ЯЁ][а-яё]+|\b[А-ЯЁ]+\b")


def normalize_name(word):
    parsed_word = morph.parse(word)[0]
    return parsed_word.normal_form


def extract_and_normalize_names(text):
    names = name_pattern.findall(text)
    normalized_names = [normalize_name(name) for name in names]
    return normalized_names


def check_txt(element):
    if element.endswith(".txt"):
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
        with open(filename, "r+", encoding="cp1251") as file_content:
            contents = file_content.readlines()

        for string in contents:
            string = (string.replace("\n", "")).split("=")
            if "Плательщик" in string:
                doc = Doc(string[1])
                doc.segment(segmenter)
                doc.tag_ner(ner_tagger)
                for span in doc.spans:
                    if span.type == PER:
                        payer["ФИО"] = span.text

                if "фонд борьбы с лейкемией" in string[1].lower():
                    skip = 1
                payer["Плательщик"] = string[1].replace("//", " ")

            if ("ПлательщикСчет" in string) and (skip == 0):
                payer["ПлательщикСчет"] = string[1]

            if ("ПлательщикИНН" in string) and (skip == 0):
                payer["ПлательщикИНН"] = string[1]

            if ("ПлательщикРасчСчет" in string) and (skip == 0):
                payer["ПлательщикРасчСчет"] = string[1]

            if ("ПлательщикКорсчет" in string) and (skip == 0):
                payer["ПлательщикКорсчет"] = string[1]

            if ("ПлательщикБИК" in string) and (skip == 0):
                payer["ПлательщикБИК"] = string[1]

            if ("ПлательщикБанк1" in string) and (skip == 0):
                payer["ПлательщикБанк1"] = string[1]

            if ("Дата" in string) and (skip == 0):
                date = re.search(
                    r"(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)\d\d",
                    string[1],
                )
                if date:
                    payer["Дата"] = date.group()
            if ("НазначениеПлатежа" in string) and (skip == 0):
                payer["НазначениеПлатежа"] = string[1]
                mail = re.search(
                    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.\w+", string[1]
                )
                if mail:
                    payer["Почта"] = mail.group(0)
                telephone = re.search(r"((\+7|7|8)+([0-9]){10})", string[1])
                if telephone:
                    payer["Телефон"] = telephone.group()
                target = re.search(r"FBL([0-9]){4}", string[1])
                if target:
                    payer["Цель"] = target.group()

            if ("Сумма" in string) and (skip == 0):
                payer["Сумма"] = (string[1].split("."))[0]

            if "КонецДокумента" in string[0]:
                if skip == 0:
                    payer_list.append(payer)
                payer = {}
                skip = 0

    for payer in payer_list:
        names_patients = extract_and_normalize_names(payer.get("НазначениеПлатежа"))
        doc = Doc(payer.get("НазначениеПлатежа"))
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)
        for span in doc.spans:
            if span.type == PER:
                span.normalize(morph_vocab)
                names_patients.extend(re.split(" .+? ", span.normal))
        payer["Пациент"] = names_patients

    for payer in payer_list:
        cond = Conditions(payer)
        for condition in cond.statements:
            if condition[1]:
                payer["Тип"] = condition[0]

    return payer_list
