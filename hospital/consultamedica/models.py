from django.db import models
import datetime


class Consulta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    cantpacientes = models.PositiveIntegerField(db_column='cantPacientes')
    nombreespecialista = models.CharField(db_column='nombreEspecialista', max_length=50, db_collation='utf8_spanish_ci')
    tipoconsulta = models.ForeignKey('Tipoconsulta', models.DO_NOTHING, db_column='tipoConsulta')
    estado = models.CharField(max_length=10, db_collation='utf8_spanish_ci')

    class Meta:
        managed = False
        db_table = 'Consulta'

class Paciente(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nombre = models.CharField(max_length=50, db_collation='utf8_spanish_ci')
    edad = models.IntegerField()
    nohistoriaclinica = models.IntegerField(db_column='noHistoriaClinica')
    fechanac = models.DateField(db_column='fechaNac', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Paciente'
        
class Hospital(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    hospital = models.CharField(db_column='Hospital', max_length=50, db_collation='utf8_spanish_ci')
    idconsulta = models.ForeignKey(Consulta, models.DO_NOTHING, db_column='IDConsulta')
    idpaciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='IDPaciente')
    registrofecha = models.DateTimeField(db_column='registrofecha', default=datetime.datetime.now(), blank=True)

    class Meta:
        managed = False
        db_table = 'Hospital'


class Panciano(models.Model):
    id = models.OneToOneField('Paciente', models.DO_NOTHING, db_column='ID', primary_key=True)
    tienedieta = models.IntegerField(db_column='tieneDieta')

    class Meta:
        managed = False
        db_table = 'PAnciano'


class Pjoven(models.Model):
    id = models.OneToOneField('Paciente', models.DO_NOTHING, db_column='ID', primary_key=True)
    fumador = models.IntegerField(db_column='fumador')
    fumadesde = models.PositiveIntegerField(db_column='fumaDesde', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PJoven'


class Pninno(models.Model):
    id = models.OneToOneField('Paciente', models.DO_NOTHING, db_column='ID', primary_key=True)
    relacionpesoestatura = models.IntegerField(db_column='relacionPesoEstatura')

    class Meta:
        managed = False
        db_table = 'PNinno'


class Salaespera(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    idpaciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='IDPaciente')
    estado = models.PositiveIntegerField(db_column='estado')
    registrofecha = models.DateTimeField(db_column='registrofecha', default=datetime.datetime.now(), blank=True)
    prioridad = models.FloatField(db_column='prioridad')
    riesgo = models.FloatField(db_column='riesgo')
    llegada = models.DateTimeField(db_column='llegada')

    class Meta:
        managed = False
        db_table = 'SalaEspera'


class Salapendiente(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    idpaciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='IDPaciente')
    estado = models.IntegerField(db_column='estado')
    llegada = models.DateTimeField(db_column='llegada', default=datetime.datetime.now(), blank=True)
    prioridad = models.FloatField(db_column='prioridad')

    class Meta:
        managed = False
        db_table = 'SalaPendiente'


class Tipoconsulta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nombre = models.CharField(max_length=50, db_collation='utf8_spanish_ci')
    descripcion = models.CharField(max_length=150, db_collation='utf8_spanish_ci')

    class Meta:
        managed = False
        db_table = 'TipoConsulta'
