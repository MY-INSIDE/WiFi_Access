from subprocess import check_output as t
from platform import system as s
from os import path
from .Error import WiFi_Error


def wifi_names():
    # Список, который будет хронить имена сетей Wi-Fi
    wifi_names_list = []

    try:
        # Если версия Android'a менее 10
        try:
            # Запись вывода в переменную, с терминала, по запросу вывода информации хронящей нужные данные
            response = t('sudo cat /data/misc/wifi/wpa_supplicant.conf', shell=True)

            # Очистка лишнего для получения чистого списка имён Wi-Fi
            for wifi_name in str(response).split('network=')[1:]:
                wifi_name = str(str(wifi_name).split('ssid="')[1]).split('"')[0]
                wifi_names_list.append(wifi_name)


        # Если версия Android'a более 10
        except:
            # Запись вывода в переменную, с терминала, по запросу вывода информации хронящей нужные данные
            response = t('sudo cat /data/misc/apexdata/com.android.wifi/WifiConfigStore.xml', shell=True)

            # Очистка лишнего для получения чистого списка имён Wi-Fi
            for wifi_name in str(response).split('<string name="ConfigKey">&quot;')[1:]:
                wifi_name = str(wifi_name).split('&quot;WPA_PSK</string>')[0]
                if len(wifi_name) < 1000:
                    wifi_names_list.append(wifi_name)
                else:
                    wifi_name = str(wifi_name).split('&quot;NONE</string>')[0]
                    wifi_names_list.append(wifi_name)

    except: raise WiFi_Error('Возникла ошибка при просмотре Wi-Fi конфига')

    return wifi_names_list



def passwords(wifi_name):
    # Если версия Android'a менее 10
    try:
        try:
            # Запись вывода в переменную, с терминала, по запросу вывода информации хронящей нужные данные
            response = t('sudo cat /data/misc/wifi/wpa_supplicant.conf', shell=True)

            # Очистка лишнего и получения названия файлов, подключённых сетей
            wifi_pass = str(response).split(f'ssid="{wifi_name}"')[1]
            wifi_pass = str(wifi_pass).split(f'id_str="%7B%22creatorUid%22%3A%221000%22%2C%22configKey%22%3A%22%5C%22{wifi_name}%5C%22WPA_PSK%22%7D"')[0]
            try:    wifi_pass = str(str(wifi_pass).split(f'psk="')[1]).split(f'"')[0]
            except: wifi_pass = 'Отсутствует'


        # Если версия Android'a более 10
        except:
            # Запись вывода в переменную, с терминала, по запросу вывода информации хронящей нужные данные
            response = t('sudo cat /data/misc/apexdata/com.android.wifi/WifiConfigStore.xml', shell=True)

            # Очистка лишнего и получения названия файлов, подключённых сетей
            response = str(response).split(f'<string name="ConfigKey">&quot;{wifi_name}&quot;')[1]
            response = str(response).split(f'<int name="WEPTxKeyIndex" value="0" />')[0]
            if 'name="PreSharedKey">&quot;' in str(response).split(f'<string name="SSID">&quot;{wifi_name}&quot;</string>')[1]:
                wifi_pass = str(response).split('<string name="PreSharedKey">&quot;')[1]
                wifi_pass = str(wifi_pass).split('&quot;</string>')[0]
            elif 'name="PreSharedKey" />' in str(response).split(f'<string name="SSID">&quot;{wifi_name}&quot;</string>')[1]:
                wifi_pass = 'Отсутствует'

    except: raise WiFi_Error('Возникла ошибка при просмотре Wi-Fi конфига')

    return wifi_pass



def main():
    # Список хронящий все имена и пароли Wi-Fi сетей
    wifi_list = []

    if s() == 'Linux':
        if path.exists('/data/data'):
            # Цикл получения спика всех имён сетей, и их пароля
            for wifi_name in wifi_names():
                password = passwords(wifi_name)
                wifi_list.append({'name': wifi_name, 'password': password})
    
    else: raise WiFi_Error('Упс, похоже что Вы запускаете не с Android!')

    return wifi_list



if __name__ == '__main__':
    main()