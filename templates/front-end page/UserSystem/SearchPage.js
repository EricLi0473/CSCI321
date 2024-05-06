function showImage(algorithm) {
    var lsmImage = document.getElementById('lsmImage');
    var linearImage = document.getElementById('linearImage');
    var svmImage = document.getElementById('svmImage');
  
    // 隐藏所有图像
    lsmImage.style.display = 'none';
    linearImage.style.display = 'none';
    svmImage.style.display = 'none';
  
    // 根据传入的算法名称显示对应的图像
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