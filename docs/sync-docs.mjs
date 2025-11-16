#!/usr/bin/env node
/**
 * Sync documentation from co-located sources
 * Creates symlinks to READMEs and other markdown files throughout the codebase
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const docsDir = path.join(__dirname, 'src', 'content', 'docs');

// Mapping of source files to destination paths in docs
const docMappings = [
  // Main docs
  { src: '../README.md', dest: 'index.mdx', title: 'Introduction' },

  // Tools documentation
  { src: '../tools/commit_changes/PROMPT.md', dest: 'tools/commit-prompt.md', title: 'Commit Message Prompt' },
  { src: '../tools/review_changes/PROMPT.md', dest: 'tools/review-prompt.md', title: 'Code Review Prompt' },
  { src: '../tools/review_changes/SCORING_SYSTEM.md', dest: 'tools/scoring.md', title: 'Gerrit Scoring System' },

  // Evaluations
  { src: '../evals/README.md', dest: 'evals/index.md', title: 'Evaluation System' },
  { src: '../evals/storage/README.md', dest: 'evals/storage.md', title: 'Storage API' },
  { src: '../evals/commit_changes/README.md', dest: 'evals/commit-changes.md', title: 'Commit Evaluations' },
  { src: '../evals/review_changes/README.md', dest: 'evals/review-changes.md', title: 'Review Evaluations' },

  // Development
  { src: '../CLAUDE.md', dest: 'development/claude.md', title: 'Claude Code Guide' },
  { src: '../PROMPT_IMPROVEMENTS.md', dest: 'development/prompt-improvements.md', title: 'Prompt Engineering' },
  { src: '../specs/01-review-functionality.md', dest: 'development/specs-review.md', title: 'Review Specification' },
];

/**
 * Create directory if it doesn't exist
 */
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

/**
 * Add frontmatter to markdown content
 */
function addFrontmatter(content, title, description = '') {
  // Check if frontmatter already exists
  if (content.startsWith('---')) {
    return content;
  }

  const frontmatter = `---
title: ${title}${description ? `\ndescription: ${description}` : ''}
---

`;
  return frontmatter + content;
}

/**
 * Create symlink or copy file with frontmatter
 */
function syncFile(srcPath, destPath, title) {
  const fullSrcPath = path.resolve(rootDir, srcPath);
  const fullDestPath = path.join(docsDir, destPath);

  // Ensure destination directory exists
  ensureDir(path.dirname(fullDestPath));

  // Remove existing symlink or file
  if (fs.existsSync(fullDestPath)) {
    fs.unlinkSync(fullDestPath);
  }

  // Read source file
  if (!fs.existsSync(fullSrcPath)) {
    console.warn(`⚠️  Source file not found: ${srcPath}`);
    return;
  }

  const content = fs.readFileSync(fullSrcPath, 'utf-8');
  const withFrontmatter = addFrontmatter(content, title);

  // Write to destination
  fs.writeFileSync(fullDestPath, withFrontmatter);
  console.log(`✓ Synced: ${srcPath} → ${destPath}`);
}

/**
 * Main sync function
 */
function main() {
  console.log('📚 Syncing documentation...\n');

  // Ensure docs directory exists
  ensureDir(docsDir);

  // Sync all mapped files
  for (const { src, dest, title } of docMappings) {
    syncFile(src, dest, title);
  }

  console.log('\n✨ Documentation sync complete!');
}

main();
