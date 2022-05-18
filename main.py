import asyncio
import json
from random import randint
import string
import sys
from tkinter import E
from numpy import true_divide
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


async def make_path(side: str, main_board:list , from_row:int, from_col: int):
    len_main_board = len(main_board)
    path=[]
    if side == 'S':
        for row in range (len_main_board): #make a func from here?
            for col in range (len_main_board):
                if row==from_row and col==from_col:
                    # apply the rules to make a path
                    flag_row=row
                    flag_col=col
                    while flag_row!=0:

                        string = 'flag_row: ' + str(flag_row) + ' flag_col: '+ str(flag_col)
                        print( string )
                        
                        if main_board[ flag_row - 1 ][flag_col] == '-':
                            flag_row,flag_col = await where_to_go(side, main_board,flag_row,flag_col)
                            path.append( ( flag_row , flag_col) )
                            continue
                        
                        if main_board[ flag_row - 2 ][flag_col] == ' ':
                            flag_row -= 2
                            path.append( ( flag_row , flag_col) )
                            continue

                        if main_board[ flag_row - 2 ][flag_col] == 'S':
                            flag_row,flag_col = await where_to_go(side, main_board,flag_row,flag_col)
                            path.append( ( flag_row , flag_col) )
                            continue

                        #if main_board[ flag_row - 2 ][flag_col] == 'N':
                        if ( flag_row - 3 ) > 0 and main_board[ flag_row - 3 ][flag_col] == ' ':
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

                            flag_row,flag_col = await where_to_go(side, main_board,flag_row,flag_col)
                            path.append( ( flag_row , flag_col) )

                        '''
                        if main_board[ flag_row - 2 ][flag_col] == ' ' and main_board[ flag_row - 1 ][flag_col] == ' ':
                            flag_row -= 2
                        else:
                            if main_board[ flag_row - 2 ][flag_col] == 'N': #when it is in front of N
                                if (flag_row - 4 ) > 0 : # can you jump it?
                                        #string = 'flag_row: ' + str(flag_row) + ' flag_col: '+ str(flag_col)
                                        #print( string )
                                        flag_row -= 4
                                else:
                                    if (flag_col + 2) < 17 and main_board[ flag_row - 3 ][flag_col + 2 ] == ' ': # can you jump up to the right?
                                        flag_row -= 2
                                        flag_col += 2
                                    elif (flag_col - 2) > 0 and main_board[ flag_row - 3 ][flag_col - 2 ] == ' ':# can you jump up to the left?
                                        flag_row -= 2
                                        flag_col -= 2
                                    else:
                                        flag_row,flag_col = await where_to_go(side, main_board,flag_row,flag_col)
                            else:
                                flag_row,flag_col = await where_to_go(side, main_board,flag_row,flag_col)
                        path.append( ( flag_row , flag_col) )      
                        '''   
    #else: # with use a N


    return path
# -------

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(start(auth_token))
    else:
        print('please provide your auth_token')