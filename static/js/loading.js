'use strict';

{

class Icon {

  constructor(canvas){
    this.dpr = window.devicePixelRatio;
    this.adjustPixel(canvas);
    this.newW = canvas.width;
    this.newH = canvas.height;
    this.ctx = canvas.getContext('2d');
    this.r = 80;
    this.angle = 0;
  }

  adjustPixel(canvas) {
    const w = canvas.width;
    const h = canvas.height;
    const newW = w * this.dpr;
    const newH = h * this.dpr;
    canvas.width = newW;
    canvas.height = newH;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
  }

  draw() {
    this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    this.ctx.fillRect(0, 0, this.newW, this.newH);

    this.ctx.save();

    this.ctx.translate(this.newW / 2, this.newH / 2);
    this.ctx.rotate(Math.PI / 180 * this.angle);

    this.ctx.beginPath();
    this.ctx.moveTo(0, 0 -this.r - (5 * this.dpr));
    this.ctx.lineTo(0, 0 -this.r + (5 * this.dpr));
    this.ctx.strokeStyle = 'gray';
    this.ctx.lineWidth = 5 * this.dpr;
    this.ctx.stroke();

    this.ctx.restore();
  }

  update() {
    this.angle += 14;
  }

  run(){
    this.update();
    this.draw();

    setTimeout(() => {
      this.run();
    }, 80);
  }

}

// ---------------------------------------------------------------------------

const contentsFormatter = document.querySelector('.contents-formatter');
const form = document.querySelector('form');  // 要素セレクター
const loading = document.querySelector('.loading');

form.addEventListener('submit', handleOnSubmit);

function handleOnSubmit() {
  hideContents();
  showLoading();
  runLoading();
}

function hideContents() {
  contentsFormatter.classList.add('-hidden');
}
function showLoading() {
  loading.classList.remove('-hidden');
}

function runLoading() {
  drawIcon();
  drawText();
}

function drawIcon() {
  const canvas = document.querySelector('.loading__canvas');
  if(typeof canvas.getContext === 'undefined'){
    console.error('Canvas is not supported.');
    return;
  }
  const icon = new Icon(canvas);
  icon.run();
}

function drawText() {
  const element = document.querySelector('.loading__text-dot');
  const DOT_MAX = 3;
  let dotCount = 0;
  let dot = '';
  setInterval(() => {
    if(dotCount < DOT_MAX) {
      dot += '.'
      dotCount++;
    } else {
      dot = '';
      dotCount = 0;
    }
    element.innerHTML = dot;
  }, 800);
}
  
}