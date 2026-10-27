import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Bikini Bottom Pong", page_icon="🧽", layout="wide")
st.title("🧽 Bikini Bottom Pong 🍍")
st.caption("SpongeBob vs. Patrick — first to 7 Krabby Patties wins!")

components.html(r"""
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>
*{box-sizing:border-box}body{margin:0;background:linear-gradient(#087ab0,#063a72);color:#fff;font-family:'Trebuchet MS',Arial,sans-serif;text-align:center;overflow-x:hidden}
.top{display:flex;justify-content:space-around;align-items:center;padding:12px 0 5px;max-width:900px;margin:auto}
.name{font-size:clamp(16px,3vw,25px);font-weight:900;text-shadow:2px 3px #08416a}.score{font-size:clamp(26px,5vw,46px);font-weight:900;color:#ffef66;text-shadow:2px 3px #194573}
canvas{display:block;width:min(96%,900px);height:auto;aspect-ratio:900/500;margin:auto;border:5px solid #ffdf5c;border-radius:18px;box-shadow:0 7px 0 #b67a22,0 12px 25px #002a47;background:#0b8dc0;outline:none;touch-action:none}
.controls{padding:15px 0 5px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}button,select{border:0;border-radius:18px;background:#ffdf5c;color:#3c3763;font-size:16px;font-weight:900;padding:12px 18px;cursor:pointer;box-shadow:0 4px #d19a38}button:hover{background:#fff399}select{background:#f8d2eb}#message{font-weight:bold;min-height:28px;padding:8px;color:#fff6b1}.hint{font-size:13px;margin:4px 0 10px;opacity:.95}
</style></head><body>
<div class="top"><div class="name">🧽 SPONGEBOB <div class="score" id="pScore">0</div></div><div style="font-weight:900;color:#ffec7b">BIKINI BOTTOM<br>🏓 PONG</div><div class="name">⭐ PATRICK (CPU)<div class="score" id="cScore">0</div></div></div>
<canvas id="game" width="900" height="500" tabindex="0" aria-label="Play Pong as SpongeBob against Patrick"></canvas>
<div class="controls"><button id="start">▶ Start / Resume</button><button id="pause">⏸ Pause</button><button id="restart">🔄 Restart</button><select id="difficulty" aria-label="Difficulty"><option value="easy">Easy</option><option value="normal" selected>Normal</option><option value="hard">Hard</option></select></div>
<div id="message">Click Start, then use W / S or ↑ / ↓ to move SpongeBob.</div><div class="hint">On phones/tablets, drag your finger up and down the game.</div>
<script>
const canvas=document.getElementById('game'),c=canvas.getContext('2d'),W=900,H=500;
const paddleH=104,paddleW=29,px=36,cx=W-65,rad=12;
let py=H/2-paddleH/2,cy=py,bx=W/2,by=H/2,vx=5,vy=2.3,ps=0,cs=0,playing=false,ended=false,last=0;
const keys=new Set(),clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const bubbleData=Array.from({length:24},(_,i)=>({x:Math.random()*W,y:Math.random()*H,r:3+Math.random()*13,s:.2+Math.random()*.45}));
const message=t=>document.getElementById('message').textContent=t;
function score(){document.getElementById('pScore').textContent=ps;document.getElementById('cScore').textContent=cs}
function serve(d){bx=W/2;by=H/2;vx=d*5;vy=(Math.random()*4-2)||1.7}
function reset(){ps=cs=0;py=cy=H/2-paddleH/2;ended=false;playing=true;serve(Math.random()<.5?1:-1);score();message('Go SpongeBob! Catch that Krabby Patty!');canvas.focus()}
document.getElementById('start').onclick=()=>{if(ended)reset();else{playing=true;message('Krabby Patty rally in progress!');canvas.focus()}};
document.getElementById('pause').onclick=()=>{playing=false;message('Taking a jellyfishing break!')};
document.getElementById('restart').onclick=reset;
window.addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','w','s','W','S'].includes(e.key)){e.preventDefault();keys.add(e.key.toLowerCase())}});
window.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));
window.addEventListener('blur',()=>keys.clear());
function touchMove(e){let rect=canvas.getBoundingClientRect(),y=(e.clientY-rect.top)*H/rect.height;py=clamp(y-paddleH/2,0,H-paddleH)}
canvas.addEventListener('pointerdown',e=>{canvas.setPointerCapture(e.pointerId);touchMove(e);canvas.focus()});canvas.addEventListener('pointermove',e=>{if(e.buttons)touchMove(e)});
function update(dt){
 const speed=7*dt;
 if(keys.has('w')||keys.has('arrowup'))py-=speed;
 if(keys.has('s')||keys.has('arrowdown'))py+=speed;
 py=clamp(py,0,H-paddleH);
 let difficulty=document.getElementById('difficulty').value;
 let aiSpeed={easy:2.7,normal:4.0,hard:5.5}[difficulty]*dt;
 let target=vx>0?by:H/2;
 cy=clamp(cy+clamp(target-(cy+paddleH/2),-aiSpeed,aiSpeed),0,H-paddleH);
 bx+=vx*dt;by+=vy*dt;
 if(by<rad){by=rad;vy=Math.abs(vy)}if(by>H-rad){by=H-rad;vy=-Math.abs(vy)}
 if(vx<0&&bx-rad<=px+paddleW&&bx+rad>=px&&by+rad>=py&&by-rad<=py+paddleH){bx=px+paddleW+rad;vx=Math.min(Math.abs(vx)*1.055,11);vy=((by-(py+paddleH/2))/(paddleH/2))*5.5}
 if(vx>0&&bx+rad>=cx&&bx-rad<=cx+paddleW&&by+rad>=cy&&by-rad<=cy+paddleH){bx=cx-rad;vx=-Math.min(Math.abs(vx)*1.055,11);vy=((by-(cy+paddleH/2))/(paddleH/2))*5.5}
 if(bx<-rad){cs++;serve(1);score()}if(bx>W+rad){ps++;serve(-1);score()}
 if(ps>=7||cs>=7){ended=true;playing=false;message(ps>=7?'🏆 SpongeBob wins! Best fry cook in Bikini Bottom!':'⭐ Patrick wins! Try again, SpongeBob!')}
}
function flower(x,y,r,color){c.strokeStyle=color;c.lineWidth=5;c.lineCap='round';for(let j=0;j<5;j++){let a=j*Math.PI*2/5;c.beginPath();c.moveTo(x+Math.cos(a)*r*.27,y+Math.sin(a)*r*.27);c.lineTo(x+Math.cos(a)*r,y+Math.sin(a)*r);c.stroke()}c.beginPath();c.arc(x,y,r*.25,0,7);c.stroke()}
function background(t){
 let g=c.createLinearGradient(0,0,0,H);g.addColorStop(0,'#0a95cd');g.addColorStop(.7,'#127da7');g.addColorStop(1,'#126a9a');c.fillStyle=g;c.fillRect(0,0,W,H);
 flower(160,90,32,'#85daee');flower(740,110,37,'#efc7fa');flower(490,60,21,'#c1eaa2');
 c.fillStyle='#edda9c';c.fillRect(0,H-37,W,37);c.fillStyle='#d5ba7f';for(let i=0;i<W;i+=37){c.beginPath();c.arc(i+12,H-18,2.4,0,7);c.fill()}
 for(let i=0;i<16;i++){let x=i*65-25;c.strokeStyle='#7db975';c.lineWidth=3;c.beginPath();c.moveTo(x,H-37);c.quadraticCurveTo(x-12,H-66,x+5,H-81);c.stroke()}
 bubbleData.forEach(b=>{let y=(b.y-t*b.s*.018+H+50)%(H+50);c.strokeStyle='rgba(220,248,255,.45)';c.lineWidth=2;c.beginPath();c.arc(b.x,y,b.r,0,7);c.stroke()});
 c.strokeStyle='rgba(255,255,255,.40)';c.lineWidth=3;c.setLineDash([11,14]);c.beginPath();c.moveTo(W/2,0);c.lineTo(W/2,H-37);c.stroke();c.setLineDash([])
}
function sponge(y){c.save();c.translate(px,y);c.fillStyle='#ffe24c';c.strokeStyle='#765b19';c.lineWidth=3;c.beginPath();c.roundRect(0,0,paddleW,paddleH-24,5);c.fill();c.stroke();c.fillStyle='#bdad20';[[6,9,3],[22,16,4],[9,57,4],[21,69,3]].forEach(a=>{c.beginPath();c.arc(...a,0,7);c.fill()});
 c.fillStyle='#fff';c.beginPath();c.arc(11,29,8,0,7);c.arc(24,29,8,0,7);c.fill();c.fillStyle='#2da9eb';c.beginPath();c.arc(12,29,3,0,7);c.arc(24,29,3,0,7);c.fill();c.fillStyle='#4c2f21';c.fillRect(13,49,9,3);c.fillStyle='#fff';c.fillRect(13,52,4,7);c.fillRect(19,52,4,7);c.fillStyle='#fff';c.fillRect(0,paddleH-24,paddleW,9);c.fillStyle='#854525';c.fillRect(0,paddleH-15,paddleW,15);c.fillStyle='#e64c53';c.beginPath();c.moveTo(11,paddleH-24);c.lineTo(18,paddleH-24);c.lineTo(15,paddleH-13);c.fill();c.restore()}
function patrick(y){c.save();c.translate(cx,y);c.fillStyle='#ffa2b2';c.strokeStyle='#9c4e69';c.lineWidth=2;c.beginPath();c.moveTo(14,0);c.lineTo(28,42);c.lineTo(28,75);c.lineTo(24,75);c.lineTo(28,paddleH);c.lineTo(0,paddleH);c.lineTo(5,75);c.lineTo(0,75);c.lineTo(0,42);c.closePath();c.fill();c.stroke();c.fillStyle='#fff';c.beginPath();c.ellipse(10,43,5,8,0,0,7);c.ellipse(20,43,5,8,0,0,7);c.fill();c.fillStyle='#1b2638';c.beginPath();c.arc(11,44,2,0,7);c.arc(19,44,2,0,7);c.fill();c.strokeStyle='#854759';c.beginPath();c.arc(15,57,4,0,Math.PI);c.stroke();c.fillStyle='#9cdd78';c.fillRect(0,76,paddleW,16);c.fillStyle='#a064bd';c.fillRect(7,80,6,5);c.fillRect(21,84,5,4);c.restore()}
function patty(){c.save();c.translate(bx,by);c.fillStyle='#f1b84e';c.beginPath();c.ellipse(0,-5,rad+3,7,0,Math.PI,Math.PI*2);c.fill();c.fillStyle='#66a244';c.fillRect(-rad-2,-5,2*rad+4,4);c.fillStyle='#75412b';c.fillRect(-rad-1,-1,2*rad+2,5);c.fillStyle='#ffe48b';c.beginPath();c.ellipse(0,6,rad+3,5,0,0,7);c.fill();c.fillStyle='#fff2b1';for(let i=-7;i<=7;i+=7){c.fillRect(i,-8,3,2)}c.restore()}
function draw(t){background(t);sponge(py);patrick(cy);patty();if(!playing){c.fillStyle='rgba(3,30,58,.44)';c.fillRect(180,202,540,85);c.fillStyle='#fff7aa';c.font='bold 26px Trebuchet MS';c.textAlign='center';c.fillText(ended?'MATCH OVER!':'PRESS START TO PLAY',W/2,254)}}
function loop(t){let dt=Math.min((t-last)/16.666||1,2);last=t;if(playing)update(dt);draw(t);requestAnimationFrame(loop)}requestAnimationFrame(loop);
</script></body></html>
""", height=760, scrolling=True)
