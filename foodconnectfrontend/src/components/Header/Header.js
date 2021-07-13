import React from 'react'
import FastfoodIcon from "@material-ui/icons/Fastfood";
import { Nav, Navbar, Button, Form, FormControl } from "react-bootstrap";

function Header() {
    return (
      <div>
        <>
          <Navbar bg="primary" variant="dark">
            <Navbar.Brand href="#home">FoodConnect</Navbar.Brand>
            <Nav className="mr-auto">
              <Nav.Link href="#home">Home</Nav.Link>
              <Nav.Link href="#restaurants">Restaurants</Nav.Link>
              <Nav.Link href="#friends">Friends</Nav.Link>
              <Nav.Link href="#profile">Profile</Nav.Link>
            </Nav>
          </Navbar>
        </>
      </div>
    );
}

export default Header
