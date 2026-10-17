(function () {
  const canvas = document.getElementById("aura");
  if (!canvas || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const gl = canvas.getContext("webgl", { alpha: true, antialias: false, powerPreference: "low-power" });
  if (!gl) return;

  const vs = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  const fs = [
    "precision mediump float;",
    "uniform vec2 r;uniform float t;uniform vec2 m;uniform float s;",
    "float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}",
    "float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);",
    "return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}",
    "float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*n(p);p=p*2.02+vec2(3.1,1.7);a*=.5;}return v;}",
    "void main(){",
    "vec2 uv=gl_FragCoord.xy/r;vec2 q=(gl_FragCoord.xy-.5*r)/r.y;",
    "float tt=t*.05;",
    "vec2 w=vec2(fbm(q*2.+tt),fbm(q*2.-tt+4.));",
    "float f=fbm(q*2.4+w*1.6+vec2(0.,s*.0006));",
    "float d=length(q-(m-.5)*vec2(r.x/r.y,1.));",
    "float halo=exp(-d*3.2);",
    "vec3 teal=vec3(.18,.83,.75);vec3 amber=vec3(.94,.69,.23);vec3 blue=vec3(.35,.66,1.);",
    "vec3 c=mix(teal,blue,smoothstep(.3,.8,f));",
    "c=mix(c,amber,smoothstep(.55,1.,fbm(q*3.-w*2.+tt*2.))*.7);",
    "float v=smoothstep(.35,.9,f)*.16+halo*.12;",
    "float edge=smoothstep(.0,.45,1.-length(uv-.5)*1.1);",
    "gl_FragColor=vec4(c*v*edge,v*edge);",
    "}"
  ].join("\n");

  function sh(type, src) {
    const o = gl.createShader(type);
    gl.shaderSource(o, src);
    gl.compileShader(o);
    return o;
  }
  const prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs));
  gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const U = { r: gl.getUniformLocation(prog, "r"), t: gl.getUniformLocation(prog, "t"), m: gl.getUniformLocation(prog, "m"), s: gl.getUniformLocation(prog, "s") };

  let mx = 0.5, my = 0.5, cx = 0.5, cy = 0.5, w = 0, h = 0;
  const scale = 0.5;
  function resize() {
    w = Math.floor(innerWidth * scale);
    h = Math.floor(innerHeight * scale);
    canvas.width = w;
    canvas.height = h;
    gl.viewport(0, 0, w, h);
  }
  addEventListener("resize", resize);
  addEventListener("pointermove", (e) => { mx = e.clientX / innerWidth; my = 1 - e.clientY / innerHeight; });
  resize();

  let vis = true;
  document.addEventListener("visibilitychange", () => { vis = !document.hidden; });
  const t0 = performance.now();
  function frame(now) {
    requestAnimationFrame(frame);
    if (!vis) return;
    cx += (mx - cx) * 0.05;
    cy += (my - cy) * 0.05;
    gl.uniform2f(U.r, w, h);
    gl.uniform1f(U.t, (now - t0) / 1000);
    gl.uniform2f(U.m, cx, cy);
    gl.uniform1f(U.s, scrollY);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  requestAnimationFrame(frame);
})();
