import React from "react";
import { Link } from "react-router-dom";
import Footer from '../../components/footer/index';
import Header from "../../components/header/index";
import Image from '../../images/FoodConnect2.jpeg';
import './home.css';

export default function Home() {
  return (
    <>
      <Header />
      <main className="home">
        <section className="banner" style={{ backgroundImage: 'url(' + Image + ')' }}>
          <div className="container">
            <h1>FoodConnect</h1>
            <p>The ultimate social media network for foodies.
            Remember where you've been and what you've eaten!
          </p>
            <div className="buttons">
              <Link className="sign-up" to="/sign-up">Sign Up</Link>
              <Link className="login-button" to="/login">Login</Link>
            </div>
          </div>
        </section>
        <section className="features">
          <div className="container">
            <h2>Features</h2>
            <div className="Feature-boxes">
              <div className="box">
                <span class="fa-stack fa-3x features-icon">
                  <i class="fa fa-circle fa-stack-2x"></i>
                  <i class="fa fa-plus fa-stack-1x fa-inverse"></i>
                </span>
                <h3>Track Restaurnts</h3>
                <p>Add a restaurant visit, leaving a trail of breadcrumbs for your restaurant history.</p>
              </div>
              <div className="box">
                <span class="fa-stack fa-3x features-icon">
                  <i class="fa fa-circle fa-stack-2x"></i>
                  <i class="fa fa-camera fa-stack-1x fa-inverse"></i>
                </span>
                <h3>Upload Food Photos</h3>
                <p>Upload your food pictures for each restaurant visit and leave comments, to remember what tasted good.</p>
              </div>
              <div className="box">
                <span class="fa-stack fa-3x features-icon">
                  <i class="fa fa-circle fa-stack-2x"></i>
                  <i class="fa fa-users fa-stack-1x fa-inverse"></i>
                </span>
                <h3>Connect With Friends</h3>
                <p>Connect with your friends to see what restaurants they visited and what they ate.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
