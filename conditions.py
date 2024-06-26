# self.fields = {
#    "Плательщик": "",
#    "ПлательщикСчет": "",
#    "ПлательщикИНН": "",
#    "ПлательщикРасчСчет": "",
#    "ПлательщикКорсчет": "",
#    "ПлательщикБИК": "",
#    "ПлательщикБанк1": "",
#    "НазначениеПлатежа": "",
#    "Тип": "", # Таня добавляй его при совпадении условия и не завершай цикл! завершаться он будет только когда дойдет до конца statements
#    "ФИО": "" # Доставай его ДО того как будешь вычислять тип
# }


class Conditions:
    def __init__(self, fields):
        self.fields = fields
        self.statements = [
            ("Мерч", "АНО Такие дела" in self.fields.get("Плательщик")),
            ("Мерч", "Купишуз" in self.fields.get("Плательщик")),
            (
                "Мерч",
                "Интернет Решения" in self.fields.get("Плательщик")
                and "Договор КОМИСС ИР-77449/21 от 07.09.2021"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "Мерч",
                'АО "ТИНЬКОФФ БАНК"' in self.fields.get("Плательщик")
                and "Перевод средств по договору № 201509-2691 от 19.05.2022 по Реестру Операций по продаже товаров и услуг"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "Мерч",
                'АО "ТИНЬКОФФ БАНК"' in self.fields.get("Плательщик")
                and "Терминал CF LEUKEMIA FOUNDATION"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "ФЛ",
                self.fields.get("ФИО")
                and self.fields.get("ФИО") in self.fields.get("Плательщик")
                and "Благотворительное пожертвование на уставную деятельность"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "ФЛ",
                self.fields.get("ФИО")
                and self.fields.get("ФИО") in self.fields.get("Плательщик")
                and self.fields.get("ПлательщикСчет").startswith(("40817", "40820")),
            ),
            (
                "ФЛ",
                self.fields.get("ФИО")
                and self.fields.get("ФИО") in self.fields.get("Плательщик")
                and "Перевод с карты " in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "ФЛ_приложение",
                "Филиал № 7701 Банка ВТБ (ПАО)" in self.fields.get("Плательщик"),
            ),
            (
                "ФЛ_элекснет",
                'АО НКО "ЭЛЕКСНЕТ"' in self.fields.get("Плательщик"),
            ),
            ("Платформа", "ООО НКО ЮМани" in self.fields.get("Плательщик")),
            ("Платформа", 'ПАО "МТС-БАНК"' in self.fields.get("Плательщик")),
            (
                "Платформа",
                'РНКО "ВК Платёжные решения"' in self.fields.get("Плательщик"),
            ),
            (
                "Платформа",
                'Филиал "Корпоративный" ПАО "Совкомбанк"'
                in self.fields.get("Плательщик")
                and "Пожертвование. Зачисление по эквайрингу за"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "Платформа",
                'ПАО "СОВКОМБАНК"' in self.fields.get("Плательщик")
                and "Пожертвование. Зачисление соц.баллов за"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "Платформа",
                'Филиал "Корпоративный" ПАО "Совкомбанк"'
                in self.fields.get("Плательщик")
                and "Зачисление переводов по СБП за"
                in self.fields.get("НазначениеПлатежа"),
            ),
            ("Платформа", 'ООО "Нескучный город"' in self.fields.get("Плательщик")),
            ("Платформа", "Вклад в будущее" in self.fields.get("Плательщик")),
            ("Платформа", "Милосердие" in self.fields.get("Плательщик")),
            ("Платформа", 'ООО "Нескучный город"' in self.fields.get("Плательщик")),
            ("Платформа", 'АНО "КРР "МОЙ РАЙОН"' in self.fields.get("Плательщик")),
            ("Платформа", "ПРОСТО ПОМОГИ" in self.fields.get("Плательщик")),
            ("Платформа", "7702420633" in self.fields.get("ПлательщикИНН")),
            ("Платформа", "9702014610" in self.fields.get("ПлательщикИНН")),
            ("БФ", "Помощь рядом" in self.fields.get("Плательщик")),
            ("БФ", "КУЛЬТУРА БЛАГОТВОРИТЕЛЬНОСТИ" in self.fields.get("Плательщик")),
            (
                "БФ",
                self.fields.get("ПлательщикСчет").startswith("40703")
                and not any(
                    [
                        "Платформа" == self.fields.get("Тип"),
                        "Грант" == self.fields.get("Тип"),
                    ]
                ),
            ),
            (
                "ЮЛ_озон",
                "Интернет решения" in self.fields.get("Плательщик")
                and "Договор ИР-81138/21 от 15.09.2021"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "ЮЛ_озон",
                "ИП/Индивидуальный предприниматель Жигулова"
                in self.fields.get("Плательщик"),
            ),
            (
                "ЮЛ_озон",
                "ИП/Индивидуальный предприниматель Гуйда"
                in self.fields.get("Плательщик"),
            ),
            ("ЮЛ_фарма", "ПФАЙЗЕР" in self.fields.get("Плательщик")),
            ("ЮЛ_фарма", "Фармстандарт" in self.fields.get("Плательщик")),
            ("ЮЛ_фарма", "АФОФАРМ" in self.fields.get("Плательщик")),
            (
                "ЮЛ_фарма",
                self.fields.get("Плательщик") == 'ООО "ЭббВи"'
                and self.fields.get("ПлательщикИНН") == "7743855873",
            ),
            (
                "ЮЛ_фарма",
                self.fields.get("Плательщик") == 'ООО "АСТЕЛЛАС ФАРМА ПРОДАКШЕН"'
                and self.fields.get("ПлательщикИНН") == "7709948951",
            ),
            (
                "ЮЛ_фарма",
                self.fields.get("Плательщик") == 'ООО "ДЖОНСОН & ДЖОНСОН"'
                and self.fields.get("ПлательщикИНН") == "7725216105",
            ),
            (
                "ЮЛ_фарма",
                self.fields.get("Плательщик") == 'ООО "ТАКЕДА ФАРМАСЬЮТИКАЛС"'
                and self.fields.get("ПлательщикИНН") == "7711067140",
            ),
            (
                "ЮЛ_фарма",
                self.fields.get("Плательщик") == 'ООО "НОВАРТИС ФАРМА"'
                and self.fields.get("ПлательщикИНН") == "7705772224",
            ),
            (
                "ЮЛ_фарма",
                self.fields.get("Плательщик") == 'АО "РОШ-МОСКВА"'
                and self.fields.get("ПлательщикИНН") == "7728055569",
            ),
            (
                "ЮЛ_фарма",
                self.fields.get("Плательщик") == 'ООО "АСТРАЗЕНЕКА ФАРМАСЬЮТИКАЛЗ"'
                and self.fields.get("ПлательщикИНН") == "7704579700",
            ),
            (
                "Процент",
                "Выплата процентов по депозиту по договору №"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "Процент",
                'Возврат процентов с депозита "Овернайт"'
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "Процент",
                "процент" in self.fields.get("НазначениеПлатежа").lower()
                and self.fields.get("ПлательщикСчет").startswith("42202"),
            ),
            (
                "Мероприятие",
                'АО "ТИНЬКОФФ БАНК"' in self.fields.get("Плательщик")
                and "Зачисление средств по терминалам эквайринга"
                in self.fields.get("НазначениеПлатежа"),
            ),
            (
                "Мероприятие",
                'АО "ТИНЬКОФФ БАНК"' in self.fields.get("Плательщик")
                and "Терминал FOND BORBY S LEIKEMIEY"
                in self.fields.get("НазначениеПлатежа"),
            ),
            ("Грант", "7714997129" in self.fields.get("ПлательщикИНН")),
            ("Грант", "5003039076" in self.fields.get("ПлательщикИНН")),
            ("Грант", "7703424091" in self.fields.get("ПлательщикИНН")),
            ("Грант", "7704253508" in self.fields.get("ПлательщикИНН")),
            ("Грант", "7702231587" in self.fields.get("ПлательщикИНН")),
            (
                "ЮЛ",
                self.fields.get("ПлательщикСчет").startswith(
                    ("40702", "40701", "40802", "40807", "40907")
                ),
            ),
        ]
