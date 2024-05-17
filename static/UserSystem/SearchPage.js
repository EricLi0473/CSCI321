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
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch('/getPredictionResult', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 处理成功的情况，例如显示结果
                console.log('Prediction result:', data.result);
            } else {
                // 显示错误信息
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });