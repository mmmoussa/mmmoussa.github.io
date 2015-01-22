from tkinter import *
from tkinter import messagebox
from egyptGame import EgyptGame

class egyptGameGUI():

	def __init__(self, master):		

		# --- Window Menu ---
		menu = Menu(master)
		master.config(menu=menu)
		fileMenu = Menu(menu)
		menu.add_cascade(label="File", menu=fileMenu)
		fileMenu.add_command(label="Start game", command=self.newGame)
		fileMenu.add_separator()
		fileMenu.add_command(label="About", command=self.about)
		fileMenu.add_separator()
		fileMenu.add_command(label="Exit", command=root.quit)

		# --- Character info display ---
		self.characterFrame = Frame(master, bd=2, relief=SOLID, height=50, bg="black")
		self.characterFrame.pack(fill=X)
		self.playerLabel = Label(self.characterFrame, text="Player", anchor=E, bg="black", fg="white")
		self.vLabel = Label(self.characterFrame, text=" vs. ", bg="black", fg="white")
		self.enemyLabel = Label(self.characterFrame, text="Enemy", anchor=W, bg="black", fg="white")
		self.playerLabel.grid(row=0, column=0, sticky=W)
		self.vLabel.grid(row=0, column=1)
		self.enemyLabel.grid(row=0, column=2, sticky=E)
		self.characterFrame.grid_columnconfigure(1, weight=2)

		# --- Main info display ---
		self.mainFrame = Frame(master)
		self.mainFrame.pack(fill=BOTH, expand=1)
		self.mainMessage = Label(self.mainFrame, justify=LEFT, anchor=W)
		self.mainMessage.pack(side=TOP, fill=X)

		# --- Action button location ---
		self.actionFrame = Frame(master, height=30)
		self.actionFrame.pack(fill=X)

		# --- Initial start button ---
		self.startNewGame = Button(self.actionFrame, text="Start Game", command=self.newGame)
		self.startNewGame.pack(side=RIGHT, padx=5)

		# --- Buttons that will be needed ---
		self.newGameButton = Button(self.actionFrame, text="Continue", command=self.choosePlayer)
		self.submitNameButton = Button(self.actionFrame, text="Submit", command=self.confirmPlayer)
		self.startGameButton = Button(self.actionFrame, text="Continue", command=self.startGame)
		self.submitAttackButton = Button(self.actionFrame, text="Submit", command=self.playerTurnResult)
		self.playerNextButton = Button(self.actionFrame, text="Continue", command=self.enemyTurn)
		self.enemyNextButton = Button(self.actionFrame, text="Continue", command=self.playerTurn)
		self.endRoundButton = Button(self.actionFrame, text="Continue", command=self.roundEnd)
		self.newEnemyButton = Button(self.actionFrame, text="Continue", command=self.newEnemy)
		self.newRoundButton = Button(self.actionFrame, text="Continue", command=self.playerTurn)

	# --- About messagebox ---
	def about(self):
		messagebox.showinfo(title="About", message="This game is created by Mohamed Moussa in support of a free and democratic Egypt.")

	# --- Running game ---
	def newGame(self):
		for widget in self.actionFrame.children.values():
			widget.pack_forget()
		for widget in self.mainFrame.children.values():
			widget.pack_forget()
		self.mainMessage.pack(side=TOP, fill=X)

		self.game = EgyptGame()
		self.game.setup(self.mainMessage)
		self.newGameButton.pack(side=RIGHT, padx=5)

	def choosePlayer(self):
		self.newGameButton.pack_forget()
		self.mainMessage.config(text="")
		self.mainMessage.pack_forget()
		self.nameLabel = Label(self.mainFrame, text="Name:", justify=LEFT)
		self.nameLabel.pack(side=LEFT, anchor=N)
		self.playerName = StringVar()
		self.nameEntry = Entry(self.mainFrame, textvariable=self.playerName)
		self.nameEntry.pack(side=LEFT, anchor=N)
		self.submitNameButton.pack(side=RIGHT, padx=5)

	def confirmPlayer(self):
		self.nameLabel.pack_forget()
		self.nameEntry.pack_forget()
		self.submitNameButton.pack_forget()
		self.mainMessage.pack(side=TOP, fill=X)
		self.game.player.name = self.playerName.get()
		if self.game.player.name == "":
			self.game.player.name = "Too lazy to enter name"
			messagebox.showinfo(title="So lazy!", message="You're so lazy you didn't even enter a name! Well, I've given you one.")
		self.mainMessage.config(text='Your name is "{}".'.format(self.game.player.name))
		self.startGameButton.pack(side=RIGHT, padx=5)

	def startGame(self):
		self.startGameButton.pack_forget()
		self.updateCharacters()
		self.mainMessage.config(text="")
		self.playerTurn()

	def playerTurn(self):
		try:
			self.newRoundButton.pack_forget()
		except:
			pass
		try:
			self.enemyNextButton.pack_forget()
		except:
			pass

		if self.game.enemy.health == 0:
			self.game.roundEnd()
		else:
			self.game.playerAttackChoice(self.mainMessage, self.mainFrame)
			self.submitAttackButton.pack(side=RIGHT, padx=5)

	def playerTurnResult(self):
		self.submitAttackButton.pack_forget()
		self.game.playerAttackResult(self.mainMessage)
		self.updateCharacters()
		if self.game.enemy.health == 0:
			self.endRoundButton.pack(side=RIGHT, padx=5)
		else:
			self.playerNextButton.pack(side=RIGHT, padx=5)

	def enemyTurn(self):
		self.playerNextButton.pack_forget()
		self.game.enemyTurn(self.mainMessage)
		self.updateCharacters()
		if self.game.player.health == 0:
			self.endRoundButton.pack(side=RIGHT, padx=5)
		else:
			self.enemyNextButton.pack(side=RIGHT, padx=5)

	def roundEnd(self):
		try:
			self.endRoundButton.pack_forget()
		except:
			pass

		if self.game.player.health == 0:
			self.mainMessage.config(text="Oh no! Sisi defeated you! How unfortunate! Better luck next time!")
			self.startNewGame.pack(side=RIGHT, padx=5)
		elif self.game.gameEnded:
			self.mainMessage.config(text="Congratulations! You defeated Sisi and liberated Egypt!")
			self.startNewGame.pack(side=RIGHT, padx=5)
		elif self.game.enemy.health == 0:
			self.game.roundEnd(self.mainMessage)
			self.newEnemyButton.pack(side=RIGHT, padx=5)
		else:
			pass

	def newEnemy(self):
		self.newEnemyButton.pack_forget()	
		self.game.newEnemy(self.mainMessage)
		if self.game.gameEnded == True:
			self.endRoundButton.pack(side=RIGHT, padx=5)
		else:
			self.updateCharacters()
			self.newRoundButton.pack(side=RIGHT, padx=5)

	def updateCharacters(self):
		self.playerLabel.config(text=self.game.player)
		self.enemyLabel.config(text=self.game.enemy)

# --- Setting up window ---
root = Tk()
root.minsize(600,300)
root.geometry("600x300")
rTitle = root.title("Sisi Fighter")

egyptGameGUI(root)

root.mainloop()
