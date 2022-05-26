import asyncio
import json
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



# make by bruno ---
async def process_your_turn(websocket, request_data):
    side = request_data['data']['side']

    # make a matrix board
    request_data_board = request_data['data']['board']
    board = [
        list(request_data_board[0:17]),
        list(request_data_board[17:34]),
        list(request_data_board[34:51]),
        list(request_data_board[51:68]),
        list(request_data_board[68:85]),
        list(request_data_board[85:102]),
        list(request_data_board[102:119]),
        list(request_data_board[119:136]),
        list(request_data_board[136:153]),
        list(request_data_board[153:170]),
        list(request_data_board[170:187]),
        list(request_data_board[187:204]),
        list(request_data_board[204:221]),
        list(request_data_board[221:238]),
        list(request_data_board[238:255]),
        list(request_data_board[255:272]),
        list(request_data_board[272:289])
    ]

    # check wall
    wall_orientation = 'h'
    put_wall = False

    if side == 'S':
        wall_row = 1
        if board[3][3] == ' ' and board[3][4] == ' ' and board[3][6] == ' ':
            wall_col = 2
            put_wall = True
        if board[3][11] == ' ' and board[3][12] == ' ' and board[3][13] == ' ':
            wall_col = 5
            put_wall = True
        if board[3][0] == ' ' and board[3][1] == ' ' and board[3][2] == ' ' :
            wall_col = 0
            put_wall = True
        if board[3][14] == ' ' and board[3][15] == ' ' and board[3][16] == ' ':
            wall_col = 7
            put_wall = True


    else:
        wall_row = 6
        if board[13][3] == ' ' and board[13][4] == ' ' and board[13][6] == ' ':
            wall_col = 2
            put_wall = True
        if board[13][11] == ' ' and board[13][12] == ' ' and board[13][13] == ' ':
            wall_col = 5
            put_wall = True
        if board[13][0] == ' ' and board[13][1] == ' ' and board[13][2] == ' ':
            wall_col = 0
            put_wall = True
        if board[13][14] == ' ' and board[13][15] == ' ' and board[13][16] == ' ':
            wall_col = 7
            put_wall = True


    # process wall  
    if put_wall:
        await send(
            websocket,
            'wall',
            {
                'game_id': request_data['data']['game_id'],
                'turn_token': request_data['data']['turn_token'],
                'row': wall_row,
                'col': wall_col,
                'orientation': wall_orientation
            },
        )
    else: # process move  
        await process_move(websocket,request_data,side,board)
    
        
async def process_move(websocket, request_data, side, board):

    #select a pawn
    done = False
    if side == 'S':
        for i, row in reversed( list( enumerate(board) ) ):
            for j, _ in reversed( list( enumerate(row) ) ):
                if board[i][j] == 'S':
                    from_row_double = i
                    from_col_double = j

                    done = True
                    break
            if done:
                break   
    else:
        for i, row in list( enumerate(board) ):
            for j, _ in list( enumerate(row) ):
                if board[i][j] == 'N':
                    from_row_double = i
                    from_col_double = j

                    done = True
                    break
            if done:
                break   


    right_path_array = await right_path(side,board,from_row_double,from_col_double)
    left_path_array = await left_path(side,board,from_row_double,from_col_double)

    to_row_double , to_col_double = await next_move( side, from_row_double, from_col_double, right_path_array, left_path_array)


    to_row = to_row_double/2
    to_col = to_col_double/2

    from_row = from_row_double/2
    from_col = from_col_double/2

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

async def right_path(side: str, board:list, row:int, col:int):
    path = [ ]
    flag_row=row
    flag_col=col

    repeat_move=False
        
    if side == 'S':
        while flag_row!=0:
            #move up
            if(flag_row-1)>-1 :
                if board[ flag_row -1 ][ flag_col ] != '-': 
                
                    if board[flag_row-2][flag_col] == ' ':  
                        if ( flag_row-2, flag_col ) not in path: 
                            flag_row -= 2
                            path.append( ( flag_row , flag_col) )
                            continue
                        else:
                            repeat_move=True
                    
                    if board[flag_row-2][flag_col] == 'N': 
                        # can i jump a pawn?
                        if ( flag_row - 3 ) > -1 and board[ flag_row - 3 ][flag_col] == ' ':
                            flag_row -= 4
                            path.append( ( flag_row , flag_col) )
                            continue
                        else: # diagonal jump
                            if (flag_col + 2) < 17 and board[ flag_row - 2 ][flag_col + 2 ] == ' ':
                                flag_row -= 2
                                flag_col += 2
                                path.append( ( flag_row , flag_col) )
                                continue

                            if (flag_col - 2) > -1 and board[ flag_row - 2 ][flag_col - 2 ] == ' ':
                                flag_row -= 2
                                flag_col -= 2
                                path.append( ( flag_row , flag_col) )
                                continue

            #move right
            if (flag_col + 1) < 17:
                if board[ flag_row ][ flag_col + 1 ] != '|' and board[ flag_row ][ flag_col + 2 ] == ' ':
                    if ( flag_row, flag_col+2 ) not in path: 
                        flag_col += 2
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
                if board[ flag_row +1 ][ flag_col ] != '-': 
                    
                    if board[ flag_row +2][ flag_col ] == ' ':
                        if ( flag_row+2, flag_col ) not in path: 
                            flag_row += 2
                            path.append( ( flag_row , flag_col) )
                            continue
                        else:
                            repeat_move=True

                    if board[flag_row+2][flag_col] == 'S':
                        # can i jump a pawn?
                        if ( flag_row + 3 ) < 17 and board[ flag_row + 3 ][flag_col] == ' ':
                            flag_row += 4
                            
                            path.append( ( flag_row , flag_col) )
                            continue
                        else: # right diagonal jump
                            if (flag_col + 2) < 17 and board[ flag_row + 2 ][flag_col + 2 ] == ' ':
                                flag_row += 2
                                flag_col += 2
                                path.append( ( flag_row , flag_col) )
                                continue

                            #  left diagonal jump
                            if (flag_col - 2) > -1 and board[ flag_row + 2 ][flag_col - 2 ] == ' ':
                                flag_row += 2
                                flag_col -= 2
                                path.append( ( flag_row , flag_col) )
                                continue
    
            #move right
            if (flag_col + 1) < 17:
                if board[ flag_row ][ flag_col + 1 ] != '|' and board[ flag_row ][ flag_col + 2 ] == ' ':
                    if ( flag_row, flag_col+2 ) not in path: 
                        flag_col += 2
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
            if(flag_row-1)>-1 :
                if board[ flag_row -1 ][ flag_col ] != '-' and board[flag_row-2][flag_col] == ' ':  
                    if ( flag_row-2, flag_col ) not in path: 
                        flag_row -= 2
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


async def left_path(side: str, board:list, row:int, col:int):
    path = []
    flag_row=row
    flag_col=col

    repeat_move=False
    if side == 'S':
        while flag_row!=0:
            #move up
            if(flag_row-1)>-1 :
                if board[ flag_row -1 ][ flag_col ] != '-': 
                
                    if board[flag_row-2][flag_col] == ' ':  
                        if ( flag_row-2, flag_col ) not in path: 
                            flag_row -= 2
                            path.append( ( flag_row , flag_col) )
                            continue
                        else:
                            repeat_move=True
                    
                    if board[flag_row-2][flag_col] == 'N': 
                        # can i jump a pawn?
                        if ( flag_row - 3 ) > -1 and board[ flag_row - 3 ][flag_col] == ' ':
                            flag_row -= 4
                            path.append( ( flag_row , flag_col) )
                            continue
                        else: # diagonal jump
                            if (flag_col + 2) < 17 and board[ flag_row - 2 ][flag_col + 2 ] == ' ':
                                flag_row -= 2
                                flag_col += 2
                                path.append( ( flag_row , flag_col) )
                                continue

                            if (flag_col - 2) > -1 and board[ flag_row - 2 ][flag_col - 2 ] == ' ':
                                flag_row -= 2
                                flag_col -= 2
                                path.append( ( flag_row , flag_col) )
                                continue
            
            #move left
            if (flag_col - 1) > -1:
                if board[ flag_row ][ flag_col - 1 ] != '|' and board[ flag_row ][ flag_col - 2 ] == ' ':
                    if ( flag_row, flag_col-2 ) not in path: 
                        flag_col -= 2
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
                if board[ flag_row +1 ][ flag_col ] != '-': 
                    
                    if board[ flag_row +2][ flag_col ] == ' ':
                        if ( flag_row+2, flag_col ) not in path: 
                            flag_row += 2
                            path.append( ( flag_row , flag_col) )
                            continue
                        else:
                            repeat_move=True

                    if board[flag_row+2][flag_col] == 'S':
                        # can i jump a pawn?
                        if ( flag_row + 3 ) < 17 and board[ flag_row + 3 ][flag_col] == ' ':
                            flag_row += 4
                            
                            path.append( ( flag_row , flag_col) )
                            continue
                        else: # right diagonal jump
                            if (flag_col + 2) < 17 and board[ flag_row + 2 ][flag_col + 2 ] == ' ':
                                flag_row += 2
                                flag_col += 2
                                path.append( ( flag_row , flag_col) )
                                continue

                            #  left diagonal jump
                            if (flag_col - 2) > -1 and board[ flag_row + 2 ][flag_col - 2 ] == ' ':
                                flag_row += 2
                                flag_col -= 2
                                path.append( ( flag_row , flag_col) )
                                continue

            #move left
            if (flag_col - 1) > -1:
                if board[ flag_row ][ flag_col - 1 ] != '|' and board[ flag_row ][ flag_col - 2 ] == ' ':
                    if ( flag_row, flag_col-2 ) not in path: 
                        flag_col -= 2
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
            if(flag_row-1) > -1:
                if board[ flag_row -1 ][ flag_col ] != '-' and board[flag_row-2][flag_col] == ' ':  
                    if ( flag_row-2, flag_col ) not in path: 
                        flag_row -= 2
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
    return path[0][0], path[0][1]

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

# -------

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(start(auth_token))
    else:
        print('please provide your auth_token')