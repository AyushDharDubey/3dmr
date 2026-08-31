# 3D Model Repository

3DMR is an open-source repository for storing, validating, and serving real world 3D models (glTF/GLB) linked to OpenStreetMap features, aiming to improve the quality of 3D rendering of map rendering.
The deployed version of the project can be experienced at [3dmr](https://3dmr.eu/)

## Documentation

- [API Documentation](https://3dmr.eu/docs)
- [Local Development Setup](docs/development.md)
- [Deployment and Operations](docs/deployment.md)

## Searching for models

The search box in the navigation bar matches words in a model's title or description.
The [search page](https://3dmr.eu/search) (the "Filters" link next to the search box) offers two more filters:

| Filter     | URL parameter        | Matches                                                                                                                                              |
| ---------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Text       | `query=<words>`      | Models whose title or description contains the words (case-insensitive).                                                                             |
| Category   | `category=<name>`    | Models filed under that category by their uploader. The search page lists every category currently in use.                                            |
| Tag        | `tag=<key>=<value>`  | Models carrying that exact OpenStreetMap-style tag, e.g. `building=yes` or `man_made=tower`. Only the first `=` separates the key from the value.      |

Filters combine: a model is listed only if it matches all of them. Searches are plain `GET` links that can be bookmarked or shared, for example:

```
https://3dmr.eu/search?query=tower&category=building&tag=man_made=tower
```

Clicking a category or tag label on a model's page runs the corresponding search.

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and a codebase overview.

## Project History

This project was [originally developed](https://gitlab.com/n42k/3dmr) as part of Google Summer of Code 2017 by [Pedro Amaro](https://github.com/n42k), under the mentorship of the OpenStreetMap community with [Jan Marsch](https://github.com/kekscom) and [Tobias Knerr](https://github.com/tordanik) as mentors. The project was aimed at creating a repository for 3D models and their metadata, for use by the OpenStreetMap community.
