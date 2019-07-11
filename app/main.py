import bottle
import os
import random

board_width = None
board_height = None
last_move = None

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
        'taunt': 'Get your neck chopped!',
        'head_url': head_url,
        'name': 'NinjaGaiden Snake'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    next_move = findFood(data)
    if next_move is None:
        next_move = findSafePlace(data)
    print next_move
    return {
        'move': next_move,
        'taunt': 'Come get some!'
    }


def getSnake(gameState, id):
    for snake in gameState["snakes"]:
        if snake["id"] == id:
            return snake


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
        print options
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
    print available_moves
    if last_move and gameState["food"][0][0] < head[0] and last_move in available_moves:
            move = last_move

    if gameState["food"][0][0] < head[0] and "left" in available_moves:
        move = "left"

    if gameState["food"][0][0] > head[0] and "right" in available_moves:
        move = "right"

    if gameState["food"][0][1] < head[1] and "up" in available_moves:
        move = "up"

    if gameState["food"][0][1] > head[1] and "down" in available_moves:
        move = "down"

    global last_move
    last_move = move
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
