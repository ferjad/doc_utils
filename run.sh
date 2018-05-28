docker network create deepdoc
docker run --net deepdoc -d -p 5000:5000 --name ui ui
docker run --net deepdoc -d -p 9200:9200 --name tesseract tesseract
docker run --net deepdoc -d -p 9400:9400 --name parser parser
