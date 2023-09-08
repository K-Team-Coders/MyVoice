# WARMONGER PROJECT: CRAWLER.![Лого CRAWLER](/uav.png)

### *Доброго времени суток!* **Вашему вниманию** представляется распределенная автоматизированная система сбора и обработки информации под шифром "**WARWONGER**" (пер. англ. Милитарист, в отношении наших Западных оппонентов.) - **Ветка CRAWLER** - модуль предназначенный для обработки вебсайтов с БПЛА и их комплектующими.

# Требования к эксплуатации

**Для запуска приложения представлены следующие требования:**

1) *PostgreSQL => 14.0*
2) *Python => 3.10.0*
3) *Библиотеки из requirements.txt (для работы парсера и fastAPI)*
4) *API-ключ Yandex-MapAPI*
5) *Широкополосное стабильное подключение к ИТКС "Интернет"*

# Установка приложения

#### Подключение к БД

Создайте файл *DB.env* в корне проекта, напишите в нем данные для подключения к БД PostgreSQL


`PORT =5432`

`DB_HOST = db`

`POSTGRES_DB = myvoice_db`

`POSTGRES_USER = myvoice_user`

`POSTGRES_PASSWORD = myvoice_user_pass`

#### Виртуальное окружение

Откройте терминал в корне проекта, выполните команды:

```python
python -m venv venv

\venv\Scripts\activate

pip install -r requirements.txt
```

# Запуск приложения

Вы создали виртуальное окружение и загрузили необходимые библиотеки, теперь можно запустить backend-часть и scrapy-часть проекта

#### Настройка отношений в БД

Для работы парсеров и fastAPI необходимо создать отношения из файла databaseConfig.py

Выполните в терминале:

`python databaseConfig.py`

#### FastAPI

В папке **fastAPI**, выполнить:

`uvicorn main:app --host=ваш_хост --port=предпочитаемый_порт --reload`

На этом этапе поднят инстанс FastAPI, он необходим для работы веб-приложения администратора.

#### Scrapy parsers

Парсеры вынесены за пределы Backend-части в целях безопасности (secure by design).

Не выходя из окружения, переходим в папку **sites** запускаем на выбор парсеры:

`scrapy crawl aeromotus` - Для запуска паука под сайт aeromotus

`scrapy crawl dronescnas` - Для запуска паука под сайт-БД dronescnas

`scrapy crawl mavikSpider` - Для запуска паука под сайт dji

`scrapy crawl metaspider ` - Для запуска Метапаука

#### Frontend

Откройте терминал в папке ***frontend***, выполните команды:

`npm install`

`npm run serve`

После этого frontend-часть этого проекта будет доступна либо на *http://localhost:8080/*, либо на *http://localhost:8081/*

## Принцип работы проекта

Была выполнена задача минимум - сделаны краулеры под основные сайты с записью в БД, либо в xlsx файл. Для решения задачи сбора данных с любого сайта был разработан прототип Метапаука.

![Схема Метапаука](/metaspider.png)

Основой для создания прототипа составила гипотеза - данные характеристик БПЛА находятся обычно в html-тэгах `<table>, <li>, <ul>, <ol>.`

Для их нахождения необходимо составить покрывающий граф ссылок сайта, грубо говоря - карту сайта. В целях создания универсального средства, было принято решение отказаться от Sitemap в файлах robots.txt, так как не на всех сайта присутсвует данная возможность.

Парсеры scrapy собирают данные в PostgreSQL, FastAPI работает с приложением на Vue.js которое визуализирует собранные данные.

### Оценка дальности полета БПЛА

*Оценка дальности полета БПЛА* представлена на странице **"Обзор БПЛА разных государтсв"** веб-приложения. Назначение данной страницы представляет собой обзор БПЛА различных государтсв с возможностью фильтрации по странам, а также нанесения метки выбранного БПЛА на любую локацию карты мира для оценки дальности полета для симулирования возможностей БПЛА.

1. Описание к каждому объекту представлено в виде карточки, с возможностью более детального обзора информации о конкретном БПЛА.

![Карточка](/hawk.png) ![Карточка подробнее](/hawk_ext.png)

2. Нажав на любую карточку, оператор получает возможность поставить метку БПЛА на любой локации карты, расположенной на нижней части страницы.
3. Метка представлят собой 2 окружности двух цветов: **красная и синяя.**
4. Радиус **КРАСНОЙ** окружности предназначен для демонстрации возможности полета БПЛА в обе стороны (центр окружности(локация вылета) -> край окружности(макимальная дальность полета) -> центр окружности(локация вылета) )
5. Радиус **СИНЕЙ** окружности предназначен для демонстрации возможности полета БПЛА в только в одну сторону (центр окружности(локация вылета) -> край окружности(макимальная дальность полета))

![дальность](/range.png)
*Рисунок 1*: Страница веб-приложения

*Рисунок 2*: В качестве примера был выбран БПЛА "Мavic" с дальностью полета 15 км.

*Рисунки 3,4*: Для примера местами взлета были взяты различные области г. Москва.

### Для наглядности БПЛА были разбиты на 3 группы, представленных в таблице:

| Группа | Скорость, км/ч |        Иконка |
| ------------ | :-----------------------: | ------------------: |
| I            |           0-92           | ![1](/dronesmall.png) |
| II           |     меньше 463     |     ![2](/uavmid.png) |
| III          |     463 и более     |   ![3](/uavlarge.png) |

Данное решение реализовано с применением YandexMapAPI

### Screencast

Мы собрали данные с предоставленных сайтов и визуализировали их с помощью нашей системы. Если вам интересно посмотреть как это выглядит - предлагаю ознакомиться с записью ниже,

*https://disk.yandex.ru/d/GCF-M9KGPJBdmQ*
