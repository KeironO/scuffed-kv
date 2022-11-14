# scuffed-kv

scuffed-kv is a low performance and non-distributed key-value store accessible through an HTTP API, that is built around a modular configuration to enable features on the fly.

## Getting Started

The easiest way to get this up and running is to make use of docker and docker-compose.

In the scuffed-kv directory, simply run:

```
docker-compose build
```

Once complete, start the project using:

```
docker-compose up -d
```

Now go onto `http://localhost:80/docs` and you should see the documentation.


### Persistent Storage

```
version: "3.9"
services:
  scuffedkv:
    build: .
    volumes:
      - ./db:/scuffed-kv/db
    ports:
      - 80
```


### Reverse Proxy with Traefik

```
version: "3.9"
services:
  scuffedkv:
    build: .
    volumes:
      - ./db:/scuffed-kv/db
    ports:
      - 80
    networks:
        - proxy
    labels:
        - "traefik.enable=true"
        - "traefik.http.routers.scuffedkv.rule=Host(`scuffedkv.domain.com`)"
        - "traefik.http.routers.scuffedkv.tls=true"
        - "treafik.port=80"
        - "traefik.http.routers.scuffedkv.entrypoints=websecure"
        - "traefik.http.routers.scuffedkv.tls.certresolver=letsencrypt"
        - "traefik.http.middlewares.scuffedkv.headers.SSLRedirect=true"
        - "traefik.http.middlewares.scuffedkv.headers.browserXSSFilter=true"
        - "traefik.http.middlewares.scuffedkv.headers.STSPreload=true"
    restart: unless-stopped

networks:
   proxy:
     driver: bridge
     name: proxy
```

## Documentation

### GET

```
curl -X GET \
  'http://localhost:80/api/kv/126941005' \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "value": "Subdural hemorrhage due to birth trauma"
    }'
```

Returns:

```
{
  "value": "Subdural hemorrhage due to birth trauma"
}
```

