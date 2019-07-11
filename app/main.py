import bottle
import os
import random
import pprint

pp = pprint.PrettyPrinter(indent=4)

board_width = None
board_height = None
optimal_move = None

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    global board_width
    global board_height
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': 'Let it burn!',
        'head_url': head_url,
        'name': 'Dumpster Snake'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    next_move = findFood(data)
    if next_move is None:
        next_move = findSafePlace(data)
    return {
        'move': next_move,
        'taunt': 'Come get some!'
    }


def getSnake(gameState, id):
    for snake in gameState["snakes"]:
        if snake["id"] == id:
            return snake

def takenSpaces(gameState):
    spaces = []
    snakes = gameState["snakes"]
    for snake in snakes:
        spaces += snake["coords"]
    return spaces


def findOptimalPath(gameState):
    available_moves = availableMoves(gameState)
    optimal_move_count = 0
    optimal_move = None
    for move in availableMoves:
        move_count = space_available(move, gameState)
        print move, move_count
        if move_count > optimal_move_count:
            optimal_move_count = move_count
            optimal_move = move

    return optimal_move





def space_available(move, gameState):
    mySnake = getSnake(gameState, gameState["you"])
    head_x, head_y = mySnake["coords"][0]
    illegal_moves = takenSpaces(gameState)
    count_space = 0
    if move is 'left':
        while head_x > 0:
            head_x = head_x - 1
            if [head_x, head_y] in illegal_moves:
                return count
            else:
                count += 1
    if move is 'right':
        while head_x < board_width:
            head_x = head_x + 1
            if [head_x, head_y] in illegal_moves:
                return count
            else:
                count += 1
    if move is 'up':
        while head_y > 0:
            head_y = head_y - 1
            if [head_x, head_y] in illegal_moves:
                return count
            else:
                count += 1
    if move is 'down':
        while head_y < board_height:
            head_y = head_y + 1
            if [head_x, head_y] in illegal_moves:
                return count
            else:
                count += 1
    return count


def availableMoves(gameState):
    options = ['left', 'right', 'up', 'down']
    snakes = gameState["snakes"]
    for snake in snakes:
        head_x, head_y = snake["coords"][0]
        new_head = [head_x - 1, head_y]
        if 0 > head_x - 1 or new_head in snake["coords"]:
            options.remove('left')
        new_head = [head_x + 1, head_y]
        if board_width <= head_x + 1 or new_head in snake["coords"]:
            options.remove('right')
        new_head = [head_x, head_y - 1]
        if 0 > head_y - 1 or new_head in snake["coords"]:
            options.remove('up')
        new_head = [head_x, head_y + 1]
        if board_height <= head_y + 1 or new_head in snake["coords"]:
            options.remove('down')
    return options


def avoidCollision(snakes, move):
    for snake in snakes:
        head_x, head_y = snake["coords"][0]
        if move is "left":
            # x coord
            new_head = [head_x - 1, head_y]
            if 0 > head_x - 1 or new_head in snake["coords"]:
                return False
        if move is "right":
            # x coord
            new_head = [head_x + 1, head_y]
            if board_width <= head_x + 1 or new_head in snake["coords"]:
                return False
        if move is "up":
            # x coord
            new_head = [head_x, head_y - 1]
            if 0 > head_y - 1 or new_head in snake["coords"]:
                return False
        if move is "down":
            # x coord
            new_head = [head_x, head_y + 1]
            if board_height <= head_y + 1 or new_head in snake["coords"]:
                return False
    return True


def findFood(gameState):

    mySnake = getSnake(gameState, gameState["you"])
    head = mySnake["coords"][0]

    available_moves = availableMoves(gameState)
    move = None
    if optimal_move and gameState["food"][0][0] < head[0] and optimal_move in available_moves:
            move = findOptimalPath(gameState)

    if gameState["food"][0][0] < head[0] and "left" in available_moves:
        move = "left"

    if gameState["food"][0][0] > head[0] and "right" in available_moves:
        move = "right"

    if gameState["food"][0][1] < head[1] and "up" in available_moves:
        move = "up"

    if gameState["food"][0][1] > head[1] and "down" in available_moves:
        move = "down"

    global optimal_move
    optimal_move = move
    return move


def findSafePlace(gameState):

    mySnake = getSnake(gameState, gameState["you"])
    head = mySnake["coords"][0]
    move = None
    if avoidCollision(gameState["snakes"], "left"):
        move = "left"

    if avoidCollision(gameState["snakes"], "right"):
        move = "right"

    if avoidCollision(gameState["snakes"], "up"):
        move = "up"

    if avoidCollision(gameState["snakes"], "down"):
        move = "down"
    return move

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
