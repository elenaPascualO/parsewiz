"""JSON to CSV converter."""

import io
import itertools
import json
from typing import Any

import pandas as pd

from backend.config import MAX_EXPANDED_ROWS
from backend.converters.base import BaseConverter


class JsonToCsvConverter(BaseConverter):
    """Converts JSON data to CSV format.

    Handles nested JSON structures by expanding arrays into multiple rows
    (Cartesian product / denormalization).
    """

    def convert(self, content: bytes) -> bytes:
        """Convert JSON to CSV.

        Args:
            content: JSON content as bytes.

        Returns:
            CSV content as bytes.

        Raises:
            ValueError: If JSON is invalid or cannot be converted.
        """
        df = self._json_to_dataframe(content)
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue().encode("utf-8")

    def preview(
        self, content: bytes, page: int = 1, page_size: int = 10
    ) -> dict[str, Any]:
        """Generate preview of JSON data with pagination.

        Args:
            content: JSON content as bytes.
            page: Page number (1-indexed). Defaults to 1.
            page_size: Number of rows per page. Defaults to 10.

        Returns:
            Preview dictionary with columns, rows, total_rows, and pagination info.
        """
        df = self._json_to_dataframe(content)
        total_rows = len(df)
        total_pages = max(1, (total_rows + page_size - 1) // page_size)

        # Ensure page is within bounds
        page = max(1, min(page, total_pages))

        # Calculate slice indices
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        # Get the page slice
        page_df = df.iloc[start_idx:end_idx]

        return {
            "columns": df.columns.tolist(),
            "rows": page_df.values.tolist(),
            "total_rows": total_rows,
            "current_page": page,
            "total_pages": total_pages,
            "page_size": page_size,
        }

    def _json_to_dataframe(self, content: bytes) -> pd.DataFrame:
        """Parse JSON and convert to DataFrame.

        Handles arrays of objects and expands nested arrays into multiple rows
        using Cartesian product (denormalization).

        Args:
            content: JSON content as bytes.

        Returns:
            A pandas DataFrame.

        Raises:
            ValueError: If JSON cannot be parsed or converted.
        """
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File encoding error: Unable to decode as UTF-8. "
                f"Please ensure the file is saved with UTF-8 encoding. Details: {e}"
            ) from e

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
            ) from e

        # Handle different JSON structures
        if isinstance(data, list):
            if not data:
                raise ValueError(
                    "JSON array is empty. The file contains '[]' with no data."
                )
            # Check if items are objects
            if not all(isinstance(item, dict) for item in data):
                raise ValueError(
                    "JSON array must contain objects. Found non-object items in array."
                )
            # Expand each object and combine all rows
            all_rows: list[dict[str, Any]] = []
            for item in data:
                all_rows.extend(self._expand_object(item))
            self._check_row_limit(len(all_rows))
            return pd.DataFrame(all_rows)

        elif isinstance(data, dict):
            # Single object - expand it fully
            rows = self._expand_object(data)
            self._check_row_limit(len(rows))
            return pd.DataFrame(rows)

        else:
            raise ValueError(
                f"Invalid JSON structure. Expected an array of objects or an object, "
                f"but got {type(data).__name__}."
            )

    def _check_row_limit(self, row_count: int) -> None:
        """Check if row count exceeds the safety limit.

        Args:
            row_count: Number of rows generated.

        Raises:
            ValueError: If row count exceeds MAX_EXPANDED_ROWS.
        """
        if row_count > MAX_EXPANDED_ROWS:
            raise ValueError(
                f"Expansion would create {row_count} rows (limit: {MAX_EXPANDED_ROWS}). "
                f"The nested arrays in your JSON create too many combinations. "
                f"Consider simplifying your JSON structure or processing it in parts."
            )

    def _expand_object(
        self, obj: dict[str, Any], prefix: str = ""
    ) -> list[dict[str, Any]]:
        """Expand an object with nested arrays into multiple flat rows.

        Creates the Cartesian product of all nested arrays, producing one row
        per combination. Scalar fields are repeated in each row.

        Args:
            obj: The object to expand.
            prefix: Prefix for nested keys (used for dot notation).

        Returns:
            A list of flat dictionaries, one per row.
        """
        # Separate scalars from nested structures
        scalars: dict[str, Any] = {}
        array_expansions: list[tuple[str, list[dict[str, Any]]]] = []

        for key, value in obj.items():
            full_key = f"{prefix}{key}"

            if isinstance(value, dict):
                # Recursively expand nested objects
                nested_rows = self._expand_object(value, f"{full_key}.")
                if len(nested_rows) == 1:
                    # Single row - merge into scalars
                    scalars.update(nested_rows[0])
                else:
                    # Multiple rows - add to array expansions
                    array_expansions.append((full_key, nested_rows))

            elif isinstance(value, list):
                if value and all(isinstance(item, dict) for item in value):
                    # Array of objects - expand each item with key prefix
                    expanded_items: list[dict[str, Any]] = []
                    for item in value:
                        item_rows = self._expand_object(item, f"{full_key}.")
                        expanded_items.extend(item_rows)
                    array_expansions.append((full_key, expanded_items))
                elif value:
                    # Array of primitives - convert to JSON string
                    scalars[full_key] = json.dumps(value)
                else:
                    # Empty array
                    scalars[full_key] = "[]"

            else:
                # Scalar value
                scalars[full_key] = value

        # If no arrays to expand, return single row with scalars
        if not array_expansions:
            return [scalars] if scalars else [{}]

        # Compute Cartesian product of all array expansions
        array_rows_list = [rows for _, rows in array_expansions]
        product = list(itertools.product(*array_rows_list))

        # Combine scalars with each product combination
        result: list[dict[str, Any]] = []
        for combination in product:
            row = scalars.copy()
            for expanded_row in combination:
                row.update(expanded_row)
            result.append(row)

        return result if result else [scalars]
