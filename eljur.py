import logging
import os
from json import JSONDecodeError
from typing import List

import requests
from urllib3.exceptions import InsecureRequestWarning

from lesson import Lesson

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def setup_logger(name):
    """ Возвращает логгер """
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)
    return logger



class EljurError(Exception):
    """ Класс ошибки связанной с журналом """
    pass


class AuthError(EljurError):
    """ Класс ошибки авторизации """
    pass


class Eljur:
    """ Класс для работы с элекронным журналом schools48.ru """

    def __init__(self, login: str, password: str):
        """ Создаёт экземпляр класса электронного журнала и производит авторизацию """
        self.log = setup_logger('Eljur')
        self.url = 'https://schools48.ru/'
        auth_request = requests.post(f'{self.url}/auth/login',
                                     data={'login_login': login, 'login_password': password},
                                     verify=False)
        if auth_request.status_code == 200 and auth_request.json()['success']:
            self.log.info('Успешная авторизация')
        else:
            try:
                self.log.error('Ошибка авторизации: %s', auth_request.json()['message'])
                raise AuthError(auth_request.json()['message'])
            except JSONDecodeError:
                self.log.error('Ошибка авторизации, статус-код: %s, %s', auth_request.status_code, auth_request.text)
                raise AuthError(f"HTTP {auth_request.status_code}: {auth_request.json()['message']}")

        self.cookies = auth_request.cookies
        # Запрос-заглушка, чтобы журнал подумал, что мы реальный пользователь и перешли по редиректу на /
        requests.get(self.url, cookies=self.cookies, verify=False)

    def get_lessons_for_week(self, day_in_week: str) -> List[Lesson]:
        """ Метод получает все уроки за неделю, содержащую day_in_week

        :param day_in_week: дата в виде в формате ГГГГ-мм-дд
        """
        # TODO: реализация получения уроков через обращение к API и запись
        return []


if __name__ == '__main__':
    eljur = Eljur(os.environ.get('LOGIN', None), os.environ.get('PASSWORD', None))
    """
    Выводит уроки на заданной неделе в формате
    <Lesson object at 0x101d6cfd0 name="Литература" index="1" office="Кабинет №№37-ОУ48" 
    time="2020-03-02 08:00:00-2020-03-02 08:45:00" mark="" 
    theme="Вн.чт. «Данко» (Отрывок из рассказа М.Горького «Старуха Изергиль» )"
    teacher="Почапская Елена Валентиновна" homework="читать 8 главу">
    ...
    """
    for lesson in eljur.get_lessons_for_week('05-03-2020'):
        print(lesson)
