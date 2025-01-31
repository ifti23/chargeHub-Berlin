"""Entry Point of the rest-api backend"""

import argparse
from app import create_app

# Run the app
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the REST API backend.")
    parser.add_argument(
        "--env",
        type=str,
        choices=["development", "testing", "default"],
        default="default",
        help="Specify the environment to run the app (default: development).",
    )
    args = parser.parse_args()

    match (args.env):
        case "development":
            config_class = "app.config.DevelopmentConfig"
        case "testing":
            config_class = "app.config.TestingConfig"
        case _:
            config_class = "app.config.Config"

    app = create_app(config_class=config_class)
    app.run(host="0.0.0.0", port=app.config["SERVER_PORT"])
