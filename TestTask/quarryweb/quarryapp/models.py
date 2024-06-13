from django.db import models


class DumpTruck(models.Model):
    board_number = models.CharField('Бортовой номер самосвала', max_length=20)
    model = models.CharField('Модель самосвала', max_length=20)
    max_load = models.IntegerField('Максимальная грузоподъёмность, тонн')


class Trip(models.Model):
    current_load = models.IntegerField('Текущий вес груза, тонн')
    SiO2_procent = models.FloatField('Содержание диоксида кремния, %')
    Fe_procent = models.FloatField('Содержание железа, %')
    current_truck = models.ForeignKey('DumpTruck', on_delete=models.PROTECT)
    coordinates = models.CharField('Координаты выгрузки', max_length=10,  null=True)

    def to_json(self):
        return {
            'id': self.id,
            'current_load': self.current_load,
            'Fe_procent': self.Fe_procent,
            'SiO2_procent': self.SiO2_procent,
            'current_truck': self.current_truck,
            'board_number': self.current_truck.board_number,
            'max_load': self.current_truck.max_load,
            'model': self.current_truck.model,
            'coordinates': self.coordinates,
            'overload': round((self.current_load - self.current_truck.max_load) / self.current_truck.max_load * 100)
            if self.current_load > self.current_truck.max_load else 0
        }


class Storage(models.Model):
    name = models.CharField('Название склада', null=False, max_length=20)
    volume_before_unloading = models.IntegerField('Объём до разгрузки, тонн', null=False)
    volume_after_unloading = models.IntegerField('Объём после разгрузки, тонн', null=False)
    SiO2_procent = models.FloatField()
    Fe_procent = models.FloatField()

    def to_json(self):
        return {
            'name': self.name,
            'volume_before_unloading': self.volume_before_unloading,
            'volume_after_unloading': self.volume_after_unloading,
            'SiO2_procent': self.SiO2_procent,
            'Fe_procent': self.Fe_procent
        }

    def __str__(self):
        return f'{self.SiO2_procent}% SiO2, {self.Fe_procent}% Fe'
