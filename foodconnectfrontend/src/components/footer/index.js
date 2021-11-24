

import React from "react";
import { Link } from "react-router-dom";
import './footer.css';

export default function Footer() {
  return (
    <>
      <footer>
        <div className="container">
          <p><Link to='/'>Breadcrumbs</Link> &copy; 2016</p>
        </div>
      </footer>
    </>
  );
}
