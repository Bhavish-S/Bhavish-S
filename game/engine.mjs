export const ladders = Object.freeze({4: 25, 13: 46, 33: 49, 42: 63, 62: 81, 74: 92});
export const snakes = Object.freeze({27: 5, 40: 3, 54: 31, 66: 45, 89: 53, 99: 41});

export function move(position, roll) {
  if (!Number.isInteger(position) || position < 0 || position > 100 || !Number.isInteger(roll) || roll < 1 || roll > 6) {
    throw new RangeError('Invalid position or dice roll');
  }
  const landed = position + roll;
  if (landed > 100) return { position, landed: position, kind: 'overshoot', won: position === 100 };
  const destination = ladders[landed] ?? snakes[landed] ?? landed;
  return { position: destination, landed, kind: ladders[landed] ? 'ladder' : snakes[landed] ? 'snake' : 'move', won: destination === 100 };
}

export function dice() {
  const bytes = new Uint8Array(1);
  do { crypto.getRandomValues(bytes); } while (bytes[0] >= 252);
  return bytes[0] % 6 + 1;
}
