import importlib.util
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import Mock

spec = importlib.util.spec_from_file_location('yap', Path(__file__).parents[1] / 'scripts/yap.py')
yap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(yap)

def event(cue, duration=None, until=None, kind='flash'):
    return {'src0': cue, 'src1': until, 'kind': (kind, duration), 'png': 'test.png'}

class OverlayTimingTests(unittest.TestCase):
    def test_flash_keeps_explicit_and_default_durations(self):
        instance = object.__new__(yap.Yap)
        instance._add = Mock()
        instance.flash(None, 2, dur=4.5)
        self.assertEqual(instance._add.call_args.args[3], ('flash', 4.5))
        instance.flash(None, 2)
        self.assertEqual(instance._add.call_args.args[3], ('flash', 1.5))
        for bad in [0, -1, math.nan, math.inf]:
            with self.assertRaises(ValueError):
                instance.flash(None, 2, dur=bad)

    def test_speed_maps_cue_but_not_output_hold(self):
        result = yap.resolve_overlay_intervals([event(10.3, 4.5)], lambda t: t / 1.03, 20)[0]
        self.assertEqual((result['start_frame'], result['end_frame']), (300, 435))
        self.assertEqual(result['end'] - result['start'], 4.5)

    def test_source_endpoint_is_mapped(self):
        result = yap.resolve_overlay_intervals([event(10.3, until=15.45, kind='hold')], lambda t: t / 1.03, 20)[0]
        self.assertEqual((result['start_frame'], result['end_frame']), (300, 450))

    def test_conflicts_are_not_silently_shortened(self):
        overlays = [event(0, 4.5), event(4, 1.5)]
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            yap.resolve_overlay_intervals(overlays, lambda t: t, 10)
        self.assertEqual(overlays[0]['kind'][1], 4.5)
        with self.assertRaisesRegex(ValueError, 'exceeds video end'):
            yap.resolve_overlay_intervals([event(9, 4.5)], lambda t: t, 10)

    def test_touching_events_and_invalid_durations(self):
        result = yap.resolve_overlay_intervals([event(0, 1.5), event(1.5, 3)], lambda t: t, 4.5)
        self.assertEqual(result[0]['end_frame'], result[1]['start_frame'])
        for bad in [0, -1, math.nan, math.inf]:
            with self.assertRaises(ValueError):
                yap.resolve_overlay_intervals([event(0, bad)], lambda t: t, 10)

    @unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg unavailable')
    def test_actual_ffmpeg_visibility_frames(self):
        events = yap.resolve_overlay_intervals([event(0, 1.5), event(3, 4.5)], lambda t: t, 8)
        enable = '+'.join(f"gte(n,{e['start_frame']})*lt(n,{e['end_frame']})" for e in events)
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp) / 'red.png'
            yap.Image.new('RGB', (8, 8), 'red').save(png)
            raw = subprocess.check_output(['ffmpeg', '-hide_banner', '-loglevel', 'error',
                '-filter_complex_threads', '1', '-f', 'lavfi', '-i', 'color=black:s=8x8:r=30:d=8',
                '-loop', '1', '-framerate', '30', '-i', str(png),
                '-filter_complex', f"[0:v][1:v]overlay=enable='{enable}',format=rgb24[out]",
                '-map', '[out]', '-frames:v', '240', '-f', 'rawvideo', 'pipe:1'])
        stride = 8 * 8 * 3
        visible = [i for i in range(240) if raw[i * stride] > 200]
        self.assertEqual(visible, list(range(45)) + list(range(90, 225)))

if __name__ == '__main__':
    unittest.main()
