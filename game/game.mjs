import {ladders, snakes, move, dice} from './engine.mjs';
const $ = id => document.getElementById(id);
let positions = [0, 0], turn = 0, finished = false, busy = false, pending;
const squares = new Map();
for (let row = 9; row >= 0; row--) {
  for (let col = 0; col < 10; col++) {
    const n = row * 10 + (row % 2 ? 10 - col : col + 1);
    const square = document.createElement('div');
    square.className = 'square' + (ladders[n] ? ' ladder' : snakes[n] ? ' snake' : n === 100 ? ' finish' : '');
    square.setAttribute('role', 'listitem');
    square.setAttribute('aria-label', `Square ${n}${ladders[n] ? `, ladder to ${ladders[n]}` : snakes[n] ? `, snake to ${snakes[n]}` : ''}`);
    square.innerHTML = `<span>${n}</span>${ladders[n] || snakes[n] ? `<span class="destination">${ladders[n] ? '↗' : '↘'}${ladders[n] || snakes[n]}</span>` : ''}<span class="tokens"></span>`;
    squares.set(n, square); $('board').append(square);
  }
}
function name(player) { return $('mode').value === 'computer' ? player === 0 ? 'You' : 'Computer' : `Player ${player + 1}`; }
function render() {
  for (const square of squares.values()) square.querySelector('.tokens').replaceChildren();
  positions.forEach((position, player) => {
    if (!position) return;
    const token = document.createElement('span'); token.className = `token p${player + 1}`;
    token.textContent = player + 1; token.setAttribute('aria-label', `${name(player)} at square ${position}`);
    squares.get(position).querySelector('.tokens').append(token);
  });
  $('players').innerHTML = positions.map((position, player) => `<div class="player p${player + 1} ${turn === player ? 'active' : ''}">${name(player)}<strong>${position || 'Start'}</strong></div>`).join('');
  $('roll').disabled = finished || busy || (turn === 1 && $('mode').value === 'computer');
  $('roll').textContent = finished ? 'Game complete ✓' : busy ? 'Rolling…' : 'Roll the dice ↗';
}
function log(message) {
  const li = document.createElement('li'); li.textContent = message; $('history').prepend(li);
  while ($('history').children.length > 5) $('history').lastChild.remove();
}
function takeTurn() {
  if (busy || finished) return;
  busy = true; render();
  const roll = dice(); $('dice').textContent = ['⚀','⚁','⚂','⚃','⚄','⚅'][roll - 1];
  $('dice').setAttribute('aria-label', `Rolled ${roll}`);
  pending = setTimeout(() => {
    const player = turn; const result = move(positions[player], roll); positions[player] = result.position;
    let message = `${name(player)} rolled ${roll}. `;
    message += result.kind === 'overshoot' ? 'Need an exact roll to reach 100.' : result.kind === 'ladder' ? `Ladder! ${result.landed} → ${result.position}.` : result.kind === 'snake' ? `Snake! ${result.landed} → ${result.position}.` : `Moved to ${result.position}.`;
    finished = result.won; busy = false; log(message);
    if (finished) { $('status').textContent = `${name(player)} ${player === 0 && $('mode').value === 'computer' ? 'win' : 'wins'}! Start a new game?`; render(); return; }
    turn = 1 - turn;
    $('status').textContent = `${message} ${name(turn)} ${turn === 0 && $('mode').value === 'computer' ? 'play' : 'plays'} next.`;
    render();
    if (turn === 1 && $('mode').value === 'computer') pending = setTimeout(takeTurn, 650);
  }, matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 220);
}
function reset() {
  clearTimeout(pending); positions = [0,0]; turn = 0; finished = false; busy = false;
  $('dice').textContent = '—'; $('dice').setAttribute('aria-label', 'Dice not rolled');
  $('status').textContent = $('mode').value === 'computer' ? 'Your move. Roll to begin.' : 'Player 1, roll to begin.';
  $('history').innerHTML = '<li>The board is ready.</li>'; render();
}
$('roll').addEventListener('click', () => { if (!(turn === 1 && $('mode').value === 'computer')) takeTurn(); });
$('reset').addEventListener('click', reset); $('mode').addEventListener('change', reset); reset();
