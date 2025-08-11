import psycopg2
from pathlib import Path


def export_file(dataset_id: int, output_file: Path):
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(dbname="uudex", user="uudex_user", password="uudex", host="localhost")

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the query to retrieve the BLOB data
    # Replace with your table and column names, and proper WHERE condition
    cursor.execute("SELECT payload FROM dataset WHERE dataset_id = %s", (dataset_id, ))

    # Fetch the BLOB data
    blob_data = cursor.fetchone()[0]

    # Write the binary data to a file
    output_file.write_bytes(blob_data)

    # Close the connection
    cursor.close()
    conn.close()

    print("PDF has been exported successfully to output.pdf")
    return True


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_id", type=int, help="The data to export the payload to.")
    parser.add_argument("output_file", help="The file to write the payload to.")

    opts = parser.parse_args()

    path = Path(opts.output_file)
    path.parent.mkdir(exist_ok=True)

    if export_file(opts.dataset_id, path):
        print("Successful!")
    else:
        print("Failed")
