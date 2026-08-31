# Personal Finance Product — "SpendWise"

## Product problem
Young professionals often know how much money they earn but lack a simple way to:
- understand where money is going,
- stay within a monthly budget,
- detect unusual spending,
- build an emergency-fund habit.

## Product hypothesis
A lightweight personal finance assistant that combines:
1. transaction categorization,
2. budget tracking,
3. spending alerts,
4. simple savings goals,
5. monthly financial health summaries.

## Target user
25–35 year old salaried professionals who manage finances primarily through bank statements/apps.

## MVP
- Add/import transactions
- Categorize transactions
- Set monthly category budgets
- Show budget utilization
- Flag unusual spending
- Track savings goal

## North Star Metric
**Weekly active users who review their financial health dashboard and take at least one action.**

## Core metrics
Activation: first transaction imported + first budget created
Engagement: weekly active users
Retention: 4-week retention
Outcome: users staying within budget
Guardrail: false-positive alert rate

## Suggested PM artifacts
See `docs/PRD.md`, `docs/metrics.md`, `docs/roadmap.md`, `docs/user_stories.md`.

## Demo
```bash
pip install -r requirements.txt
streamlit run app.py
```
