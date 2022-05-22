import asyncio
import json
from random import randint
import sys
import websockets
import time

async def send(websocket, action, data):
    message = json.dumps(
        {
            'action': action,
            'data': data,
        }
    )
    print(message)
    await websocket.send(message)


async def start(auth_token):
    uri = "wss://4yyity02md.execute-api.us-east-1.amazonaws.com/ws?token={}".format(auth_token)
    while True:
        try:
            print('connection to {}'.format(uri))
            async with websockets.connect(uri) as websocket:
                await play(websocket)
        except KeyboardInterrupt:
            print('Exiting...')
            break
        except Exception:
            print('connection error!')
            time.sleep(3)


async def play(websocket):
    while True:
        try:
            request = await websocket.recv()
            print(f"< {request}")
            request_data = json.loads(request)
            if request_data['event'] == 'update_user_list':
                pass
            if request_data['event'] == 'gameover':
                pass
            if request_data['event'] == 'challenge':
                # if request_data['data']['opponent'] == 'favoriteopponent':
                await send(
                    websocket,
                    'accept_challenge',
                    {
                        'challenge_id': request_data['data']['challenge_id'],
                    },
                )
            if request_data['event'] == 'your_turn':
                await process_your_turn(websocket, request_data)
        except KeyboardInterrupt:
            print('Exiting...')
            break
        except Exception as e:
            print('error {}'.format(str(e)))
            break  # force login again


async def process_your_turn(websocket, request_data):
    if randint(0, 4) >= 1:
        await process_move(websocket, request_data)
    else:
        await process_wall(websocket, request_data)


async def process_move(websocket, request_data):
        side = request_data['data']['side']
        pawn_board = [[None for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                string_row = request_data['data']['board'][17*(row*2): 17*(row*2) + 17]
                pawn_board[row][col] = string_row[col * 2]
        for row in range(9):
            for col in range(9):
                if pawn_board[row][col] == side:
                    from_row = row
                    from_col = col
                    to_col = col
                    break
        to_row = from_row + (1 if side == 'N' else -1)
        if pawn_board[to_row][from_col] != ' ':
            to_row = to_row + (1 if side == 'N' else -1)
        await send(
            websocket,
            'move',
            {
                'game_id': request_data['data']['game_id'],
                'turn_token': request_data['data']['turn_token'],
                'from_row': from_row,
                'from_col': from_col,
                'to_row': to_row,
                'to_col': to_col,
            },
        )


async def process_wall(websocket, request_data):
    await send(
        websocket,
        'wall',
        {
            'game_id': request_data['data']['game_id'],
            'turn_token': request_data['data']['turn_token'],
            'row': randint(0, 8),
            'col': randint(0, 8),
            'orientation': 'h' if randint(0, 1) == 0 else 'v'
        },
    )
    


# make by bruno ---
async def where_to_go(side: str, board:list, row:int, col:int):
    if side == 'S':
        for r in range( len(board) ): #make a func from here?
            for c in range( len(board) ):
                if c == col and r == row:
                    #string = 'c: '+ str(c) + ' col: ' + str(col) + ' r: ' + str(r) + ' row:' + str(row)
                    #print( string )
                    if ( col + 2 ) < 17 and board[ row ][ col + 1 ] == ' ': #move to right
                        col += 2
                        return row,col
                    elif ( col - 2 ) > 0 and board[ row ][ col - 1 ] == ' ': #move to left
                        col -= 2
                        return row,col
                    else:
                        row += 2
                        return row,col
    else: # N
        for r in range( len(board) ): #make a func from here?
            for c in range( len(board) ):
                if c == col and r == row:
                    if ( col + 2 ) < 17 and board[ row ][ col + 1 ] == ' ': #move to right
                        col += 2
                        return row,col
                    elif ( col - 2 ) > 0 and board[ row ][ col - 1 ] == ' ': #move to left
                        col -= 2
                        return row,col
                    else:
                        row -= 2
                        return row,col

async def right_back(side: str, board:list, row:int, col:int):
    path = []
    flag_row=row
    flag_col=col

    repeat_move=False
        
    if side == 'S':
        while flag_row!=0:
            #move up
            if(flag_row-1)>0 :
                if board[ flag_row -1 ][ flag_col ] != '-' and board[flag_row-2][flag_col] == ' ':  
                    if ( flag_row-2, flag_col ) not in path: 
                        flag_row -= 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move right
            if (flag_col + 1) < 17:
                if board[ flag_row ][ flag_col + 1 ] != '|' and board[ flag_row ][ flag_col + 2 ] == ' ':
                    if ( flag_row, flag_col+2 ) not in path: 
                        flag_col += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move down
            if (flag_row + 1) < 17 :
                if board[ flag_row +1 ][ flag_col ] != '-' and board[ flag_row +2][ flag_col ] == ' ':
                    if ( flag_row+2, flag_col ) not in path: 
                        flag_row += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move left
            if (flag_col - 1) > -1:
                if board[ flag_row ][ flag_col - 1 ] != '|' and board[ flag_row ][ flag_col - 2 ] == ' ':
                    if ( flag_row, flag_col-2 ) not in path: 
                        flag_col -= 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #if we get here it means we can't move forward without repeating some movement
            if repeat_move:

                start = len(path)-2
                for i in range(start,-1,-1 ):
                    path.append( path[i] )
                    flag_row = path[-1][0]
                    flag_col = path[-1][1]

    else: #N
        while flag_row!=16:
            #move down
            if (flag_row + 1) < 17 :
                if board[ flag_row +1 ][ flag_col ] != '-' and board[ flag_row +2][ flag_col ] == ' ':
                    if ( flag_row+2, flag_col ) not in path: 
                        flag_row += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True
    
            #move right
            if (flag_col + 1) < 17:
                if board[ flag_row ][ flag_col + 1 ] != '|' and board[ flag_row ][ flag_col + 2 ] == ' ':
                    if ( flag_row, flag_col+2 ) not in path: 
                        flag_col += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True
            
            #move up
            if(flag_row-1)>-1 :
                if board[ flag_row -1 ][ flag_col ] != '-' and board[flag_row-2][flag_col] == ' ':  
                    if ( flag_row-2, flag_col ) not in path: 
                        flag_row -= 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move left
            if (flag_col + 1) > -1:
                if board[ flag_row ][ flag_col + 1 ] != '|' and board[ flag_row ][ flag_col + 2 ] == ' ':
                    if ( flag_row, flag_col+2 ) not in path: 
                        flag_col += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True
            
            #if we get here it means we can't move forward without repeating some movement
            if repeat_move:
                start = len(path)-2
                for i in range(start,-1,-1 ):
                    path.append( path[i] )
                    flag_row = path[-1][0]
                    flag_col = path[-1][1]

    return path
            
async def left_back(side: str, board:list, row:int, col:int):
    path = []
    flag_row=row
    flag_col=col

    repeat_move=False
    if side == 'S':
        while flag_row!=0:
            #move up
            if(flag_row-1) > -1 :
                if board[ flag_row -1 ][ flag_col ] != '-' and board[flag_row-2][flag_col] == ' ':  
                    if ( flag_row-2, flag_col ) not in path: 
                        flag_row -= 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move left
            if (flag_col - 1) > -1:
                if board[ flag_row ][ flag_col - 1 ] != '|' and board[ flag_row ][ flag_col - 2 ] == ' ':
                    if ( flag_row, flag_col-2 ) not in path: 
                        flag_col -= 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move down
            if (flag_row + 1) < 17 :
                if board[ flag_row +1 ][ flag_col ] != '-' and board[ flag_row +2][ flag_col ] == ' ':
                    if ( flag_row+2, flag_col ) not in path: 
                        flag_row += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True
            
            #move right
            if (flag_col + 1) < 17:
                if board[ flag_row ][ flag_col + 1 ] != '|' and board[ flag_row ][ flag_col + 2 ] == ' ':
                    if ( flag_row, flag_col+2 ) not in path: 
                        flag_col += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #if we get here it means we can't move forward without repeating some movement
            if repeat_move:

                start = len(path)-2
                for i in range(start,-1,-1 ):
                    path.append( path[i] )
                    flag_row = path[-1][0]
                    flag_col = path[-1][1]

    else: #N
        while flag_row!=16:

            #move down
            if (flag_row + 1) < 17 :
                if board[ flag_row +1 ][ flag_col ] != '-' and board[ flag_row +2][ flag_col ] == ' ':
                    if ( flag_row+2, flag_col ) not in path: 
                        flag_row += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move left
            if (flag_col - 1) > -1:
                if board[ flag_row ][ flag_col - 1 ] != '|' and board[ flag_row ][ flag_col - 2 ] == ' ':
                    if ( flag_row, flag_col-2 ) not in path: 
                        flag_col -= 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move up
            if(flag_row-1) > -1:
                if board[ flag_row -1 ][ flag_col ] != '-' and board[flag_row-2][flag_col] == ' ':  
                    if ( flag_row-2, flag_col ) not in path: 
                        flag_row -= 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #move right
            if (flag_col + 1) < 17:
                if board[ flag_row ][ flag_col + 1 ] != '|' and board[ flag_row ][ flag_col + 2 ] == ' ':
                    if ( flag_row, flag_col+2 ) not in path: 
                        flag_col += 2
                        path.append( ( flag_row , flag_col) )
                        continue
                    else:
                        repeat_move=True

            #if we get here it means we can't move forward without repeating some movement
            if repeat_move:
                start = len(path)-2
                for i in range(start,-1,-1 ):
                    path.append( path[i] )
                    flag_row = path[-1][0]
                    flag_col = path[-1][1]
    return path

async def get_row_col_next_move(path):
    return path[0][0],path[0][1]

async def next_move(side:str,row:int,col:int,right_path:list,left_path:list ):

    if len(right_path) == len(left_path):

        left_score = await path_score(side, right_path ,row, col)
        right_score = await path_score(side, left_path,row, col)
        
        if right_score > left_score:
            new_row, new_col = await get_row_col_next_move(right_path)
            return new_row, new_col
        else:
            new_row, new_col = await get_row_col_next_move(left_path)
            return new_row, new_col
    
    if len(right_path) < len(left_path):
        new_row, new_col = await get_row_col_next_move(right_path)
        return new_row, new_col

    if len(right_path) > len(left_path):
        new_row, new_col = await get_row_col_next_move(left_path)
        return new_row, new_col

async def path_score(side:str, path:list, row:int, col:int):
    score=0
    flag_path=[(row,col)] + path

    if side == 'S':
        for i in range( 1,len(flag_path) ):
            move_from = flag_path[i-1]
            move_to = flag_path[i]
            
            #up 
            if( move_from[0] > move_to[0] and move_from[1] == move_to[1] ):
                score += (16 - move_to[0])

            #down
            if( move_from[0] < move_to[0] and move_from[1] == move_to[1] ):
                score -= (16 - move_to[0])
                        
    else:
        for i in range( 1,len(flag_path) ):
            move_from = flag_path[i-1]
            move_to = flag_path[i]
            
            #up 
            if( move_from[0] > move_to[0] and move_from[1] == move_to[1] ):
                score -= move_from[0]

            #down
            if( move_from[0] < move_to[0] and move_from[1] == move_to[1] ):
                score += move_to[0]

    return score 

async def make_path(side: str, main_board:list , from_row:int, from_col: int):
    len_main_board = len(main_board)
    path=[]

    for row in range (len_main_board): #get index row and index col
        for col in range (len_main_board):
            if row==from_row and col==from_col:
                flag_row=row
                flag_col=col
                break
    
    if side == 'S':
        while flag_row!=0:
            if main_board[ flag_row - 1 ][flag_col] == '-':
                
                path_of_right = await right_back(side,main_board,flag_row,flag_col)
                left_path = await left_back(side,main_board,flag_row,flag_col)
                flag_row, flag_col = await next_move( side, flag_row, flag_col, path_of_right, path_of_left)

                path.append( ( flag_row , flag_col) )
                continue
            
            if main_board[ flag_row - 2 ][flag_col] == ' ':
                flag_row -= 2
                path.append( ( flag_row , flag_col) )
                continue

            if main_board[ flag_row - 2 ][flag_col] == 'S':
                
                path_of_right = await right_back(side,main_board,flag_row,flag_col)
                path_of_left = await left_back(side,main_board,flag_row,flag_col)
                flag_row, flag_col = await next_move( side, flag_row, flag_col, path_of_right, path_of_left)

                path.append( ( flag_row , flag_col) )
                continue

            if ( flag_row - 3 ) > -1 and main_board[ flag_row - 3 ][flag_col] == ' ':
                flag_row -= 4
                path.append( ( flag_row , flag_col) )
                continue
            else:
                if (flag_col + 2) < 17 and main_board[ flag_row - 2 ][flag_col + 2 ] == ' ':
                    flag_row -= 2
                    flag_col += 2
                    path.append( ( flag_row , flag_col) )
                    continue

                if (flag_col - 2) > -1 and main_board[ flag_row - 2 ][flag_col - 2 ] == ' ':
                    flag_row -= 2
                    flag_col -= 2
                    path.append( ( flag_row , flag_col) )
                    continue

                path_of_right = await right_back(side,main_board,flag_row,flag_col)
                path_of_left = await left_back(side,main_board,flag_row,flag_col)
                flag_row, flag_col = await next_move( side, flag_row, flag_col, path_of_right, path_of_left)

                path.append( ( flag_row , flag_col) )
                continue
 
    #else: # with use a N


    return path
# -------

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(start(auth_token))
    else:
        print('please provide your auth_token')