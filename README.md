# simple-api
installation for common linux distro
```sh
git clone https://github.com/FilArt/simple-api.git
cd simple-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser  # interactively create user
```

launching
```sh
./manage.py runserver
```
