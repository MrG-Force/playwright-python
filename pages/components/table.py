from playwright.sync_api import Locator
from typing import List, Dict


class Table:
    def __init__(self, table_element: Locator):
        self.table_element = table_element

    def get_headers(self) -> List[str]:
        return self.table_element.get_by_role(role="columnheader").all_inner_texts()

    def get_rows_as_dict(self, key_column: str) -> Dict[str, Dict[str, str]]:
        """
        Returns the table rows as a dictionary of dictionaries, using the specified column's values as keys.

        Parameters:
        key_column (str): The column name whose values will be used as keys.

        Returns:
        Dict[str, Dict[str, str]]: A dictionary where keys are the values from the specified key_column,
                                   and values are dictionaries representing the table rows.
        """
        headers = self.get_headers()
        key_column_index = headers.index(key_column)
        rows = {}

        row_elements = self.table_element.locator("tbody tr").all()

        for row_element in row_elements:
            row_dict = {}
            cell_elements = row_element.locator("td").all()
            for header, cell_element in zip(headers, cell_elements):
                row_dict[header] = cell_element.inner_text().strip()

            key = cell_elements[key_column_index].inner_text().strip()
            rows[key] = row_dict

        return rows

    def get_row_as_dict_by_column_name_and_value(
        self, column: str, value: str
    ) -> Dict[str, str]:
        """
        Returns the row as a dictionary where the specified column has the specified value.

        Parameters:
        column (str): The column name to search for the value.
        value (str): The value to search for in the specified column.

        Returns:
        Dict[str, str]: A dictionary representing the row where each key is a column name and the value is the cell value.
        """
        headers = self.get_headers()
        column_index = headers.index(column) if column in headers else -1
        if column_index == -1:
            return {}

        row_elements = self.table_element.locator("tbody tr").all()
        for row_element in row_elements:
            cell_element = row_element.locator("td").locator(f"nth={column_index + 1}")
            if cell_element.inner_text().strip() == value:
                row_dict = {}
                cell_elements = row_element.locator("td").all()
                for header, cell_element in zip(headers, cell_elements):
                    row_dict[header] = cell_element.inner_text().strip()
                return row_dict

        return {}
