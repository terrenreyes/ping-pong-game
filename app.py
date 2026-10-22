
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Ping Pong Game",
    page_icon="🏓",
    layout="wide"
)

st.title("🏓 Ping Pong Game")
st.write("Play against the computer! First to 7 points wins.")
st.info("Click inside the game, then use W/S or ↑/↓ to move your paddle.")

components.html(
    """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    background: #101827;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 0;
}
canvas {
    background: #080e1b;
    border: 3px solid #00e5ff;
    border-radius: 12px;
    max-width: 98%;
    outline: none;
}
button {
    background: #00c8e8;
    color: #09111e;
    border: none;
    border-radius: 8px;
    padding: 12px 22px;
    margin: 12px 6px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}
button:hover {
    background: #79edff;
}
#status {
    color: #facc15;
    font-size: 18px;
    margin: 10px;
}
</style>
</head>
<body>

<h2>PLAYER vs COMPUTER</h2>
<h1><span id="playerScore">0</span> : <span id="cpuScore">0</span></h1>

<canvas id="game" width="800" height="450" tabindex="0"></canvas>

<div id="status">Press Start Game</div>

<button onclick="startGame()">Start Game</button>
<button onclick="togglePause()">Pause / Resume</button>
<button onclick="restartGame()">Restart</button>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

const paddleWidth = 13;
const paddleHeight = 85;
const playerX = 25;
const cpuX = W - 38;

let playerY = H / 2 - paddleHeight / 2;
let cpuY = playerY;

let ballX = W / 2;
let ballY = H / 2;
let ballVX = 5;
let ballVY = 3;

let playerScore = 0;
let cpuScore = 0;
let running = false;
let finished = false;

const keys = {};

function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
}

function resetBall(direction) {
    ballX = W / 2;
    ballY = H / 2;
    ballVX = direction * 5;
    ballVY = (Math.random() * 4 - 2) || 2;
}

function updateScore() {
    document.getElementById("playerScore").textContent = playerScore;
    document.getElementById("cpuScore").textContent = cpuScore;
}

function setStatus(message) {
    document.getElementById("status").textContent = message;
}

function restartGame() {
    playerScore = 0;
    cpuScore = 0;
    playerY = H / 2 - paddleHeight / 2;
    cpuY = playerY;
    running = true;
    finished = false;
    resetBall(Math.random() < 0.5 ? 1 : -1);
    updateScore();
    setStatus("Game on! First to 7 wins.");
    canvas.focus();
}

function startGame() {
    if (finished) {
        restartGame();
    } else {
        running = true;
        setStatus("Game on!");
        canvas.focus();
    }
}

function togglePause() {
    if (finished) return;
    running = !running;
    setStatus(running ? "Game on!" : "Paused");
    canvas.focus();
}

window.addEventListener("keydown", function(e) {
    if (["ArrowUp", "ArrowDown", "w", "s", "W", "S"].includes(e.key)) {
        e.preventDefault();
        keys[e.key.toLowerCase()] = true;
    }
});

window.addEventListener("keyup", function(e) {
    keys[e.key.toLowerCase()] = false;
});

window.addEventListener("blur", function() {
    for (const key in keys) keys[key] = false;
});

function update() {
    if (!running || finished) return;

    if (keys["arrowup"] || keys["w"]) playerY -= 7;
    if (keys["arrowdown"] || keys["s"]) playerY += 7;

    playerY = clamp(playerY, 0, H - paddleHeight);

    // Computer follows the ball
    let cpuCenter = cpuY + paddleHeight / 2;
    let target = ballY;

    if (ballVX < 0) target = H / 2;

    if (cpuCenter < target - 10) cpuY += 4;
    if (cpuCenter > target + 10) cpuY -= 4;

    cpuY = clamp(cpuY, 0, H - paddleHeight);

    ballX += ballVX;
    ballY += ballVY;

    // Bounce off top and bottom
    if (ballY <= 9 || ballY >= H - 9) {
        ballVY *= -1;
        ballY = clamp(ballY, 9, H - 9);
    }

    // Player paddle collision
    if (
        ballVX < 0 &&
        ballX - 9 <= playerX + paddleWidth &&
        ballX + 9 >= playerX &&
        ballY + 9 >= playerY &&
        ballY - 9 <= playerY + paddleHeight
    ) {
        ballX = playerX + paddleWidth + 9;
        ballVX = Math.min(Math.abs(ballVX) + 0.3, 10);
        ballVY = ((ballY - (playerY + paddleHeight / 2)) /
                   (paddleHeight / 2)) * 5;
    }

    // Computer paddle collision
    if (
        ballVX > 0 &&
        ballX + 9 >= cpuX &&
        ballX - 9 <= cpuX + paddleWidth &&
        ballY + 9 >= cpuY &&
        ballY - 9 <= cpuY + paddleHeight
    ) {
        ballX = cpuX - 9;
        ballVX = -Math.min(Math.abs(ballVX) + 0.3, 10);
        ballVY = ((ballY - (cpuY + paddleHeight / 2)) /
                   (paddleHeight / 2)) * 5;
    }

    if (ballX < -10) {
        cpuScore++;
        resetBall(1);
        updateScore();
    }

    if (ballX > W + 10) {
        playerScore++;
        resetBall(-1);
        updateScore();
    }

    if (playerScore >= 7 || cpuScore >= 7) {
        finished = true;
        running = false;
        setStatus(playerScore >= 7 ?
            "🏆 YOU WIN! Press Restart to play again." :
            "💻 COMPUTER WINS! Press Restart to try again.");
    }
}

function draw() {
    ctx.clearRect(0, 0, W, H);

    // Center line
    ctx.strokeStyle = "#34445d";
    ctx.setLineDash([12, 12]);
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(W / 2, 0);
    ctx.lineTo(W / 2, H);
    ctx.stroke();
    ctx.setLineDash([]);

    // Player paddle
    ctx.fillStyle = "#00e5ff";
    ctx.fillRect(playerX, playerY, paddleWidth, paddleHeight);

    // Computer paddle
    ctx.fillStyle = "#ff4d91";
    ctx.fillRect(cpuX, cpuY, paddleWidth, paddleHeight);

    // Ball
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.arc(ballX, ballY, 9, 0, Math.PI * 2);
    ctx.fill();
}

let previousTime = 0;
let accumulator = 0;
const step = 1000 / 60;

function gameLoop(timestamp) {
    if (!previousTime) previousTime = timestamp;
    accumulator += Math.min(timestamp - previousTime, 100);
    previousTime = timestamp;

    while (accumulator >= step) {
        update();
        accumulator -= step;
    }

    draw();
    requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);
</script>
</body>
</html>
    """,
    height=660
)
