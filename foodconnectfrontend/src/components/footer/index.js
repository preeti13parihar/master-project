

import React from "react";
import { Link } from "react-router-dom";
import './footer.css';

export default function Footer() {
  return (
    <>
      <footer>
        <div className="container">
          <p><Link to='/'>FoodConnect</Link> &copy; 2021</p>
        </div>
      </footer>
    </>
  );
}
