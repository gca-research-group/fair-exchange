# Application

## Table of Content

-   [How to Run](#how-to-run)
-   [License](#license)
-   [Contact](#contact)

---

## How to Run

> **Tip for Windows users:** Some shell scripts are provided to simplify the setup. We recommend using the **Git Bash** terminal for compatibility.

### Prerequisites

-   Docker
-   Python 3.11 or higher
-   Poetry

### Setup Steps

1. **Clone the repository**

```sh
git clone https://github.com/gca-research-group/fair-exchange-v2
```

2. **Set up environment variables**

    - Provide values for MongoDB, PostgreSQL, and RabbitMQ.
    - Configuration files are located in `.docker/appA/env/`.
    - Use the example files as templates.
    - Optionally, run the script `.scripts/appA/env.sh` to auto-fill the variables.

3. **Run the database**

```sh
# PostgreSQL
./.scripts/appA/up.sh
```

4. **Run the application**

```sh
# navigate to the project folder
cd project

# activate the environment
poetry shell

# create the migrations
flask db migrate

# apply the migrations
flask db upgrade

# run the application
task start
```

6. **Access the application**

The application is available at http://localhost:6000

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

If you have any questions or issues, feel free to [open an issue](https://github.com/gca-research-group/smart-contract-execution-monitoring-system/issues) or contact the maintainers.
