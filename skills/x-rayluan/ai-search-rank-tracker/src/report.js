const { toCsvRow } = require('./utils');

function renderMarkdownReport(output) {
  const { brand, prompts, engines, summary, results, generatedAt } = output;
  const lines = [];
  lines.push('# AI Search Rank Tracker Report');
  lines.push('');
  lines.push(`- **Brand:** ${brand}`);
  lines.push(`- **Prompts:** ${prompts.length}`);
  lines.push(`- **Engines:** ${engines.join(', ')}`);
  lines.push(`- **Overall score:** ${summary.overallScore}/100`);
  lines.push(`- **Generated at:** ${generatedAt}`);
  lines.push('');
  lines.push('## Summary');
  lines.push('');
  lines.push(`- Engines mentioning brand: ${summary.engineMentions}`);
  lines.push(`- Best rank: ${summary.bestRank ?? 'not found'}`);
  lines.push(`- Competitors seen: ${summary.competitors.length ? summary.competitors.join(', ') : 'none detected'}`);
  lines.push(`- Sentiment mix: ${JSON.stringify(summary.sentimentBreakdown)}`);
  lines.push('');
  lines.push('## Results');
  lines.push('');

  for (const item of results) {
    lines.push(`### ${item.engine} — ${item.prompt}`);
    lines.push(`- Mentioned: ${item.mentioned ? 'yes' : 'no'}`);
    lines.push(`- Rank: ${item.rank ?? 'not found'}`);
    lines.push(`- Mention type: ${item.mentionType}`);
    lines.push(`- Sentiment: ${item.sentiment}`);
    lines.push(`- Competitors: ${item.competitors.length ? item.competitors.join(', ') : 'none detected'}`);
    lines.push(`- Excerpt: ${item.excerpt || 'n/a'}`);
    lines.push(`- Score: ${item.score ?? 'n/a'}`);
    if (item.error) lines.push(`- Error: ${item.error}`);
    lines.push('');
  }

  return lines.join('\n');
}

function renderCsvReport(output) {
  const header = [
    'engine',
    'prompt',
    'brand',
    'mentioned',
    'rank',
    'mentionType',
    'sentiment',
    'competitors',
    'excerpt',
    'score',
    'error',
    'startedAt',
    'finishedAt'
  ];

  const rows = output.results.map((item) =>
    toCsvRow([
      item.engine,
      item.prompt,
      item.brand,
      item.mentioned,
      item.rank ?? '',
      item.mentionType,
      item.sentiment,
      (item.competitors || []).join('|'),
      item.excerpt || '',
      item.score ?? '',
      item.error || '',
      item.startedAt || '',
      item.finishedAt || ''
    ])
  );

  return [toCsvRow(header), ...rows].join('\n');
}

module.exports = {
  renderMarkdownReport,
  renderCsvReport,
};
