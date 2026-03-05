#!/usr/bin/env node
/**
 * search.js — поиск по Налоговому кодексу РК
 *
 * Режимы:
 *   node search.js --article=320 [--year=2026] [--lang=ru]
 *   node search.js --keyword="дивиденды" [--year=2026] [--lang=ru]
 *   node search.js --topic="налог на прибыль МСБ" [--year=2026] [--lang=ru]
 *
 * Возвращает JSON: { found: bool, results: [{ article, title, text, context }] }
 */

import { readFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR  = join(__dirname, "..", "data");

// Контекст: сколько параграфов до и после совпадения возвращать
const CONTEXT_PARAGRAPHS_BEFORE = 2;
const CONTEXT_PARAGRAPHS_AFTER  = 5;
const MAX_RESULTS                = 10;

// ── File loader ────────────────────────────────────────────────────────────────
function loadFile(year, lang) {
  const path = join(DATA_DIR, `tax-code-${year}-${lang}.md`);
  if (!existsSync(path)) {
    throw new Error(
      `File not found: ${path}\nRun: node scripts/download.js --year=${year} --lang=${lang}`
    );
  }
  return readFileSync(path, "utf-8");
}

// ── Split file into article blocks ─────────────────────────────────────────────
function splitArticles(content) {
  // Articles are marked as "## Статья N." or "## N-бап" in the markdown
  const articleRegex = /^## ((?:Статья|Artikel)\s+\d+[\.\-].*|[\d]+-(?:бап|статья).*)/im;
  const lines = content.split("\n");
  const articles = [];
  let current = null;

  for (const line of lines) {
    const match = line.match(/^## ((?:Статья|Artikel)\s+(\d+)[\.\-]?(.*)|(\d+)-(бап|статья)(.*))$/i);
    if (match) {
      if (current) articles.push(current);
      const num = match[2] || match[4];
      const titleRest = (match[3] || match[6] || "").trim();
      const full = match[1].trim();
      current = {
        number: parseInt(num),
        title: full,
        text: line + "\n",
        lines: [line],
      };
    } else if (current) {
      // Stop collecting at the next ## section header (new article)
      if (line.match(/^## /) && !line.match(/^## (Статья|[\d]+-бап)/i)) {
        articles.push(current);
        current = null;
      } else {
        current.text += line + "\n";
        current.lines.push(line);
      }
    }
  }
  if (current) articles.push(current);
  return articles;
}

// ── Split file into paragraphs for context search ──────────────────────────────
function splitParagraphs(content) {
  return content.split(/\n\n+/).filter(p => p.trim().length > 0);
}

// ── Highlight match in text ────────────────────────────────────────────────────
function highlight(text, keyword) {
  if (!keyword) return text;
  const re = new RegExp(`(${escapeRegex(keyword)})`, "gi");
  return text.replace(re, "**$1**");
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// ── Search by article number ───────────────────────────────────────────────────
function searchByArticle(articles, num) {
  const found = articles.filter(a => a.number === num);
  return found.map(a => ({
    article: a.number,
    title: a.title,
    text: a.text.trim(),
    matchType: "article",
  }));
}

// ── Search by keyword ──────────────────────────────────────────────────────────
function searchByKeyword(content, articles, keyword) {
  const kw = keyword.toLowerCase();
  const paragraphs = splitParagraphs(content);
  const results = [];
  const seenArticles = new Set();

  for (let i = 0; i < paragraphs.length; i++) {
    if (!paragraphs[i].toLowerCase().includes(kw)) continue;

    // Find which article this paragraph belongs to
    const para = paragraphs[i];
    const article = findArticleForParagraph(articles, para);

    if (article && seenArticles.has(article.number)) continue;
    if (article) seenArticles.add(article.number);

    // Build context
    const before = paragraphs.slice(Math.max(0, i - CONTEXT_PARAGRAPHS_BEFORE), i);
    const after  = paragraphs.slice(i + 1, i + 1 + CONTEXT_PARAGRAPHS_AFTER);

    results.push({
      article: article?.number ?? null,
      title: article?.title ?? null,
      matchParagraph: highlight(para, keyword),
      context: [
        ...before,
        `>>> ${highlight(para, keyword)} <<<`,
        ...after,
      ].join("\n\n"),
      matchType: "keyword",
    });

    if (results.length >= MAX_RESULTS) break;
  }
  return results;
}

// ── Search by topic (multi-keyword) ───────────────────────────────────────────
function searchByTopic(content, articles, topic) {
  // Split topic into keywords, score paragraphs by hits
  const keywords = topic.toLowerCase()
    .split(/[\s,]+/)
    .filter(w => w.length > 2);

  const paragraphs = splitParagraphs(content);
  const scored = paragraphs.map((p, i) => {
    const lower = p.toLowerCase();
    const score = keywords.reduce((s, kw) => s + (lower.includes(kw) ? 1 : 0), 0);
    return { para: p, idx: i, score };
  }).filter(x => x.score > 0)
    .sort((a, b) => b.score - a.score);

  const results = [];
  const seenArticles = new Set();

  for (const { para, idx, score } of scored) {
    const article = findArticleForParagraph(articles, para);
    if (article && seenArticles.has(article.number)) continue;
    if (article) seenArticles.add(article.number);

    const before = paragraphs.slice(Math.max(0, idx - CONTEXT_PARAGRAPHS_BEFORE), idx);
    const after  = paragraphs.slice(idx + 1, idx + 1 + CONTEXT_PARAGRAPHS_AFTER);

    let highlighted = para;
    for (const kw of keywords) {
      highlighted = highlight(highlighted, kw);
    }

    results.push({
      article: article?.number ?? null,
      title: article?.title ?? null,
      score,
      context: [
        ...before,
        `>>> ${highlighted} <<<`,
        ...after,
      ].join("\n\n"),
      matchType: "topic",
    });

    if (results.length >= MAX_RESULTS) break;
  }
  return results;
}

function findArticleForParagraph(articles, para) {
  // Find the article whose text contains this paragraph
  return articles.find(a => a.text.includes(para)) ?? null;
}

// ── Main ───────────────────────────────────────────────────────────────────────
const args = Object.fromEntries(
  process.argv.slice(2)
    .filter(a => a.startsWith("--"))
    .map(a => {
      const eq = a.indexOf("=");
      return [a.slice(2, eq), a.slice(eq + 1)];
    })
);

const year    = parseInt(args.year ?? "2026");
const lang    = (args.lang ?? "ru").toLowerCase();
const article = args.article ? parseInt(args.article) : null;
const keyword = args.keyword ?? null;
const topic   = args.topic   ?? null;

if (!article && !keyword && !topic) {
  console.error("Usage: node search.js --article=320 | --keyword=<text> | --topic=<text> [--year=2026] [--lang=ru|kaz]");
  process.exit(1);
}

try {
  const content  = loadFile(year, lang);
  const articles = splitArticles(content);

  let results;
  if (article !== null) {
    results = searchByArticle(articles, article);
  } else if (keyword) {
    results = searchByKeyword(content, articles, keyword);
  } else {
    results = searchByTopic(content, articles, topic);
  }

  const output = {
    year,
    lang,
    query: { article, keyword, topic },
    totalArticles: articles.length,
    found: results.length > 0,
    results,
  };

  console.log(JSON.stringify(output, null, 2));
} catch (e) {
  console.error(JSON.stringify({ found: false, error: e.message }));
  process.exit(1);
}
