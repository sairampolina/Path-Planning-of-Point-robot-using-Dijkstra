
"""

@author: sairam polina
"""

import copy
import numpy as np
import cv2
import heapq as hq
import time

def createObstacles(canvas):
    """
    This function takes canvas as input
    returns: Canvas with obstacles drawn in it
    """
    height,width,_ = canvas.shape
    # print(shape)
    for i in range(width):
        for j in range(height):
            if(i-5<=0) or (i-395>=0) or (j-5 <=0) or (j-245>=0):
                canvas[j][i] = [0,255,0]

            if ((i-300)**2+(j-65)**2-(45**2))<=0:
                canvas[j][i] = [0,255,0]
            
            if (j+(0.57*i)-218.53)>=0 and (j-(0.57*i)+10.04)>=0 and (i-240)<=0 and (j+(0.57*i)-310.04)<=0 and (j-(0.57*i)-81.465)<=0 and (i-160)>=0:
                canvas[j][i] = [0,255,0]

            if ((j+(0.316*i)-71.1483)>=0 and (j+(0.857*i)-145.156)<=0 and (j-(0.114*i)-60.909)<=0) or ((j-(1.23*i)-28.576)<=0 and (j-(3.2*i)+202.763)>=0 and (j-(0.114*i)-60.909)>=0):
                canvas[j][i] = [0,255,0]
    # cv2.imshow('canvas',canvas)
    # cv2.waitKey(5000)
    # cv2.destroyAllWindows()
    return canvas

def getInputs(canvas):
    """
    This function takes input from user for Initial node state and Goal node
    returns: Initial state and final state of the puzzle to be solved
    """
    initial_state = []
    final_state = []
    while True:
        while True:
            x_start = input("Enter the X - Co-ordinate of Start Node: ")
            if(int(x_start)<0 or int(x_start)>canvas.shape[1]-1):
                print("Enter Valid X - Co-ordinate")
                continue
            else:
                initial_state.append(int(x_start))
                break
        
        while True:
            y_start = input("Enter the Y - Co-ordinate of Start Node: ")
            if(int(y_start)<0 or int(y_start)>canvas.shape[0]-1):
                print("Enter Valid Y - Co-ordinate")
                continue
            else:
                initial_state.append(int(y_start))
                break
        
        if(canvas[canvas.shape[0]-1 - initial_state[1]][initial_state[0]][1]==255):
            print("Entered start node is inside obstacle space")
            initial_state.clear()
        else:
            break
    
    while True:
        while True:
            x_goal = input("Enter the X - Co-ordinate of Goal Node: ")
            if(int(x_goal)<0 or int(x_goal)>canvas.shape[1]-1):
                print("Enter Valid X - Co-ordinate")
                continue
            else:
                final_state.append(int(x_goal))
                break
        while True:
            y_goal = input("Enter the Y - Co-ordinate of Goal Node: ")
            if(int(y_goal)<0 or int(y_goal)>canvas.shape[0]-1):
                print("Enter Valid Y - Co-ordinate")
                continue
            else:
                final_state.append(int(y_goal))
                break
       
        # print(canvas[canvas.shape[0]-1 - final_state[1]][final_state[0]])
        if(canvas[canvas.shape[0]-1 - final_state[1]][final_state[0]][1]==255):
            print("Entered Goal node is inside obstacle space")
            final_state.clear()
        else:
            break
    return initial_state,final_state


# 8 fuctions are defined which represent the motion in 8 directions
def move_up(node,canvas):
  
    next_node = copy.deepcopy(node)
    # if(canvas.shape[0] - (current_node[1]+1)>0) and (canvas[canvas.shape[0]-current_node[1]+1][current_node[0]][0]<255):
    #     current_node = [current_node[0], canvas.shape[0] - (current_node[1] + 1)]
    if(next_node[1]-1 > 0) and (canvas[next_node[1]-1][next_node[0]][1]<255):
        next_node[1] = next_node[1] - 1 
        return True,tuple(next_node)
    else:
        return False,tuple(next_node)

def move_down(node,canvas):
   
    next_node = copy.deepcopy(node)
    
    if(next_node[1]+1 < canvas.shape[0]) and (canvas[next_node[1]+1][next_node[0]][1]<255):
        next_node[1] = next_node[1] + 1 
        return True,tuple(next_node)
    else:
        return False,tuple(next_node)
    

def move_left(node,canvas):
    
    next_node = copy.deepcopy(node)
    if(next_node[0]-1 > 0) and (canvas[next_node[1]][next_node[0]-1][1]<255):
        next_node[0] = next_node[0] - 1 
        return True,tuple(next_node)
    else:
        return False,tuple(next_node)


def move_right(node,canvas):
    
    next_node = copy.deepcopy(node)
    # if(canvas.shape[0] - (current_node[1]+1)>0) and (canvas[canvas.shape[0]-current_node[1]+1][current_node[0]][0]<255):
    #     current_node = [current_node[0], canvas.shape[0] - (current_node[1] + 1)]
    if(next_node[0]+1 < canvas.shape[1]) and (canvas[next_node[1]][next_node[0]+1][1]<255):
        next_node[0] = next_node[0] + 1 
        return True,tuple(next_node)
    else:
        return False,tuple(next_node)

def move_top_right(node,canvas):
    
    next_node = copy.deepcopy(node)
    # if(canvas.shape[0] - (current_node[1]+1)>0) and (canvas[canvas.shape[0]-current_node[1]+1][current_node[0]][0]<255):
    #     current_node = [current_node[0], canvas.shape[0] - (current_node[1] + 1)]
    if(next_node[1]-1 > 0) and (next_node[0]+1 <canvas.shape[1]) and (canvas[next_node[1]-1][next_node[0]+1][1]<255):
        next_node[1] = next_node[1] - 1
        next_node[0] = next_node[0] + 1 
        return True,tuple(next_node)
    else:
        return False,tuple(next_node)

def move_bottom_right(node,canvas):
   
    next_node = copy.deepcopy(node)
    if(next_node[1]+1 < canvas.shape[0]) and (next_node[0]+1 <canvas.shape[1]) and (canvas[next_node[1]+1][next_node[0]+1][1]<255):
        next_node[1] = next_node[1] + 1
        next_node[0] = next_node[0] + 1 
        return True,tuple(next_node)
    else:
        return False,tuple(next_node)

def move_bottom_left(node,canvas):
   
    next_node = copy.deepcopy(node)
    if(next_node[1]+1 < canvas.shape[0]) and (next_node[0]-1 >0) and (canvas[next_node[1]+1][next_node[0]-1][1]<255):
        next_node[1] = next_node[1] + 1
        next_node[0] = next_node[0] - 1 
        return True,tuple(next_node)
    else:
        return False,tuple(next_node)

def move_top_left(node,canvas):
  
    next_node = copy.deepcopy(node)
    if(next_node[1]-1 > 0) and (next_node[0]-1 >0) and (canvas[next_node[1]-1][next_node[0]-1][1]<255):
        next_node[1] = next_node[1] - 1
        next_node[0] = next_node[0] - 1 
        return True,tuple(next_node)
    else:
        return False,tuple(next_node)

def Dijkstra(initial_state,final_state,canvas):
    
    # implementation of Dijkstra algorithm
    open_list = []
    
    '''open list is a heap queue which has the cost as the key to sort the heap'''
   
    hq.heapify(open_list)
    hq.heappush(open_list,[0,initial_state,initial_state])  # [0: cost, 1: parent node, 2: present node]
   
    closed_list = {}
    
    '''Closed list is a dictionary which has key as the current node and value as the parent node'''
    
    back_track_flag = False
    while(len(open_list)>0):
        
        node = hq.heappop(open_list)
        
        closed_list[(node[2][0],node[2][1])] = node[1] #Converting to tuple because the key for dictionary should be immutable
        present_cost = node[0] #Present node cost to come
        if list(node[2]) == final_state: #Checks if the popped node is goal node
            back_track_flag = True
            print("Back Track") #Back tracking starts
            break #come out of the while loop
        
        flag,next_node = move_up(node[2],canvas)
        if(flag):
            if next_node not in closed_list:
                temp = False
                for i in range(len(open_list)):
                    if(open_list[i][2] == list(next_node)):
                        temp = True
                        if((present_cost+1)<open_list[i][0]): # Updating the cost and parent node
                            open_list[i][0] = present_cost+1
                            open_list[i][1] = node[2]
                            hq.heapify(open_list)
                        break
                if(not temp): #Pushing the node if it is not present in both closed and open lists
                    hq.heappush(open_list,[present_cost+1, node[2], list(next_node)])
                    hq.heapify(open_list)
                    
        
        flag,next_node = move_top_right(node[2],canvas)
        if(flag):
            if next_node not in closed_list:
                temp = False
                for i in range(len(open_list)):
                    if(open_list[i][2] == list(next_node)):
                        temp = True
                        if((present_cost+1.4)<open_list[i][0]):# Updating the cost and parent node
                            open_list[i][0] = present_cost+1.4
                            open_list[i][1] = node[2]
                            hq.heapify(open_list)
                        break
                if(not temp):#Pushing the node if it is not present in both closed and open lists
                    hq.heappush(open_list,[present_cost+1.4, node[2], list(next_node)])
                    hq.heapify(open_list)
                   
                
        flag,next_node = move_right(node[2],canvas)
        if(flag):
            if next_node not in closed_list:
                temp = False
                for i in range(len(open_list)):
                    if(open_list[i][2] == list(next_node)):
                        temp = True
                        if((present_cost+1)<open_list[i][0]):# Updating the cost and parent node
                            open_list[i][0] = present_cost+1
                            open_list[i][1] = node[2]
                            hq.heapify(open_list)
                        break
                if(not temp):#Pushing the node if it is not present in both closed and open lists
                    hq.heappush(open_list,[present_cost+1, node[2], list(next_node)])
                    hq.heapify(open_list)
            
    
        flag,next_node = move_bottom_right(node[2],canvas)
        if(flag):
            if next_node not in closed_list:
                temp = False
                for i in range(len(open_list)):
                    if(open_list[i][2] == list(next_node)):
                        temp = True
                        if((present_cost+1.4)<open_list[i][0]):# Updating the cost and parent node
                            open_list[i][0] = present_cost+1.4
                            open_list[i][1] = node[2]
                            hq.heapify(open_list)
                        break
                if(not temp):#Pushing the node if it is not present in both closed and open lists
                    hq.heappush(open_list,[present_cost+1.4, node[2], list(next_node)])
                    hq.heapify(open_list)
        
        flag,next_node = move_down(node[2],canvas)
        if(flag):
            if next_node not in closed_list:
                temp = False
                for i in range(len(open_list)):
                    if(open_list[i][2] == list(next_node)):
                        temp = True
                        if((present_cost+1)<open_list[i][0]):# Updating the cost and parent node
                            open_list[i][0] = present_cost+1
                            open_list[i][1] = node[2]
                            hq.heapify(open_list)
                        break
                if(not temp):#Pushing the node if it is not present in both closed and open lists
                    hq.heappush(open_list,[present_cost+1, node[2], list(next_node)])
                    hq.heapify(open_list)
        
        flag,next_node = move_bottom_left(node[2],canvas)
        if(flag):
            if next_node not in closed_list:
                temp = False
                for i in range(len(open_list)):
                    if(open_list[i][2] == list(next_node)):
                        temp = True
                        if((present_cost+1.4)<open_list[i][0]):# Updating the cost and parent node
                            open_list[i][0] = present_cost+1.4
                            open_list[i][1] = node[2]
                            hq.heapify(open_list)
                        break
                if(not temp):#Pushing the node if it is not present in both closed and open lists
                    hq.heappush(open_list,[present_cost+1.4, node[2], list(next_node)])
                    hq.heapify(open_list)
        
        flag,next_node = move_left(node[2],canvas)
        if(flag):
            if next_node not in closed_list:
                temp = False
                for i in range(len(open_list)):
                    if(open_list[i][2] == list(next_node)):
                        temp = True
                        if((present_cost+1)<open_list[i][0]):# Updating the cost and parent node
                            open_list[i][0] = present_cost+1
                            open_list[i][1] = node[2]
                            hq.heapify(open_list)
                        break
                if(not temp):#Pushing the node if it is not present in both closed and open lists
                    hq.heappush(open_list,[present_cost+1, node[2], list(next_node)])
                    hq.heapify(open_list)
        
        flag,next_node = move_top_left(node[2],canvas)
        if(flag):
           
            if next_node not in closed_list:
                temp = False
                for i in range(len(open_list)):
                    if(open_list[i][2] == list(next_node)):
                        temp = True
                        if((present_cost+1.4)<open_list[i][0]):# Updating the cost and parent node
                            open_list[i][0] = present_cost+1.4
                            open_list[i][1] = node[2]
                            hq.heapify(open_list)
                        break
                if(not temp):#Pushing the node if it is not present in both closed and open lists
                    hq.heappush(open_list,[present_cost+1.4, node[2], list(next_node)])
                    hq.heapify(open_list)


        hq.heapify(open_list)
   
    if(back_track_flag):
        #Call the backtrack function
        back_track(initial_state,final_state,closed_list,canvas)
    
def back_track(initial_state,final_state,closed_list,canvas):
    
    """
    This function takes input of initial , final states and canvas
    returns: Produces the visulalization video and optimal path between goal and start nodes
    """
    
    explored_nodes = closed_list.keys() #Returns all the nodes that are explored
   
    path_stack = [] #A List which stores co-ordinates from start to goal
    
    for explored_node in explored_nodes:
        canvas[explored_node[1]][explored_node[0]] = [0,0,255] #assigning red color to explored nodes
        cv2.imshow("Nodes Exploring Visulization",canvas)
        cv2.waitKey(1)
    
    parent_node = closed_list[tuple(final_state)]
    
    path_stack.append(final_state) #Appending the final state for starting the loop
    
    while(parent_node!=initial_state):
        
        path_stack.append(parent_node)
        parent_node = closed_list[tuple(parent_node)]
       
    
    cv2.circle(canvas,tuple(initial_state),3,(255,0,0),-1)
    cv2.circle(canvas,tuple(final_state),3,(255,0,0),-1)
    path_stack.append(initial_state) #Appending the initial state for breaking the loop
    
    while(len(path_stack)>0):
        path_node = path_stack.pop()
        canvas[path_node[1]][path_node[0]] = [255,255,0]
    
    cv2.imshow("Nodes Exploring Visulization",canvas)        

if __name__=='__main__':
    
    canvas = np.ones((250,400,3),dtype="uint8")
    canvas=createObstacles(canvas)
    initial_state,final_state = getInputs(canvas)
    
    #Changing world coordinates to map co-ordinates:
    initial_state[1] = canvas.shape[0]-1 - initial_state[1]
    final_state[1] = canvas.shape[0]-1 - final_state[1]
    
    Dijkstra(initial_state,final_state,canvas)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()