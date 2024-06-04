import React, {useState} from 'react'
import Logo from './Assets/TI_Logo.png'
import './header.css'
import {Link} from 'react-router-dom'


const Header = (props) => 
{
  const [ActiveNav, SetActiveNav] = useState(props.active_state) /* REACT Hook (Using this we will make that section active where the user currently is) */
  /* ActiveNav is updated every time we click on one of the options of the NavBar  */

  return (
    <div className="header">
            <Link to='/repositories'><img src={Logo} alt='Logo' style={{marginLeft:"20px", marginTop:"20px"}}height={"50px"}/></Link>
            <button className='button button3'>Refresh</button>
            <nav> 
              <Link to="/repositories" title="Repositories" onClick={() => SetActiveNav('Repositories')} className={ActiveNav === "Repositories" ? 'active' : ''}>Repositories</Link> 
              <Link to="/users" title="Users" onClick={() => SetActiveNav('Users')} className={ActiveNav === "Users" ? 'active' : ''}>Users</Link>
            </nav>
    </div>)
}

export default Header