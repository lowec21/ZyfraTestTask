from quarryapp.models import Storage, Trip
from django.shortcuts import render

from shapely.geometry import Point
from shapely.wkt import loads


def main_index(request):
    storage = Storage.objects.first()  # объект склада
    trips = Trip.objects.select_related('current_truck').all()  # объекты поездок

    # Собираем данные для таблицы поездок
    table_trip_data = []
    trip_ids = []

    for trip in trips:  # проходим по всем поездкам
        trip_data = trip.to_json()
        table_trip_data.append(trip_data)  # пополняем список поездок для контекста
        trip_ids.append(trip_data['id'])

    if request.method == 'POST':
        wkt_polygon = "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"  # назначаем координаты полигона
        polygon = loads(wkt_polygon)  # создаём полигон
        before_volume_in_storage = storage.volume_after_unloading

        # перед новым расчётом, меняем значение объёма "до разгрузки" на "после разгрузки" из предыдущего расчёта
        storage.volume_before_unloading = storage.volume_after_unloading
        storage.save()

        for trip in trips:
            trip.coordinates = request.POST.get(str(trip.id))  # присваиваем координаты
            trip.save()

            point_coords = trip.coordinates.split()
            point = Point(point_coords)

            if polygon.contains(point):  # проверяем, попали ли координаты в полигон, если True, производим расчёт

                # считаем сколько сейчас SiO2 на складе в тоннах
                mass_SiO2_in_storage = before_volume_in_storage / 100 * storage.SiO2_procent

                # считаем сколько сейчас Fe на складе в тоннах
                mass_Fe_in_storage = before_volume_in_storage / 100 * storage.Fe_procent

                # считаем сколько в текущем грузе SiO2 в тоннах
                mass_SiO2_in_trip = trip.current_load / 100 * trip.SiO2_procent

                # считаем сколько в текущем грузе Fe в тоннах
                mass_Fe_in_trip = trip.current_load / 100 * trip.Fe_procent

                # прибавляем текущий груз к объёму на складе
                storage.volume_after_unloading += trip.current_load

                # считаем процент SiO2 на складе после разгрузки
                storage.SiO2_procent = round((mass_SiO2_in_storage + mass_SiO2_in_trip) / storage.volume_after_unloading * 100, 1)

                # считаем процент Fe на складе после разгрузки
                storage.Fe_procent = round((mass_Fe_in_storage + mass_Fe_in_trip) / storage.volume_after_unloading * 100, 1)

                before_volume_in_storage = storage.volume_after_unloading

                storage.save()

        # Собираем контекст для POST-запроса
        context = {
            'table_trip_data': table_trip_data,
            'table_storage_data': storage.to_json()
        }

        return render(request, 'quarryapp/tables.html', context)

    # Собираем контекст для GET-запроса
    context = {
        'table_trip_data': table_trip_data,
        'table_storage_data': storage.to_json()
    }

    return render(request, 'quarryapp/tables.html', context)
