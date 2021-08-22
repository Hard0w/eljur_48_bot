import logging
from json import JSONDecodeError

import requests
from urllib3.exceptions import InsecureRequestWarning

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


if __name__ == '__main__':
    eljur = Eljur('login', 'password')