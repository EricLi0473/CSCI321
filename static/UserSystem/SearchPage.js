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

    document.getElementById('fileInput').addEventListener('change', function() {
    var fileInput = document.getElementById('fileInput');
    var tickerInput = document.getElementById('tickerSymbol');

    if (fileInput.files.length > 0) {
    tickerInput.disabled = true;
} else {
    tickerInput.disabled = false;
}
});
//
function showImage(algorithm) {
    var lsmImage = document.getElementById('lsmImage');
    var linearImage = document.getElementById('linearImage');
    var svmImage = document.getElementById('svmImage');

    lsmImage.style.display = 'none';
    linearImage.style.display = 'none';
    svmImage.style.display = 'none';

    switch (algorithm) {
      case 'LR':
        lsmImage.style.display = 'block';
        break;
      case 'LSTM':
        linearImage.style.display = 'block';
        break;
      case 'GRU':
        svmImage.style.display = 'block';
        break;
      default:
        break;
    }
  }
    // form.addEventListener('submit', function(event) {
    //     event.preventDefault();
    //
    //     const formData = new FormData(form);
    //
    //     fetch('/getPredictionResult', {
    //         method: 'POST',
    //         body: formData
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             // 处理成功的情况，例如显示结果
    //             console.log('Prediction result:', data.result);
    //         } else {
    //             // 显示错误信息
    //             alert(data.error);
    //         }
    //     })
    //     .catch(error => {
    //         console.error('Error:', error);
    //     });
    // });