# Перезапуск скрипта Планировщиком задач в случае ошибки

Данный проект создан в качестве примера настройки перезапуска Планировщиком задач Python-скрипта в случае ошибки

## Настройка

Для того, чтобы перезапуск скрипта по предлагаемой методике работал, необходимо чтобы в планировщике задач был включен журнал всех заданий

<p align="center">
    <img src="./img/1.png" alt="Turn on event log" height=330/>
</p>

Если журнал всех заданий включен, то на вкладке `Журнал` отработавших задач должен быть отображен список событий, аналогичный приведенному на иллюстрации

<p align="center">
    <img src="./img/2.png" alt="Event log example" height=330/>
</p>

Создаем в Планировщике задач папку `TestFolder`<br>

<p align="center">
    <img src="./img/3.png" alt="Create folder named TestFolder" />
</p>

Создаем новую задачу с именем `ScriptRestart`.

<p align="center">
    <img src="./img/4.png" alt="Create task named ScriptRestart" height=330/>
</p>

Добавляем триггеры запуска задачи:

1. Первый триггер устанавливаем на срабатывание по требуемому расписанию

    <p align="center">
        <img src="./img/5.png" alt="Set up first trigger" height=330/>
    </p>

1. Второй триггер устанавливаем на срабатывание при событии. Настраиваем отложенный запуск на 30 секунд или больше (чтобы процессы необходимые для успешной работы запускаемого скрипта успели завершиться)

    <p align="center">
        <img src="./img/6.png" alt="Set up second trigger" height=280 />
    </p>

    Создаем фильтр события. Переключаемся на вкладку `XML` и ставим галочку `изменить запрос вручную`. В поле ввода текста вставляем указанное XML-выражение

    ```xml
    <QueryList>
      <Query Id="0" Path="Microsoft-Windows-TaskScheduler/Operational">
        <Select Path="Microsoft-Windows-TaskScheduler/Operational">
          *[System[EventID=201]] and
          *[EventData[Data[@Name='TaskName']='\TestFolder\ScriptRestart']] and
          *[EventData[Data[@Name='ResultCode']!='0']]
        </Select>
      </Query>
    </QueryList>
    ```

    <p align="center">
        <img src="./img/7.png" alt="Create event filter" height=300 />
    </p>

    Сохраняем триггер

На вкладке `Действия` добавляем новое действие для задачи. В поле `Программа или сценарий` указываем путь к файлу интерпретатора Python `python.exe`, в поле ввода рабочей папки указываем абсолютный путь к папке с запускаемым скриптом, а в качестве аргумента передаем название файла скрипта.

<p align="center">
    <img src="./img/8.png" alt="Set up action" height=360 />
</p>

Готово. Сохраняем задачу.

### Дополнительно

Если нам не нужно, чтобы задача находилась в отдельной папке (напр. `TestFolder`), то мы можем создать задачу в корневой папке Планировщика задач. В таком случае в XML-выражении вместо аргумента `*[EventData[Data[@Name='TaskName']='\TestFolder\ScriptRestart']]` должен стоять аргумент `*[EventData[Data[@Name='TaskName']='\ScriptRestart']]`

---

## Работа скрипта

Созданная и настроенная нами задача запустится по расписанию и выведет окно с сообщением.

Если появится сообщение `Success`, значит скрипт отработал успешно.

<p align="center">
    <img src="./img/9.png" alt="Successful script execution result" height=152 />
</p>

<div class="page"/>

Если появится сообщение `Fail`, значит скрипт завершился с ошибкой. В таком случае наш скрипт будет перезапускаться с заданной задержкой до тех пор, пока не появится сообщение `Success`

<p align="center">
    <img src="./img/10.png" alt="Failed script execution result" height=152/>
</p>

## Заключение

После завершения работы задачи, на вкладке `Журнал` можно увидеть событие с кодом 201, которое для успешного выполнения задачи будет выглядеть так:

<p align="center">
    <img src="./img/11.png" alt="Event log on success"  height=220/>
</p>

В случае ошибки описание события будет следующим:

<p align="center">
    <img src="./img/12.png" alt="Event log on fail"  height=220/>
</p>

Таким образом, мы настроили перезапуск нашего скрипта в случае, если в журнале планировщика задач появляется запись о событии с кодом 201 (успешное завершение задачи) с кодом результата (ResultCode) отличным от 0 (Обычно программа возвращает код 0 в случае завершения без ошибок). Необходимо отметить, что в случае, когда скрипт не может завершиться успешно в силу объективных причин (напр. отключение интернета), по настроенной нами логике он будет перезапускаться бесконечно.