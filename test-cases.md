# Manual Test Cases and Demo-Mode Results

These results describe the local no-key demo mode, not a language model evaluation. The basic server routes and transformation functions were exercised locally.

| Case | Input | Expected check | Observed demo-mode behavior |
|---|---|---|---|
| 1. Basic cleanup | `i went to the store yesterday` | Capitalization, punctuation, compare both styles | `I went to the store yesterday.` in both styles; formal adds terminal punctuation |
| 2. Repeated article | `She saw the the bird` | Remove obvious repeated word | `She saw the bird.` |
| 3. Extra spaces | `We   are   ready` | Normalize whitespace | `We are ready.` |
| 4. Uncertain source | `The report may indicate a delay.` | Keep uncertainty; display source separately | Source sentence shown as stated; demo does not infer added facts |
| 5. Empty input | blank | Validation message | `Enter some text first.` |
| 6. Long input | over 5,000 characters | Server rejects oversized text | HTTP 400 with length guidance |
| 7. API mode | valid configured key and endpoint | Model returns JSON fields | Requires provider credentials/network; not run without a key |

## Interpretation and limitations

Demo mode uses transparent string rules, not generative AI. It is intentionally modest and does not reliably detect grammar, preserve all nuances, or produce stylistically rich rewrites. The model mode depends on a compatible endpoint and its output schema; malformed responses or network failures return an error. Model-generated “facts” can still be misclassified and the interpretation can introduce unsupported meaning. Human review is required.
