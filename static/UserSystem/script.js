const line = document.getElementById('line');
const handle = document.getElementById('handle');
const number = document.getElementById('number');

let isDragging = false;
let minPosition = 0;
let maxPosition = line.offsetWidth;

handle.addEventListener('mousedown', startDrag);
window.addEventListener('mouseup', stopDrag);
window.addEventListener('mousemove', drag);

function startDrag(e) {
    isDragging = true;
}

function stopDrag() {
    isDragging = false;
}

function drag(e) {
    if (!isDragging) return;

    let newPosition = e.clientX - line.getBoundingClientRect().left;
    if (newPosition < minPosition) {
        newPosition = minPosition;
    } else if (newPosition > maxPosition) {
        newPosition = maxPosition;
    }

    handle.style.left = newPosition + 'px';
    let percent = (newPosition / maxPosition) * 100;
    number.textContent = Math.round(percent);
}
