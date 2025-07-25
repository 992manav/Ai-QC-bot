import React, { useEffect, useState } from "react";
import Papa from "papaparse";
import { DataGrid } from "@mui/x-data-grid";

const CsvViewPage = () => {
  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/download-csv")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch CSV");
        return res.text();
      })
      .then((text) => {
        const parsed = Papa.parse(text, { header: true, skipEmptyLines: true });
        setRows(parsed.data.map((row, i) => ({ id: i, ...row })));
        setColumns(
          parsed.meta.fields.map((field) => ({
            field,
            headerName: field,
            flex: 1,
            sortable: true,
            minWidth: 120,
          }))
        );
      })
      .catch((err) => setError(err.message));
  }, []);

  if (error)
    return <div style={{ color: "red", padding: "1rem" }}>{error}</div>;

  return (
    <div style={styles.wrapper}>
      <h2 style={styles.heading}>📄 CSV Table Viewer</h2>
      <div style={styles.tableContainer}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={25}
          rowsPerPageOptions={[10, 25, 50, 100]}
          disableSelectionOnClick
          sx={{
            border: "none",
            fontFamily: "Segoe UI, sans-serif",
            fontSize: "14px",
          }}
        />
      </div>
    </div>
  );
};

const styles = {
  wrapper: {
    height: "100vh",
    width: "100vw",
    display: "flex",
    flexDirection: "column",
    backgroundColor: "#f9fafb",
    padding: "16px",
    boxSizing: "border-box",
  },
  heading: {
    fontSize: "24px",
    fontWeight: "600",
    marginBottom: "12px",
    paddingLeft: "8px",
  },
  tableContainer: {
    flexGrow: 1,
    backgroundColor: "#fff",
    borderRadius: "8px",
    overflow: "hidden",
  },
};

export default CsvViewPage;
