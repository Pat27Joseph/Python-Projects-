class Game: 
    def __init__(self):
        self.score = 0
    
    def update_score(self, points):
        self.score += points

    def get_score(self):
        return self.score
    
#Example usage 
game = Game()

#Play the game and update the score
game.update_score(9)
game.update_score(5)
game.update_score(-3)

#Get the first score
final_score = game.get_score()
print("Final Score: ", final_score)