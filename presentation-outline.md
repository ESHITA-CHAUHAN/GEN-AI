# 5–10 Minute Presentation and Demonstration

1. **Problem and objective (1 min):** Explain how grammar and readability issues can obscure a writer's meaning. The tool aims to improve clarity while preserving source claims.
2. **Tools and design (1 min):** Python standard library HTTP server, HTML/CSS/JavaScript interface, and optional OpenAI-compatible model endpoint. No secret is stored in the project.
3. **Workflow (1 min):** User enters text → selects style(s) → server validates → local demo rules or configured model generates output → screen compares original and rewrite and labels source facts separately.
4. **Live demo (2–3 min):** Enter `i think the results is good but we need more time`; generate both styles. Then use a source with uncertainty such as `The survey may suggest that students prefer online notes.` Discuss why “may” must remain.
5. **Testing and limitations (1 min):** Show the test table; explain that demo mode is a rules-based fallback and model results require human review.
6. **Future work and contributions (1 min):** Mention stronger grammar evaluation, multilingual support, saved revisions, and user study. Each group member describes their documented contribution.

## Contribution record (confirm before submission)

- Eshita Chauhan: project coordination and requirements/report review.
- Divanshi Mittal: interface and user workflow.
- Vanshika Vats: prompts, output labels and evaluation design.
- Aymaan Dhingra: Python server, integration and test cases.

The group should edit this record if actual contributions differ.
