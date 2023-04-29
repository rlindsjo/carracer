track_1 = [
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "           ooooooooooooooooooooooooooooooooooooooooooooo        ",
    "          o                                             o       ",
    "         o                                               o      ",
    "        o                                                 o     ",
    "       o                                                   o    ",
    "      o                                                    o    ",
    "     o                                                     o    ",
    "     o               ooooooooooooooooo                     o    ",
    "     o              o                 o                    o    ",
    "     o             o                   o                   o    ",
    "     o            o                     o                 o     ",
    "      oooooooooooo                       o               o      ",
    "                                         o              o       ",
    "                                         o            oo        ",
    "                                         o          oo          ",
    "                                        o          o            ",
    "                                       o          o             ",
    "          oooooooooooo                o           o             ",
    "         o            o              o            o             ",
    "        o              o            o             o             ",
    "       o                o          o              o             ",
    "      o                  oooooooooo               o             ",
    "     o                                            o             ",
    "     o                                            o             ",
    "     o                                           o              ",
    "     o                                          o               ",
    "     o                                         o                ",
    "      o                                       o                 ",
    "       o                                     o                  ",
    "        oooooooooooooooooo>oooooooooooooooooo                   ",
    "                                                                ",
    "                                                                ",
    "                                                                "
]

direction_data = {
    'q': {'dir': 135, 'next': ('w', 'q', 'a'), 'move': (-1, -1)},
    'w': {'dir': 90, 'next': ('q', 'w', 'e'), 'move': (0, -1)},
    'e': {'dir': 45, 'next': ('d', 'e', 'w'), 'move': (1, -1)},
    'a': {'dir': 180, 'next': ('q', 'a', 'z'), 'move': (-1, 0)},
    'd': {'dir': 0, 'next': ('e', 'd', 'c'), 'move': (1, 0)},
    'z': {'dir': 225, 'next': ('a', 'z', 'x'), 'move': (-1, 1)},
    'x': {'dir': 270, 'next': ('z', 'x', 'c'), 'move': (0, 1)},
    'c': {'dir': 316, 'next': ('x', 'c', 'd'), 'move': (1, 1)}
}


class Track:
    def __init__(self, track_source):
        self.track_source = self.calculate_track(track_source)

    def on_track(self, x, y):
        return self.track_tile(int(x / 20), int(y / 20))

    def track_tile(self, x, y):
        return 0 <= y < len(self.track_source) and \
               0 <= x < len(self.track_source[y]) and \
               self.track_source[y][x] is not None

    def calculate_track(self, source):
        rows = len(source)
        cols = len(source[0])
        track = [[None for i in range(cols)] for j in range(rows)]

        # Find start
        pos = (0, 0)
        for row in range(rows):
            for col in range(cols):
                if source[row][col] == '>':
                    pos = (row, col)
                    break

        print(pos)
        # Start ->
        direction = 'd'
        # Follow track
        while track[pos[0]][pos[1]] is None:
            direction, next_pos = self.__find_next(pos, direction, source)
            track[pos[0]][pos[1]] = direction

            pos = next_pos

        # Fatten
        for row in range(rows):
            for col in range(cols):
                if source[row][col] in ">o":
                    if not track[row - 1][col]:
                        i = "deqazc".find(track[row][col]);
                        if i != -1:
                            track[row - 1][col] = 'cdazxx'[i]
                    if not track[row + 1][col]:
                        i = "deqazc".find(track[row][col]);
                        if i != -1:
                            track[row + 1][col] = 'ewwqad'[i]
                    if not track[row][col - 1]:
                        i = "ewqzxc".find(track[row][col]);
                        if i != -1:
                            track[row][col - 1] = 'deaxcd'[i]
                    if not track[row][col + 1]:
                        i = "ewqzxc".find(track[row][col]);
                        if i != -1:
                            track[row][col + 1] = 'wqaazx'[i]

        return track

    @staticmethod
    def __find_next(pos, direction, source):
        data = direction_data[direction]
        for dir_next in (data['next']):
            delta = direction_data[dir_next]['move']
            next_pos = (pos[0] + delta[1], pos[1] + delta[0])
            if source[next_pos[0]][next_pos[1]] in "o>":
                return dir_next, next_pos
