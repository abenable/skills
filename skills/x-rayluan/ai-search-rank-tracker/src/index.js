#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { runEnginePrompt } = require('./engines');
const { parseResponse } = require('./parser');
const { buildSummary, scoreResult } = require('./scoring');
const { renderMarkdownReport, renderCsvReport } = require('./report');

async function main() {
  const inputPath = process.argv[2] || path.join(__dirname, '..', 'prompts', 'starter.json');
  const config = JSON.parse(fs.readFileSync(inputPath, 'utf8'));

  const brand = config.brand;
  const aliases = config.aliases || [];
  const prompts = config.prompts || [];
  const engines = config.engines || ['chatgpt', 'claude', 'gemini', 'perplexity'];
  const results = [];

  for (const prompt of prompts) {
    for (const engine of engines) {
      const startedAt = new Date().toISOString();
      try {
        const raw = await runEnginePrompt(engine, prompt);
        const parsed = parseResponse({ engine, prompt, brand, aliases, rawResponse: raw });
        const score = scoreResult(parsed);
        results.push({ ...parsed, score, startedAt, finishedAt: new Date().toISOString() });
        console.log(`[OK] ${engine} | ${prompt}`);
      } catch (err) {
        results.push({
          engine,
          prompt,
          brand,
          mentioned: false,
          rank: null,
          mentionType: 'none',
          sentiment: 'unknown',
          competitors: [],
          excerpt: '',
          rawResponse: '',
          error: err.message,
          score: 0,
          startedAt,
          finishedAt: new Date().toISOString()
        });
        console.error(`[ERR] ${engine} | ${prompt} | ${err.message}`);
      }
    }
  }

  const summary = buildSummary(results);
  const output = { brand, aliases, prompts, engines, summary, results, generatedAt: new Date().toISOString() };

  const outputDir = path.join(__dirname, '..', 'output');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const safeBrand = String(brand).replace(/[^a-z0-9\-.]/gi, '_');
  const jsonPath = path.join(outputDir, `${safeBrand}-report.json`);
  const mdPath = path.join(outputDir, `${safeBrand}-report.md`);
  const csvPath = path.join(outputDir, `${safeBrand}-report.csv`);

  fs.writeFileSync(jsonPath, JSON.stringify(output, null, 2), 'utf8');
  fs.writeFileSync(mdPath, renderMarkdownReport(output), 'utf8');
  fs.writeFileSync(csvPath, renderCsvReport(output), 'utf8');

  console.log(`Saved JSON report to ${jsonPath}`);
  console.log(`Saved Markdown report to ${mdPath}`);
  console.log(`Saved CSV report to ${csvPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
