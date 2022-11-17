'use strict';

{

const checkboxList = document.querySelectorAll('.join-table__checkbox');
const warning = document.querySelector('.join__warning-oversize');
const btnJoin = document.querySelector('.join__btn-submit');

const MAX_SIZE = 25;

let totalCheckedCount = 0;
let totalSize = 0;

checkboxList.forEach(item => {
  item.addEventListener('change', handleOnChange);
})

function handleOnChange(){
  initVars();
  checkboxList.forEach(item => {
    if(item.checked){
      addSize(item);
      countChecked();
    }
  })
  if(totalSize >= MAX_SIZE){
    showWarning();
    hideBtn();
  } else {
    hideWarning();
    if(totalCheckedCount >= 2){
      showBtn();
    } else {
      hideBtn();
    }
  }
}



function initVars(){
  totalCheckedCount = 0;
  totalSize = 0;
}

function addSize(checkedItem){
  const id = `size-${checkedItem.closest('.table tbody tr').dataset.id}`;
  const element = document.getElementById(id);
  const value = element.innerText.replace(/[a-z|A-Z]+/g, '');
  totalSize += Number(value);
}

function countChecked(){
  totalCheckedCount++;
}

function showBtn(){
  btnJoin.removeAttribute('disabled');
}
function hideBtn(){
  btnJoin.setAttribute('disabled', true);
}

function showWarning(){
  warning.classList.remove('-hidden');
  warning.innerText = `データサイズの合計を${MAX_SIZE}MB未満にしてください。`;
}
function hideWarning(){
  warning.classList.add('-hidden');
}

}