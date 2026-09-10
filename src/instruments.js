// Instruments: the things that snap. Each returns HTML for a "before" state; the page adds .snap to flip to "after".
// Keep them purely visual — no text explanation here, that lives in story.js.
const btn = (label, cls='') => `<span class="btnui ${cls}">${label}</span>`;
export const INSTRUMENTS = {
  robot: {
    before: `<div class="card"><b>Page checker</b><div class="ok">✓ page loads</div><div class="ok">✓ finds button "Submit"</div><div class="ok">✓ pressing "Submit" orders</div></div>`,
    after:  `<div class="card"><b>Page checker</b><div class="ok">✓ page loads</div><div class="bad">✗ finds button "Submit"</div><div class="bad">✗ pressing "Submit" orders</div><div class="stamp">HALT</div></div>`,
  },
  counter: {
    before: `<div class="meter"><div class="needle"></div><i></i></div>`,
    after:  `<div class="zero">0</div>`,
  },
  calendar: {
    before: `<div class="cal">${Array.from({length:28},(_,i)=>`<span class="${i===0?'now':i===21?'mark':''}">${i+1}</span>`).join('')}<div class="legend"><i class="now"></i> today: day 1 &nbsp; <i class="mark"></i> marketing report: day 22</div></div>`,
    after:  `<div class="cal">${Array.from({length:28},(_,i)=>`<span class="${i<21?'x':i===21?'now':''}">${i+1}</span>`).join('')}<div class="legend"><i class="x"></i> counter at zero &nbsp; <i class="now"></i> day 22: report opened</div></div>`,
  },
  voice: {
    before: `<div style="display:grid;gap:14px;justify-items:start"><div class="say">Button. "Submit."</div>${btn('SUBMIT')}</div>`,
    after:  `<div style="display:grid;gap:14px;justify-items:start"><div class="say">Button. "Submit."</div>${btn('CONTINUE')}<div class="stamp" style="right:-30px;top:60px">??</div></div>`,
  },
  shopDE: {
    before: `<div style="display:grid;gap:10px;justify-items:start"><div class="card" style="min-width:0"><b>German shop</b>${btn('ABSENDEN')}</div></div>`,
    after:  `<div style="display:grid;gap:10px;justify-items:start"><div class="card" style="min-width:0"><b>German shop</b>${btn('FORTFAHREN','clip')}</div></div>`,
  },
  mirror: {
    before: `<div class="screen"><i></i><i style="width:60%"></i><i></i><div class="row r">${btn('SUBMIT')}</div></div>`,
    after:  `<div class="screen" dir="rtl"><i></i><i style="width:60%"></i><i></i><div class="row r">${btn('متابعة')}</div><div class="stamp" style="left:-20px;right:auto;top:-14px">FLIPPED</div></div>`,
  },
  article: {
    before: `<div class="card"><b>Help: how do I finish my order?</b>Click the blue <mark>Submit</mark> button on the <mark>left</mark>.</div>`,
    after:  `<div class="card"><b>Help: how do I finish my order?</b>Click the blue <del>Submit</del> button on the <del>left</del>.<div class="env">Support: 14 new</div></div>`,
  },
};
