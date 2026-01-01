// Squares.js - Ported from React Bits Backgrounds
// Minimalist grid background

function initSquares() {
    const container = document.getElementById('squares-bg');
    if (!container) return;

    const canvas = document.createElement('canvas');
    canvas.className = 'squares-canvas';
    container.appendChild(canvas);
    const ctx = canvas.getContext('2d');

    const config = {
        direction: 'diagonal',
        speed: 0.2,
        borderColor: '#F0F0F0',
        squareSize: 40,
        hoverFillColor: '#FFF5F6', // Very subtle light red
    };

    let numSquaresX, numSquaresY;
    let gridOffset = { x: 0, y: 0 };
    let hoveredSquare = null;

    function resizeCanvas() {
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
        numSquaresX = Math.ceil(canvas.width / config.squareSize) + 1;
        numSquaresY = Math.ceil(canvas.height / config.squareSize) + 1;
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function drawGrid() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const startX = Math.floor(gridOffset.x / config.squareSize) * config.squareSize;
        const startY = Math.floor(gridOffset.y / config.squareSize) * config.squareSize;

        for (let x = startX; x < canvas.width + config.squareSize; x += config.squareSize) {
            for (let y = startY; y < canvas.height + config.squareSize; y += config.squareSize) {
                const squareX = x - (gridOffset.x % config.squareSize);
                const squareY = y - (gridOffset.y % config.squareSize);

                if (
                    hoveredSquare &&
                    Math.floor((x - startX) / config.squareSize) === hoveredSquare.x &&
                    Math.floor((y - startY) / config.squareSize) === hoveredSquare.y
                ) {
                    ctx.fillStyle = config.hoverFillColor;
                    ctx.fillRect(squareX, squareY, config.squareSize, config.squareSize);
                }

                ctx.strokeStyle = config.borderColor;
                ctx.lineWidth = 1;
                ctx.strokeRect(squareX, squareY, config.squareSize, config.squareSize);
            }
        }

        // Add a subtle radial fade
        const gradient = ctx.createRadialGradient(
            canvas.width / 2,
            canvas.height / 2,
            0,
            canvas.width / 2,
            canvas.height / 2,
            Math.sqrt(canvas.width ** 2 + canvas.height ** 2) / 2
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0)');
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0.8)');

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function updateAnimation() {
        const effectiveSpeed = Math.max(config.speed, 0.1);
        gridOffset.x = (gridOffset.x - effectiveSpeed + config.squareSize) % config.squareSize;
        gridOffset.y = (gridOffset.y - effectiveSpeed + config.squareSize) % config.squareSize;

        drawGrid();
        requestAnimationFrame(updateAnimation);
    }

    container.addEventListener('mousemove', (event) => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;

        const startX = Math.floor(gridOffset.x / config.squareSize) * config.squareSize;
        const startY = Math.floor(gridOffset.y / config.squareSize) * config.squareSize;

        const hoveredSquareX = Math.floor((mouseX + gridOffset.x - startX) / config.squareSize);
        const hoveredSquareY = Math.floor((mouseY + gridOffset.y - startY) / config.squareSize);

        hoveredSquare = { x: hoveredSquareX, y: hoveredSquareY };
    });

    container.addEventListener('mouseleave', () => {
        hoveredSquare = null;
    });

    updateAnimation();
}

document.addEventListener('DOMContentLoaded', initSquares);

