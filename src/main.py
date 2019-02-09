#!/usr/bin/python
# coding=utf-8

import sys
import textwrap

from log.log_processor import LogProcessor


def get_input_file_path():
    if len(sys.argv) > 2:
        print "No momento, só é possível passar um arquivo por vez"
        exit()
    if len(sys.argv) == 2:
        param = sys.argv[1]
        if param == "help":
            print textwrap.dedent(
                """\
                Mode de usar:
                - Chamar o método já passando o caminho para o arquivo como parâmetro;
                - Rodar o programa sem parâmetros;
                - Passar o parâmetro 'help' para ler essa ajuda"""
            )
            exit()
        else:
            return param
    else:
        return raw_input("Entre com o caminho para o arquivo de log: ")


def print_result(log_data):
    header = ["Posição Chegada", "Código Piloto", "Nome Piloto", "Qtde Voltas Completadas", "Tempo Total de Prova"]

    row_format = "{:<25}" * len(header)
    print row_format.format(*header)

    for i in log_data.pilots_data:
        a = [
            "%.2d" % i.position,
            "%.3d" % i.pilot_id,
            i.pilot_name,
            "%.2d" % i.completed_laps,
            i.race_duration
        ]
        print row_format.format(*a)


file_path = get_input_file_path()
parsed = LogProcessor().parse_log_file(file_path)
print_result(parsed)
