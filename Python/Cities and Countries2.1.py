#Работа с задачкой
# vul = "Russia: Moscow, Saint Petersburg, Novosibirsk, USA: New York, Los Angeles, Chicago, France: Paris, Marseille, Lyon"

# ХОЧУ УВИДЕТЬ ФУНКЦИЮ, КОТОРОЙ ДАЮ НАЗВАНИЕ СТРАНЫ - ВЫВОДИТ ЕЁ ГОРОДА И ИХ КОЛИЧЕСТВО.
# пример запуска
# fun("Russia")


vul = "Russia: Moscow, Saint Petersburg, Novosibirsk; USA: New York, Los Angeles, Chicago; France: Paris, Marseille, Lyon"

def fun(country_name):
    countries = vul.split(';')
    for parts in countries:
        parts = parts.strip()
        if parts.startswith(country_name + ':'):
            country, cities_country = parts.split(':', 1)
            cities = []
            parts = cities_country.split(',')
            for city in parts:
                city = city.strip()
                cities.append(city)
            print(str("Страна: ") + str(country))
            print("Города:")
            for city in cities:
                print(str('- ')+str(city))
            print(str("Количество городов: ")+str(len(cities)))
            return
    else:
        print(str('Страна ')+str(country_name)+str(' не найдена.'))

fun('USA')



