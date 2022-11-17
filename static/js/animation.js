'use strict';

{

const tl = gsap.timeline(
  {
    delay: 2,
    repeat: -1,
    repeatDelay: 8
  }
);

tl.from(
  '.circle-from-left',
  {
    transformOrigin: '0% 0%',
    ease: 'power4.out',
    duration: 2.5,
    xPercent: -100,
    x: '-30vw'
  }
)
tl.from(
  '.circle-from-right',
  {
    transformOrigin: '0% 0%',
    ease: 'power4.out',
    duration: 2.5,
    xPercent: 100,
    x: '70vw'
  },
  '<'
)

tl.to(
  ['.circle-from-left','.circle-from-right'],
  {
    duration: 0.01,
    border: 'none',
  }
)

tl.to(
  ['.circle-from-left','.circle-from-right'],
  {
    ease: 'elastic.out',
    duration: 1.5,
    backgroundColor: '#ed7a2f',
    scale: 1.5 
  }
)

tl.to(
  ['.circle-from-left','.circle-from-right'],
  {
    delay: 1,
    duration: 0.5,
    opacity: 0,
    y: '-15vw',
    ease: 'back.in'
  }
)

}