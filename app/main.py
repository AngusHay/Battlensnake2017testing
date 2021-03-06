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
		'name': 'The God-King'
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
	
	board = [[1 for i in range(board_width)] for i in range(board_height)]
	
	you_id = data[u'you']
	
	snakes = data['snakes']
	you = 0;
	for snake in snakes:
		for location in snake['coords']:
			board[location[0]][location[1]] = 0
			
		if snake['id'] == you_id:
			you = snake
	
	you_x = you['coords'][0][0]
	you_y = you['coords'][0][1]
		
	# check for edge of board
	#if you_y <= 0:
	#	avail_directions[0] = 0
	
	#if you_y >= (board_height - 1):
	#	avail_directions[1] = 0
		
	if you_x <= 0:
		avail_directions[2] = 0
	
	if you_x >= (board_width - 1):
		avail_directions[3] = 0
	
	print "location: %d %d" % (you_x, you_y)
	
	# check up
	target_x = you_x
	target_y = you_y - 1
	if target_y < 0:
		avail_directions[0] = 0
	elif board[target_x][target_y] == 0:
		avail_directions[0] = 0
		print "debug info up"
	
	# check down
	target_x = you_x
	target_y = you_y + 1
	if target_y > (board_height - 1):
		avail_directions[1] = 0
	elif board[target_x][target_y] == 0:
		avail_directions[1] = 0
		print "debug info down"
		
	# check left
	target_x = you_x - 1
	target_y = you_y
	if target_x < 0:
		avail_directions[2] = 0
	elif board[target_x][target_y] == 0:
		avail_directions[2] = 0
		print "debug info left"
	
	# check down
	target_x = you_x + 1
	target_y = you_y
	if target_x > (board_width - 1):
		avail_directions[3] = 0
	elif board[target_x][target_y] == 0:
		avail_directions[3] = 0
		print "debug info right"
	
	print "directions available: %d %d %d %d" % (avail_directions[0], avail_directions[1], avail_directions[2], avail_directions[3])
	
	possible_moves = []
	
	if avail_directions[0]:
		possible_moves.append('up')
		#move = 'up'
	if avail_directions[2]:
		possible_moves.append('left')
		#move = 'left'
	if avail_directions[1]:
		possible_moves.append('down')
		#move = 'down'
	if avail_directions[3]:
		possible_moves.append('right')
		#move = 'right'
	
	# generate "random" number
	randomval = 0;
	for snake in snakes:
		for location in snake['coords']:
			randomval = randomval + location[0] + location[1]
	
	randomval = randomval % len(possible_moves)
	print "randomval: %d" % len(possible_moves)
	
	move = possible_moves[randomval]
	
	
	
	return {
		# 'move': random.choice(directions),
		'move': move,
		'taunt': 'Bow down!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
