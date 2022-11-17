'use strict';

{

const emailInput = document.querySelector('.signup__input-email');
const passwordInput = document.querySelector('.signup__input-password');
const confirmInput = document.querySelector('.signup__input-confirmPassword');

const emailWarning = document.querySelector('.signup__warning-email');
const passwordWarning = document.querySelector('.signup__warning-password');

const button = document.querySelector('.signup__btn-submit');



let emailIsCorrect = false;
let passwordIsSame = false;

let btnOnceClicked = false;



button.addEventListener('click', (e) => {
  btnOnceClicked = true;
  testEmail();
  checkPasswordValueSame();
  if(!emailIsCorrect || !passwordIsSame){
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

passwordInput.addEventListener('keyup', () => {
  if(!btnOnceClicked){
    return;
  }
  checkPasswordValueSame();
});
confirmInput.addEventListener('keyup', () => {
  if(!btnOnceClicked){
    return;
  }
  checkPasswordValueSame();
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

function checkPasswordValueSame() {
  const passwordValue = passwordInput.value;
  const confirmValue = confirmInput.value;
  if(passwordValue === confirmValue && passwordValue !== '' && confirmValue !== ''){
    passwordIsSame = true;
    passwordWarning.classList.add('-hidden');
  } else {
    passwordIsSame = false;
    passwordWarning.classList.remove('-hidden');
  }
}

}