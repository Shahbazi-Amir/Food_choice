# Cookbook research notes

## Source checked
- *کتاب مستطاب آشپزی، از سیر تا پیاز* — نجف دریابندری، با همکاری فهیمه راستکار، نشر کارنامه.
- Publisher metadata confirms the current two-volume edition is 1,966 pages.
- Public catalogue/table-of-contents descriptions show the book is organized much more broadly than a flat meal list: culinary schools, kitchen/equipment, ingredients (meat, poultry, egg, fish, dairy, vegetables, rice, stock), followed by cooking/recipe material.

## Product implication
The app should not copy the book's wording or recipes. We use it as a structural reference: food identity, ingredient families, cooking techniques, and culinary families are separate dimensions.

For Food Choice the user-facing taxonomy is intentionally simpler than the book:
- food family (what kind of dish it is)
- cooking method (how it is cooked)
- time
- cost band
- light/medium/heavy
- familiarity (usual / wants-to-try / catalogue fallback)

This avoids the earlier modelling error where labels such as `گریل` behaved like a loose category and could rank an incompatible dish such as kuku.

## Editorial rule
Recipe text in this repository must be independently written. Do not transcribe copyrighted cookbook instructions. Cookbook/source metadata may be stored for editorial provenance, but the app copy must remain original.
