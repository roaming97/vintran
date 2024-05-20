# vintran

**vin**tage file **tran**sfer

Free web file transfer tool made with Python and Flask and compatibility in mind. It is meant to run well on older browsers running on older computers so that files can be sent from there.

## Building

This project requires at least [Python 3.8](https://www.python.org/downloads/) installed on your computer or server.

Clone the repository and navigate into the directory:

```sh
$ git clone https://github.com/roaming97/vintran.git
$ cd vintran
```

> [!TIP]
> Create a virtual environment then activate it:
>
> ```sh
> $ python3 -m venv venv
> ```

Activate on **Unix**

```sh
$ source venv/bin/activate
```

Activate on **Windows**

```powershell
> .\venv\Scripts\activate
```

Install the dependencies:

```sh
$ pip install -r requirements.txt
```

Or you can build and install the app as a Python package for deployment:

```sh
$ pip install -e .
```

## Running

Set the proper environment variables following the example ([.env.example](./.env.example)):
```python
SECRET="MY_SECRET_KEY"
DATABASE_URI='sqlite:///mydatabase.sqlite'
```

This command starts a production server on `localhost:5000`:

```sh
$ flask --app vintran run
```

## Contributing

If you encounter any errors or bugs, open an issue.
Pull requests are welcome.