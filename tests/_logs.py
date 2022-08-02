from time import time
from typing import Callable


def test_function(function: Callable):
    def wrapper(*args):
        print(f"[RUNNING {function.__name__}]")
        start_time = time()
        output = function(*args)
        end_time = time()
        print(
            f"[EXECUTION FINISHED] Function run successfully in {end_time - start_time} secs",
            end="\n\n\n",
        )
        return output

    return wrapper
