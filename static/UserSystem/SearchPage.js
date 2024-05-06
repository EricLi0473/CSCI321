function showImage(algorithm) {
    var lsmImage = document.getElementById('lsmImage');
    var linearImage = document.getElementById('linearImage');
    var svmImage = document.getElementById('svmImage');

    lsmImage.style.display = 'none';
    linearImage.style.display = 'none';
    svmImage.style.display = 'none';

    switch (algorithm) {
      case 'LSM':
        lsmImage.style.display = 'block';
        break;
      case 'Linear':
        linearImage.style.display = 'block';
        break;
      case 'SVM':
        svmImage.style.display = 'block';
        break;
      default:
        break;
    }
  }