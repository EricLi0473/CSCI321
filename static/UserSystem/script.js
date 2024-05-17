        const line = document.getElementById('line');
        const handle = document.getElementById('handle');
        const number = document.getElementById('number');
        const timeFrameInput = document.getElementById('timeFrame');

        let isDragging = false;
        let minPosition = 0;
        let maxPosition = line.offsetWidth - handle.offsetWidth;

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

            let newPosition = e.clientX - line.getBoundingClientRect().left - handle.offsetWidth / 2;
            if (newPosition < minPosition) {
                newPosition = minPosition;
            } else if (newPosition > maxPosition) {
                newPosition = maxPosition;
            }

            handle.style.left = newPosition + 'px';
            let percent = (newPosition / maxPosition) * 100;

            // 将百分比限制在最小为1
            let displayNumber = Math.max(1, Math.round((percent / 100) * 100));
            number.textContent = displayNumber;
            timeFrameInput.value = displayNumber;
        }