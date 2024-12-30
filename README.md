# Desafio Desenvolvedor Python - BemAgro

## Descrição

Este projeto consiste em uma API Flask para processamento de arquivos geoespaciais. A API recebe arquivos shapefile (.shp), GeoJSON (.geojson) ou KML (.kml), converte as geometrias para LineString, corrige o sistema de coordenadas para EPSG:4326 e retorna um arquivo shapefile compactado em um arquivo ZIP.

Este projeto foi desenvolvido como parte do desafio para a vaga de Desenvolvedor Python da Bemagro.

## Como executar

### Pré-requisitos

* Python 3.12 ou superior

### Bibliotecas

* geopandas==1.0.1
* shapely==2.0.6
* pyproj==3.7.0
* Flask==3.1.0
* zipfile36==0.1.3

### Instalação

1. Clone o repositório: `git clone <URL do repositório>`
2. Instale as dependências: `pip install -r requirements.txt`

### Execução

1. Execute a API: `python app.py`
2. Acesse a API em: `http://127.0.0.1:5000/`

## Exemplos de uso

### Enviar arquivo via Postman

1. Crie uma requisição POST para a URL `/upload`.
2. No corpo da requisição, selecione a opção "form-data".
3. Adicione uma chave chamada "file" com o tipo "File" e selecione o arquivo ZIP.
4. Envie a requisição.

### Estrutura do arquivo ZIP

O arquivo ZIP deve conter apenas um arquivo, que pode ser:

* Um arquivo shapefile (.shp) com seus arquivos auxiliares (.shx, .dbf, .prj).
* Um arquivo GeoJSON (.geojson).
* Um arquivo KML (.kml).

## Observações

* O script converte todas as geometrias para LineString, mesmo que o arquivo de entrada contenha MultiLineStrings.
* O script corrige o sistema de coordenadas para EPSG:4326, mesmo que o arquivo de entrada esteja em outro sistema.
* O script retorna um arquivo shapefile compactado em um arquivo ZIP.

## Exemplos

Para facilitar o uso da API, este repositório inclui uma pasta com exemplos de arquivos de entrada. Você pode encontrá-los na pasta `exemplos`.

**Dentro da pasta `exemplos` você encontrará:**

* **Pastas com arquivos individuais:**
    * Shapefiles: `exemplos/shapefile`
    * GeoJSON: `exemplos/geojson`
    * KML: `exemplos/kml`
* **Pastas com arquivos compactados em ZIP:**
    * Shapefiles: `exemplos/exemplos_zip/shapefile.zip`
    * GeoJSON: `exemplos/exemplos_zip/geojson.zip`
    * KML: `exemplos/exemplos_zip/kml.zip`

**Como usar os exemplos:**

1. Faça o download dos arquivos da pasta `exemplos`.
2. **Se necessário**, descompacte os arquivos ZIP.
3. Envie os arquivos para a API usando a rota `/upload`.
4. Compare os arquivos de saída com os exemplos fornecidos.

## Melhorias futuras

* Adicionar testes unitários.
* Implementar tratamento de erros mais robusto.
* Adicionar documentação detalhada.

## Autor

* Dérick Duarte ([[Acessar meu perfil](https://github.com/derekinn)])

## Licença

MIT License
