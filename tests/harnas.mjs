// Draait het echte script uit weerbaarheid-game.html buiten de browser en schrijft per scenario, voorbereiding,
// inzet van maatregelen en complicatie op wat de game rekent. tests/test_reken.py legt dat naast reken.py.
//
//   node tests/harnas.mjs > uitkomsten.json
//
// Het script krijgt een nagebootst document dat alles slikt: de game tekent dan niets, maar rekent wel. De status
// die evalueer() zou tonen, wordt opgevangen door setStatus te vervangen.
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(ROOT, 'weerbaarheid-game.html'), 'utf8');
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');

const stub = new Proxy(function () {}, {
  get: (_t, p) => (p === Symbol.toPrimitive ? () => '' : p === Symbol.iterator ? function* () {} : p === 'length' ? 0 : stub),
  apply: () => stub, construct: () => stub, set: () => true,
});
const opslag = {};
const context = vm.createContext({
  document: stub, window: stub, navigator: stub, location: stub, history: stub,
  localStorage: { getItem: (k) => opslag[k] ?? null, setItem: (k, v) => { opslag[k] = String(v); }, removeItem: (k) => { delete opslag[k]; } },
  sessionStorage: { getItem: () => null, setItem() {}, removeItem() {} },
  setTimeout: () => 0, clearTimeout() {}, setInterval: () => 0, clearInterval() {}, requestAnimationFrame: () => 0,
  console, Math, JSON, Date, Set, Map, Array, Object, String, Number, Promise, Blob: function () {}, URL: stub, FileReader: function () {},
});
vm.runInContext(script, context);

const uit = vm.runInContext(`(() => {
  let gevangen = null;
  setStatus = (label) => { gevangen = label; };
  const kopie = (x) => JSON.parse(JSON.stringify(x));
  function deelverzamelingen(lijst, max) {
    const uit = [[]];
    for (const x of lijst) for (const s of uit.slice()) if (s.length < max) uit.push(s.concat([x]));
    return uit;
  }
  const gevallen = [];
  const scenarios = {};
  for (const dienst of Object.keys(SCENARIOS)) {
    if (!DIENSTEN[dienst]) continue;
    SCENARIOS[dienst].forEach((sc, idx) => {
      herstelScenarioData(dienst);
      const basis = kopie(sc.maatregelen || []);
      const prep = PREP_DATA[getPrepKey(dienst, idx)] || null;
      scenarios[dienst + '#' + idx] = { basis, prep: prep ? kopie(prep) : null, complicaties: kopie(sc.complicaties || []) };
      const prepCombos = prep ? deelverzamelingen(prep.opties.map((o) => o.id), prep.max || 3) : [[]];
      for (const combo of prepCombos) {
        herstelScenarioData(dienst);
        st.dienst = dienst; st.prepScenario = idx; st.prepKeuzes = new Set(combo); st.versterktNodes = new Set();
        if (prep) startVanuitPrep();
        const naPrep = kopie(sc.maatregelen || []);
        const versterkt = Array.from(st.versterktNodes);
        const oranje = naPrep.filter((m) => m.type === 'reactief' && m.status === 'oranje').map((m) => m.id);
        const reactief = naPrep.filter((m) => m.type === 'reactief').map((m) => m.id);
        const inzetten = deelverzamelingen(reactief, reactief.length);
        const overschrijvingen = [{}].concat((sc.complicaties || []).map((c) => ({ [c.degradeert]: c.nieuweEff })));
        for (const actief of inzetten) for (const ov of overschrijvingen) {
          st.dienst = dienst; st.scenario = idx; st.incident = true; st.cascading = false;
          st.actief = new Set(actief); st.effectiviteit = Object.assign({}, ov);
          gevangen = null;
          evalueer();
          gevallen.push({ dienst, idx, combo, actief, ov, naPrep, versterkt, oranje,
            eff: berekenEffectiviteit(), status: gevangen == null ? null : String(gevangen).split(' (')[0] });
        }
      }
      herstelScenarioData(dienst);
    });
  }
  // Zonder incident: een geval per dienst.
  const zonder = [];
  for (const dienst of Object.keys(SCENARIOS)) {
    if (!DIENSTEN[dienst]) continue;
    st.dienst = dienst; st.scenario = 0; st.incident = false; st.cascading = false; st.actief = new Set(); st.effectiviteit = {};
    gevangen = null; evalueer(); zonder.push({ dienst, status: gevangen });
  }
  return { scenarios, gevallen, zonder };
})()`, context);

process.stdout.write(JSON.stringify(uit));
