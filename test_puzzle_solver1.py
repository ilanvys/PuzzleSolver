from puzzle_solver import check_constraints, generate_puzzle, how_many_solutions, max_seen_cells, min_seen_cells, solve_puzzle
import sys


def test_max_seen_cells():
    sys.setrecursionlimit(9950)
    pic = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]
    assert max_seen_cells(pic, 0, 2) == 4
    assert max_seen_cells(pic, 0, 1) == 0
    assert max_seen_cells(pic, 2, 0) == 1
    assert max_seen_cells(pic, 0, 0) == 1
    assert max_seen_cells(pic, 1, 0) == 0
    assert max_seen_cells(pic, 1, 2) == 5
    assert max_seen_cells(pic, 1, 1) == 3


def test_min_seen_cells():
    sys.setrecursionlimit(9950)
    pic = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]
    assert min_seen_cells(pic, 0, 0) == 0
    assert min_seen_cells(pic, 1, 0) == 0
    assert min_seen_cells(pic, 1, 2) == 0
    assert min_seen_cells(pic, 1, 1) == 1


def test_check_constraints():
    picture1 = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]
    picture2 = [[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
    assert check_constraints(picture1, {(0, 3, 5), (1, 2, 5), (2, 0, 1)}) == 0
    assert check_constraints(picture2, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 1
    assert check_constraints(picture1, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 2


def test_solve_puzzel():
    assert solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 0)}, 3, 4) == [
        [0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
    assert solve_puzzle(
        {(0, 3, 3),
         (1, 2, 5),
         (2, 0, 1),
         (2, 3, 5)},
        3, 4) == None


def test_how_many_solutions():
    assert how_many_solutions(
        {(0, 3, 3),
         (1, 2, 5),
         (2, 0, 1),
         (0, 0, 0)},
        3, 4) == 1
    assert how_many_solutions({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3) == 2
    assert how_many_solutions({(i, j, 0) for i in range(3)
                              for j in range(3)}, 3, 3) == 1
    assert how_many_solutions(set(), 2, 2) == 16
    assert how_many_solutions({(0, 3, 3), (2, 0, 1)}, 3, 4) == 64


def test_generate_puzzle():
    picture = [[1, 0, 0], [1, 1, 1]]
    generate_puzzle(picture) in [{(0, 0, 2),
                                 (1, 2, 3)},
                                 {(1, 0, 4),
                                 (0, 1, 0),
                                  (0, 2, 0)},
                                 {(1, 0, 4),
                                  (0, 0, 2),
                                  (0, 2, 0)},
                                 {(1, 0, 4),
                                  (1, 1, 3),
                                  (0, 2, 0)},
                                 {(1, 0, 4),
                                  (1, 1, 3),
                                  (1, 2, 3)},
                                 {(1, 0, 4),
                                  (0, 1, 0),
                                  (1, 2, 3)},
                                 {(0, 0, 2),
                                  (1, 1, 3),
                                  (0, 1, 0),
                                  (0, 2, 0)}]
