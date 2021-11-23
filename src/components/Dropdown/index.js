import React, { useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import './dropdown.css';

const Dropdown = () => {

  const [isOpen, setOpen] = useState(false);
  const toggleDropdown = () => setOpen(!isOpen);
  const history = useHistory();

  function logout() {
    localStorage.removeItem('AccessToken');
    localStorage.removeItem('AccessToken');
    history.push('/');
  }

  return (
    <div className='dropdown'>
      <div className='dropdown-header' onClick={toggleDropdown}>
        <div>
          <i className="fa fa-user" aria-hidden="true"></i>
        </div>
        <i className={`fa fa-chevron-right icon ${isOpen && "open"}`}></i>
      </div>
      <div className={`dropdown-body ${isOpen && 'open'}`}>
        <ul className='d-flex flex-column ml-0'>
          <li>
            <Link to='/profile'>My Profile</Link>
          </li>
          <li>
            <Link to='/Friends'>My Friends</Link>
          </li>
          <li onClick={logout}>
            Logout
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Dropdown;