import React from "react";
import { Routes, Route } from "react-router-dom";
import VersionHistoryPage from "./pages/VersionHistoryPage";
import MainPage from "./pages/MainPage";
import CsvViewPage from "./pages/CsvViewPage";
import "./App.css";
import "./styles/VersionHistory.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainPage />} />
      <Route
        path="/version-history/:questionId"
        element={<VersionHistoryPage />}
      />
      <Route path="/csv-view" element={<CsvViewPage />} />
    </Routes>
  );
}
export default App;
