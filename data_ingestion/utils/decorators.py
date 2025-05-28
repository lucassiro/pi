import inspect
import sys
import traceback
from typing import Callable, ParamSpec, TypeVar

from loguru import logger
from rich.console import Console
from rich.traceback import Traceback

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

P = ParamSpec("P")
R = TypeVar("R")


def error_handler(func: Callable[P, R]) -> Callable[P, R | None]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            bound_args = inspect.signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()
            formatted_args = {k: repr(v) for k, v in bound_args.arguments.items()}

            logger.error(f"Error occurred: {e}")
            logger.error(f"Function: {func.__name__}")
            logger.error(f"Arguments: {formatted_args}")
            logger.error(f"Module: {func.__module__}")
            logger.error(f"File: {func.__code__.co_filename}")
            logger.error(f"Line: {func.__code__.co_firstlineno}")
            logger.error("Full Traceback:\n" + "".join(traceback.format_exc()))
            logger.error("Function execution failed. Returning None due to error.")
            return None

    return wrapper


console = Console()


# def error_handler_v2(func: Callable[P, R]) -> Callable[P, R | None]:
#     def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             bound_args = inspect.signature(func).bind(*args, **kwargs)
#             bound_args.apply_defaults()
#             formatted_args = {k: repr(v) for k, v in bound_args.arguments.items()}

#             # Logs comuns
#             logger.error(f"Error occurred: {e}")
#             logger.error(f"Function: {func.__name__}")
#             logger.error(f"Arguments: {formatted_args}")
#             logger.error(f"Module: {func.__module__}")
#             logger.error(f"File: {func.__code__.co_filename}")
#             logger.error(f"Line: {func.__code__.co_firstlineno}")
#             logger.error("Function execution failed. Returning None due to error.")

#             # Exibir traceback formatado com Rich
#             rich_tb = Traceback.from_exception(type(e), e, e.__traceback__, show_locals=True)
#             console.print(rich_tb)

#             return None

#     return wrapper


def error_handler_v2(func: Callable[P, R]) -> Callable[P, R | None]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Format arguments
            bound_args = inspect.signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()
            formatted_args = {k: repr(v) for k, v in bound_args.arguments.items()}

            # Log what rich won't cover
            logger.error(f"Function: {func.__name__}")
            logger.error(f"Arguments: {formatted_args}")
            logger.error("Function execution failed. Returning None due to error.")

            # Render rich traceback to string
            rich_tb = Traceback.from_exception(type(e), e, e.__traceback__, show_locals=True)
            rich_console = Console(file=sys.stderr, width=120, record=True)
            rich_console.print(rich_tb)

            # Export and log the rich-formatted traceback
            rich_traceback_str = rich_console.export_text()
            logger.error("Rich-formatted traceback:\n" + rich_traceback_str)

            return None

    return wrapper
