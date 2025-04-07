# Public Bulletin Board (PBB)

## Table of Content

-   [Set Up](#set-up)
-   [Running the application](#running-the-application)

## Set Up

-   Required dependencies

    -   Docker
    -   Python +3.11
    -   Poetry

-   Environment variables

1. Within the `.docker/alice/env` folder create a `.env.database` file
2. Within the `project` folder create a `.env` file
3. Fill them with the following values:

```.env
# the database user
# if you are not using the default value (`postgres`), you may need to adjust the postgres container
POSTGRES_USER=postgres

# the database password
POSTGRES_PASSWORD=

# the database name
POSTGRES_DB=

# the database host
# if you are running the application in a docker containter, the POSTGRES_HOST should be the name of the postgres container
POSTGRES_HOST=

# the postgres port
POSTGRES_PORT=
```

## Running the application

-   Activate the environment

```sh
poetry shell
```

-   Creating the migrations

```sh
flask db migrate
```

-   Appying the migrations

```sh
flask db upgrade
```

-   Running the application

```sh
flask run --reload
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on GitHub or contact the maintainers.
