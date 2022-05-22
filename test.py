import unittest
from main import next_move, right_back, left_back, path_score, make_path
from boards import *

class TestRightBack(unittest.IsolatedAsyncioTestCase):
    async def test_right_back_1(self):
        check_list = [ (8,6),(6,6),(4,6),(6,6),(8,6),(10,6),(12,6),(12,8),(10,8),(8,8),(6,8),(4,8),(2,8),(0,8)]
        check_path = await right_back('S', board_1, 8, 4)
        self.assertEqual( check_path, check_list )

    async def test_right_back_2(self):
        check_list = [ (8,6),(10,6),(12,6),(10,6),(8,6),(6,6),(4,6),(4,8),(6,8),(8,8),(10,8),(12,8),(14,8),(16,8) ]
        check_path = await right_back('N', board_2, 8, 4)
        self. assertEqual( check_path, check_list )

class TestLeftBack(unittest.IsolatedAsyncioTestCase):
    async def test_left_back_1(self):
        check_list = [(8,10),(10,10),(12,10),(10,10),(8,10),(6,10),(4,10),(4,8),(6,8),(8,8),(10,8),(12,8),(14,8),(16,8)]
        check_path = await left_back('N', board_3, 8, 12)
        self.assertEqual( check_path, check_list )

    async def test_left_back_2(self):
        check_list = [ (8,10),(6,10),(4,10),(6,10),(8,10),(10,10),(12,10),(12,8),(10,8),(8,8),(6,8),(4,8),(2,8),(0,8) ]
        check_path = await left_back('S', board_4, 8, 12)
        self.assertEqual( check_path, check_list )

class TestPathScore(unittest.IsolatedAsyncioTestCase):
    async def test_path_score_1(self):
        path = [(4,8),(6,8),(8,8),(10,8),(12,8),(14,8),(16,8)]
        check_score = await path_score('N', path, 4, 8 )
        self.assertEqual( check_score, 66 )
    
    async def test_path_score_2(self):
        path = [(4,8),(2,8),(0,8),]
        check_score = await path_score('S', path, 4, 8 )
        self.assertEqual( check_score, 30 )

class TestNextMove(unittest.IsolatedAsyncioTestCase):
    async def test_next_move_1(self):
        right_path = [ (8,6),(6,6),(4,6),(6,6),(8,6),(10,6),(12,6),(12,8),(10,8),(8,8),(6,8),(4,8),(2,8),(0,8)]
        left_path = [ (8,2),(8,0),(6,0),(4,0),(2,0),(0,0) ]
        row,col = await next_move('S',8,4, right_path, left_path)
        self.assertAlmostEqual( row, 8 )
        self.assertAlmostEqual( col, 2 )


class TestMakePath(unittest.IsolatedAsyncioTestCase):
    async def test_make_path(self):
        path = [ (14,4),(12,4),(10,4),(8,4),(8,2),(8,0),(6,0),(4,0),(2,0),(0,0) ]
        check_path = await make_path('S', board_1, 16, 4)
        self.assertListEqual( check_path, path )


if __name__ == "__main__":
   unittest.main()