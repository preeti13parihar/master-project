import { Buffer } from 'buffer';
import React, { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import { toast } from 'react-toastify';
import Footer from "../../components/footer";
import Header from "../../components/header";
import { login } from "../../services/apis";
import "./login.css";


export default function Login() {

  const [formData, setFormData] = useState({});
  const [loading, setloading] = useState(false);
  const history = useHistory();

  function handleInputChange(event) {
    if (!event) return;
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  }

  function handleSubmit(e) {
    e.preventDefault();
    setloading(true);

    const encodedString = Buffer.from(`${formData.email}:${formData.password}`).toString('base64');
    login(encodedString).then(response => {
      console.log(response, 'success response');
      if (response?.headers?.http_accesstoken) {
        const { http_accesstoken, http_refreshtoken } = response.headers;
        localStorage.setItem('AccessToken', http_accesstoken);
        localStorage.setItem('RefreshToken', http_refreshtoken);
      }
      setloading(false);
      history.push('/Profile');
    }).catch(err => {
      console.log('err,', err);
      setloading(false);
      toast.error('Incorrect username or password.');

    });
  }

  return (
    <>
      <Header />

      <main>
        <section className="login login-height">
          <div className="container">
            <div className="login-head">
              <h2>Login</h2>
            </div>
            <div className="login-form">
              <form onSubmit={handleSubmit}>
                <label for="email">Email address</label>
                <input
                  type="email"
                  id="email"
                  className="form-control"
                  name="email"
                  placeholder="example@gmail.com"
                  required
                  onChange={handleInputChange}
                  value={formData?.email}
                />
                <label for="password">Password</label>
                <input
                  type="password"
                  id="password"
                  className="form-control"
                  name="password"
                  placeholder="**********"
                  required
                  onChange={handleInputChange}
                  value={formData?.password}
                />
                <button
                  class="btn btn-lg btn-primary btn-block btn-homepage"
                  type="submit"
                  disabled={loading}
                >
                  <span class="fa fa-sign-in" aria-hidden="true"></span> Login
                </button>
              </form>
              <p>
                Don't have account? <Link to="/sign-up">Sign up here</Link>
              </p>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
