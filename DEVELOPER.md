# DEVELOPER

## Setup development environment
Clone the repository and `cd` into it.
To install a local conda environment for the project:

```shell
conda env create -f environment.yml
```
Make sure you have selected the project's environment in your IDE when you run test or in the shell

```shell
# environment_name: use name in environment.yml
conda activate environment_name
```

# Versioning Guideline
The goal of versioning is to provide backwards compatibility for the user.
This means that the old version of the Router should still be available and working after a new version is released.

The minimum version of a route function is defined by the @version annotation in the route definition.
When a new version is necessary, a new route function needs to be created that is annotated with the new version number.
The application then uses the VersionedApp to automatically deploy apps for all routers of the application with the correct router functions.

Routers are only versioned as major and minor versions. Patch versions are not supposed to change the interface of the application.

Major versions are used for breaking changes in the overall application as well as for deprecation waves.

Minor versions are used for changes in the interface of the router. This includes:
- Removing or changing input parameters
- Adding, removing or changing output fields

Patch versions can be used for:
- Bugfixes
- Performance improvements
- Adding new input parameters with default values that do not change the behavior of the router
## Versioning Schema
The versioning schema is `{major}.{minor}.{patch}[{release}{build}]` where the
latter part (release and build) is optional.
Release takes the following values:
- _null_
- _dev_ (to indicate a actively developed version)
- _a_ (alpha)
- _b_ (beta)
- _rc_ (release candidate)
- _post_ (post release hotfixes)

### Bump version identifier
It is recommended to do `--dry-run` prior to your actual run.
```bash
# increase version identifier
bump2version [major/minor/patch/release/build]  # --verbose --dry-run

# e.g.
bump2version minor  # e.g. 0.5.1 --> 0.6.0
bump2version minor --new-version 0.7.0  # e.g. 0.5.1 --> 0.7.0
```
After a successful release, the version identifier should be bumped to the `dev` state to indicate
that master/main is under development. The exact version does not matter to much, e.g. work that was
initially considered a patch could be bumped as a minor release upon release.
```bash
bump2version release --new-version 0.6.0dev1  # e.g. 0.5.1 --> 0.6.0dev1
```