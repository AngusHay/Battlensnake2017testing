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
    avail_directions = [1, 1, 1, 1];
    
    # check up
    if data.snakes[you].coords[0] == 0:
        avail_directions[0] = 0;
    
    if avail_directions[0] == 1:
        
        return {
            'move': 'up',
            'taunt': 'Your father was a hampster and your mother smelled of elderberries!'
        }

    return {
        'move': random.choice(directions),
        'taunt': 'Your father was a hampster and your mother smelled of elderberries!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
