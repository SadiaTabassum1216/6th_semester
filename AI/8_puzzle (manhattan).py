import heapq

# https://tristanpenman.com/demos/n-puzzle/#

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_blank(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j

def is_valid_move(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def generate_successors(board):
    i, j = find_blank(board)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    successors = []

    for dx, dy in moves:
        x, y = i + dx, j + dy
        if is_valid_move(x, y):
            new_board = [row[:] for row in board]
            new_board[i][j], new_board[x][y] = new_board[x][y], new_board[i][j]
            successors.append((new_board, (x, y)))

    return successors

def astar_8puzzle(initial_state, goal_state):
    open_list = [(0, initial_state)]
    closed_set = set()
    parent_map = {tuple(map(tuple, initial_state)): None}
    g_scores = {tuple(map(tuple, initial_state)): 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal_state:
            path = []
            while current is not None:
                path.append(current)
                current = parent_map.get(tuple(map(tuple, current)), None)
            return path[::-1]

        closed_set.add(tuple(map(tuple, current)))

        for successor, move in generate_successors(current):
            if tuple(map(tuple, successor)) in closed_set:
                continue

            g_score = g_scores[tuple(map(tuple, current))] + 1
            if g_score < g_scores.get(tuple(map(tuple, successor)), float('inf')):
                g_scores[tuple(map(tuple, successor))] = g_score
                f_score = g_score + sum(manhattan_distance((i, j), goal_pos)
                                       for i, row in enumerate(successor)
                                       for j, goal_pos in enumerate(goal_state))
                heapq.heappush(open_list, (f_score, successor))
                parent_map[tuple(map(tuple, successor))] = current

    return None

initial_state = [
    [1, 2, 3],
    [8, 0, 6],
    [4, 5, 7]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

result = astar_8puzzle(initial_state, goal_state)

if result:
    for state in result:
        print("\n".join(" ".join(str(cell) for cell in row) for row in state))
        print("---------------------")
else:
    print("No solution found!")
