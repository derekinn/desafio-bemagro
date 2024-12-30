import geopandas as gpd
from shapely.geometry import LineString, MultiLineString
import zipfile
import os
import tempfile  # Importando a biblioteca tempfile

def process_file(input_path, output_path="output"):
    # Função para processar os arquivos de entrada (.shp, .geojson, .kml)
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"O arquivo {input_path} não foi encontrado.")

        # Cria um diretório temporário para extrair o conteúdo do arquivo ZIP
        with tempfile.TemporaryDirectory() as temp_dir:
            # Verifica se o arquivo é um arquivo .zip e descompacta caso positivo
            if input_path.endswith('.zip'):
                print("Arquivo ZIP detectado. Descompactando...")
                with zipfile.ZipFile(input_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Encontra o arquivo .shp, .geojson ou .kml dentro do arquivo ZIP
                supported_extensions = ['.shp', '.geojson', '.kml']
                input_file = next(
                    (f for f in os.listdir(temp_dir)
                     if any(f.endswith(ext) for ext in supported_extensions)),
                    None
                )
                if not input_file:
                    raise ValueError(
                        f"Nenhum arquivo {', '.join(supported_extensions)} encontrado no ZIP."
                    )

                input_path = os.path.join(temp_dir, input_file)

            # Lê o arquivo corretamente, dependendo a extensão do mesmo
            if input_path.endswith('.shp'):
                gdf = gpd.read_file(input_path)
            elif input_path.endswith('.geojson'):
                gdf = gpd.read_file(input_path, driver='GeoJSON')
            elif input_path.endswith('.kml'):
                gdf = gpd.read_file(input_path, driver='KML')
            else:
                raise ValueError("Formato de arquivo não suportado.")

            # Função para transformar MultiLineString em LineString 
            def convert_geometry(geom):
                if isinstance(geom, LineString):
                    return geom
                elif isinstance(geom, MultiLineString):
                    all_coords = []
                    for line in geom.geoms:
                        all_coords.extend(line.coords)
                    return LineString(all_coords) if all_coords else None
                return None

            # Aplicando a conversão nas geometrias
            gdf["geometry"] = gdf["geometry"].apply(convert_geometry)

            # Removendo as possíveis geometrias invalidas
            gdf = gdf[gdf["geometry"].notnull()]

            # Convertendo para o sistema de coordenadas EPSG:4326
            if gdf.crs is None:
                print("CRS não definido. Definindo para EPSG:4326")
                gdf.set_crs("EPSG:4326", allow_override=True, inplace=True)
            elif gdf.crs.to_string() != "EPSG:4326":
                print("Convertendo para EPSG:4326")
                gdf = gdf.to_crs("EPSG:4326")

            # Criando a pasta de saída, se não existir
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Caminho para salvar o arquivo shapefile processado
            shapefile_path = os.path.join(output_path, "lines.shp")
            print(f"Salvando em {shapefile_path}")
            gdf.to_file(shapefile_path, driver="ESRI Shapefile")

            # Compactando os arquivos em um arquivo .zip para facilitar o download
            zip_file = f"{output_path}.zip"
            print(f"Compactando os arquivos em: {zip_file}")
            with zipfile.ZipFile(zip_file, "w") as zipf:
                for file in os.listdir(output_path):
                    if file.endswith(('.shp', '.shx', '.dbf', '.prj')):
                        zipf.write(os.path.join(output_path, file), arcname=file)

            print("Processamento concluído com sucesso!")
            return zip_file

    except FileNotFoundError:
        print(f"Erro: O arquivo {input_path} não foi encontrado.")
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

# Deixei um exemplo no respositório para caso o script seja executado diretamente, processa o arquivo "Curvas_Teste.shp"
if __name__ == "__main__":
    process_file("exemplos/shapefiles/exemplo.shp")