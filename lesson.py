import datetime


class Lesson:
    """ Класс для сохранения информации об уроке внутри дня """
    def __init__(self, name: str, index: int, comment: str, attendance: str, office: str,
                 date: str, time_begin: str, time_end: str, mark: str, theme: str, materials: list,
                 teacher: str, homework: str):
        """ Создаёт экзеспляр класс дисциплины """
        # Имя дисциплины
        self.name: str = name
        self.comment: str = comment
        # Признак посещаемости
        self.attendance: str = attendance
        # Кабинет
        self.office: str = office
        # Номер урока
        self.index: int = index
        # Время начала и конца
        self.time_begin: datetime = datetime.datetime.strptime(f'{date} {time_begin}', '%Y-%m-%d %H:%M:%S')
        self.time_end: datetime = datetime.datetime.strptime(f'{date} {time_end}', '%Y-%m-%d %H:%M:%S')
        # Оценка
        self.mark: str = mark
        # Тема урока
        self.theme: str = theme
        # Материалы
        # TODO: разобраться с типом данных
        self.materials = materials
        # ФИО учителя
        self.teacher = teacher
        # Домашнее задание
        self.homework = homework

    def __repr__(self):
        return f'<Lesson object at {hex(id(self))} name="{self.name}" index="{self.index}" office="{self.office}" ' \
               f'time="{self.time_begin}-{self.time_end}" mark="{self.mark}" theme="{self.theme}"' \
               f'teacher="{self.teacher}" homework="{self.homework}">'


if __name__ == '__main__':
    """ Пример заполнения класса урока """
    literature_1 = Lesson(name="Литература",
                          index=1,
                          comment="",
                          attendance="",
                          office="Кабинет №№37-ОУ48",
                          date="2020-03-02",
                          time_begin="08:00:00",
                          time_end="08:45:00",
                          mark="",
                          theme="Вн.чт. «Данко» (Отрывок из рассказа М.Горького «Старуха Изергиль» )",
                          materials=[],
                          teacher="Почапская Елена Валентиновна",
                          homework="читать 8 главу")
    print(str(literature_1))
