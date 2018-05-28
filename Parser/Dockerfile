FROM microsoft/dotnet:latest

WORKDIR /app


COPY Parser.csproj .

RUN dotnet restore

# copy and build everything else

COPY . .

RUN dotnet publish -c Release -o out

EXPOSE 9400/tcp
ENTRYPOINT ["dotnet", "out/Parser.dll", "--server.urls", "http://0.0.0.0:9400"]

