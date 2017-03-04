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
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']
    avail_directions = [1, 1, 1, 1]
    
    move = 'down'
    
    board_height = data['height']
    board_width = data['width']
    
    you_id = data[u'you']
    
    snakes = data['snakes']
    you = 0;
    for snake in snakes:
        if snake['id'] == you_id:
            you = snake
    
    you_x = you['coords'][0][0]
    you_y = you['coords'][0][1]
        
    if you_y <= 0:
        move = 'left'
    
    if you_x >= (board_width - 1):
        move = 'up'
    
    if you_y >= (board_height - 1):
        move = 'right'
        
    if you_x <= 0:
        move = 'down'
    
    #snakes = data['snakes']
    #you_index = snakes[data['you']]
    
    #snake = snakes[you_index]
    
    
    
        
    return {
        #'move': random.choice(directions),
        'move': move,
        'taunt': 'Your father was a hampster and your mother smelled of elderberries!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
