cd UI
docker build --rm -t ui .
cd ..

cd Parser
docker build --rm -t parser .

cd ..

cd Tesseract
docker build --rm -t tesseract .
cd ..
