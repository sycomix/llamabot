"""LlamaBot configuration."""
import openai
import typer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import os
from .utils import configure_environment_variable

app = typer.Typer()


@app.command()
def api_key(
    api_key: str = typer.Option(
        ..., prompt=True, hide_input=True, confirmation_prompt=True
    ),
) -> None:
    """
    Configure the API key for llamabot.

    .. code-block:: python

        configure(api_key="your_api_key_here")

    :param api_key: The API key to be used for authentication.
    """
    configure_environment_variable(env_var="OPENAI_API_KEY", env_value=api_key)


@app.command()
def default_model(model_name=None):
    """Configure the default model for llamabot.

    If no model name is provided,
    or if the model name is not one of those that the user's API key has access to,
    then the user will be prompted for a model name.

    :param model_name: The name of the model to be used for default
    """
    from dotenv import load_dotenv

    from llamabot.config import llamabotrc_path

    load_dotenv(llamabotrc_path)

    openai.api_key = os.getenv("OPENAI_API_KEY")

    model_list = openai.Model.list()["data"]
    available_models = [x["id"] for x in model_list if "gpt" in x["id"]]
    available_models.sort()

    if model_name in available_models:
        configure_environment_variable(
            env_var="OPENAI_DEFAULT_MODEL", env_value=model_name
        )
        return

    completer = WordCompleter(available_models)

    typer.echo("These are the GPT models available to you:")
    for model in available_models:
        typer.echo(model)

    while True:
        default_model = prompt(
            "Please type the name of the model you'd like to use: ",
            completer=completer,
            complete_while_typing=True,
            default=available_models[-1],
        )
        if default_model in available_models:
            configure_environment_variable(
                env_var="OPENAI_DEFAULT_MODEL", env_value=default_model
            )
            break
