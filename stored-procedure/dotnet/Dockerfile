FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base
WORKDIR /app
EXPOSE 8080
EXPOSE 9004

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["StoredProcedureSqli.csproj", "."]
RUN dotnet restore "./StoredProcedureSqli.csproj"
COPY . .
WORKDIR "/src/."
RUN dotnet build "StoredProcedureSqli.csproj" -c Debug -o /app/build

FROM build AS publish
RUN dotnet publish "StoredProcedureSqli.csproj" -c Debug -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
# Copy source files for debugging
COPY --from=build /src /src

RUN apt-get update && apt-get install -y unzip \
    && curl -sSL https://aka.ms/getvsdbgsh | bash /dev/stdin -v latest -l /vsdbg \
    && rm -rf /var/lib/apt/lists/*

ENV DOTNET_DEBUG="true"

RUN echo '#!/bin/bash\n\
if [ "$DOTNET_DEBUG" = "true" ]; then\n\
    echo "Use: docker exec -it sqli_dotnet_app /vsdbg/vsdbg --interpreter=vscode"\n\
fi\n\
dotnet StoredProcedureSqli.dll' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
