'use strict';

{

const emailInput = document.querySelector('.login__input-email');
const emailWarning = document.querySelector('.login__warning-email');

const button = document.querySelector('.login__btn-submit');



let emailIsCorrect = false;

let btnOnceClicked = false;



button.addEventListener('click', (e) => {
  btnOnceClicked = true;
  testEmail();
  if(!emailIsCorrect){
    e.preventDefault();
    return;
  }
});

emailInput.addEventListener('keyup', () => {
  if(!btnOnceClicked){
    return;
  }
  testEmail();
});



function testEmail() {
  const value = emailInput.value;
  const regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/g;
  const isCorrect = regex.test(value);
  if(isCorrect && value !== ''){
    emailIsCorrect = true;
    emailWarning.classList.add('-hidden');
  } else {
    emailIsCorrect = false;
    emailWarning.classList.remove('-hidden');
  }
}

}