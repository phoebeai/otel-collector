# Contributing

## Release Management

This project uses [release-please](https://github.com/googleapis/release-please) to automate releases. It tracks commits to `main` and creates release PRs automatically.

### Conventional Commits

All commits to `main` should follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. This allows release-please to automatically determine version bumps and generate changelogs.

#### Commit Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Common Types

| Type | Description | Version Bump |
|------|-------------|--------------|
| `feat` | A new feature | Minor (0.X.0) |
| `fix` | A bug fix | Patch (0.0.X) |
| `docs` | Documentation only | Patch |
| `chore` | Maintenance tasks | Patch |
| `refactor` | Code refactoring | Patch |
| `test` | Adding or updating tests | Patch |
| `ci` | CI/CD changes | Patch |

#### Breaking Changes

For breaking changes, add `!` after the type or include `BREAKING CHANGE:` in the footer:

```
feat!: remove deprecated endpoint

BREAKING CHANGE: The /v1/legacy endpoint has been removed.
```

Breaking changes trigger a major version bump (X.0.0).

#### Examples

```
feat: add support for custom exporters
fix: resolve memory leak in batch processor
docs: update configuration examples
chore: bump otel collector version to 0.140.0
feat(receiver): add datadog receiver metrics
fix!: change default port from 4317 to 4318
```

### Release Process

1. Merge PRs with conventional commit messages to `main`
2. Release-please automatically creates/updates a release PR titled "chore(main): release X.Y.Z"
3. The release PR accumulates changes and updates the changelog
4. When ready to release, merge the release PR
5. Release-please creates a GitHub Release with the changelog
6. The CD workflow builds and pushes the Docker image tagged with the release version

### Changelog

The changelog is automatically generated in `CHANGELOG.md` based on conventional commits. You should not edit this file manually.
