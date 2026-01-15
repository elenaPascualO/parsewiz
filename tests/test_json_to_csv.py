"""Tests for JSON to CSV converter."""

import csv
import io

import pytest

from backend.converters.json_to_csv import JsonToCsvConverter


class TestJsonToCsvConverter:
    """Tests for JsonToCsvConverter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = JsonToCsvConverter()

    def test_convert_simple_json(self, simple_json: bytes):
        """Test converting simple JSON array to CSV."""
        result = self.converter.convert(simple_json)
        assert isinstance(result, bytes)

        # Parse CSV and verify
        reader = csv.DictReader(io.StringIO(result.decode("utf-8")))
        rows = list(reader)

        assert len(rows) == 3
        assert rows[0]["name"] == "Alice"
        assert rows[0]["age"] == "30"
        assert rows[0]["city"] == "New York"

    def test_convert_nested_json(self, nested_json: bytes):
        """Test converting nested JSON with flattening."""
        result = self.converter.convert(nested_json)
        assert isinstance(result, bytes)

        # Parse CSV and verify flattened columns
        reader = csv.DictReader(io.StringIO(result.decode("utf-8")))
        rows = list(reader)

        assert len(rows) == 2
        assert "address.street" in reader.fieldnames
        assert "address.city" in reader.fieldnames
        assert rows[0]["address.street"] == "123 Main St"

    def test_preview_simple_json(self, simple_json: bytes):
        """Test preview generation with pagination."""
        result = self.converter.preview(simple_json, page=1, page_size=2)

        assert "columns" in result
        assert "rows" in result
        assert "total_rows" in result
        assert "current_page" in result
        assert "total_pages" in result
        assert "page_size" in result

        assert result["columns"] == ["name", "age", "city"]
        assert len(result["rows"]) == 2
        assert result["total_rows"] == 3
        assert result["current_page"] == 1
        assert result["total_pages"] == 2
        assert result["page_size"] == 2

    def test_convert_empty_array_raises(self):
        """Test that empty array raises ValueError."""
        empty_json = b"[]"
        with pytest.raises(ValueError, match="empty"):
            self.converter.convert(empty_json)

    def test_convert_invalid_json_raises(self):
        """Test that invalid JSON raises ValueError with line/column info."""
        invalid_json = b"not json"
        with pytest.raises(ValueError, match=r"Invalid JSON at line \d+, column \d+"):
            self.converter.convert(invalid_json)

    def test_convert_invalid_json_shows_position(self):
        """Test that JSON error shows exact position of error."""
        # JSON with error on line 3
        invalid_json = b'[\n  {"name": "Alice"},\n  {"name": }\n]'
        with pytest.raises(ValueError, match=r"line 3"):
            self.converter.convert(invalid_json)

    def test_convert_single_object(self):
        """Test converting a single JSON object."""
        single_obj = b'{"name": "Alice", "age": 30}'
        result = self.converter.convert(single_obj)

        reader = csv.DictReader(io.StringIO(result.decode("utf-8")))
        rows = list(reader)

        assert len(rows) == 1
        assert rows[0]["name"] == "Alice"

    def test_convert_nested2_single_object_with_arrays(self):
        """Test nested2.json: single object with multiple nested arrays.

        The object has 4 batters and 7 toppings, which should expand to
        4 × 7 = 28 rows via Cartesian product.
        """
        with open("tests/sample_files/nested2.json", "rb") as f:
            content = f.read()

        result = self.converter.convert(content)
        reader = csv.DictReader(io.StringIO(result.decode("utf-8")))
        rows = list(reader)

        # 4 batters × 7 toppings = 28 rows
        assert len(rows) == 28

        # Verify scalar fields are preserved in every row
        for row in rows:
            assert row["id"] == "0001"
            assert row["type"] == "donut"
            assert row["name"] == "Cake"
            assert row["ppu"] == "0.55"

        # Verify nested array fields are expanded
        assert "batters.batter.id" in reader.fieldnames
        assert "batters.batter.type" in reader.fieldnames
        assert "topping.id" in reader.fieldnames
        assert "topping.type" in reader.fieldnames

        # Verify first row has correct batter and topping
        assert rows[0]["batters.batter.id"] == "1001"
        assert rows[0]["batters.batter.type"] == "Regular"
        assert rows[0]["topping.id"] == "5001"
        assert rows[0]["topping.type"] == "None"

    def test_convert_nested3_array_with_nested_arrays(self):
        """Test nested3.json: array of objects each with nested arrays.

        - Object 1: 4 batters × 7 toppings = 28 rows
        - Object 2: 1 batter × 5 toppings = 5 rows
        - Object 3: 2 batters × 4 toppings = 8 rows
        - Total: 41 rows
        """
        with open("tests/sample_files/nested3.json", "rb") as f:
            content = f.read()

        result = self.converter.convert(content)
        reader = csv.DictReader(io.StringIO(result.decode("utf-8")))
        rows = list(reader)

        # Total expected rows: 28 + 5 + 8 = 41
        assert len(rows) == 41

        # Check that all 3 products are represented
        product_ids = set(row["id"] for row in rows)
        assert product_ids == {"0001", "0002", "0003"}

        # Count rows per product
        rows_per_product = {}
        for row in rows:
            pid = row["id"]
            rows_per_product[pid] = rows_per_product.get(pid, 0) + 1

        assert rows_per_product["0001"] == 28  # 4 × 7
        assert rows_per_product["0002"] == 5   # 1 × 5
        assert rows_per_product["0003"] == 8   # 2 × 4

    def test_expansion_limit_exceeded(self):
        """Test that exceeding MAX_EXPANDED_ROWS raises ValueError."""
        # Create JSON with arrays that would produce too many rows
        # Using a structure with many nested arrays
        import json
        from backend.config import MAX_EXPANDED_ROWS

        # Create arrays that will exceed the limit when multiplied
        # e.g., 200 items × 200 items = 40000 rows > 10000 limit
        large_array = [{"id": str(i)} for i in range(200)]
        data = {
            "name": "test",
            "array1": large_array,
            "array2": large_array,
        }

        content = json.dumps(data).encode("utf-8")

        with pytest.raises(ValueError, match=f"limit: {MAX_EXPANDED_ROWS}"):
            self.converter.convert(content)

    def test_preview_nested2_pagination(self):
        """Test pagination works correctly with expanded nested data."""
        with open("tests/sample_files/nested2.json", "rb") as f:
            content = f.read()

        # Get first page
        result = self.converter.preview(content, page=1, page_size=10)

        assert result["total_rows"] == 28
        assert result["total_pages"] == 3  # 28 rows / 10 per page = 3 pages
        assert result["current_page"] == 1
        assert len(result["rows"]) == 10

        # Get last page
        result = self.converter.preview(content, page=3, page_size=10)

        assert result["current_page"] == 3
        assert len(result["rows"]) == 8  # 28 - 20 = 8 remaining rows
