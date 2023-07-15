<h1 align="center">Insurance calculator service</h1>

<p align="center">
    <a href="https://github.com/0dminnimda/insurance_calculator_service/blob/main/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/0dminnimda/insurance_calculator_service">
    </a>
    <a href="https://pypi.org/project/insurance_calculator_service/">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/insurance_calculator_service">
    </a>
    <a href="https://github.com/0dminnimda/insurance_calculator_service/actions/workflows/ci.yml">
        <img alt="CI" src="https://github.com/0dminnimda/insurance_calculator_service/actions/workflows/ci.yml/badge.svg">
    </a>
</p>

This repo implements this [task](/TASK.md)

## Installation and Launch

Clone the repo and go to it's root folder

```bash
git clone https://github.com/0dminnimda/insurance_calculator_service.git
cd insurance_calculator_service
```

Then run python command in the root folder

```bash
python -m insurance_calculator_service
```

You can even change some options

```bash
python -m insurance_calculator_service --help
```

Now when you lanched the app just go to the host, by default http://localhost:80.

To see what things are possible and play around go to http://localhost:80/docs

## Debug

To debug you'll need to install this app as python package. (Personally I'll recommend to use virtualenv)

```bash
pip install -e .
```

Then just run the `__main__.py` file in the debug mode. It uses absolute imports to allow for that kind of behaviour.

## Docker

If you would like to use docker, just run

```bash
docker-compose up -d
```

## Tests

All tests are located at [`tests`](/tests) folder.

To run tests you need to first install the package prepared for testing

```bash
pip install -e .[test]
```

And then run pytest

```bash
python -m pytest
```

## Formatting

Code is formatter using [black](https://github.com/psf/black)

You can get it along with this project by running

```bash
pip install -e .[fmt]
```
