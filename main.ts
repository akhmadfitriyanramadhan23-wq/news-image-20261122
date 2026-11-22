// THE WORLD TODAY — Sunday 22 November 2026 (Node 22, standard library only).
// This entry's image is the entry.png beside this file, drawn fresh for this
// bounty by tools/make-image.py; the program copies it to /output/entry.png.
// The gate takes a whole PNG of at most 1 MiB and 1024 by 1024 pixels, and the
// judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) {
  throw new Error('entry.png is missing from the repository');
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
