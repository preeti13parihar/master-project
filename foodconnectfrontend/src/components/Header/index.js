import React from "react";
import { Link } from "react-router-dom";
import Logo from '../../images/logo.png'
import './header.css'

export default function Header() {
  return (
    <>
    <header>
        <div className="logo">
          <Link to="/">
            <img src={Logo}></img>
          </Link>
        </div>
        <ul>
          <li><Link to="/sign-up">Sign Up</Link></li>
          <li><Link to="/login">Login</Link></li>
        </ul>
    </header>
  </>
  );
}
