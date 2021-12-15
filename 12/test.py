import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input_large = """dc-end
                            HN-start
                            start-kj
                            dc-start
                            dc-HN
                            LN-dc
                            HN-end
                            kj-sa
                            kj-HN
                            kj-dc"""
    sample_input_small = """start-A
                            start-b
                            A-c
                            A-b
                            b-d
                            A-end
                            b-end"""
    sample_input_biggest = """  fs-end
                                he-DX
                                fs-he
                                start-DX
                                pj-DX
                                end-zg
                                zg-sl
                                zg-pj
                                pj-he
                                RW-he
                                fs-DX
                                pj-RW
                                zg-RW
                                start-pj
                                he-WI
                                zg-he
                                pj-fs
                                start-RW"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return build_cave_graph(f)

    def test_sample_minimal(self):
        cave_graph = self.parse_input("""   start-a
                                            start-b
                                            a-end
                                            b-end""")
        self.assertEqual({"a", "b"}, {c.name for c in cave_graph.connected_caves})
        paths = get_all_paths(cave_graph)
        self.assertEqual({"start,a,end",
                          "start,b,end"}, {",".join(cave_list) for cave_list in paths})

    def test_sample_input_small(self):
        cave_graph = self.parse_input(self.sample_input_small)
        paths = get_all_paths(cave_graph)
        self.assertEqual(sorted([line.strip() for line in """   start,A,b,A,c,A,end
                                                                start,A,b,A,end
                                                                start,A,b,end
                                                                start,A,c,A,b,A,end
                                                                start,A,c,A,b,end
                                                                start,A,c,A,end
                                                                start,A,end
                                                                start,b,A,c,A,end
                                                                start,b,A,end
                                                                start,b,end""".split("\n")]),
                         sorted([",".join(cave_list) for cave_list in paths]))

    def test_sample_input_big(self):
        cave_graph = self.parse_input(self.sample_input_large)
        paths = get_all_paths(cave_graph)
        self.assertEqual(sorted([line.strip() for line in """   start,HN,dc,HN,end
                                                                start,HN,dc,HN,kj,HN,end
                                                                start,HN,dc,end
                                                                start,HN,dc,kj,HN,end
                                                                start,HN,end
                                                                start,HN,kj,HN,dc,HN,end
                                                                start,HN,kj,HN,dc,end
                                                                start,HN,kj,HN,end
                                                                start,HN,kj,dc,HN,end
                                                                start,HN,kj,dc,end
                                                                start,dc,HN,end
                                                                start,dc,HN,kj,HN,end
                                                                start,dc,end
                                                                start,dc,kj,HN,end
                                                                start,kj,HN,dc,HN,end
                                                                start,kj,HN,dc,end
                                                                start,kj,HN,end
                                                                start,kj,dc,HN,end
                                                                start,kj,dc,end""".split("\n")]),
                         sorted([",".join(cave_list) for cave_list in paths]))

    def test_sample_input_biggest(self):
        cave_graph = self.parse_input(self.sample_input_biggest)
        paths = get_all_paths(cave_graph)
        self.assertEqual(226, len(paths))
