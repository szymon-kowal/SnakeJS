const gameBoard = document.querySelector('.gameBoard');
const ctx = gameBoard.getContext('2d');
const scoreTxt = document.querySelector('.score');
const reset = document.querySelector('.reset');

const gameWidth = gameBoard.width;
const gameHeight = gameBoard.height;

const gameSpeed = 125;
const numberElements = 20;
const unitSize = gameHeight/numberElements;
console.log(unitSize)

let score = 0;
let running = false;
let xVel = unitSize;
let yVel = 0;

let foodX;
let foodY;

let allowLeftKey = false;
let allowRightKey = true;
let allowUpKey = true;
let allowDownKey = true;

let snake = [
    {x:unitSize * 4, y:0},
    {x:unitSize * 3, y:0},
    {x:unitSize * 2, y:0},
    {x:unitSize, y:0},
    {x:0, y:0}
]

let flagStart = 0;

window.addEventListener('keydown',changeDirection);
window.addEventListener('keydown',startGame);

reset.addEventListener('click', resetGame);

startWindow();

function gameStart(){
    running = true;
    scoreTxt.textContet = score;

    createFood();
    drawFood();
    nextTick();
}

function nextTick(){
    if (running) {
        setTimeout(() => {
        clearBoard();
        drawFood();
        moveSnake();
        drawSnake();
        checkGameOver();
        nextTick();
        }, gameSpeed);
    }
    else {
        displayGameOver();
    }
};

function clearBoard(){
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, gameWidth, gameHeight);
}

function createFood(){
    function randomFood(min, max) {
        const randNum = Math.round((Math.random() * (max - min) + min) / unitSize ) * unitSize;
        return randNum
    } 
    foodX = randomFood(0, gameWidth - unitSize)
    foodY = randomFood(0, gameHeight - unitSize)
    console.log(foodX, foodY)
}

function drawFood(){
    ctx.fillStyle = 'red';
    ctx.fillRect(foodX, foodY, unitSize, unitSize)
}

function moveSnake(){
    const head = {x: snake[0].x + xVel, 
        y: snake[0].y + yVel};

    snake.unshift(head);
    if (snake[0].x == foodX && snake[0].y == foodY) {
        score += 1;
        scoreTxt.textContent = score;
        createFood();
    } else {
        snake.pop();
    }
}

function drawSnake(){
    ctx.fillStyle = 'green';
    ctx.strokeStyle = 'black';
    snake.forEach(snakePart => {
        ctx.fillRect(snakePart.x, snakePart.y, unitSize, unitSize);
        ctx.strokeRect(snakePart.x, snakePart.y, unitSize, unitSize);
    })
}


function changeDirection(event){
    

    switch(true){
        case(event.key === 'ArrowLeft' && allowLeftKey):
            xVel = -unitSize;
            yVel = 0;

            allowRightKey = false;
            allowLeftKey = true;
            allowUpKey = true;
            allowDownKey = true;
            break;
        case(event.key === 'ArrowRight' && allowRightKey == true):
            xVel = unitSize;
            yVel = 0;

            allowRightKey = true;
            allowLeftKey = false;
            allowUpKey = true;
            allowDownKey = true;
            break;
        case(event.key === 'ArrowUp' && allowUpKey):
            xVel = 0;
            yVel = -unitSize;

            allowUpKey = true;
            allowDownKey = false;
            allowLeftKey = true;
            allowRightKey = true;
            break;
        case(event.key === 'ArrowDown' && allowDownKey):
            xVel = 0;
            yVel = unitSize;

            allowDownKey = true;
            allowUpKey = false;
            allowLeftKey = true;
            allowRightKey = true;
            console.log(event.key)
            break;
        }
}

function checkGameOver(){
    switch(true){
        case (snake[0].x < 0):
            running = false;
            break;
        case (snake[0].x >= gameWidth):
            running = false;
            break;
        case (snake[0].y < 0):
            running = false;
            break;
        case (snake[0].y >= gameHeight):
            running = false;
        break;
    }
    for (let i = 1; i < snake.length; i++){
        if(snake[i].x == snake[0].x && snake[i].y == snake[0].y){
            running = false;
        }
    }
}

function displayGameOver(){
    ctx.font = "60px Arial";
    ctx.fillStyle = 'black';
    ctx.textAlign = 'center';
    ctx.fillText("Game Over!", gameWidth/2, gameHeight/2)
}

function resetGame(){
    clearTimeout(gameSpeed)
    score = 0;
    xVel = unitSize;
    yVel = 0;
    snake = [
        {x:unitSize * 4, y:0},
        {x:unitSize * 3, y:0},
        {x:unitSize * 2, y:0},
        {x:unitSize, y:0},
        {x:0, y:0}
    ]
    allowLeftKey = false;
    allowRightKey = true;
    allowUpKey = true;
    allowDownKey = true;
    
    scoreTxt.textContent = score;
    gameStart();
}

function startWindow() {
    clearBoard();
    ctx.font = "40px Arial";
    ctx.fillStyle = 'black';
    ctx.textAlign = 'center';
    ctx.fillText("Press ENTER to play !", gameWidth/2, gameHeight/2)
}

function startGame(event) {
    if (event.key === 'Enter' && flagStart == 0){
        flagStart = 1;
        gameStart()
        createFood()
        drawFood()
        
    }
}