# -*- coding: utf-8 -*-

import random

#GARDAMOS AS POSICIONS REFERIDAS AS FILAS, COLUMNAS E CADROS.
filas = []
for i in range(0,81,9):
	filas.append(range(i,i+9))

columnas = []
for i in range(9):
	columnas.append(range(i,81,9))

cadros = []
for i in range(1,4):
	for z in range(0,9,3):
		cadros.append([range(x,x+3) for x in range((27*(i-1))+z,(27*i)+z,9)])
cadros = [c[0]+c[1]+c[2] for c in cadros]
	
#CLASE PARA GARDAR DATOS DAS CASILLAS
class casilla():
	def __init__(self,valor):
		self.posibles = range(1,10)
		random.shuffle(self.posibles)
		self.posibles_copia = self.posibles[:]
		self.valor = valor
		if valor:
			self.marcada = True
		else:
			self.marcada = False
	def __repr__(self):
		return ("("+str(self.marcada)+","+str(self.posibles_copia)+
				","+str(self.posibles)+","+str(self.valor)+")")
				
#FUNCIÓNS PARA COMPROBAR SE UN SUDOKU É CORRECTO
def comprobar_filas(taboleiro):
	for i in range(0,81,9):
		if 0 in [x.valor for x in taboleiro[i:i+9]]:
			return False
		elif len(list(set([x.valor for x in taboleiro[i:i+9]]))) != 9:
			return False
	return True
	
def comprobar_columnas(taboleiro):
	for i in range(9):
		if 0 in [x.valor for x in taboleiro[i:81:9]]:
			return False
		elif len(list(set([x.valor for x in taboleiro[i:81:9]]))) != 9:
			return False
	return True
	
def comprobar_cadros(taboleiro):
	for cadro in cadros:
		if 0 in [taboleiro[x].valor for x in cadro]:
			return False
		elif len(list(set([taboleiro[x].valor for x in cadro]))) != 9:
			return False
	return True

def comprobar_sudoku(taboleiro):
	if (comprobar_filas(taboleiro) and comprobar_columnas(taboleiro)
		and comprobar_cadros(taboleiro)):
		return True
	else:
		return False
				
				
#FUNCIÓN PARA COMPROBAR AS POSIBILIDADES DE CADA CASILLA 
#CANDO SE ENGADE UN VALOR A UNHA
def quitar_posibles(taboleiro,num,pos,copia=True):
	fila_afectada = filas[pos/9]
	columna_afectada = columnas[pos-9*(pos/9)]
	for cadro in cadros:
		if pos in cadro:
			cadro_afectado = cadro
	casillas_afectadas = fila_afectada+columna_afectada+cadro_afectado
	casillas_afectadas.remove(pos)
	for c in casillas_afectadas:
		if copia:
			if num in taboleiro[c].posibles_copia and not taboleiro[c].marcada:
					taboleiro[c].posibles_copia.remove(num)
		else:
			taboleiro[c].posibles = taboleiro[c].posibles_copia
	return taboleiro

#COMPROBAMOS SE O TABOLEIRO É IDÓNEO PARA AVANZAR
def valido(taboleiro,pos):
	fila_a_comprobar = filas[pos/9]
	columna_a_comprobar = columnas[pos-9*(pos/9)]
	for cadro in cadros:
		if pos in cadro:
			cadro_a_comprobar = cadro
	casillas_a_comprobar = fila_a_comprobar+columna_a_comprobar+cadro_a_comprobar
	casillas_a_comprobar = list(set([x for x in casillas_a_comprobar if x>pos]))
	
	#COMPROBAMOS SE ALGUNHA CASILLA SE QUEDOU SEN POSIBLES NÚMEROS
	posibles_por_casilla = [taboleiro[x].posibles_copia for x in casillas_a_comprobar
							if not taboleiro[x].marcada]
	if [] in posibles_por_casilla:
		
		print "ERROR"
		print u"> casilla sen posibles números"
		print "pos: ",pos
		print "casilla_propia: ",taboleiro[pos]
		for c in casillas_a_comprobar:
			if not taboleiro[c].posibles_copia:
				print "pos casilla error: ",c
				print "casilla do error: ", taboleiro[c]
		debuxar_sudoku(taboleiro)
		print "-"*30
		
		return False
		
	#COMPROBAMOS O NÚMERO DE POSIBLES NÚMEROS NA FILA,COLUMNA E CADRO
	posibles_fila_casilla = [taboleiro[x].posibles_copia for x in fila_a_comprobar if x>pos]
	posibles_columna_casilla = [taboleiro[x].posibles_copia for x in columna_a_comprobar if x>pos]
	posibles_cadro_casilla = [taboleiro[x].posibles_copia for x in cadro_a_comprobar if x>pos]
	
	count = -1
	que = ["fila","columna","cadro"]
	
	for lista_posibles in [posibles_fila_casilla,posibles_columna_casilla,posibles_cadro_casilla]:
	
		count += 1
		
		posibles_total = []
		for i in lista_posibles:
			posibles_total += i
		
		if len(list(set(posibles_total))) < len(lista_posibles):
		
			print "ERROR"
			print ">",que[count]
			print "pos: ",pos
			print "casilla_propia: ",taboleiro[pos]
			print "posibles casillas: ",lista_posibles
			print "posibles total: ",posibles_total
			print "len posibles:", len(list(set(posibles_total))), "necesarios:", len(lista_posibles)
			debuxar_sudoku(taboleiro)
			print "-"*30
		
			return False
	return True
	
#CREAMOS/RESOLVEMOS O SUDOKU
def crear_sudoku():
	#CREAMOS O TABOLEIRO A 0	
	casillas = []
	for i in range(81):
		casillas.append(casilla(0))
	#RESOLVER
	for p in range(len(casillas)):
		if casillas[p].posibles:
			for n in casillas[p].posibles:
				print "pos:",p, "intentando con... ",n
				for u in casillas:
					u.posibles_copia = u.posibles[:]
				casillas = quitar_posibles(casillas,n,p)
				#COMPROBAMOS SE O NÚMERO 'n' É VALIDO
				if valido(casillas,p):		
					casillas[p].valor = n
					casillas[p].marcada = True
					casillas = quitar_posibles(casillas,n,p,False)
					break
				if n == casillas[p].posibles[-1]:
					return casillas
		else:
			return casillas
	return casillas

#FUNCIÓN PARA DEBUXAR O SUDOKU NO TERMINAL
def debuxar_sudoku(taboleiro):
	for c in range(len(taboleiro)):
		if c%27 == 0:
			print
		if c%9 == 0:
			print
		if c%3 == 0:
			print " ",
		print taboleiro[c].valor,
	print
	print
	print "Sudoku correcto? ", comprobar_sudoku(taboleiro)

#PROBAS	
intentos = 0
while True:
	intentos += 1
	casillas = crear_sudoku()
	if not 0 in [c.valor for c in casillas]:
		break
	else:
		debuxar_sudoku(casillas)
		
print "intentos: %r" % intentos

#AMOSAMOS O RESULTADO
debuxar_sudoku(casillas)