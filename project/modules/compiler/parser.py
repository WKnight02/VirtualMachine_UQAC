"""
The class Parser
"""

__all__ = ['parser']
class parser():
	"""Class Parser
	"""
	Error = []
	Commandes = []
	operations = {
		#Data manipulation
		"DTA":1,
		"SET":2,
		"LD":2,
		"ST":2,
		"MV":2,
		#Arithmetic
		"ADD":2,
		"SUB":2,
		"MUL":2,
		"DIV":2,
		#logic
		"OR":2,
		"AND":2,
		"XOR":2,
		"NOT":1,
		#comparaison
		"LT":2,
		"GT":2,
		"LE":2,
		"GE":2,
		"EQ":2,
		"EZ":1,
		"NZ":1,
		#Flow control
		"JMP":1,
		"JMZ":1,
		"JMO":1,
		"JMC":1,
		#Autre
		"NOP":0'
		"HLT":0
	}
	def __init___(self,*args,**kargs):
		"""
			initialise la classe parser
		"""
		super.__init___()
		
		
		
	
	def parse(self,text):
	
	
		#adada 
		ligne =0
		#Separe les lignes de commande par ligne
		commands = text.split("\n")
		for com in commands:
			ligne = ligne +1
			#Supprime les espaces inutiles
			command = com.split(" ")
			while command.count(''): del command[command.index('')]
			#Recupere la commande nettoyer
			CleanCom = command
			#Regarde si la commande contient plus de 3 parametre
			try:
				print(CleanCom[0])
				if len(CleanCom[1:]) > self.operations[str(CleanCom[0])]:
					#Ajoute une entree dans le tableau d erreur avec la ligne correspondante
					self.Error.append("Ligne"+str(ligne)+": Trop d'argument")
				elif len(CleanCom) !=0:
					#Ajoute une commande au tableau Commandes
					self.Commandes.append(CleanCom)
			except:
				self.Error.append("Ligne"+str(ligne)+": Operateur inconnue")

Text = "ADD 2 3 \n NZ 3 \n \n ADD \n NOP"
parses = parser()
parses.parse(Text)
print(parses.Commandes)
print(parses.Error)
		
