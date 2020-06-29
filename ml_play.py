dir=0
center=0
class MLPlay:
    def __init__(self, player):
        self.player = player
        global dir
        global center
        if self.player == "player1":
            self.player_no = 0
            dir=1
        elif self.player == "player2":
            self.player_no = 1
            dir=1
        elif self.player == "player3":
            self.player_no = 2
            dir=-1
        elif self.player == "player4":
            self.player_no = 3
            dir=-1
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        #print(self.car_lane)
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            global center
            speed_ahead = 100
            speed_backl = 100
            speed_backr = 100
            if self.car_pos[0] <= 30: # left bound
                #print("lb")
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 600: # right bound
                #print("rb")
                grid.add(3)
                grid.add(6)
                grid.add(9)
            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    if(len(scene_info["coins"])>0):
                        for i in range (len(scene_info["coins"])):
                            #print(scene_info["coins"][i])
                            self.coins_pos = scene_info["coins"][i]
                            coin_x = self.car_pos[0] - self.coins_pos[0] # x relative position
                            coin_y = self.car_pos[1] - self.coins_pos[1] # y relative position
                            if(coin_y<180 and coin_y>-10 and coin_x<105 and coin_x>15):
                                grid.add(11)    #left
                                #print('left')  
                            if( coin_y<180 and coin_y>-10 and coin_x<-15 and coin_x>-105):
                                grid.add(10)    #right
                                #print('right')
                            if(coin_y<180 and coin_y>-10 and coin_x<15 and coin_x>-15):
                                grid.add(12)    
                                #print('stay')  
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y <300:
                            grid.add(2)
                            if y < 200:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y > 80 and y < 150:
                            grid.add(3)
                        elif y < -80 and y > -120:
                            speed_backr = car["velocity"]
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y > 80 and y < 150:
                            grid.add(1)
                        elif y < -80 and y > -120:
                            speed_backl = car["velocity"]
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
                    if(abs(y)<=85 and x>0 and x<=45):
                        grid.add(13)
                    if(abs(y)<=85 and x<0 and x>=-45):
                        grid.add(14)
                
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            global dir
            #if self.player_no == 0:
            #    print(grid)
            #print(self.car_pos[0])
            #print(dir)

            if len(grid) == 0:
                return ["SPEED"]
            else:
                if(dir==-1):
                    if (2 not in grid): # Check forward
                        if (12 in grid):
                            return ["SPEED"]
                        if(13 in grid):#l
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if(14 in grid):#r
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            return ["SPEED"]
                    else:
                        if (5 in grid): # NEED to BRAKE
                            if (4 not in grid) and (1 not in grid): # turn left 
                                if self.car_vel < speed_ahead:
                                    if (10 in grid) and (3 not in grid) and (6 not in grid) : # turn right
                                        dir=1
                                        return ["SPEED", "MOVE_RIGHT"]
                                    else:
                                        dir=-1
                                        return ["SPEED", "MOVE_LEFT"]
                                else:
                                    dir=-1
                                    return ["BRAKE", "MOVE_LEFT"]
                            elif (6 not in grid) and (3 not in grid): # turn right
                                if self.car_vel < speed_ahead:
                                        dir=1
                                        return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    dir=1
                                    return ["BRAKE", "MOVE_RIGHT"]
                            else : 
                                if self.car_vel < speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    return ["BRAKE"]
                        if (self.car_pos[0] <= 40 ):
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if (self.car_pos[0] >= 590 ):
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        if (12 in grid):
                            return ["SPEED"]
                        if(13 in grid):#l
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if(14 in grid):#r
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]

                      
                      
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid): # turn left 
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid): # turn right
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 not in grid) and (7 not in grid): # turn left 
                            dir=-1
                            return ["MOVE_LEFT"]    
                        if (6 not in grid) and (9 not in grid): # turn right
                            dir=1
                            return ["MOVE_RIGHT"]
                        else:
                            return ["SPEED"]
                if(dir==1):
                    if (2 not in grid): # Check forward
                        if (12 in grid):
                            return ["SPEED"]
                        if(13 in grid):#l
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if(14 in grid):#r
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            return ["SPEED"]
                    else:
                        if (5 in grid): # NEED to BRAKE
                            if (6 not in grid) and (3 not in grid): # turn right
                                if self.car_vel < speed_ahead:
                                    dir=1
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    dir=1
                                    return ["BRAKE", "MOVE_RIGHT"]
                                    
                            elif (4 not in grid) and (1 not in grid): # turn left 
                                if self.car_vel < speed_ahead:
                                    dir=-1
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    dir=-1
                                    return ["BRAKE", "MOVE_LEFT"]
                            else : 
                                if self.car_vel < speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    return ["BRAKE"]
                        if (self.car_pos[0] >= 590 ):
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        if (self.car_pos[0] <= 40 ):
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if (12 in grid):
                            return ["SPEED"]
                        if(14 in grid):#r
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        if(13 in grid):#l
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid): # turn right
                            dir=1
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid): # turn left 
                            dir=-1
                            return ["SPEED", "MOVE_LEFT"]
                        if (6 not in grid) and (9 not in grid): # turn right
                            dir=1
                            return ["MOVE_RIGHT"]
                        if (4 not in grid) and (7 not in grid): # turn left 
                            dir=-1
                            return ["MOVE_LEFT"]
                        else:
                            return ["SPEED"]
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass