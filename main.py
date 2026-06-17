#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from servicios.sistema import SistemaEntrevistas

app = Flask(__name__)
sistema = SistemaEntrevistas()

# ============================================================================
# RUTAS HTML
# ============================================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/candidatos')
def vista_candidatos():
    return render_template('candidatos.html')


@app.route('/candidatos/nuevo')
def vista_nuevo_candidato():
    return render_template('candidato_nuevo.html')


@app.route('/busquedas')
def vista_busquedas():
    return render_template('busquedas.html')


@app.route('/busquedas/nueva')
def vista_nueva_busqueda():
    return render_template('busqueda_nueva.html')


@app.route('/evaluaciones')
def vista_evaluaciones():
    return render_template('evaluaciones.html')


@app.route('/turnos')
def vista_turnos():
    return render_template('turnos.html')


# ============================================================================
# API CANDIDATOS
# ============================================================================

@app.route('/api/candidatos', methods=['GET', 'POST'])
def api_candidatos():

    if request.method == 'GET':

        lista_candidatos = []

        for candidato in sistema._candidatos:
            lista_candidatos.append(
                candidato.obtener_info_compacta()
            )

        return jsonify(lista_candidatos), 200

    elif request.method == 'POST':

        datos = request.get_json() or {}

        try:

            nuevo_candidato = sistema.registrar_candidato(
                nombre=datos.get('nombre'),
                email=datos.get('email'),
                telefono=datos.get('telefono'),
                anos_experiencia=int(datos.get('anos_experiencia', 0)),
                cv=datos.get('cv', '')
            )

            if nuevo_candidato and 'habilidades' in datos:
                nuevo_candidato.agregar_multiples_habilidades(
                    datos['habilidades']
                )

            return jsonify({
                "status": "success",
                "id": nuevo_candidato.id if nuevo_candidato else None
            }), 201

        except Exception as e:

            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400


# ============================================================================
# API BUSQUEDAS
# ============================================================================

@app.route('/api/busquedas', methods=['GET', 'POST'])
def api_busquedas():

    if request.method == 'GET':

        lista_busquedas = []

        for busqueda in sistema._busquedas:
            lista_busquedas.append(
                busqueda.obtener_info_compacta()
            )

        return jsonify(lista_busquedas), 200

    elif request.method == 'POST':

        datos = request.get_json() or {}

        try:

            nueva_busqueda = sistema.crear_busqueda(
                titulo=datos.get('titulo_puesto'),
                descripcion=datos.get('descripcion'),
                salario_min=float(datos.get('salario_minimo', 0)),
                salario_max=float(datos.get('salario_maximo', 0)),
                skills=datos.get('skills_requeridos', []),
                exp_min=int(datos.get('experiencia_minima', 0))
            )

            return jsonify({
                "status": "success",
                "id": nueva_busqueda.id if nueva_busqueda else None
            }), 201

        except Exception as e:

            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400


# ============================================================================
# API EVALUACIONES
# ============================================================================

@app.route('/api/evaluaciones', methods=['GET', 'POST'])
def api_evaluaciones():

    if request.method == 'GET':

        lista_evaluaciones = []

        for e in sistema._servicio_evaluacion.obtener_todas_evaluaciones():

            lista_evaluaciones.append({
                "id": e.id,
                "candidato_id": e.candidato.id,
                "candidato_nombre": e.candidato.nombre,
                "busqueda_id": e.busqueda.id,
                "busqueda_titulo": e.busqueda.titulo_puesto,
                "evaluador": e.evaluador,
                "resultado": e.resultado.value,
                "puntuacion": e.puntuacion,
                "comentarios": e.comentarios
            })

        return jsonify(lista_evaluaciones), 200

    elif request.method == 'POST':

        datos = request.get_json() or {}

        try:

            nueva_eval = sistema.evaluar_candidato(
                candidato_id=int(datos.get('candidato_id')),
                busqueda_id=int(datos.get('busqueda_id')),
                evaluador=datos.get('evaluador'),
                resultado=datos.get('resultado'),
                puntuacion=float(datos.get('puntuacion', 0)),
                comentarios=datos.get('comentarios', '')
            )

            if not nueva_eval:
                raise Exception(
                    "No se pudo crear la evaluación. Verifique candidato y búsqueda."
                )

            return jsonify({
                "status": "success",
                "id": nueva_eval.id
            }), 201

        except Exception as e:

            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400


# ============================================================================
# API TURNOS
# ============================================================================

@app.route('/api/turnos', methods=['GET', 'POST'])
def api_turnos():

    if request.method == 'GET':

        lista_turnos = []

        for t in sistema._servicio_calendario.obtener_todos_turnos():

            lista_turnos.append({
                "id": t.id,
                "evaluacion_id": t.evaluacion.id,
                "candidato_nombre": t.evaluacion.candidato.nombre,
                "puesto": t.evaluacion.busqueda.titulo_puesto,
                "fecha": str(t.fecha),
                "hora": t.hora,
                "entrevistador": t.entrevistador,
                "sala": t.sala,
                "estado": t.estado.value
            })

        return jsonify(lista_turnos), 200

    elif request.method == 'POST':

        datos = request.get_json() or {}

        try:

            nuevo_turno = sistema.agendar_turno(
                evaluacion_id=int(datos.get('evaluacion_id')),
                fecha=datos.get('fecha'),
                hora=datos.get('hora'),
                entrevistador=datos.get('entrevistador'),
                sala=datos.get('sala')
            )

            if not nuevo_turno:
                raise Exception(
                    "No se pudo agendar el turno. Verifique evaluación aprobada y disponibilidad."
                )

            return jsonify({
                "status": "success",
                "id": nuevo_turno.id
            }), 201

        except Exception as e:

            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )