#!/usr/bin/env zx

/**
 * Automated Git Commit Generator using Claude API
 *
 * This script:
 * 1. Analyzes current uncommitted git changes
 * 2. Sends the diff to Claude API (Haiku 3.5)
 * 3. Generates an informative commit message
 * 4. Creates the git commit
 *
 * Prerequisites:
 * - Git repository with changes
 * - GIT_API_KEY environment variable set with Anthropic API key
 *
 * Usage:
 *   npx zx tools/commit-changes.js
 *   # or with env var inline:
 *   GIT_API_KEY=your_key npx zx tools/commit-changes.js
 */

import Anthropic from '@anthropic-ai/sdk';
import { $ } from 'zx';

/**
 * Check if there are uncommitted changes
 */
async function hasUncommittedChanges() {
  const status = await $`git status --porcelain`;
  return status.stdout.trim().length > 0;
}

/**
 * Get git diff and status information
 */
async function getGitChanges() {
  const status = await $`git status --short`;
  const diff = await $`git diff`;
  const stagedDiff = await $`git diff --staged`;

  return {
    status: status.stdout,
    diff: diff.stdout,
    stagedDiff: stagedDiff.stdout
  };
}

/**
 * Call Claude API to generate commit message
 */
async function generateCommitMessage(changes) {
  const apiKey = process.env.GIT_API_KEY;

  if (!apiKey) {
    throw new Error('GIT_API_KEY environment variable is not set');
  }

  const prompt = `You are a git commit message generator. Analyze the following git changes and create a clear, informative commit message.

Git Status:
${changes.status}

Staged Changes:
${changes.stagedDiff || '(no staged changes)'}

Unstaged Changes:
${changes.diff || '(no unstaged changes)'}

Rules for the commit message:
1. First line: Brief summary (50 chars or less) in imperative mood (e.g., "Add feature" not "Added feature")
2. If needed, add a blank line then a detailed description
3. Focus on WHAT changed and WHY, not HOW
4. Be concise but informative
5. Use conventional commit prefixes if appropriate (feat:, fix:, docs:, refactor:, test:, chore:)

Return ONLY the commit message text, nothing else. Do not include any explanations or markdown formatting.`;

  const client = new Anthropic({
    apiKey: apiKey
  });

  const response = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 1024,
    messages: [
      {
        role: 'user',
        content: prompt
      }
    ]
  });

  if (response.content && response.content.length > 0 && response.content[0].type === 'text') {
    let message = response.content[0].text.trim();

    // Strip markdown code fences if present (```...``` or ```text...```)
    message = message.replace(/^```[a-z]*\n?/i, '').replace(/\n?```$/i, '');

    return message.trim();
  } else {
    throw new Error('No content in Claude API response');
  }
}

/**
 * Stage all changes
 */
async function stageAllChanges() {
  console.log('Staging all changes...');
  await $`git add -A`;
}

/**
 * Create git commit with the generated message
 */
async function createCommit(message) {
  await $`git commit -m ${message}`;
  console.log('\n✓ Commit created successfully!');
}

/**
 * Main execution function
 */
async function main() {
  try {
    console.log('🔍 Checking for uncommitted changes...\n');

    if (!(await hasUncommittedChanges())) {
      console.log('No uncommitted changes found. Nothing to commit.');
      process.exit(0);
    }

    const changes = await getGitChanges();

    console.log('📊 Current changes:');
    console.log(changes.status);
    console.log();

    // Stage all changes if there are unstaged changes
    if (changes.diff.trim().length > 0) {
      await stageAllChanges();
      // Get updated changes after staging
      const stagedDiff = await $`git diff --staged`;
      changes.stagedDiff = stagedDiff.stdout;
      changes.diff = '';
    }

    console.log('🤖 Generating commit message with Claude API...\n');

    const commitMessage = await generateCommitMessage(changes);

    console.log('📝 Generated commit message:');
    console.log('─'.repeat(50));
    console.log(commitMessage);
    console.log('─'.repeat(50));
    console.log();

    console.log('💾 Creating commit...');
    await createCommit(commitMessage);

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

// Run the script
await main();
