<template>
    <div >
      <span ref="text_isOpened" class="Sphere"></span>
        <h1  v-if="text_isOpened">СОСАААТЬ {{ opened_textID }}</h1>
    </div>
   
  </template>
  
  <script>
  import TagCloud from 'TagCloud'
  export default {
    components:  [TagCloud],
    data(){
        return {
            text_isOpened: false,
            opened_textID: '',
        }
    },
    methods:{
        openTag(opened_textID){
            this.text_isOpened = true
            this.opened_textID = opened_textID
            console.log(this.text_isOpened)
            return this.opened_textID
        }
    },
    mounted(){
        
      const Texts = [
             'Жора', 'Еда', 'По идее один кластер??', 'Шавуха'
          ];
  
          let tagCloud = TagCloud('.Sphere', Texts, {
  
              // Sphere radius in px
              radius: 230,
  
              // animation speed
              // slow, normal, fast
              maxSpeed: 'fast',
              initSpeed: 'fast',
  
              // Rolling direction [0 (top) , 90 (left), 135 (right-bottom)] 
              direction: 135,
  
              // interaction with mouse or not [Default true (decelerate to rolling init speed, and keep rolling with mouse).]
              keep: true
  
          });
  
          // Giving color to each text in sphere
          let color = '#544adde1';

          document.querySelector('.Sphere').style.color = color;
          let rootEl = document.querySelector('.tagcloud');
            rootEl.addEventListener('click', function clickEventHandler(e) {
            if (e.target.className === 'tagcloud--item') {
            //  window.open(`https://www.google.com/search?q=${e.target.innerText}`, '_blank');
            const box = `
  <div id='box'>
    <button id='button-1'>Button</button>
  </div>`;

document.body.innerHTML = box;
            
    }
});
    }
  }
  </script>
  
  <style>
                
   /*     Importing Google fonts    */
   @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
  
  .backbody {
    background-color: #000;
  }
  
   /* Applying CSS to sphere */
  .tagcloud {
    display: inline-block;
    top: 100px;
    left: 32%;
    font-weight: bold;
    letter-spacing: 1px;
    font-family: 'Roboto', italic;
    font-size: 20px;
  }
  
  /* Change color of each text in sphere on hover   */
  .tagcloud--item:hover {
    color: #1a128fe1 ;
  }
  </style>