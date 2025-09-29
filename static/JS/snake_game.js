const canvas = document.getElementById('gameCanvas');
	const ctx = canvas.getContext('2d');
	const socket = io();

	let direction;

	document.addEventListener('keydown', (event) => {
		if (event.key === 'ArrowUp') direction = 'UP';
		if (event.key === 'ArrowDown') direction = 'DOWN';
		if (event.key === 'ArrowLeft') direction = 'LEFT';
		if (event.key === 'ArrowRight') direction = 'RIGHT';
		console.log('Direction changed: ', direction)
		socket.emit('change_direction', direction);
        });
	document.getElementById("restartButton").addEventListener('click', function() {
		socket.emit('game_restart');		
	});
	//Draws the snake and food given their values
	function drawGame(snake_head, snake, food) {
		const  TILE_SIZE = 25;

		ctx.clearRect(0, 0, canvas.width, canvas.height);
	
		
		ctx.fillStyle = 'black';
		ctx.fillRect(snake_head.x, snake_head.y, TILE_SIZE, TILE_SIZE);
		
		if (Array.isArray(snake)) {
			snake.forEach(segment => {
			ctx.fillStyle = 'green';
			ctx.fillRect(segment.x, segment.y, TILE_SIZE, TILE_SIZE);	
			});
		}

		ctx.fillStyle = 'red';
		ctx.fillRect(food.x, food.y, TILE_SIZE, TILE_SIZE)
		//console.log("If this prints, hello, this function is working.")
}

	socket.on('connect', () => {
		console.log('Client connected!!');
		socket.emit('start_game');
	;})
	socket.on('game_started', () => {
		console.log('Client game started');

	;})


	socket.on('game_state', (data) => {
		console.log('Received game state: ', data);
		drawGame(data.snake_head, data.snake, data.food);
	});	
	function gameLoop() {
		socket.emit('move');
	
}
	socket.on('disconnect', () => {
	console.log('Socket client disconnected!')
	;})

	setInterval(gameLoop, 100);
