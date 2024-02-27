from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Consulta,Hospital,Paciente,Pninno,Pjoven,Panciano,Salaespera,Salapendiente,Tipoconsulta
from datetime import datetime


def index(request):
    return HttpResponse("Vista desde consultamedica")

def verpaciente(request,id):
    
    resultado = Paciente.objects.get(id=id)
    prioridad = calcular_prioridad(resultado)
    paciente_a_sala_pendientes(resultado,prioridad)
    print(resultado)
    return HttpResponse("ver paciente " + resultado.nombre + " - modelo "+ resultado._meta.model.__name__ + " - prioridad "+ str(prioridad)  )


def mayorriesgo(request,nro):    
    resultado = listar_pacientes_mayor_riesgo(nro)
    print(resultado)
    mayor_riesgo = ', '.join([str(i.nombre) for i in resultado])
    return HttpResponse("listar_pacientes_mayor_riesgo ->" + mayor_riesgo )

def atender(request):    
    atender_paciente()
    return HttpResponse("atender " )

def liberar(request):    
    liberar_consultas()
    return HttpResponse("liberar" )

def fumadorurgente(request):    
    resultado = listar_pacientes_fumadores_urgentes()
    print(resultado)
    fumadores = '-'.join([str(i) for i in resultado])
    return HttpResponse("fumadorurgente -> " + fumadores )

def masatendido(request):    
    resultado = consulta_mas_pacientes_atendidos()
    print(resultado)
    return HttpResponse("masatendido -> " + resultado.tipoconsulta.nombre +  " - " + resultado.nombreespecialista )

def masanciano(request):    
    resultado = paciente_mas_anciano()
    print(resultado)
    return HttpResponse("masanciano -> " + resultado.nombre)

def optimizar(request):    
    optimizar_atencion()
    return HttpResponse("optimizar" )



def buscarpaciente(id):
    paciente = Pninno.objects.filter(id=id)[:1]
    if paciente:
        return paciente.get()
    paciente = Pjoven.objects.filter(id=id)[:1]
    if paciente:
        return paciente.get()
    paciente = Panciano.objects.filter(id=id)[:1]
    if paciente:
        return paciente.get()
    else:
        return None

def ingreso_paciente(request):
    paciente = registrar_paciente(request.POST)
    prioridad_valor = calcular_prioridad(paciente)
    paciente_a_sala_pendientes(paciente,prioridad_valor)
    atender_paciente()
    return HttpResponse("paciente "+paciente.id.nombre + " registrado" )

def registrar_paciente(paciente):
    nuevo = None
    fecha_nac = datetime.strptime(paciente['fechanac'], '%Y-%m-%d')
    fecha_hoy = datetime.today()
    annos = abs((fecha_hoy.year - fecha_nac.year))
    nuevo_paciente = Paciente(
        nombre=paciente['nombre'], 
        edad=annos,
        nohistoriaclinica=paciente['nohistoriaclinica'],
        fechanac=paciente['fechanac']
        )
    nuevo_paciente.save()
    if annos <= 15:
        nuevo = Pninno(
        id=nuevo_paciente,
        relacionpesoestatura=paciente['relacionpesoestatura']
        )
        nuevo.save()
        
    elif 15 < annos <= 40:
        nuevo = Pjoven(
        id=nuevo_paciente,
        fumador=paciente['fumador'],
        fumadesde=paciente['fumadesde'],
        )
        nuevo.save()
        
    elif annos > 40:
        nuevo = Panciano(
        id=nuevo_paciente,
        tienedieta=paciente['tienedieta'],
        )
        nuevo.save()
    return nuevo


def calcular_prioridad(paciente):
    if hasattr(paciente, 'pninno'):
        if paciente.edad <= 5:
            return paciente.pninno.relacionpesoestatura + 3
        elif paciente.edad <= 12:
            return paciente.pninno.relacionpesoestatura + 2
        else:
            return paciente.pninno.relacionpesoestatura + 1
    elif hasattr(paciente, 'pjoven'):
        fechahoy = datetime.today()
        annoactual = fechahoy.year
        if paciente.pjoven.fumador:
            return (annoactual - paciente.pjoven.fumadesde) / 4 + 2
        else:
            return 2
    elif hasattr(paciente, 'panciano'):
        if paciente.panciano.tienedieta and 60 <= paciente.edad <= 100:
            return paciente.edad / 20 + 4
        else:
            return paciente.edad / 30 + 3
        
def calcular_riesgo(paciente):
    if hasattr(paciente, 'panciano'):
        return (paciente.edad * calcular_prioridad(paciente)) / 100 + 5.3
    else:
        return (paciente.edad * calcular_prioridad(paciente)) / 100

def listar_pacientes_mayor_riesgo(nrohistoria):
    pacientes_mayor_riesgo = []
    paciente_hist = Paciente.objects.get(nohistoriaclinica = nrohistoria)
    pacientes = Paciente.objects.all()
    for patient in pacientes:
        if calcular_riesgo(patient) > calcular_riesgo(paciente_hist):
            pacientes_mayor_riesgo.append(patient)
    return pacientes_mayor_riesgo

def atender_paciente():
    atender_sala_espera()
    pacientes_pendientes = Salapendiente.objects.filter(estado = 1).order_by('-prioridad','-llegada')
    for pacientepend in pacientes_pendientes:
        consultas_disponibles = Consulta.objects.filter(estado='Disponible')
        prioridad_valor = calcular_prioridad(pacientepend.idpaciente)
        riesgo_valor = calcular_riesgo(pacientepend.idpaciente)
        if not consultas_disponibles:
            paciente_a_sala_espera(pacientepend.idpaciente,prioridad_valor,riesgo_valor,pacientepend.llegada)
        else:
            resultadoconsulta = False
            if riesgo_valor > 4:
                resultadoconsulta = pasar_a_consulta(pacientepend.idpaciente,'Urgencias')
            else:
                if hasattr(pacientepend.idpaciente, 'pninno'):
                    resultadoconsulta = pasar_a_consulta(pacientepend.idpaciente,'Pediatria')
                else:
                    resultadoconsulta = pasar_a_consulta(pacientepend.idpaciente,'CGI')
            
            sacar_de_sala_pendientes(pacientepend.idpaciente)
            if not resultadoconsulta:
                paciente_a_sala_espera(pacientepend.idpaciente,prioridad_valor,riesgo_valor,pacientepend.llegada)
    
def atender_sala_espera():
    pacientes_espera = Salaespera.objects.filter(estado = 1).order_by('-prioridad','-llegada')
    for pacienteesp in pacientes_espera:
        consultas_disponibles = Consulta.objects.filter(estado='Disponible')
        if not consultas_disponibles:
            break
        riesgo_valor = calcular_riesgo(pacienteesp.idpaciente)
        resultadoconsulta = False
        if riesgo_valor > 4:
            resultadoconsulta = pasar_a_consulta(pacienteesp.idpaciente,'Urgencias')
        else:
            if hasattr(pacienteesp.idpaciente, 'pninno'):
                resultadoconsulta = pasar_a_consulta(pacienteesp.idpaciente,'Pediatria')
            else:
                resultadoconsulta = pasar_a_consulta(pacienteesp.idpaciente,'CGI')
        if resultadoconsulta:
                sacar_de_sala_espera(pacienteesp.idpaciente)
    
def pasar_a_consulta(paciente,tipoconsulta):
    consulta = Consulta.objects.filter(tipoconsulta__nombre=tipoconsulta,estado='Disponible').first()
    if consulta:
        consulta.estado='Ocupada'
        consulta.cantpacientes+=1
        consulta.save()
        nuevo_registro = Hospital(
            hospital="Sagrado Corazon",
            idconsulta = consulta,
            idpaciente = paciente
        )
        nuevo_registro.save()
        return True
    else:
        return False

def paciente_a_sala_pendientes(pacienteid,val_prioridad):
    paciente_pendiente = Salapendiente(
        idpaciente=pacienteid,
        estado=1,
        llegada=datetime.today(),
        prioridad=val_prioridad
    )
    paciente_pendiente.save()
    
def sacar_de_sala_pendientes(pacienteid):
    paciente_pendiente = Salapendiente.objects.filter(idpaciente__id=pacienteid.id,estado=1).order_by('-llegada')[:1].get()
    paciente_pendiente.estado = 0
    paciente_pendiente.save()
    return paciente_pendiente
    
def paciente_a_sala_espera(paciente,val_prioridad,val_riesgo,llegada_fecha):
    paciente_espera = Salaespera(
        idpaciente=paciente,
        estado=1,
        registrofecha=datetime.today(),
        prioridad=val_prioridad,
        riesgo = val_riesgo,
        llegada = llegada_fecha
    )
    paciente_espera.save()
    
def sacar_de_sala_espera(pacienteid):
    paciente_espera = Salaespera.objects.filter(idpaciente__id=pacienteid.id,estado=1).order_by('-registrofecha')[:1].get()
    paciente_espera.estado = 0
    paciente_espera.save()
    return paciente_espera

def liberar_consultas():
    consultas = Consulta.objects.filter(estado = 'Ocupada')
    for consulta in consultas:
        consulta.estado = 'Disponible'
        consulta.save()
    atender_sala_espera()
        
        

def listar_pacientes_fumadores_urgentes():
    fumadores_urgentes = []
    pacientes = Pjoven.objects.filter(fumador = 1)
    for paciente in pacientes:
        if calcular_riesgo(paciente.id) > 4:
            fumadores_urgentes.append(paciente.id.nombre)
    return fumadores_urgentes

def consulta_mas_pacientes_atendidos():
    consulta = Consulta.objects.order_by('-cantpacientes')[:1].get()
    return consulta

def paciente_mas_anciano():
    paciente = Paciente.objects.filter(salaespera__estado = 1).order_by('-edad')[:1].get()
    return paciente

def optimizar_atencion():
    pacientes_pendientes = list(Salapendiente.objects.filter(estado=1).order_by('-prioridad','-llegada'))
    sorted(pacientes_pendientes, key=lambda p: (calcular_riesgo(p.idpaciente), orden_optimo_r(p.idpaciente), p.prioridad, p.llegada ),reverse=True)
    pacientes_espera = list(Salaespera.objects.filter(estado=1).order_by('-prioridad','-llegada'))    
    listado_pacientes = pacientes_espera + pacientes_pendientes
    
    
    for pacientetmp in listado_pacientes:        
        paciente = pacientetmp.idpaciente
        resultadoconsulta = False
        riesgo_valor = calcular_riesgo(paciente)
        if riesgo_valor > 4:
            resultadoconsulta = pasar_a_consulta(paciente,'Urgencias')
        else:
            if hasattr(paciente, 'pninno'):
                resultadoconsulta = pasar_a_consulta(paciente,'Pediatria')
            else:
                resultadoconsulta = pasar_a_consulta(paciente,'CGI')
        
        if resultadoconsulta:
            if isinstance(pacientetmp,Salaespera):
                sacar_de_sala_espera(paciente)
            if isinstance(pacientetmp,Salapendiente):
                sacar_de_sala_pendientes(paciente) 

    consultas = Consulta.objects.filter(estado = 'Ocupada')
    for consulta in consultas:
        consulta.estado = 'Disponible'
        consulta.save()
    


def orden_optimo_r(paciente):
    if hasattr(paciente, 'pninno') or hasattr(paciente, 'pninno') :
        return -1
    else:
        return 1
    
