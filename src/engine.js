// Engine: renders PAGES from story.js into #app. No story text lives here.
import { HEROES } from './heroes.js';
import { INSTRUMENTS } from './instruments.js';
import { ISSUE, ISSUES, PAGES, CAREFUL } from './story.js';

const state = { hero: null, name: '', role: 'dev', mood: 'confident', i: 0, est1: null, est2: null, right: 0, asked: 0 };
const RESET = { ...state };
const devName = () => state.role === 'dev' ? (state.name || HEROES[state.hero].name) : HEROES[state.hero].name;
const you = () => state.role === 'dev' ? devName() : (state.name || 'you');
const think = (t) => state.mood === 'careful' ? (CAREFUL[t] ?? t) : t;
const app = document.getElementById('app');
const h = (html) => { const t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; };
const art = (key, cls = 'art', style = '') => { const src = HEROES[state.hero]?.art[key]; return src ? `<img class="${cls}" src="${src}" alt="" style="${style}">` : ''; };
const BURST = `<svg class="burst" viewBox="0 0 200 200" aria-hidden="true"><polygon fill="#FFD22E" stroke="#111" stroke-width="3" points="100,4 116,38 152,18 146,58 190,56 158,84 196,110 154,116 174,158 134,140 132,186 100,156 68,186 66,140 26,158 46,116 4,110 42,84 10,56 54,58 48,18 84,38"/></svg>`;
const guessPages = () => PAGES.filter(p => p.type === 'guess').length;

function masthead(sub) {
  return `<div class="masthead"><h1>${ISSUE.title.replace(' the ', '<br>the ')}</h1><span>${sub}</span></div>`;
}
function stagger() { document.querySelectorAll('.panel:not([hidden])').forEach((p, i) => setTimeout(() => p.classList.add('in'), 150 + i * 400)); }
function go() { state.i++; window.scrollTo({ top: 0 }); render(); }
function inst(name, phase) { return `<div class="fx inst">${INSTRUMENTS[name][phase]}</div>`; }

/* ---------- cover ---------- */
function renderCover() {
  const hero = HEROES.maya;
  const issues = ISSUES.map(i => `<button class="opt ${i.available ? '' : 'soon'} ${i.n === ISSUE.number ? 'on' : ''}" ${i.available ? '' : 'disabled'}><b>#${i.n}</b> ${i.title}<small>${i.available ? i.tagline : 'coming soon'}</small></button>`).join('');
  app.replaceChildren(h(`<div class="page cover">
    <div class="tag">Issue #${ISSUE.number} · ${ISSUE.tagline}</div>
    <div class="coverart"><div class="half"></div><div class="title">${ISSUE.title.replace(' the ', '<br>the ')}</div>
      <img class="art" src="${hero.art.alarm}" alt=""><div class="sfx" style="left:6%;right:auto;top:auto;bottom:8%;transform:rotate(-8deg) scale(1);font-size:clamp(28px,5vw,44px);color:var(--yel)">IT'S JUST<br>ONE WORD!</div></div>
    <div class="setup">
      <label class="fld"><span>Your name</span><input id="nm" maxlength="18" placeholder="optional"></label>
      <div class="fld"><span>Play as</span><div class="opts" id="role">
        <button class="opt on" data-v="dev"><b>The developer</b><small>You get the ticket. You do the work.</small></button>
        <button class="opt" data-v="writer"><b>The ticket writer</b><small>You send the note. You go to lunch.</small></button></div></div>
      <div class="fld"><span>Mood</span><div class="opts" id="mood">
        <button class="opt on" data-v="confident"><b>Confident</b><small>"Easy."</small></button>
        <button class="opt" data-v="careful"><b>Careful</b><small>"Hmm."</small></button></div></div>
      <div class="fld"><span>Issue</span><div class="opts">${issues}</div></div>
      <button class="btn big" id="start">Read Issue #${ISSUE.number} ▸</button>
    </div></div>`));
  const pick = (id, key) => document.querySelectorAll(`#${id} .opt`).forEach(b => b.onclick = () => { document.querySelectorAll(`#${id} .opt`).forEach(x => x.classList.remove('on')); b.classList.add('on'); state[key] = b.dataset.v; });
  pick('role', 'role'); pick('mood', 'mood');
  document.getElementById('start').onclick = () => { state.name = document.getElementById('nm').value.trim(); state.hero = 'maya'; go(); };
}

/* ---------- estimate (first and last) ---------- */
function renderEstimate(p, key) {
  const name = devName(); const again = key === 'est2'; const writer = state.role === 'writer';
  app.replaceChildren(h(`<div class="page">${masthead(`Issue #${ISSUE.number} · ${writer ? 'Your ticket' : name + "'s Tuesday"}`)}
    <div class="grid">
      <div class="panel wide" style="min-height:250px"><div class="bg cyan"></div><div class="half"></div>
        <div class="cap tl">${again ? 'Same ticket. Same button.' : (writer ? 'Tuesday. 9:14 AM. You write a note.' : p.caps[0])}</div>
        ${art(p.pose, 'art', 'left:-4px;bottom:-16px;height:245px')}
        <div class="think" style="left:170px;top:34px">${again ? 'Hmm.' : think(p.think)}</div>
        <div class="sticky" style="position:absolute;right:14px;top:50px;width:46%;font-size:16px"><small style="display:block;font-size:12px;color:#7A6410">${writer ? 'from: you · to: ' + name : 'from: product · to: ' + name}</small>${ISSUE.ticket}</div>
      </div>
      <div class="panel wide q in"><div class="bubble">${writer ? 'How long do you think it takes?' : p.q}</div>
        ${again ? `<div class="cmp"><div><b>${p.choices[state.est1]}</b>you said, first time</div></div>` : ''}
        <div class="choices">${p.choices.map((c, i) => `<button class="ch" data-i="${i}"><b>${'ABC'[i]}</b> ${c}</button>`).join('')}</div>
      </div>
    </div></div>`));
  stagger();
  document.querySelectorAll('.ch').forEach(b => b.onclick = () => { state[key] = +b.dataset.i; go(); });
}

/* ---------- guess page ---------- */
function chat(msgs) { return `<div class="phonechat">${msgs.map(m => `<div class="msg ${m.who}">${m.text}</div>`).join('')}</div>`; }
function renderGuess(p, n) {
  const name = devName(); const writer = state.role === 'writer'; const w = p.w;
  app.replaceChildren(h(`<div class="page"><div class="progress">Page ${n} / ${guessPages()}</div>${masthead(`${p.title}`)}
    <div class="grid">
      <div class="panel"><div class="bg ${p.p1.bg}"></div><div class="half"></div><div class="cap tl">${writer ? w.p1cap : p.p1.cap}</div>
        ${writer ? chat(w.chat) : art(p.p1.pose, 'art', 'left:-4px;bottom:-16px;height:225px') + (p.p1.think ? `<div class="think" style="left:150px;top:34px">${think(p.p1.think)}</div>` : '')}</div>
      <div class="panel"><div class="bg ${p.p2.bg}"></div><div class="half"></div><div class="cap tl">${p.p2.cap}</div>
        <div class="fx inst" style="top:64%">${INSTRUMENTS[p.p2.inst].before}</div></div>
      <div class="panel wide q"><div class="bubble">${p.q.text}</div>
        <div class="choices">${p.q.choices.map((c, i) => `<button class="ch" data-i="${i}"><b>${'ABC'[i]}</b> ${c}</button>`).join('')}</div></div>
      <div class="panel wide splash" id="splash" hidden><div class="half"></div><div class="cap tl">${p.splash.cap}</div>${BURST}
        ${inst(p.splash.inst, 'after')}<div class="sfx">${p.splash.sfx}</div>${art(p.splash.pose)}<div class="cap br">${writer ? w.sub : p.splash.sub}</div></div>
      <div class="reveal" id="reveal">${art(p.reveal.face, '')}<div><span class="k" id="verdict"></span><b>${p.reveal.title}</b> ${writer ? w.text : p.reveal.text}<div class="take">${p.reveal.take}</div></div></div>
      <div class="nav" id="nav"><span class="score">Right so far: <span id="sc"></span></span><button class="btn" id="next">Next page ▸</button></div>
    </div></div>`));
  stagger();
  const chs = [...document.querySelectorAll('.ch')];
  chs.forEach(b => b.onclick = () => {
    chs.forEach(x => x.disabled = true);
    const right = +b.dataset.i === p.q.answer; state.asked++; if (right) state.right++;
    b.classList.add(right ? 'right' : 'wrong'); if (!right) chs[p.q.answer].classList.add('right');
    const sp = document.getElementById('splash'); sp.hidden = false;
    requestAnimationFrame(() => { sp.classList.add('in'); sp.scrollIntoView({ behavior: 'smooth', block: 'center' }); });
    setTimeout(() => sp.classList.add('snap'), 600);
    setTimeout(() => { document.getElementById('verdict').textContent = right ? 'You called it.' : 'Not quite.'; document.getElementById('reveal').classList.add('on'); document.getElementById('sc').textContent = `${state.right} / ${state.asked}`; document.getElementById('nav').classList.add('on'); }, 1500);
  });
  document.getElementById('next').onclick = go;
}

/* ---------- end ---------- */
function renderEnd() {
  const hh = HEROES[state.hero]; const est = PAGES[0].choices;
  const grew = state.est2 > state.est1; const writer = state.role === 'writer'; const nm = state.name ? state.name + ', ' : '';
  app.replaceChildren(h(`<div class="page end">${masthead(`Issue #${ISSUE.number} · The end`)}
    <div class="grid">
      <div class="panel wide in" style="min-height:0;padding:16px"><div class="lineup"><img src="${hh.art.relieved}" alt=""><img src="${hh.art.front}" alt=""></div>
        <div class="cmp"><div><b>${est[state.est1]}</b>first guess</div><div><b>${est[state.est2]}</b>second guess</div><div><b>${state.right} / ${state.asked}</b>snaps you saw coming</div></div>
        <div class="bubble">${nm}${grew ? 'same button. Different eyes.' : 'same answer twice. You could see the strings from the start.'}</div>
        ${writer ? '<p>You never touched the code. You wrote fourteen words on a sticky note and seven things broke. Not because you were careless — because none of those seven were visible from where you sat.</p>' : ''}
        <p>The typing was thirty seconds. Everything else was finding out what the typing would break. That finding-out is the job. It's invisible, so it's easy to leave out of a plan — and expensive when it's left out.</p>
        <p>A building has a floor plan. Software doesn't. Next time someone says <b>"just"</b>, picture the strings.</p>
        <div class="nav on"><span class="score">Free to share, copy, remix.</span><button class="btn" id="again">Read again ▸</button></div>
      </div>
      <div class="tbc">Next issue: "Just add a phone number field"…</div>
    </div></div>`));
  document.getElementById('again').onclick = () => { Object.assign(state, RESET); render(); };
}

function render() {
  if (!state.hero) return renderCover();
  const p = PAGES[state.i - 1];
  if (!p) return renderEnd();
  if (p.type === 'estimate') return renderEstimate(p, 'est1');
  if (p.type === 'end') { if (state.est2 === null) return renderEstimate(PAGES[0], 'est2'); return renderEnd(); }
  const n = PAGES.slice(0, state.i).filter(x => x.type === 'guess').length;
  return renderGuess(p, n);
}
render();
