docker build --no-cache -f Dockerfile -t cat_frontend:1.0 .
docker run --name cat_frontend --restart unless-stopped -it -d -p 8000:8000 cat_frontend:1.0
