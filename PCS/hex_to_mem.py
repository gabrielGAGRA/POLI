# Salve este código como converter.py
import re
import sys


def convert_hex_to_mem(input_file_path, output_file_path):
    """
    Converte um arquivo .hex com bytes separados por espaço para o formato
    compatível com $readmemh (uma palavra de 32 bits por linha).
    """
    try:
        with open(input_file_path, "r") as f_in:
            content = f_in.read()

        # Remove endereços (@...), quebras de linha e espaços extras
        content = re.sub(r"@\w+", "", content)
        hex_bytes = content.split()

        if not hex_bytes:
            print(f"Erro: Nenhum byte hexadecimal encontrado em '{input_file_path}'.")
            return

        with open(output_file_path, "w") as f_out:
            # Agrupa de 4 em 4 bytes
            for i in range(0, len(hex_bytes), 4):
                if i + 4 <= len(hex_bytes):
                    # Concatena os 4 bytes para formar a palavra de 32 bits
                    word = "".join(hex_bytes[i : i + 4])
                    f_out.write(word.lower() + "\n")

        print(f"Conversão concluída! Arquivo '{output_file_path}' criado.")

    except FileNotFoundError:
        print(f"Erro: O arquivo de entrada '{input_file_path}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Uso: python converter.py <arquivo_de_entrada.hex> <arquivo_de_saida.mem>"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_hex_to_mem(input_file, output_file)
