import random
import os
import sys, tty, termios


class _Getch:
  def __call__(self):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(3)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class Game:
  
  CELLS = ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
          (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
          (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
          (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
          (0, 4), (1, 4), (2, 4), (3, 4), (4, 4))

  def getkey(self):
    inkey = _Getch()
    while(1):
      k = inkey()
      if k != '':
        break
    if k == '\x1b[A':
      move = "UP"
    elif k=='\x1b[B':
      move = "DOWN"
    elif k=='\x1b[C':
      move = "RIGHT"
    elif k=='\x1b[D':
      move = "LEFT"
    else:
      move = None
    return move
  
  
  def __init__(self):
    
    self.pos = random.sample(self.CELLS, 3)
    self.player, self.monster, self.door = self.pos
    self.clear_screen()
    print("#"*5, end="")
    print(" Welcome to Reach or Die ", end="")
    print("#"*5)
    print("Move towards the door. Beware a monster also awaits you!")
    print("[M]: Monster\n[X]:Player\nDoor is hidden")
    print("NOTE: Use ARROW KEYS to MOVE, UP, RIGHT and LEFT\n")
    self.draw_grid()
    input("Hit any key to continue")
    while True:
      self.clear_screen()
      self.draw_grid()
      self.player_move()
      if self.check_player_status():
        won = True
        break
      self.monster_move()
      if self.check_killed():
        won = False
        break
    self.clear_screen()
    if won:
      print("Hooray! Door found. You Won!")
      input("Hit enter to continue")
    else:
      print("Oo, it seems monster killed. Better luck next time!")
      input("Hit enter to continue")
      
  def clear_screen(self):
    os.system('clear')
    
  
  def check_killed(self):
    
    mx, my = self.monster
    px, py = self.player
    if mx == px and my == py:
      return True
    else:
      return False
  def check_player_status(self):
    
    dx, dy = self.door
    px, py = self.player
    if dx == px and dy == py:
      return True
    else:
      return False
  
  def get_valid_moves(self, obj):
    x, y = obj
    valid_moves = ["DOWN", "UP", "RIGHT", "LEFT"]
    if x == 0:
      valid_moves.remove("LEFT")
    elif x == 4:
      valid_moves.remove("RIGHT")
    elif y == 0:
      valid_moves.remove("UP")
    elif y == 4:
      valid_moves.remove("DOWN")
    return valid_moves
  
  # function to get monster move
  def monster_move(self):
    
    mx, my = self.monster
    dx, dy = self.door
    valid_moves = self.get_valid_moves(self.monster)
    if ("UP" in valid_moves) and (my - 1 != dy and mx != dx):
      my -= 1
    elif ("DOWN" in valid_moves) and (my + 1 != dy and mx != dx):
      my += 1
    elif ("LEFT" in valid_moves) and (mx - 1 != dx and my != dy):
      mx -= 1
    elif ("RIGHT" in valid_moves) and (mx + 1 != dx and my != dy):
      mx += 1
    self.monster = mx, my
    
  # function to get player move
  def player_move(self):
    
    valid_moves = self.get_valid_moves(self.player)
    x, y = self.player
    print("You can move:", end="")
    for move in valid_moves:
      print("{} ".format(move), end="")
    print("\n")
    #player_move = input("Please enter your move: ").upper()
    while True:
      player_move = self.getkey()
      if player_move == None:
        print("Invalid Key. Hit key again")
        continue
      else:
        break;
    if player_move in valid_moves:
      if player_move == "UP":
        y -= 1
      elif player_move == "DOWN":
        y += 1
      elif player_move == "RIGHT":
        x += 1
      elif player_move == "LEFT":
        x -= 1
    else:
      self.player_move()
    self.player = x, y
    
    
  # To draw grid on the console   
  def draw_grid(self):
    
    print("="*20)
    px, py = self.player
    mx, my = self.monster
    dx, dy = self.door
    for i in range(0, 5):
      print("|", end="")
      for j in range(0, 5):
        if j == px and i == py:
          print("X", end="")
        elif j == mx and i == my:
          print("M", end="")
        else:
          print("_", end="")
        if j < 4:
          print("|", end="")
      print("|")
    print("="*20)
    
    
    
Game()
