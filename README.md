## To host app in development so youc an send webhook link to paystack type the following.

```bash
npx untun@latest tunnel http://localhost:8008
```

## Then you'd get the url, and in paystack webhook settings, you can add the url to the webhook url. So when payment is made you'd receive it.

# To Perfom Alembic migrations

## Enter the docker console

```bash
docker ps
# Get the container id of  the shs portal-web
docker exec -it <container_id> /bin/bash
```

## Then run the following commands

```bash
# This will create the tables.
alembic upgrade head

# If you want to downgrade(reset) the tables
alembic downgrade base
```
