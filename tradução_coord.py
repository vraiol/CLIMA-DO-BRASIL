import csv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable

def coordenadas_para_localizacao(lon, lat):  # Invertei a ordem dos parâmetros
    geolocator = Nominatim(user_agent="meu_app/1.0", timeout=10)
    try:
        location = geolocator.reverse(f"{lat}, {lon}", language='pt')
        if location and location.raw.get('address'):
            estado = location.raw['address'].get('state', "Estado desconhecido")
            cidade = location.raw['address'].get('city', "Cidade desconhecida")
            if cidade == "Cidade desconhecida":
                cidade = location.raw['address'].get('town', "Cidade desconhecida")
                if cidade == "Cidade desconhecida":
                    cidade = location.raw['address'].get('village', "Cidade desconhecida")
                    if cidade == "Cidade desconhecida":
                        cidade = location.raw['address'].get('island', "Cidade desconhecida")
            return estado, cidade
        else:
            return "Estado desconhecido", "Cidade desconhecida"
    except GeocoderUnavailable:
        return "Serviço temporariamente indisponível", "Serviço temporariamente indisponível"

def traduzir_coordenadas(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)  # Lê o cabeçalho existente
        header.extend(["Estados", "Cidades"])  # Adiciona os novos cabeçalhos
        writer.writerow(header)  # Escreve o novo cabeçalho no arquivo de saída

        for row in reader:
            if len(row) > 7 and ' ' in row[7]:  # Verifica se a coluna de coordenadas tem os dados esperados
                lon, lat = row[7].split()  # Invertei a ordem para longitude e depois latitude
                estado, cidade = coordenadas_para_localizacao(lon, lat)
                row.append(estado)  # Adiciona o estado à linha original
                row.append(cidade)  # Adiciona a cidade/ilha à linha original
            else:
                row.append("Dados inválidos")
                row.append("Dados inválidos")
            writer.writerow(row)  # Escreve a linha completa (original + novos dados) no arquivo de saída

# Use os nomes dos seus arquivos aqui
input_file = 'clima_brasil_polido.csv'
output_file = 'clima_brasil_atualizado.csv'

traduzir_coordenadas(input_file, output_file)
