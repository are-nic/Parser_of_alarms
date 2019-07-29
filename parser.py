# импорт библиотек
import sys, glob, serial, os, re

# присваиваем переменной серийный порт
ser = serial.Serial()

# ################ Поиск доступных портов windows, linux
def scan():                                             # функция поиска портов
    '''поиск доступных портов. возврат списка tuples (num, name)'''
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux'):
        # исключает текущий терминал - "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        raise EnvironmentError('Неподдерживаемая ОС')

    result = []                                          # пустой список для сбора доступных портов
    for port in ports:
        try:
            s = serial.Serial(port)                      # открываем доступный порт
            s.close()                                    # закрываем
            result.append(port)                          # добавляем порт в список доступных
        except (OSError, serial.SerialException):
            pass
    return result                                        # возвращаем список доступных портов в программу
##################################


ports = scan()                                                  # присваиваем переменной ports значения функции scan()
if ports:                                                       # если есть доступные порты...
    print('Доступные порты:')
    print(ports)                                                # выводим доступные порты
    if len(ports) > 1:                                          # если портов больше чем один
        ser.port = 'COM' + input('Введите адрес COM порта ')    # то ввести номер порта, к которому подключиться
    else:                                                       # иначе работаем с одним доступным портом
        ser.port = ports[0]
    ser = serial.Serial(str(ser.port), 9600, timeout=1)         # устанавливаем настройки порта
    print('Работаем с портом ' + ser.port)
else:                                                           # если нет доступных портов
    print('\nНет доступных COM портов, проверьте подключние.\n')
    sys.exit()                                                  # закрыть программу
try:
    while True:
        line = ser.readline().decode('utf-8')[:-2]              # прочесть и конвертировать строку из b'xxx'\r\n' в xxx
        if re.search(r'MINOR|MAJOR|INFO|NMI', line):            # если в строке встречается MINOR or MAJOR or INFO or NMI
            print(line)                                         # вывести информацию из COM-порта
            line2 = ser.readline().decode('utf-8')[:-2]         # прочесть вторую строку после сообщения об ошибке
            print(line2)                                        # вывод второй строки после сообщения об ошибке
            with open('harris_alarm.txt', 'a') as alarm_file:   # открывает файл, если файла нет: создает его. параметр 'a' - добавляет запись в тот же файл с конца строки. автоматически закрывает файл после работы с ним
                alarm_file.write(str(line)+'\n'+str(line2)+'\n')     # записывает в файл данные переменной line (то что приходит в порт)
except serial.SerialException:
    pass
# ser.close()
