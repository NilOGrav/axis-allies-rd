# GitHub Workflow

This project uses GitHub as the central repository for the project files, documentation, data, and version history.

The normal workflow is:

1. **Start by getting the latest remote version**
2. **Check the local repository status**
3. **Do your work**
4. **Review the changes**
5. **Commit the changes**
6. **Push the commit to GitHub**

## Starting work

Before starting significant work, make sure the local repository is up to date:

    git pull
    git status

`git pull` downloads and merges the latest changes from GitHub.

`git status` shows whether there are local changes that need attention.

If `git pull` reports conflicts, resolve them before continuing.

## Working on the project

Make the required changes to the files.

During work, `git status` can be used at any time to check what has changed:

    git status

Review the actual changes before committing:

    git diff

## Saving changes to GitHub

When the changes are ready:

    git add .
    git commit -m "Short description of the change"
    git push

A commit records a version of the changes locally. `git push` sends that commit to GitHub.

Use clear commit messages describing what was changed, for example:

    git commit -m "Update research system documentation"

## After pushing

Check that the local repository is clean:

    git status

A clean working tree normally means that all intended changes have been committed.

## Working with multiple contributors

GitHub is the shared versioned repository. Therefore:

- Pull before starting significant work.
- Do not overwrite changes you did not make.
- Review `git status` before committing.
- Review `git diff` when changes are substantial.
- Use separate commits for logically separate changes where practical.
- Push completed work so it is available to the other contributors.

---

# Creating a New Version

A **version** is a named, stable point in the project's development history. Normal commits record ongoing work; a version is created when the project reaches a point that should be identifiable and reproducible later.

Before creating a new version:

1. Make sure the intended changes have been committed.
2. Make sure the local repository is clean.
3. Make sure the latest commits have been pushed to GitHub.
4. Decide on the version number.

Check the repository:

    git status

If everything is committed and pushed, create a version tag.

For example, for version `v1.0.0`:

    git tag -a v1.0.0 -m "Version 1.0.0"
    git push origin v1.0.0

The tag permanently identifies that particular commit as version `v1.0.0`.

### Version numbering

Use a consistent version-numbering scheme. The usual format is:

    MAJOR.MINOR.PATCH

For example:

    v1.0.0
    v1.1.0
    v1.1.1

The exact meaning of the version components should follow the project's established versioning policy.

### Creating a GitHub Release

A Git tag can also be turned into a GitHub Release.

In GitHub:

1. Open the repository.
2. Go to **Releases**.
3. Choose **Create a new release**.
4. Select the version tag that was created.
5. Add release notes describing the important changes.
6. Publish the release.

The release provides a human-readable description of what changed in that version, while the Git tag identifies the exact repository state.

### Recommended version workflow

    git status
    git add .
    git commit -m "Description of final changes"
    git push

    git tag -a v1.0.0 -m "Version 1.0.0"
    git push origin v1.0.0

Then create the corresponding GitHub Release if a published release is desired.

**Important:** Do not create a version tag while there are uncommitted changes. The purpose of a version tag is to identify a specific, reproducible state of the project.

## If you need to discard local changes

Sometimes the local repository needs to be replaced by the version currently on GitHub. This is an exceptional operation because it can permanently discard local work.

See **Overwriting Your Local Git Repository** below before doing this.

### Quick reference

**Normal update:**

    git pull

**Check status:**

    git status

**Review changes:**

    git diff

**Save changes:**

    git add .
    git commit -m "Description"
    git push

**Create a version:**

    git tag -a v1.0.0 -m "Version 1.0.0"
    git push origin v1.0.0

**Check final state:**

    git status

---

## Overwriting Your Local Git Repository

To overwrite your local Git repository with the remote version, you can use `git fetch` followed by `git reset --hard origin/<branch-name>`, where `<branch-name>` is the name of your branch. This will discard all local changes and make your local branch match the remote branch exactly.

### Step-by-Step Commands

1. Fetch the Latest Changes

Use the command to download the latest changes from the remote repository:

    git fetch

2. Reset Your Local Branch

Reset your local branch to match the remote branch. Replace `<branch-name>` with the name of your branch (e.g., `main`):

    git reset --hard origin/<branch-name>

### Important Considerations

**Data Loss Warning:** The `git reset --hard` command will permanently discard all local changes, including uncommitted modifications. Ensure you have backed up any important work before executing the command.

**Backup Option:** If you want to keep your local changes, create a backup branch before resetting:

    git checkout -b backup-branch
    git add .
    git commit -m "Backup of local changes"
    git checkout <branch-name>

### Summary of Commands

| Command | Description |
|---|---|
| `git fetch` | Downloads changes from the remote repository. |
| `git reset --hard origin/<branch-name>` | Resets local branch to match the remote branch, discarding local changes. |
