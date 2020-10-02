# Delivery
Delivery is flask based web application for online food ordering.

[![](https://i.ibb.co/1fxGdfh/Screenshot-2020-10-02-at-03-50-58.png)](https://i.ibb.co/nsSMnsZ/Screenshot-2020-10-02-at-03-50-58.png)[![](https://i.ibb.co/XC3YWKq/Screenshot-2020-10-01-at-19-46-05.png)](https://i.ibb.co/G5tHd8q/Screenshot-2020-10-01-at-19-46-05.png)

## Tech
Delivery uses this to work properly::

* Flask - backend
* Mongoengine - Mongodb ODM 

### Installation 
Delivery scrapper requires python3 to run. You can install dependences by yourself or run setup.py.

```sh
$ python3 setup.py
```

### Docker
Delivery is very easy to install and deploy using docker-compose.

```sh
$ docker-compose up
```

### Deploy
Another easy way to deploy is ansible playbook.
```sh
$ ansible-playbook deployment/playbook.yml
```
