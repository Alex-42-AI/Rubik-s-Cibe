from math import inf

from random import randint, choice

COLORS = ["RED", "BLUE", "YELLOW", "GREEN", "WHITE", "ORANGE"]

MOVES = [["U", "U2", "U'"], ["D", "D2", "D'"], ["L", "L2", "L'"], ["R", "R2", "R'"], ["F", "F2", "F'"],
         ["B", "B2", "B'"]]

SUPERFLIP = ["U", "R2", "F", "B", "R", "B2", "R", "U2", "L", "B2", "R", "U'", "D'", "R2", "F", "R'", "L", "B2", "U2",
             "F2"]

FLOWER = ["U2", "D2", "R2", "L2", "F2", "B2"]

inverse = {"U": "U'", "U2": "U2", "U'": "U", "D": "D'", "D2": "D2", "D'": "D", "L": "L'", "L2": "L2", "L'": "L",
           "R": "R'", "R2": "R2", "R'": "R", "F": "F'", "F2": "F2", "F'": "F", "B": "B'", "B2": "B2", "B'": "B"}


def rotate_clockwise(corner: tuple[int, int, int]) -> tuple[int, int, int]:
    return corner[2], corner[0], corner[1]


def rotate_counterclockwise(corner: tuple[int, int, int]) -> tuple[int, int, int]:
    return corner[1], corner[2], corner[0]


def flip_edge(edge: tuple[int, int]) -> tuple[int, int]:
    return edge[1], edge[0]


class Cube:
    def __init__(self):
        self.corners = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
        self.edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1), (5, 1), (5, 2), (5, 3), (5, 4)]

    def get_top(self) -> list[list[int]]:
        corners, edges = self.corners, self.edges

        return [[corners[1][0], edges[2][0], corners[2][0]], [edges[1][0], 0, edges[3][0]],
                [corners[0][0], edges[0][0], corners[3][0]]]

    def get_bottom(self) -> list[list[int]]:
        corners, edges = self.corners, self.edges

        return [[corners[4][0], edges[8][0], corners[6][0]], [edges[9][0], 5, edges[11][0]],
                [corners[5][0], edges[10][0], corners[6][0]]]

    def get_left(self) -> list[list[int]]:
        corners, edges = self.corners, self.edges

        return [[corners[1][1], edges[1][1], corners[0][2]], [edges[5][0], 2, edges[4][1]],
                [corners[5][2], edges[9][1], corners[4][1]]]

    def get_right(self) -> list[list[int]]:
        corners, edges = self.corners, self.edges

        return [[corners[3][1], edges[3][1], corners[2][2]], [edges[7][0], 4, edges[6][1]],
                [corners[7][2], edges[11][1], corners[6][1]]]

    def get_front(self) -> list[list[int]]:
        corners, edges = self.corners, self.edges

        return [[corners[0][1], edges[0][1], corners[3][2]], [edges[4][0], 1, edges[7][1]],
                [corners[4][2], edges[8][1], corners[7][1]]]

    def get_back(self) -> list[list[int]]:
        corners, edges = self.corners, self.edges

        return [[corners[2][1], edges[2][1], corners[1][2]], [edges[6][0], 3, edges[5][1]],
                [corners[5][1], edges[10][1], corners[6][2]]]

    def up(self) -> Cube:
        self.corners = [self.corners[3], *self.corners[:3], *self.corners[4:]]
        self.edges = [self.edges[3], *self.edges[:3], *self.edges[4:]]

        return self

    def down(self) -> Cube:
        self.corners = [*self.corners[:4], *self.corners[5:], self.corners[4]]
        self.edges = [*self.edges[:8], *self.edges[9:], self.edges[8]]

        return self

    def left(self) -> Cube:
        self.corners = [rotate_clockwise(self.corners[1]), rotate_counterclockwise(self.corners[5]),
                        *self.corners[2:4], rotate_counterclockwise(self.corners[0]),
                        rotate_clockwise(self.corners[4]), *self.corners[6:]]
        self.edges = [self.edges[0], flip_edge(self.edges[5]), *self.edges[2:4], self.edges[1],
                      flip_edge(self.edges[9]), *self.edges[6:9], self.edges[4], *self.edges[10:]]

        return self

    def right(self) -> Cube:
        self.corners = [*self.corners[:2], rotate_clockwise(self.corners[3]), rotate_counterclockwise(self.corners[7]),
                        *self.corners[4:6], rotate_counterclockwise(self.corners[2]),
                        rotate_clockwise(self.corners[6])]
        self.edges = [*self.edges[:3], flip_edge(self.edges[7]), *self.edges[4:6], self.edges[3],
                      flip_edge(self.edges[11]), *self.edges[8:11], self.edges[6]]

        return self

    def front(self) -> Cube:
        self.corners = [rotate_counterclockwise(self.corners[4]), *self.corners[1:3],
                        rotate_clockwise(self.corners[0]), rotate_clockwise(self.corners[7]), *self.corners[5:7],
                        rotate_counterclockwise(self.corners[3])]
        self.edges = [flip_edge(self.edges[4]), *self.edges[1:4], flip_edge(self.edges[8]), *self.edges[5:7],
                      self.edges[0], self.edges[7], *self.edges[9:]]

        return self

    def back(self) -> Cube:
        self.corners = [self.corners[0], rotate_clockwise(self.corners[2]), rotate_counterclockwise(self.corners[6]),
                        *self.corners[3:5], rotate_counterclockwise(self.corners[1]),
                        rotate_clockwise(self.corners[5]), self.corners[7]]
        self.edges = [*self.edges[:2], flip_edge(self.edges[6]), *self.edges[3:5], self.edges[2],
                      flip_edge(self.edges[10]), *self.edges[7:10], self.edges[5], self.edges[11]]

        return self

    def pattern(self, sequence: list[str]) -> Cube:
        for move in sequence:
            times = 1

            if len(move := move.upper()) == 2:
                move, note = list(move)

                if note == "2":
                    times = 2

                elif note == "'":
                    times = 3

            if move == "U":
                move_method = self.up

            elif move == "D":
                move_method = self.down

            elif move == "L":
                move_method = self.left

            elif move == "R":
                move_method = self.right

            elif move == "F":
                move_method = self.front

            elif move == "B":
                move_method = self.back

            else:
                continue

            for _ in range(times):
                move_method()

        return self

    def copy(self) -> Cube:
        result = Cube()
        result.corners = self.corners.copy()
        result.edges = self.edges.copy()

        return result

    def pattern_order(self, sequence: list[str]) -> int:
        result = 1
        self.pattern(sequence)

        while not self.solved():
            self.pattern(sequence)
            result += 1

        return result

    def scramble(self, sides: str = "UDLRFB") -> list[str]:
        sequence, legal_moves, last, length = [], [], -1, len(sides)
        n = randint(4 * length, 5 * length)

        if "U" in sides:
            legal_moves.append(MOVES[0])

        if "D" in sides:
            legal_moves.append(MOVES[1])

        if "L" in sides:
            legal_moves.append(MOVES[2])

        if "R" in sides:
            legal_moves.append(MOVES[3])

        if "F" in sides:
            legal_moves.append(MOVES[4])

        if "B" in sides:
            legal_moves.append(MOVES[5])

        for _ in range(n):
            index = choice(list(set(range(length)) - {last}))
            sequence.append(choice(legal_moves[index]))
            last = index

        self.pattern(sequence)

        return sequence

    def heuristic(self) -> int:
        up_side = self.get_top()
        down_side = self.get_bottom()
        left_side = self.get_left()
        right_side = self.get_right()
        front_side = self.get_front()
        back_side = self.get_back()
        ...

        return 0

    def solve(self, sides: str = "UDLRFB") -> list[str]:
        legal_moves = set(sides)

        def ida_star():

            def dfs(last0="", last1="", g=0):
                if not cube.heuristic():
                    return FOUND

                next_moves = []

                if "U" in legal_moves and last1 != "U" and (last1 != "D" or last0 != "U"):
                    tmp = cube.copy().up()
                    next_moves.append(("U", "U'", tmp.heuristic()))
                    next_moves.append(("U2", "U2", tmp.up().heuristic()))
                    next_moves.append(("U'", "U", tmp.up().heuristic()))

                if "D" in legal_moves and last1 != "D" and (last1 != "U" or last0 != "D"):
                    tmp = cube.copy().down()
                    next_moves.append(("D", "D'", tmp.heuristic()))
                    next_moves.append(("D2", "D2", tmp.down().heuristic()))
                    next_moves.append(("D'", "D", tmp.down().heuristic()))

                if "L" in legal_moves and last1 != "L" and (last1 != "R" or last0 != "L"):
                    tmp = cube.copy().left()
                    next_moves.append(("L", "L'", tmp.heuristic()))
                    next_moves.append(("L2", "L2", tmp.left().heuristic()))
                    next_moves.append(("L'", "L", tmp.left().heuristic()))

                if "R" in legal_moves and last1 != "R" and (last1 != "L" or last0 != "R"):
                    tmp = cube.copy().right()
                    next_moves.append(("R", "R'", tmp.heuristic()))
                    next_moves.append(("R2", "R2", tmp.right().heuristic()))
                    next_moves.append(("R'", "R", tmp.right().heuristic()))

                if "F" in legal_moves and last1 != "F" and (last1 != "B" or last0 != "F"):
                    tmp = cube.copy().front()
                    next_moves.append(("F", "F'", tmp.heuristic()))
                    next_moves.append(("F2", "F2", tmp.front().heuristic()))
                    next_moves.append(("F'", "F", tmp.front().heuristic()))

                if "B" in legal_moves and last1 != "B" and (last1 != "F" or last0 != "B"):
                    tmp = cube.copy().back()
                    next_moves.append(("B", "B'", tmp.heuristic()))
                    next_moves.append(("B2", "B2", tmp.back().heuristic()))
                    next_moves.append(("B'", "B", tmp.back().heuristic()))

                next_moves = sorted(next_moves, key=lambda s: s[-1])
                f = inf

                for move, inv, h in next_moves:
                    if (c_f := g + h + 1) > bound:
                        f = min(f, c_f)

                        break

                    path.append(move), cube.pattern([move])
                    t = dfs(last1, inv, g + 1)

                    if t == FOUND:
                        return FOUND

                    f = min(f, t)
                    path.pop(), cube.pattern([inv])

                return f

            bound, FOUND, path = (cube := self.copy()).heuristic(), -1, []

            while True:
                t = dfs()

                if t == FOUND:
                    return path

                if t <= bound:
                    bound += 1

                else:
                    bound = t

        def bfs():
            cube = self.copy()
            prev: dict[Cube, tuple[Cube, str]] = {cube: (None, "")}
            queue = [cube]

            while queue:
                c = queue.pop(0)
                next_moves: list[str] = []

                if "U" in legal_moves and "U" not in prev[c][1] and (
                        prev[c][0] is None or "D" not in prev[c][1] or "U" not in prev[prev[c][0]][1]):
                    tmp = c.copy().up()

                    if tmp not in prev:
                        next_moves.append("U")

                    if tmp.up() not in prev:
                        next_moves.append("U2")

                    if tmp.up() not in prev:
                        next_moves.append("U'")

                if "D" in legal_moves and "D" not in prev[c][1] and (
                        prev[c][0] is None or "U" not in prev[c][1] or "D" not in prev[prev[c][0]][1]):
                    tmp = c.copy().down()

                    if tmp not in prev:
                        next_moves.append("D")

                    if tmp.down() not in prev:
                        next_moves.append("D2")

                    if tmp.down() not in prev:
                        next_moves.append("D'")

                if "L" in legal_moves and "L" not in prev[c][1] and (
                        prev[c][0] is None or "R" not in prev[c][1] or "L" not in prev[prev[c][0]][1]):
                    tmp = c.copy().left()

                    if tmp not in prev:
                        next_moves.append("L")

                    if tmp.left() not in prev:
                        next_moves.append("L2")

                    if tmp.left() not in prev:
                        next_moves.append("L'")

                if "R" in legal_moves and "R" not in prev[c][1] and (
                        prev[c][0] is None or "L" not in prev[c][1] or "R" not in prev[prev[c][0]][1]):
                    tmp = c.copy().right()

                    if tmp not in prev:
                        next_moves.append("R")

                    if tmp.right() not in prev:
                        next_moves.append("R2")

                    if tmp.right() not in prev:
                        next_moves.append("R'")

                if "F" in legal_moves and "F" not in prev[c][1] and (
                        prev[c][0] is None or "B" not in prev[c][1] or "F" not in prev[prev[c][0]][1]):
                    tmp = c.copy().front()

                    if tmp not in prev:
                        next_moves.append("F")

                    if tmp.front() not in prev:
                        next_moves.append("F2")

                    if tmp.front() not in prev:
                        next_moves.append("F'")

                if "B" in legal_moves and "B" not in prev[c][1] and (
                        prev[c][0] is None or "F" not in prev[c][1] or "B" not in prev[prev[c][0]][1]):
                    tmp = c.copy().back()

                    if tmp not in prev:
                        next_moves.append("B")

                    if tmp.back() not in prev:
                        next_moves.append("B2")

                    if tmp.back() not in prev:
                        next_moves.append("B'")

                for move in next_moves:
                    c0 = c.copy().pattern([move])
                    prev[c0] = (c, move)

                    if c0.solved():
                        path = []

                        while c0 is not None:
                            path.append(prev[c0][1])
                            c0 = prev[c0][0]

                        path.pop()

                        return path[::-1]

                    queue.append(c0)

            return []

        return bfs()

    def solved(self) -> bool:
        return (self.corners, self.edges) == (
            [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)],
            [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1), (5, 1), (5, 2), (5, 3), (5, 4)])

    def __hash__(self) -> int:
        return hash((tuple(self.corners), tuple(self.edges)))

    def __eq__(self, other: Cube) -> bool:
        return (self.corners, self.edges) == (other.corners, other.edges)

    def __str__(self) -> str:
        result = ""

        for r in self.get_top():
            result += f"      {" ".join(map(str, r))}\n"

        for r in range(3):
            result += " ".join(map(str, self.get_left()[r])) + "|" + " ".join(map(str, self.get_front()[r])) + "|" + " ".join(map(str, self.get_right()[r])) + "\n"

        for r in self.get_bottom():
            result += f"      {" ".join(map(str, r))}\n"

        for r in self.get_back()[::-1]:
            result += f"      {" ".join(map(str, r[::-1]))}\n"

        return result

    def __repr__(self) -> str:
        return f"Cube({self.corners}, {self.edges})"


cube = Cube()
cube.corners[0] = rotate_clockwise(cube.corners[0])
cube.corners[1] = rotate_counterclockwise(cube.corners[1])
print(cube.solve("UFD"))

"""
["U'", 'L2', 'U2', "L'", 'U', 'L', "U'", 'L2']
['L2', 'U', "L'", "U'", 'L', 'U2', 'L2', 'U']

['U2', 'L2', "U'", "L'", "U'", "L'", 'U', "L'"]
['L', "U'", 'L', 'U', 'L', 'U', 'L2', 'U2']

["U'", 'L', 'U', 'L2', 'U', 'L2', 'U2', 'L2', 'U2', "L'"]
['L', 'U2', 'L2', 'U2', 'L2', "U'", 'L2', "U'", "L'", 'U']
"""
