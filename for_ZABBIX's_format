import sys
import serial
import re
import time

timeError = 0                                           # переменная времени ошибки, отправляемой в заббикс

while True:                                             # вечный цикл для беспрерывной работы программы
    try:
        port = "/dev/tty11"                             # указываем имя ком-порта в линукс
        ser = serial.Serial(port)                       # открываем порт
        ser.close()                                     # закрываем
        ser = serial.Serial(port, 9600, timeout=1)      # настройки ком-порта
    except serial.SerialException:                      # действия при ошибке ком-порта
        timeDelta = time.time() - timeError             # разница в текущем времени и времени последней записи ошибки
        if timeDelta > 10 or timeError == 0:            # если время с последней записи прошло более 10 сек или равно 0
            with open('/tmp/my_zabbix_traps.tmp', 'a') as alarm_file:       # открываем файл забикса на дозапись ошибки
                alarm_file.write(time.strftime('%H:%M:%S %Y/%m/%d .0.0.0.0.0.0.00.0.0.0 ', time.localtime()) +
                                 'COM-port\'s ERROR ' + '10.3.1.101 - ZBXTRAP 10.3.1.101 ' + 'COM-port is NOT AVAILABLE' + '\n')       # отправить в заббикс "COM-порт недоступен"
            timeError = time.time()                     # присваиваем переменной времени ошибки текущее время
        continue                                        # возвращаемся в начало цикла
    print('Работаем с портом ' + ser.port)              # (только для стадии тестирования программы)
    try:
        while True:
            line = ser.readline().decode('ISO-8859-1')[:-2]             # прочесть и конвертировать строку из b'xxx'\r\n' в xxx
            if re.search(r'MINOR|MAJOR|INFO|NMI', line):                # если в строке встречается MINOR or MAJOR or INFO or NMI
                print(line)                                             # вывести информацию из COM-порта
                line2 = ser.readline().decode('ISO-8859-1')[:-2]        # считать вторую строчку из порта
                print(line2)

                '''собираем строку под формат ZABBIX'''
                new_line = re.sub(r'\d\d-\w{3}-\d{4} \d\d:\d\d:\d\d \w{3}', '', line)   # убираем дату и время из первой принятой строки
                with open('/tmp/my_zabbix_traps.tmp', 'a') as alarm_file:               # открываем файл забикса на дозапись
                    alarm_file.write(time.strftime('%H:%M:%S %Y/%m/%d .0.0.0.0.0.0.00.0.0.0 ', time.localtime()) +
                                     new_line + ' 10.3.1.101 - ZBXTRAP 10.3.1.101 ' + line2 + '\n')
    except serial.SerialException:
        timeDelta = time.time() - timeError     # разница в текущем времени и времени последней записи ошибки
        if timeDelta > 10 or timeError == 0:    # если время с последней записи прошло более 10 сек или равно 0
            with open('/tmp/my_zabbix_traps.tmp', 'a') as alarm_file:        # открываем файл забикса на дозапись
                alarm_file.write(time.strftime('%H:%M:%S %Y/%m/%d .0.0.0.0.0.0.00.0.0.0 ', time.localtime()) +
                                 'COM-port\'s ERROR ' + '10.3.1.101 - ZBXTRAP 10.3.1.101 ' + 'Connection is LOST' + '\n')  # отправить в заббикс "соединение потеряно"
            timeError = time.time()                     # присваиваем переменной времени ошибки текущее время

        continue                                        # возвращаемся в начало цикла
