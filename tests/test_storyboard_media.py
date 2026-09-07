import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
SCRIPT = Path(__file__).resolve().parents[1] / 'skills/scripts/storyboard-media.py'
spec = importlib.util.spec_from_file_location('storyboard_media', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class MediaTests(unittest.TestCase):
    def test_im6_and_im7_odd_dimensions_and_no_overwrite(self):
        for im7 in (False, True):
            with tempfile.TemporaryDirectory() as d:
                root = Path(d)
                original = root/'grid.png'
                original.write_bytes(b'fixture')
                calls = []
                def which(name):
                    return '/bin/'+name if im7 or name != 'magick' else None
                def run(args):
                    calls.append(args)
                    if '-format' in args:
                        return '5 7'
                    Path(args[-1]).write_bytes(b'frame')
                    return ''
                with patch.object(m.shutil, 'which', which), patch.object(m, 'run', run):
                    result = m.split(original, root/'frames')
                    self.assertEqual(len(result['frames']), 4)
                    self.assertEqual([c[c.index('-crop')+1] for c in calls if '-crop' in c],
                                     ['2x3+0+0', '3x3+2+0', '2x4+0+3', '3x4+2+3'])
                    self.assertEqual(Path(calls[0][0]).name, 'magick' if im7 else 'identify')
                    with self.assertRaises(FileExistsError):
                        m.split(original, root/'frames')

    def test_split_failure_cleans_only_new_directory(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            original = root/'grid.png'
            original.write_bytes(b'original')
            unrelated = root/'unrelated'
            unrelated.mkdir()
            (unrelated/'keep.txt').write_text('keep')
            def run(args):
                if '-format' in args:
                    return '4 4'
                Path(args[-1]).write_bytes(b'partial')
                if args[-1].endswith('shot2.png'):
                    raise subprocess.CalledProcessError(1, args)
                return ''
            with patch.object(m.shutil, 'which', lambda name: '/bin/'+name), patch.object(m, 'run', run):
                with self.assertRaises(subprocess.CalledProcessError):
                    m.split(original, root/'frames')
                self.assertFalse((root/'frames').exists())
                self.assertEqual(original.read_bytes(), b'original')
                self.assertEqual((unrelated/'keep.txt').read_text(), 'keep')
                with self.assertRaises(FileExistsError):
                    m.split(original, unrelated)
                self.assertEqual((unrelated/'keep.txt').read_text(), 'keep')

    def concat_case(self, audio, fail=False):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            clips = [root/f'{i}.mp4' for i in range(len(audio))]
            for clip in clips: clip.write_bytes(b'video')
            calls = []
            def run(args):
                if '-show_streams' in args:
                    i = clips.index(Path(args[-1]))
                    streams = [{'codec_type':'video', 'duration':'2'}]
                    if audio[i]: streams.append({'codec_type':'audio'})
                    return json.dumps({'streams':streams})
                calls.append(args)
                if fail: raise subprocess.CalledProcessError(1, args)
                Path(args[-1]).write_bytes(b'final')
                return ''
            with patch.object(m.shutil, 'which', lambda name: '/bin/'+name), patch.object(m, 'run', run):
                output = root/'final.mp4'
                if fail:
                    with self.assertRaises(subprocess.CalledProcessError):
                        m.concat(output, clips, 1280, 720, 30)
                    self.assertFalse(output.exists())
                    self.assertFalse(list(root.glob('.storyboard-*')))
                else:
                    result = m.concat(output, clips, 1280, 720, 30)
                    self.assertEqual(result['audio'], any(audio))
                    self.assertEqual(output.read_bytes(), b'final')
                    with self.assertRaises(ValueError):
                        m.concat(output, clips, 1280, 720, 30)
                graph = calls[0][calls[0].index('-filter_complex')+1]
                self.assertIn('fps=30', graph)
                self.assertEqual(graph.count('anullsrc'), audio.count(False) if any(audio) else 0)
                for i, has in enumerate(audio):
                    self.assertEqual(f'[{i}:a:0]' in graph, has)
                self.assertEqual(len(calls), 1)
    def test_mixed_audio_preserved(self): self.concat_case([True,False,True,False])
    def test_all_silent_stays_video_only(self): self.concat_case([False,False])
    def test_all_audio(self): self.concat_case([True,True])
    def test_ffmpeg_failure_does_not_publish_or_retry(self): self.concat_case([True,False], fail=True)
    def test_invalid_geometry(self):
        with self.assertRaises(ValueError): m.concat('x.mp4', [], 1279, 720, 30)

if __name__ == '__main__':
    unittest.main()
