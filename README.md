# Insurance calculator service

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
