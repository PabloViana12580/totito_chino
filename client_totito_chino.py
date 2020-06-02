"""
Universidad del Valle de Guatemala
Inteligencia artificial - proyecto final 
Catedrático: Samuel Chavez 
Pablo Viana - 16091
"""

import socketio
import numpy as np
import random

sio = socketio.Client()

direccion = 'http://localhost:4000'
print("nombre de usuario")
username = input()
tournamentID = 1

sio.connect(direccion)

def movimiento_valido(matrix):
	posible_movement = []
	for i in range(len(matrix)):
		for k in range(len(matrix[0])):
			if(matrix[i][k] == 99):
				posible_movement.append((i,k))

	return posible_movement

@sio.event
def connect():
    print("Conectado")
    sio.emit('signin', {'user_name':username, 'tournament_id': tournamentID, 'user_role':'player'})
 
@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def ready(data):
	#Aqui se tira el movimiento con la señal play
	tablero = data['board']
	print("tablero actual")
	print(tablero[0])
	print(tablero[1])
	print("\nHaciendo tiro\n")

	"""

	Parte random del proyecto 

	while(bandera):
		direccion = randrange(2)
		posicion = randrange(30)
		if(movimiento_valido(direccion, posicion, tablero)):
			bandera = False

	print("movimiento escogido:\n ")
	movimiento.insert(0,direccion)
	movimiento.insert(1,posicion)
	print(movimiento[0])
	print(movimiento[1])
	"""
	"""
	while i < len(tablero[0]):
		#print(i)
		if tablero[0][i] == 99:
			movimiento.insert(0,0)
			movimiento.insert(1,i)
			i = 0
			break
		else:
			i + 1

	if not movimiento:
		while i < len(tablero[1]):
			if tablero[1][i] == 99:
				movimiento.insert(0,1)
				movimiento.insert(1,i)
				i = 0
				break
			else:
				i + 1
	"""
	movimiento = ia_dotsandboxes(tablero, data['player_turn_id'], 3)

	sio.emit('play', {'player_turn_id':data['player_turn_id'], 'tournament_id': tournamentID, 'game_id':data['game_id'], 'movement':[movimiento[0], movimiento[1]]})


@sio.event
def finish(data):
	print("El juego se termino")
	sio.emit('player_ready',{'tournament_id':tournamentID, 'game_id':data['game_id'], 'player_turn_id':data['player_turn_id']})


def ia_dotsandboxes(mat, play_id, lookahead):
	moves = movimiento_valido(mat)

	bestScore = -99999
	cont = 0

	for i in range(len(mat)):
		for j in range(len(mat[0])):
			if mat[i][j] == 99:
				cont = cont + 1
	#Si es el primer movimiento
	if cont >= 59:
		return random.choice(moves)
	else:
		for move in moves:
			punteo = minimax_algo(mat, move, int(lookahead), False, int(play_id), -99999, 99999)

			if punteo > bestScore:
				bestScore = punteo
				moves.clear()

			if punteo <= bestScore:
				moves.append(move)

	return random.choice(moves)

def minimax_algo(tab, jugada, k, flag, id_, alpha, beta):
	movimientos_posibles = movimiento_valido(tab)

	if flag == False:
		id_ = (id_ % 2) + 1

	if k == 0:
		return pointingmove(tab, jugada, id_)

	if flag:
		maximum = -99999

		for move in movimientos_posibles:
			punteo = minimax_algo(tab, jugada, k - 1, False, id_, alpha, beta)

			maximum = max(maximum, punteo)
			alpha = max(alpha, punteo)

			if beta <= alpha:
				break

		return maximum
	else:
		minimum = 99999

		for move in movimientos_posibles:
			punteo = minimax_algo(tab, jugada, k - 1, True, id_, alpha, beta)

			minimum = min(minimum, punteo)
			beta = min(beta, punteo)

			if beta <= alpha:
				break

		return minimum

def pointingmove(tablero,movement,id_):
        n = 6
        p_tanterior = 0
        p_turno = 0

        sum = 0
        cont = 0
        n = 6
        
        for i in range(len(tablero[0])):
            if ((i + 1) % n) != 0:
                if tablero[0][i] != 99 and tablero[0][i + 1] != 99 and tablero[1][cont + sum] != 99 and tablero[1][cont + sum + 1] != 99:
                    p_tanterior = p_tanterior + 1
                sum = sum + n
            else:
                cont = cont + 1
                sum = 0

        tablero[movement[0]][movement[1]] = 0

        sum = 0
        cont = 0

        for i in range(len(tablero[0])):
            if ((i + 1) % n) != 0:
                if tablero[0][i] != 99 and tablero[0][i + 1] != 99 and tablero[1][cont + sum] != 99 and tablero[1][cont + sum + 1] != 99:
                    p_turno = p_turno + 1
                sum = sum + n
            else:
                cont = cont + 1
                sum = 0
        
        if p_tanterior < p_turno:
            if id_ == 1:
                if p_turno - p_tanterior == 2:
                    tablero[movement[0]][movement[1]] = 2
                elif p_turno - p_tanterior == 1:
                    tablero[movement[0]][movement[1]] = 1
            else:
                if p_turno - p_tanterior == 2:
                    tablero[movement[0]][movement[1]] = -2
                elif p_turno - p_tanterior == 1:
                    tablero[movement[0]][movement[1]] = -1

        punteoFinal = abs(p_tanterior - p_turno)
        return punteoFinal
        

