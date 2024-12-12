import os, sys, openpyxl, pandas, io, uuid
# path = os.path.normpath(os.path.join(os.getcwd(), '..'))
# print(path)
# sys.path.append(path)
cur_path = "D:\\tomas\\Nextcloud\\Projetos\\Python_Pi_final\\raspberry_proj"
sys.path.append(cur_path)

from core import schema

def export_logs_to_xlsx(start_time = None, end_time = None):

    """
    1 - Extrair os resultados
    """
    database = schema.mysql_db()
    results = None
    #print(f'{start_time} : {end_time}')

    query = ("SELECT `event`, CASE WHEN users.Nome IS NOT NULL THEN users.Nome ELSE \"N/A\" END AS `Nome`,"
             " CASE WHEN `remote?` = 1 THEN \"Sim\" ELSE \"Não\" END AS `Remoto`, DATE_FORMAT(event_time,'%d-%m')"
             " FROM `logs` LEFT JOIN users ON users.ID = logs.user_id")

    if start_time is not None:
        query += " WHERE event_time >= %s"

    if end_time is not None:
        query += " WHERE" if start_time is None else " AND"
        query += " event_time <= %s"

    #print(query)
    #sys.exit(0)

    headers = ["Evento", "Nome do Utilizador", "Remoto?", "Data&Hora"]

    if start_time is not None and end_time is not None: results = database.FetchAll(query,(start_time, end_time))
    elif start_time is not None: results = database.FetchAll(query, start_time)
    elif end_time is not None: results = database.FetchAll(query, end_time)
    else: results = database.FetchAll(query)

    """
    2 - Converter para DataFrame
    """
    df = pandas.DataFrame(results, columns=headers)

    """
    3 - Criar um ficheiro XSLX mas guardá-lo na RAM
    """
    output = io.BytesIO() # Guardar objectos na RAM
    with pandas.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, engine='openpyxl', sheet_name="Registos")

        # Definir o comprimento das
        workbook = writer.book
        worksheet = writer.sheets['Registos']

        column_widths = [20, 23, 10, 21]

        # Set the column widths based on the provided list
        for col_idx, width in enumerate(column_widths, start=1):
            col_letter = openpyxl.utils.get_column_letter(col_idx)
            worksheet.column_dimensions[col_letter].width = width

    output.seek(0) # Colocar o ponteiro no inicio para depois ler

    """
    4 - Retornar o ficheiro
    """
    return output.getvalue()

if __name__ == "__main__":
    start = None
    end= None
    for arg in sys.argv[1:]:
        if arg.startswith('start='): start = arg.split('=')[1].strip(' "')  # Get the value after 'start='
        elif arg.startswith('end='): end = arg.split('=')[1].strip(' "')  # Get the value after 'end='
    file_name = uuid.uuid4()
    out = export_logs_to_xlsx(start, end)
    new_path = os.path.normpath(os.path.join(cur_path, 'extras', 'excel_logs', str(file_name)))
    print(f'{new_path}.xlsx')

    with open(f'{new_path}.xlsx', 'wb') as file:
        file.write(out)
