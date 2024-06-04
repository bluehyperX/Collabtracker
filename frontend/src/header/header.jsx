import React from 'react';
import Logo from './Assets/TI_Logo.png';
import './header.css';
import { Link } from 'react-router-dom';

const Header = ({ selectedYear, setSelectedYear }) => {
  const years = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i);

  return (
    <div className="header">
      <Link to='/repositories'>
        <img src={Logo} alt='Logo' style={{ marginLeft: "20px", marginTop: "20px" }} height={"50px"} />
      </Link>
      <select className='button button3' value={selectedYear} onChange={e => setSelectedYear(e.target.value)}>
        {years.map((year) => (
          <option key={year} value={year}>
            {year}
          </option>
        ))}
      </select>
      <nav>
        <Link to="/repositories" title="Repositories">Repositories</Link>
        <Link to="/users" title="Users">Users</Link>
      </nav>
    </div>
  );
};

export default Header;
