#!/usr/bin/env python
from hudfixer import Vec2, Rect, anchor_centrally

class TestReanchorCalculation(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_anchor_centrally(self):
        old_rect = Rect(Vec2(829.44, 544.0), Vec2(1024.0, 768.64))
        reanchored_rect = anchor_centrally(old_rect)

        self.assertEqual(reanchored.start.x, 1410)
        self.assertEqual(reanchored.start.y, 810)
        self.assertEqual(reanchored.end.x, 1674)
        self.assertEqual(reanchored.end.y, 1074)
        self.assertEqual(reanchored.scale.x, 1440)
        self.assertEqual(reanchored.scale.y, 1080)

if __name__ == '__main__':
    unittest.main()