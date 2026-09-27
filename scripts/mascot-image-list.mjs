// docs/MASCOT_IMAGES.md 를 데이터에서 다시 만든다.  npm run mascots:list
import { loadDb, writeChecklist } from './mascot-images-lib.mjs';
const { done, total } = writeChecklist(loadDb());
console.log(`docs/MASCOT_IMAGES.md — 받은 그림 ${done}/${total}`);
