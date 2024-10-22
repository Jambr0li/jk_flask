const canvas = document.getElementById('background-canvas');
const c = canvas.getContext('2d');

let mouse = {
    x: undefined,
    y: undefined,
    active: false
};
let mouseMoveTimeout;
window.addEventListener('mousemove', function(event) {
    mouse.x = event.x;
    mouse.y = event.y;
    mouse.active = true;

    this.clearTimeout(mouseMoveTimeout);

    mouseMoveTimeout = setTimeout(function() {
        mouse.active = false;
    }, 200)
});

window.addEventListener('resize', function() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    init();
});

let circleArr = [];

function init() {
    circleArr = [];
    for (let i = 0; i < 800; i++) {
        let radius = Math.random() * 3 + 1;
        let x = Math.random() * (innerWidth - radius * 2) + radius;
        let y = Math.random() * (innerHeight - radius * 2) + radius;
        let dx = (Math.random() - 0.5) * 5;
        let dy = (Math.random() - 0.5) * 5;
        circleArr.push(new Circle(x, y, dx, dy, radius));
    }
}

const bound = 50;
const maxRadius = 40;

const colorArray = [
    "#4F7CAC",
    "#C0E0DE",
    "#162521",
    "#3C474B",
    "#9EEFE5",
    "#ff9999",
];

function Circle(x, y, dx, dy, r) {
    this.x = x;
    this.y = y;
    this.dx = dx;
    this.dy = dy;
    this.r = r;
    this.minRadius = r;
    this.color = colorArray[Math.floor(Math.random() * colorArray.length)];

    this.draw = function() {
        c.beginPath();
        c.arc(this.x, this.y, this.r, 0, Math.PI * 2, false);
        c.fillStyle = this.color;
        c.fill();
    };

    this.update = function() {
        if (this.x > innerWidth - this.r || this.x < this.r) {
            this.dx = -this.dx;
        }
        if (this.y > innerHeight - this.r || this.y < this.r) {
            this.dy = -this.dy;
        }
        this.x += this.dx;
        this.y += this.dy;

        // Interactivity
        if (
            (mouse.x !== undefined && Math.abs(mouse.x - this.x) < bound &&
            Math.abs(mouse.y - this.y) < bound && mouse.active)
        ) {
            if (this.r < maxRadius) {
                this.r += 1; // Adjusted from 10 to 1 for smoother animation
            }
            this.draw();
        } else if (this.r > this.minRadius) {
            this.r -= 1;
            this.draw();
        }

        // this.draw();
    };
}

function animate() {
    requestAnimationFrame(animate);
    c.clearRect(0, 0, innerWidth, innerHeight);
    for (let i = 0; i < circleArr.length; i++) {
        circleArr[i].update();
    }
}

// Initialize canvas size and start animation
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
init();
animate();