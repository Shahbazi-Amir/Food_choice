# Food Choice — Logic Redesign Prompt

## Goal
Build a household-facing Persian food recommender that never returns a semantically wrong dish and always explains a usable cooking path after recommendation.

## Non-negotiable recommendation rules
1. Separate **food family** from **cooking method**. `گریل/منقل` is a method, not a family.
2. Food-family and cooking-method selections are semantic constraints. Never return an incompatible dish just because its time/cost/weight score is better.
3. Time, cost, and light/medium/heavy are preference dimensions. If no exact match exists, return the nearest match and state the mismatch.
4. If the user's own usual/try pool has no dish compatible with a selected family/method, expand to the catalogue only as an explicitly labelled `پیشنهاد جدید خارج از فهرست معمول` rather than returning an unrelated familiar dish.
5. If both family and method are selected and no dish satisfies both, preserve the user's declared priority. If priority is balanced, preserve method first (because method is an explicit physical cooking constraint), then family; explain what was relaxed.
6. Never silently relax a semantic filter.
7. "یکی دیگه" must keep the same constraints and ranking context.
8. Recent dishes are penalized, not permanently excluded.
9. Recommendations must prioritize familiar dishes when equally suitable, but never at the cost of semantic incompatibility.

## Taxonomy
Use two orthogonal dimensions:
- Family: rice/pilaf, stew, soup/ash, abgoosht/eshkeneh, bread-based/khorak, legumes, kofteh/dolmeh, pasta/pizza, kebab/roast, shami/kotlet, fish/seafood, kuku/omelette, sandwich/quick, cold/no-cook.
- Method: grill/charcoal, oven/roast, pan, frying, pot/steam, slow-stew, boil, no-cook.

A dish may have multiple methods where genuinely valid (e.g. burger = grill or pan; kuku = pan or oven). These alternatives must be explicit in data.

## Recipe contract
Every recommended dish must render:
- ingredient list with quantities scaled to household size when data is available;
- preparation time, cooking time, total time;
- numbered cooking steps;
- at least one primary method;
- alternative valid methods/variants when available;
- practical notes (doneness, substitutions, serving notes) where helpful;
- source/provenance metadata for editorial auditing.

Do not copy copyrighted cookbook text. Use cookbook structure and culinary facts as research/reference, then write original recipe wording.

## UI contract
After a recommendation, the user should not need to search elsewhere to cook it. Show:
1. dish identity + image placeholder/visual slot;
2. why it matched;
3. times and serving count;
4. ingredients;
5. steps;
6. alternative cooking styles;
7. `همینو می‌پزم` and `یکی دیگه`.

## Tests that must exist
- grill + <=60 min never yields kuku/omelette unless that dish explicitly supports grill;
- hard method constraint is preserved over softer time/cost/weight preferences;
- no familiar compatible dish -> compatible catalogue fallback is labelled new;
- no exact time match -> nearest compatible semantic candidate still returned;
- changing priority changes ranking among compatible candidates;
- recipe payload is complete for every recommendation candidate;
- every method in dish data is a valid taxonomy method;
- every family in dish data is a valid taxonomy family.
