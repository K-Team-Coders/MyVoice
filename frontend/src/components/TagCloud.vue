<template>
    <div>
      <span class="Sphere"></span>
    
    </div>
   
  </template>
  
  <script>
  import VueWordCloud from 'vuewordcloud';
  import TagCloud from 'TagCloud'
  export default {
    components:  [TagCloud],
    mounted(){
      const Texts = [
              'HTML', 'CSS', 'JAVASCRIPT',
              'SWIFT', 'MONGOOSE', 'REACT',
              'PYTHON', 'SASS',
              'DJANGO', 'NODEJS', 'MONGODB',
              'EXPRESS', 'MYSQL', 'JQUERY', 'JAVA'
          ];
  
          var tagCloud = TagCloud('.Sphere', Texts, {
  
              // Sphere radius in px
              radius: 230,
  
              // animation speed
              // slow, normal, fast
              maxSpeed: 'normal',
              initSpeed: 'fast',
  
              // Rolling direction [0 (top) , 90 (left), 135 (right-bottom)] 
              direction: 135,
  
              // interaction with mouse or not [Default true (decelerate to rolling init speed, and keep rolling with mouse).]
              keep: true
  
          });
  
          // Giving color to each text in sphere
          var color = '#FF5733 ';
          document.querySelector('.Sphere').style.color = color;
    }
  }
  </script>
  
  <style>
                
   /*     Importing Google fonts    */
   @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
  
  body {
    background-color: #000;
  }
  
   /* Applying CSS to sphere */
  .tagcloud {
    display: inline-block;
    top: 100px;
    left: 32%;
    font-weight: bold;
    letter-spacing: 1px;
    font-family: 'Bebas Neue', cursive;
    font-size: 20px;
  }
  
  /* Change color of each text in sphere on hover   */
  .tagcloud--item:hover {
    color: #FFC300 ;
  }
  </style>