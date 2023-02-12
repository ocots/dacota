import json

import docker

from ...backend_django.settings import CONTAINER_LANGUAGE, ContainerLanguage


def start_container(c1, c2, c3, a, alpha):
    """
    This function starts a container based on the language specified in the CONTAINER_LANGUAGE setting.
    If the language is Python, the `start_python_container` function is called.
    If the language is Julia, the `start_julia_container` function is called.
    If the language is unknown, an Exception is raised.
    """
    if CONTAINER_LANGUAGE == ContainerLanguage.PYTHON:
        start_python_container(c1, c2, c3, a, alpha)
    elif CONTAINER_LANGUAGE == ContainerLanguage.JULIA:
        start_julia_container(c1, c2, c3, a, alpha)
    else:
        raise Exception("Unknown container language")


def start_python_container(c1, c2, c3, a, alpha):
    """
    This function starts a Python container.
    It first checks if the `smith_container` image exists, and if not, raises an error message.
    Then, it creates a Docker client, starts a container from the `smith_container` image, and passes the arguments `c1`, `c2`, `c3`, `a`, and `alpha` to the `main.py` script.
    The container's output is loaded as a JSON object and returned.
    """
    check_image("smith_container")
    client = docker.from_env()
    container = client.containers.run(
        "smith_container",
        command=["python", "src/smith/main.py", c1, c2, c3, a, alpha],
        remove=True,
        stderr=True,
        stdout=True,
    )
    curve_list = json.loads(container.decode("utf-8"))

    return curve_list


# TODO: Implement this
def start_julia_container(c1, c2, c3, a, alpha):
    check_image("THE_IMAGE_NAME")
    curve_list = []
    return curve_list


def check_image(image_name="smith_container"):
    """
    This function checks if the `smith_container` image exists.
    If not, it raises an error message with instructions to build the image.
    """
    client = docker.from_env()
    try:
        client.images.get(image_name)
    except docker.errors.ImageNotFound:
        print(
            'You have to build this image first. To do it, you have to go to the smith folder present in the repo (You will find a Dockerfile there), then run: \n\t [docker build -t "smith_container" .] \n This takes several minutes'
        )
    except docker.errors.APIError:
        print("Docker API error")
    except Exception as e:
        print("Unknown error")
        print(e)
