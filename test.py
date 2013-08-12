#!/usr/bin/env python
import unittest
from hudfixer import (
    Vec2, Rect, LolRect, reanchor_centrally, get_abs_scaled_rect,
    get_lol_scaled_rect, parse_fragment, parse_fragments,
    compile_fragment, compile_fragments, reanchor_centrally_in_raf
)


class TestReanchoring(unittest.TestCase):
    def setUp(self):
        self.fragment = "Type: Icon\n\
            Name: MinimapFrame\n\
            Group: Minimap\n\
            Enabled: 1\n\
            KeepMaxScale: 1\n\
            AlwaysRespond: 0\n\
            Draggable: 0\n\
            Layer: 2\n\
            Anchor: 1,1\n\
            Rect: 829.44,544.0 - 1024.0,768.64 / 1024x768\n\
            Alpha: 1\n\
            Texture: HUDAtlas\n\
            UV: 87,7 - 391,358 / 1024x1024\n"

        self.fragments = "Type: Icon\n\
            Name: MinimapTooltip\n\
            Group: Minimap\n\
            Enabled: 0\n\
            KeepMaxScale: 1\n\
            AlwaysRespond: 0\n\
            Draggable: 0\n\
            Layer: 1\n\
            Anchor: 1,1\n\
            Rect: 1013.12,522.88 - 1013.76,523.52 / 1024x768\n\
            Alpha: 1\n\
            Texture: None\n\
            UV: 0,0 - 1,1\n\
            //////////////////////////////////////////\n\
            Type: Icon\n\
            Name: MinimapPillar\n\
            Group: Minimap\n\
            Enabled: 1\n\
            KeepMaxScale: 1\n\
            AlwaysRespond: 0\n\
            Draggable: 0\n\
            Layer: 1\n\
            Anchor: 1,1\n\
            Rect: 778.24,542.72 - 829.44,769.28 / 1024x768\n\
            Alpha: 1\n\
            Texture: HUDAtlas\n\
            UV: 5,5 - 85,358 / 1024x1024\n"
        
    def test_anchor_centrally(self):
        old_rect = LolRect(
            Vec2(829.44, 576.0),
            Vec2(1020.16, 763.52),
            1024, 768
        )
        old_rect = get_abs_scaled_rect(old_rect)
        reanchored = reanchor_centrally(old_rect, Vec2(1, 1))
        repositioned = get_lol_scaled_rect(reanchored, 1440, 1080)

        self.assertAlmostEqual(repositioned.start.x, 1361, places=0)
        self.assertAlmostEqual(repositioned.start.y, 810, places=0)
        self.assertAlmostEqual(repositioned.end.x, 1674, places=0)
        self.assertAlmostEqual(repositioned.end.y, 1074, places=0)

    def test_fragment_parsing(self):
        parsed = parse_fragment(self.fragment)
        self.assertIsInstance(parsed['Rect'], LolRect)
        self.assertIsInstance(parsed['Anchor'], Vec2)
        self.assertEqual(parsed['Rect'].start.x, 829.44)
        self.assertEqual(parsed['Rect'].start.y, 544.0)
        self.assertEqual(parsed['Rect'].end.x, 1024.0)
        self.assertEqual(parsed['Rect'].end.y, 768.64)
        self.assertEqual(parsed['Rect'].res_w, 1024)
        self.assertEqual(parsed['Rect'].res_h, 768)
        self.assertEqual(parsed['Texture'], 'HUDAtlas')

    def test_fragments_parsing(self):
        parsed = parse_fragments(self.fragments)
        self.assertEqual(len(parsed), 2)
        self.assertIsInstance(parsed[0]['Rect'], LolRect)
        self.assertEqual(parsed[0]['Rect'].start.x, 1013.12)
        self.assertEqual(parsed[1]['Rect'].start.x, 778.24)

    def test_fragment_writing(self):
        processed = compile_fragment(parse_fragment(self.fragment))
        self.assertEqual(len(parse_fragment(processed)), len(parse_fragment(self.fragment)))

    def test_fragments_writing(self):
        processed = compile_fragments(parse_fragments(self.fragments))
        self.assertEqual(len(parse_fragments(processed)), len(parse_fragments(self.fragments)))        

    def test_raf_processing(self):
        result = reanchor_centrally_in_raf(self.fragments)
        parsed = parse_fragments(result)
        self.assertIsInstance(parsed[0]['Rect'], LolRect)
        self.assertAlmostEqual(parsed[0]['Rect'].start.x, 1662.15, places=2)
        self.assertAlmostEqual(parsed[1]['Rect'].start.x, 1276.8, places=2)
        self.assertEqual(parsed[0]['Anchor'].x, 0.5)
        self.assertEqual(parsed[1]['Anchor'].x, 0.5)
        self.assertEqual(parsed[0]['Anchor'].y, 1)
        self.assertEqual(parsed[0]['Texture'], 'None')
        self.assertEqual(parsed[1]['Name'], 'MinimapPillar')
        
if __name__ == '__main__':
    unittest.main()