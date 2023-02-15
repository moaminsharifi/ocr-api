# OCR - API documentation
Simple Api for convert captcha image (and any ocr type image) to text with pertained hugging face images.

Based on python, FastApi
Use Docker and Docker Compose for deployment

![assets/ocr.png](assets/ocr.png)
- [OCR - API documentation](#ocr---api-documentation)
  - [Setup Project](#setup-project)
    - [install git lfs (git large file system)](#install-git-lfs-git-large-file-system)
    - [Ubuntu](#ubuntu)
    - [update token in `.env` file](#update-token-in-env-file)
      - [go to  `api/` directory and clone model](#go-to--api-directory-and-clone-model)
      - [Build Docker images](#build-docker-images)
      - [Run Docker images with `docker compose`](#run-docker-images-with-docker-compose)
      - [Connect to docker container](#connect-to-docker-container)
    - [manage docker containers with GUI](#manage-docker-containers-with-gui)
    - [project structure example](#project-structure-example)
    - [Example Base64 Image](#example-base64-image)


## Setup Project
### install git lfs (git large file system)
### Ubuntu 
```
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

### update token in `.env` file
#### go to  `api/` directory and clone model
```
git clone https://huggingface.co/microsoft/trocr-small-printed
```

#### Build Docker images

```bash
docker compose build
```

#### Run Docker images with `docker compose`
```bash
docker compose up --force-recreate --build
```
- use `-d` flag if want to detached after containers up
- use `--force-recreate` flag for re create docker containers 
- use `--build` flag for re create docker images

For Example ** Build and deployment **

```bash
docker compose up -d --build --force-recreate
docker compose --compatibility up -d --build --force-recreate 
```

#### Connect to docker container
```
docker exec -ti ocr-api_ocr-api bash 
```
use NAME to specify container name, normally docker container name is:

### manage docker containers with GUI
Setup portainer docker container

```bash
docker run -d  -p 2400:9000 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

then go to `http://localhost:2400` and setup admin credentials

for always started up use this roles:

```bash
docker update --restart unless-stopped portainer
```


### project structure example
```bash
api
├── sub
│   ├── router.py
│   ├── schemas.py  # pydantic models
│   ├── models.py  # db models
│   ├── dependencies.py
│   ├── config.py  # local configs
│   ├── tasks.py  # celery tasks
│   ├── constants.py
│   ├── exceptions.py
│   ├── service.py
│   └── utils.py
│   │   
│   ├── config.py  # global configs
│   ├── models.py  # global models
│   ├── schemas.py  # pydantic models
│   ├── exceptions.py  # global exceptions
│   ├── pagination.py  # global module e.g. pagination
│   ├── database.py  # db connection related stuff
│   └── main.py
├── .env
|-- .dockerignore
└── .gitignore
```

### Example Base64 Image
```python
import requests

url = "http://localhost:9090/ocr"

payload = {"image": "iVBORw0KGgoAAAANSUhEUgAAAFUAAAAhCAYAAACoRueNAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAR7SURBVGhD7Vm/axVBEH7NiSAh8IoYi6RIIS8EkRe0UER4pLQTsQgEFCyTIhCLpJGAglpYWFlZ2afy71tv9mbvZmdnZ3/cPWzywfCONzuzO998N3cvmf29eGRmDG+3tw03dAVI+aX8FODXcuTE46UIzf/u4X2zzvyjoRGrgcddrJ4YydA9KYBUvFwvxnTGKU4jGOKldY68WP5cgnPPHyM0Nz6GlH8UKHHccIlFDlEcpeslrFWl6+6M5gdyauMdsbXxjlTqlwRQm/+/YAq1jcnBlQoE4qWH2PdFGNsZ5z9aNubn6k6Rne3OipXBiZXi9xf0LFvmaDYzlFRKnBSf8lOk/Bb+gTLteWNeV5KK2xZBVey8MdcrepbGIzVXiUWKTTF7c7JJDpRpE5Lany8gB+3VjrkMSTVn0lprA6lAVInyJGKzlMlRq9T99uCYwoNTVZi3McfzLgYKHmzLXL1Mn4E1JEkqLCpSX4vS9T1KOocIC1jGCcX4aIy7LR3ymzq3TYnm762bqZC7VHlW2R+2hJxgXbNS/GVBUxyHplI65wjMcat6uu7qYFjDH4aRmRzkoKQKe8rY5WfmNuStUSaF+d0m85IzldJ4JDVQ0fVCJBTg58ex0q9lhcozeTGKVDh/3t1CSB2DEpUCgFQp5lwpLHg1a5vmiPBzPYgVFSUVkCRWUig2F1cArFCipGYrV3waL/rf59wg5KL1c2VzlQb7x576njXmM+4hnJ+ROsxUB0osi2exrb3Z4/k9pPhTEb7cp1X6KSCn666mlOXhplk+vWe+RIntcrjGCVCV6iAqtm3oN29fRY0ImyPFrOhvN/vBi4w88ft4QXGgUvDzYiyRaODP+nUW3T8+UwG0PiCW2vvHd0kc7iHdOTiSNHEkISlOUykgJGaYgfQwQCReAnxC2mucZeK7a+nTXwOc6fxZuEfcFA5EZSK6+bgndgqXRJUtqdTdslAAVaaNAbA4IM35bSP4Q+TFhs1hYwcwUsOZSkH2Z3EZ1q6/UfgTASSUzlKAplLICUSItw4jDRoBX5O15ittFjZ3ebihvPxTU88ekOr2RwikYz5NmQDnt6qS5knqaXi6o6oUCKWKhc8eweuM//IfjKHhjjEfuU+0xvw5jdafIhUgvs2gT4crehqVDjPNqdRdwycjtuAW9M6STap2/uDsZMwhcoiXZ6ItOPLUwyU9vHjhxfnXyaL3U5W6T4gHYns72DTfMwhyDym6v2sYhVQfBfVLpLL4gFRaXxSu2AqVijPHqZQWDHs4w68CXK7mLBea0FgKidhsCOPHe8gJQrPNTXXOFqqotKTzFK5Y6qfkcsMlAVL7p0hNxGt/21BFEwUWIwanZmkKsWI1AmswSqkAYYTFLPKeHCoHL3uklJHj1wpNkVqzP92vJj7nr1TuAZXKP7lqHMaQWoPRau0g3LGttd8F/+XQmIUCazpLIfk15XBSp9hfI3WK/HiZh1ulTgTKvFTgFJ0dQ2rN/tqdwbFu/61Sa6ExCwWuo3OacjipU+yvkTpFfrxEzGb/AE4qfAH7P9o7AAAAAElFTkSuQmCC"}
headers = {
    "token": "USE_ENV_TOKEN",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)

```