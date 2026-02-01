window.onload = () => {
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");

  const modal = document.getElementById("modal");
  const modalContent = document.getElementById("modal-content");
  const attackBtn = document.getElementById("attack-btn");
  const closeBtn = document.getElementById("close-btn");
  const playerInfoDiv = document.getElementById("player-info");
  let selectedHex = null;
  let hexes = [];

  // Read player info
  const playerUsername = localStorage.getItem("playerUsername") || "Unknown";
  const playerTeam = localStorage.getItem("playerTeam") || "Neutral";
  playerInfoDiv.innerHTML = `<strong>${playerUsername}</strong> · Team ${playerTeam}`;

  // Load hexes from JSON
  fetch("hexes.json")
    .then(res => res.json())
    .then(data => { hexes = data; })
    .catch(err => console.error("Failed to load hexes.json:", err));

  // Resize canvas
  function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
  resize();
  window.addEventListener("resize", resize);

  // Camera
  const camera = { x:0, y:0, zoom:1 };
  let dragging=false, lastMouse={x:0,y:0};

  canvas.addEventListener("mousedown", e=>{ dragging=true; lastMouse={x:e.clientX,y:e.clientY}; });
  canvas.addEventListener("mouseup", ()=>dragging=false);
  canvas.addEventListener("mouseleave", ()=>dragging=false);
  canvas.addEventListener("mousemove", e=>{
    if(!dragging) return;
    camera.x -= (e.clientX-lastMouse.x)/camera.zoom;
    camera.y -= (e.clientY-lastMouse.y)/camera.zoom;
    lastMouse={x:e.clientX,y:e.clientY};
  });
  canvas.addEventListener("wheel", e=>{
    const zoomAmount = e.deltaY*-0.001;
    camera.zoom=Math.min(2,Math.max(0.5,camera.zoom+zoomAmount));
  });

  // HEX PARAMETERS
  const HEX_RADIUS = 50;
  const HEX_WIDTH = Math.sqrt(3)*HEX_RADIUS;
  const HEX_HEIGHT = 2*HEX_RADIUS;

  // Convert axial to pixel
  function hexToPixel(q,r){
    return {
      x: HEX_WIDTH * (q + r/2),
      y: 0.75 * HEX_HEIGHT * r
    };
  }

  function drawHex(x,y,radius,fill,glow){
    ctx.beginPath();
    for(let i=0;i<6;i++){
      const angle = Math.PI/180*(60*i - 30);
      const px = x + radius*Math.cos(angle);
      const py = y + radius*Math.sin(angle);
      i===0?ctx.moveTo(px,py):ctx.lineTo(px,py);
    }
    ctx.closePath();
    ctx.shadowBlur=glow;
    ctx.shadowColor=fill;
    ctx.fillStyle=fill;
    ctx.fill();
    ctx.shadowBlur=0;
    ctx.strokeStyle="#222";
    ctx.lineWidth=1;
    ctx.stroke();
  }

  function getHexColor(hex){ if(!hex.owner) return "#2a2f45"; return hex.owner==="blue"?"#2563eb":"#dc2626"; }
  function getGlowByDifficulty(hex){ switch(hex.difficulty){case"easy":return 5; case"medium":return 10; case"hard":return 15; default:return 0;} }

  // Click detection
  canvas.addEventListener("click", e=>{
    if(hexes.length===0) return;
    const rect=canvas.getBoundingClientRect();
    const mouseX=(e.clientX-rect.left-canvas.width/2)/camera.zoom + camera.x;
    const mouseY=(e.clientY-rect.top-canvas.height/2)/camera.zoom + camera.y;
    for(let hex of hexes){
      const {x,y}=hexToPixel(hex.q,hex.r);
      const dx=mouseX-x, dy=mouseY-y;
      if(Math.sqrt(dx*dx+dy*dy)<HEX_RADIUS*0.95){ 
        openModal(hex); 
        break; 
      }
    }
  });

  function openModal(hex){
    selectedHex = hex;
    modalContent.innerHTML = `
      <strong>Hex ID:</strong> ${hex.id} <br>
      <strong>Owner:</strong> ${hex.owner ?? "Neutral"} <br>
      <strong>Difficulty:</strong> ${hex.difficulty}
    `;
    modal.style.display="block";
  }

  function closeModal(){ modal.style.display="none"; }
  function attackHex(){
    if(!selectedHex) return;
    alert(`Solve a ${selectedHex.difficulty} problem to capture Hex ${selectedHex.id}!`);
    closeModal();
  }

  attackBtn.addEventListener("click", attackHex);
  closeBtn.addEventListener("click", closeModal);

  // Main loop
  function loop(){
    ctx.setTransform(1,0,0,1,0,0);
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.translate(canvas.width/2,canvas.height/2);
    ctx.scale(camera.zoom,camera.zoom);
    ctx.translate(-camera.x,-camera.y);

    if(hexes.length>0){
      for(let hex of hexes){
        const {x,y}=hexToPixel(hex.q,hex.r);
        drawHex(x,y,HEX_RADIUS,getHexColor(hex),getGlowByDifficulty(hex));
      }
    }

    requestAnimationFrame(loop);
  }
  loop();
};
