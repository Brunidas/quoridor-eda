import unittest
from main import  right_path, left_path, path_score,next_move
from boards import *

class TestRightPath(unittest.IsolatedAsyncioTestCase):
    async def test_right_path_1(self):
        check_list = [(14, 4), (14, 6), (14, 8), (12, 8), (10, 8), (8, 8), (6, 8), (4, 8), (2, 8), (0, 10)]
        check_path = await right_path('S', board_8, 14, 2)
        self.assertEqual( check_path, check_list )
    
    async def test_right_path_2(self):
        check_list = [(14, 16), (16, 16), (16, 14), (16, 12), (14, 12), (14, 10), (14, 8), (12, 8), (10, 8), (8, 8), (6, 8), (4, 8), (2, 8), (0, 10)]
        check_path = await right_path('S', board_8, 14, 14)
        self. assertEqual( check_path, check_list )
    
    async def test_right_path_3(self):
        check_list = [(2, 2), (4, 2), (6, 2), (8, 2), (10, 2), (12, 2), (12, 4), (12, 6), (12, 8), (14, 8), (16, 8)]
        check_path = await right_path('N', board_8, 0, 2)
        self. assertEqual( check_path, check_list )

    async def test_right_path_4(self):
        check_list = [(2, 14), (4, 14), (6, 14), (8, 14), (10, 14), (12, 14), (12, 16), (10, 16), (8, 16), (6, 16), (4, 16), (2, 16), (0, 16), (2, 16), (4, 16), (6, 16), (8, 16), (10, 16), (12, 16), (12, 14), (10, 14), (8, 14), (6, 14), (4, 14), (2, 14), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (12, 10), (12, 8), (14, 8), (16, 8)]
        check_path = await right_path('N', board_8, 0, 14)
        self. assertEqual( check_path, check_list )

    async def test_right_path_5(self):
        check_list = [(14, 2), (12, 2), (10, 2), (8, 2), (6, 2), (4, 2), (4, 4), (4, 6), (4, 8), (2, 8), (0, 8)]
        check_path = await right_path('S', board_9, 16, 2)
        self. assertEqual( check_path, check_list )
    
    async def test_right_path_6(self):
        check_list = [(14, 14), (12, 14), (10, 14), (8, 14), (6, 14), (4, 14), (4, 16), (6, 16), (8, 16), (10, 16), (12, 16), (14, 16), (16, 16), (14, 16), (12, 16), (10, 16), (8, 16), (6, 16), (4, 16), (4, 14), (6, 14), (8, 14), (10, 14), (12, 14), (14, 14), (14, 12), (12, 12), (10, 12), (8, 12), (6, 12), (4, 12), (4, 10), (4, 8), (2, 8), (0, 8)]
        check_path = await right_path('S', board_9, 16, 14)
        self. assertEqual( check_path, check_list )

    async def test_right_path_7(self):
        check_list = [ (2, 4), (2, 6), (2, 8), (4, 8), (6, 8), (8, 8), (10, 8), (12, 8), (14, 8), (16, 8)]
        check_path = await right_path('N', board_9, 2, 2)
        self. assertEqual( check_path, check_list )
    
    async def test_right_path_8(self):
        check_list = [(2, 16), (0, 16), (0, 14), (0, 12), (2, 12), (2, 10), (2, 8), (4, 8), (6, 8), (8, 8), (10, 8), (12, 8), (14, 8), (16, 8)]
        check_path = await right_path('N', board_9, 2, 14)
        self. assertEqual( check_path, check_list )

class TestLeftPath(unittest.IsolatedAsyncioTestCase):
    async def test_left_path_1(self):
        check_list = [(14, 0), (16, 0), (16, 2), (16, 4), (14, 4), (14, 6), (14, 8), (12, 8), (10, 8), (8, 8), (6, 8), (4, 8), (2, 8), (0, 10)]
        check_path = await left_path('S', board_8, 14, 2)
        self.assertEqual( check_path, check_list )

    async def test_left_path_2(self):
        check_list = [(14, 12), (14, 10), (14, 8), (12, 8), (10, 8), (8, 8), (6, 8), (4, 8), (2, 8), (0, 10)]
        check_path = await left_path('S', board_8, 14, 14)
        self.assertEqual( check_path, check_list )

    async def test_left_path_3(self):
        check_list = [(2, 2), (4, 2), (6, 2), (8, 2), (10, 2), (12, 2), (12, 0), (10, 0), (8, 0), (6, 0), (4, 0), (2, 0), (0, 0), (2, 0), (4, 0), (6, 0), (8, 0), (10, 0), (12, 0), (12, 2), (10, 2), (8, 2), (6, 2), (4, 2), (2, 2), (2, 4), (4, 4), (6, 4), (8, 4), (10, 4), (12, 4), (12, 6), (12, 8), (14, 8), (16, 8)]
        check_path = await left_path('N', board_8, 0, 2)
        self.assertEqual( check_path, check_list )

    async def test_left_path_4(self):
        check_list = [(2, 14), (4, 14), (6, 14), (8, 14), (10, 14), (12, 14), (12, 12), (12, 10), (12, 8), (14, 8), (16, 8)]
        check_path = await left_path('N', board_8, 0, 14)
        self.assertEqual( check_path, check_list )

    async def test_left_path_5(self):
        check_list = [(14, 2), (12, 2), (10, 2), (8, 2), (6, 2), (4, 2), (4, 0), (6, 0), (8, 0), (10, 0), (12, 0), (14, 0), (16, 0), (14, 0), (12, 0), (10, 0), (8, 0), (6, 0), (4, 0), (4, 2), (6, 2), (8, 2), (10, 2), (12, 2), (14, 2), (14, 4), (12, 4), (10, 4), (8, 4), (6, 4), (4, 4), (4, 6), (4, 8), (2, 8), (0, 8)]
        check_path = await left_path('S', board_9, 16, 2)
        self.assertEqual( check_path, check_list )

    async def test_left_path_6(self):
        check_list = [(12, 14), (10, 14), (8, 14), (6, 14), (4, 14), (4, 12), (4, 10), (4, 8), (2, 8), (0, 8)]
        check_path = await left_path('S', board_9, 14, 14)
        self.assertEqual( check_path, check_list )
    
    async def test_left_path_7(self):
        check_list = [(0, 0), (2, 0), (0, 0), (0, 2), (0, 4), (2, 4), (2, 6), (2, 8), (4, 8), (6, 8), (8, 8), (10, 8), (12, 8), (14, 8), (16, 8)]
        check_path = await left_path('N', board_9, 0, 2)
        self.assertEqual( check_path, check_list )

    async def test_left_path_8(self):
        check_list = [(0, 12), (2, 12), (2, 10), (2, 8), (4, 8), (6, 8), (8, 8), (10, 8), (12, 8), (14, 8), (16, 8)]
        check_path = await left_path('N', board_9, 0, 14)
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


if __name__ == "__main__":
   unittest.main()