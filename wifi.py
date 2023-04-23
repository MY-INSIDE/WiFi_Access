from platform import system as s
from os import path
from tools.Windows import main as main_windows
from tools.Linux import main as main_linux
from tools.Android import main as main_android



class WiFi:
    @classmethod
    # Запус поиска на Windows
    def windows(self, prints=False):
        if prints == True:
            print(main_windows())

        return main_windows()


    @classmethod
    # Запус поиска на Linux
    def linux(self, prints=False):
        if prints == True:
            print(main_linux())

        return main_linux()


    @classmethod
    # Запус поиска на Android
    def android(self, prints=False):
        if prints == True:
            print(main_android())

        return main_android()


    @classmethod
    # Запуск с автоматическим определением ОС
    def start(self, prints=None):
        # Если Windows 
        if s() == 'Windows':              wifi = main_windows()
        else:
            # Если Android
            if path.exists('/data/data'): wifi = main_android()

            # Если Linux
            else:                         wifi = main_linux()

        if prints == True:
            print(wifi)

        return wifi



if __name__ == '__main__':
    wifi = WiFi()
    wifi.start(prints=True)