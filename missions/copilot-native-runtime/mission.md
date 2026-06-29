# Mission

Build Copilot-native runtime support around OMP so VS Code agents can inspect state, run repeatable tasks, and verify implementation evidence without Claude Code plugin APIs.

## Outcomes

- Keep `omp bridge` as the state and artifact inspection surface.
- Keep `.vscode/tasks.json` aligned with the repeatable validation loop.
- Keep `.github/prompts/autocopilot.prompt.md` aligned with Matt Pocock skill selection and repeat-until-green execution.