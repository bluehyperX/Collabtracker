import React, { useState } from 'react';
import { Routes, BrowserRouter as Router, Route } from 'react-router-dom';
import Repositories from './Components/Repositories.jsx';
import Users from './Components/Users.jsx';
import Header from './header/header.jsx';

const App = () => {
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

  return (
    <Router>
      <Header selectedYear={selectedYear} setSelectedYear={setSelectedYear} />
      <Routes>
        <Route exact path="/" element={<Repositories selectedYear={selectedYear} />} />
        <Route exact path="/repositories" element={<Repositories selectedYear={selectedYear} />} />
        <Route exact path="/users" element={<Users />} />
      </Routes>
    </Router>
  );
};

export default App;
