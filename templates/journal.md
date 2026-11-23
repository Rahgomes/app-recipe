# Journal template

`docs/recipe/JOURNAL.md`. One line per event, in the same commit as the work.

```markdown
# Journal

Format: `date · stage · ✅ worked / ❌ failed / 🔁 changed / ⚠️ attention · what | why`
A lesson starts with "Lesson:".

- 2026-11-18 · 6 · ✅ · 16 screens approved on the first try with 2 references attached | Lesson: approve references before the batch.
- 2026-11-19 · 8 · ❌→✅ · First build failed in Gradle due to a forced targetSdk | Lesson: do not override the SDK default.
- 2026-11-20 · 3 · 🔁 · Custom queue replaced with Firestore offline cache | Same guarantee, less code.
```

Why in the same commit: written later, the cause is already forgotten and only "fixed bug" remains.
The lessons in this kit (`LESSONS.md`) came entirely from journals like this.
