from subprocess import check_output as t
from platform import system as s
from re import findall as f
from .Error import WiFi_Error


def wifi_names():
    # Список, который будет хронить имена сетей Wi-Fi
    wifi_names_list = []

    # Запись вывода в переменную, с терминала, по запросу вывода всех когда-либо подключённых точек доступа
    response = t('netsh wlan show profiles', shell=True)

    # Находим регулярное выражение, с помощью которого и будет разделён вывов 
    split = f('\s*:\s', str(response))[0]

    # Цикл для получения чистого имени Wi-Fi сети
    for wifi_name in str(response).split(split)[1:]:
        wifi_names_list.append(wifi_name.split('\\r\\n')[0])

    return wifi_names_list



def passwords(wifi_name):
    # Запись вывода в переменную, с терминала, по запросу вывода информации о конкретной точки доступа
    response = t(f'netsh wlan show profiles name="{wifi_name}" key=clear', shell=True)

    # Находим пароль с помощью регулярного выражения
    password = f('(?:\s*:\s)(\w*)', str(response))[20]

    # Проверка, имеется ли пароль у Wi-Fi
    return password if password != '' else None



def main():
    # Список хронящий все имена и пароли Wi-Fi сетей
    wifi_list = []

    if s() == 'Windows':
        # Цикл получения и записи спика всех имён сетей, и их пароля
        for wifi_name in wifi_names():
            password = passwords(wifi_name)
            wifi_list.append({'name': wifi_name, 'password': password})

    else: raise WiFi_Error('Упс, похоже что Вы запускаете не с Windows!')

    return wifi_list



if __name__ == '__main__':
    main()