# Agent Instructions

## Git Remote

Changes must be pushed to: **https://github.com/alirezakavianifar/thesis_encryption_project.git**

Ensure the remote `origin` points to this URL. If not configured, use: `git remote add origin https://github.com/alirezakavianifar/thesis_encryption_project.git`(or `git remote set-url origin <url>` to update).

## .gitignore

If `.gitignore` does not exist, create one based on the codebase structure and language. Adapt entries to match the project's technologies and build output locations.

## README.md

The GitHub repository must always contain a `README.md` file at the root of the project. This file should explain what the project is, how it is structured, how to run it, and any other instructions necessary for understanding or running the project.

## Git Push Workflow

When the user uses the keyword "push" in a request (e.g., "please push these changes", "push", or similar), you MUST follow this specific workflow:

1. **Stage all changes**: standard `git add .`
2. **Infer Commit Message**: Generate a concise, descriptive, and professional commit message based on the recent file changes and conversation context. Do not ask the user for a commit message unless they explicitly provide one.
3. **Commit**: `git commit -m "<inferred_message>"`
4. **Push**: `git push` (or `git push -u origin <branch>` if the upstream is not set).

**Note:** You should proactively execute these commands without asking for extra confirmation if the user explicitly said "push".
