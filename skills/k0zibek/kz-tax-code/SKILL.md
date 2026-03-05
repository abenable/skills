---
name: kz-tax-code
description: "Kazakhstan tax assistant (НК РК / ҚР Салық кодексі) 2025–2026. Searches tax code articles, calculates КПН/ИПН/НДС/СН/ОПВ/ОСМС, explains КГД rules and declaration forms (910, 920, 700, 200, 300, 101). Use when the user asks about: tax rates, deductions, exemptions, specific articles (\"статья 320\", \"320-бап\"), tax calculations (\"посчитай ИПН с зарплаты\", \"сколько НДС платить\", \"налог на дивиденды\"), declarations and КГД orders, simplified tax regime (упрощёнка, патент), or any tax question in Russian or Kazakh — e.g. \"ставка НДС\", \"ҚҚС мөлшерлемесі\", \"дивиденды нерезидентам\", \"МСБ КПН\", \"жалақыдан салық есептеу\". Independent skill, no external dependencies required."
---

# kz-tax-code — Kazakhstan Tax Assistant

## Language Detection

Detect the user's language from the query. Respond in the same language:
- Russian query → respond in Russian, search with `--lang=ru`
- Kazakh query → respond in Kazakh, search with `--lang=kaz`
- Mixed or unclear → default to Russian

## References

Load these files when relevant — do not load all at once:

- **`references/tax-rates.md`** — current rates for КПН, ИПН, НДС, СН, ОПВ, ОСМС, МРП, МЗП; load for any rate/amount question
- **`references/calculators.md`** — step-by-step formulas for ИПН, КПН, НДС, упрощёнка, патент; load when user asks to calculate
- **`references/npa-index.md`** — КГД declaration forms and regulatory acts index; load for questions about declarations, forms, КГД orders

## Workflow

### 1. Article lookup
```bash
node skills/kz-tax-code/scripts/search.js --article=320 [--year=2026] [--lang=ru]
node skills/kz-tax-code/scripts/search.js --keyword="дивиденды" --year=2026 --lang=ru
node skills/kz-tax-code/scripts/search.js --topic="НДС экспорт освобождение" --year=2026 --lang=ru
```
Defaults: `--year=2026 --lang=ru`. Use article > keyword > topic (most to least precise).

### 2. Tax calculation
Read `references/calculators.md`. Show the formula, substitute the user's numbers, state the result. Always cite the article.

### 3. Rate question
Read `references/tax-rates.md`. Answer directly with the rate and article reference.

### 4. Declaration / КГД question
Read `references/npa-index.md`. Provide the form name, deadline, and КГД link.

## Response Format

Russian:
> Согласно **статье 320 НК РК 2026**, ставка ИПН для резидентов — **10%**.
> *(Статья 320, пункт 1)*

Kazakh:
> **ҚР Салық кодексінің 320-бабына** сәйкес резиденттер үшін ЖТС мөлшерлемесі — **10%**.
> *(320-бап, 1-тармақ)*

For calculations — show working:
> Жалақы: 300 000 ₸
> ОПВ (10%): − 30 000 ₸
> ОСМС (2%): − 6 000 ₸
> Стандартный вычет (14 МРП): − 55 048 ₸
> Налогооблагаемый доход: 208 952 ₸
> **ИПН (10%): 20 895 ₸**
> **На руки: 243 105 ₸**

Always state the tax code year. Do not guess — if an article is not found, say so.

## Key Notes

- НК РК 2026 (K2500000214) — действующий, принят 18.07.2025, введён с 01.01.2026
- НК РК 2025 (K1700000120) — утратил силу с 18.07.2025; использовать для периодов до 2026
- МРП и МЗП меняются ежегодно — проверять по Закону о республиканском бюджете
- Ставки СО, ОСМС, ВОСМС могут меняться — сверять с `references/tax-rates.md`
