#!/usr/bin/env node
/**
 * Entry point for the news infographic daily build.
 * Copies the pre-rendered entry.png to the configured output directory.
 * Uses only Node 22 standard library — no external dependencies.
 */

import { copyFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

function main(): void {
  // Resolve the source image path relative to this script
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(scriptDir, 'entry.png');

  // Determine destination directory from environment, defaulting to /output
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const destPath = join(outputDir, 'entry.png');

  // Perform the copy (overwrites if exists)
  copyFileSync(sourcePath, destPath);
}

main();
