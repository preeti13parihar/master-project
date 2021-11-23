import React from "react";
import { Link } from "react-router-dom";
import Logo from "../../images/logo.png";
import Dropdown from "../Dropdown/index";
import "./header.css";

export default function HeaderDashboard({ handleFilter }) {
  return (
    <>

      <header className="header-dashboard">
        <div className="logo">
          <Link to="/">
            <img src={Logo}></img>
          </Link>
        </div>
        <div className="nav">
          <ul>
            <li>
              <Link to="/Profile">Profile</Link>
            </li>
            <li>
              <Link to="/Friends">Freinds</Link>
            </li>
            <li>
              <Link to="/restaurants">Restaurnts</Link>
            </li>

            {
              handleFilter &&
              <li className="search"><input
                type="text"
                placeholder="Find restaurants by name or address"
                required=""
                autoFocus=""
                onChange={handleFilter}
              />
                <button>
                  <i class="fa fa-search" aria-hidden="true"></i>
                </button>
              </li>
            }

          </ul>
          <Dropdown />
        </div>
      </header>
    </>
  );
}
