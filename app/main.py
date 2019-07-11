import bottle
import os
import random


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
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
    return {
        'move': findFood(data),
        'taunt': 'Come get some!'
    }

def getSnake(gameState, id):
   for snake in gameState["snakes"]:
       if snake["id"] == id:
        return snake

def avoidCollision(snake, move):
    head_x, head_y = snake["coords"][0]
    if move is "left":
        # x coord
        new_head = [head_x - 1, head_y]
        if new_head in snake["coords"]:
            return False
    if move is "right":
        # x coord
        new_head = [head_x + 1, head_y]
        if new_head in snake["coords"]:
            return False
    if move is "up":
        # x coord
        new_head = [head_x, head_y + 1]
        if new_head in snake["coords"]:
            return False
    if move is "down":
        # x coord
        new_head = [head_x, head_y - 1]
        if new_head in snake["coords"]:
            return False
    return True


def findFood(gameState):

  mySnake = getSnake(gameState, gameState["you"])
  head = mySnake["coords"][0]

  move = None

  if gameState["food"][0][0] < head[0] and avoidCollision(mySnake, "left"):
        move = "left"

  if gameState["food"][0][0] > head[0] and avoidCollision(mySnake, "right"):
        move = "right"

  if gameState["food"][0][1] < head[1] and avoidCollision(mySnake, "up"):
        move = "up"

  if gameState["food"][0][1] > head[1] and avoidCollision(mySnake, "down"):
        move = "down"
  print move
  return move

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
