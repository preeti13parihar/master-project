import { Buffer } from 'buffer';
import React, { useState } from "react";
import { Link, useHistory } from 'react-router-dom';
import { toast } from "react-toastify";
import Footer from "../../components/footer";
import Header from "../../components/header";
import { register } from "../../services/apis";
import './signup.css';

const initForm = {
  "rating": 0,
  "review": "",
  "recommended_dishes": "",
  files: []
};

export default function SignUp() {

  const [loading, setloading] = useState(false);
  const history = useHistory();
  const [formData, setFormData] = useState(initForm);

  function handleInputChange(event) {
    if (!event) return;
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  }


  function handleSignUp(e) {
    e.preventDefault();
    setloading(true);

    const encodedString = Buffer.from(`${formData.email}:${formData.password}`).toString('base64');

    const body =
    {
      "user_attributes": [{
        "Name": "given_name",
        "Value": formData.firstname
      }, {
        "Name": "family_name",
        "Value": formData.lastname
      }]
    };

    register(encodedString, body).then(response => {
      console.log(response, 'success response');
      if (response?.data) {
        setloading(false);
        toast.success('Passcode Sent to Your Email');
        history.push(`/confirm-email?email=${formData.email}`);

      }
    }).catch(err => {
      console.log('err,', err.response?.data?.error);
      setloading(false);
      toast.error(err.response?.data?.error || 'Internal Server Error');

    });
  }

  return (
    <>
      <Header />
      <main>
        <section className="login sign-up">
          <div className="container">
            <div className="login-head">
              <h2>Sign up</h2>
            </div>
            <div className="login-form">
              <form onSubmit={handleSignUp}>
                <label htmlFor="email">Email address</label>
                <input type="email" id="email" name="email" placeholder="example@gmail.com" required onChange={handleInputChange} />
                <label htmlFor="password">Password</label>
                <input type="password" id="password" name="password" placeholder="**********" required="" onChange={handleInputChange} />
                <label htmlFor="firstname">First Name</label>
                <input type="text" id="firstname" name="firstname" placeholder="First Name" required="" onChange={handleInputChange} />
                <label htmlFor="lastname">Last Name</label>
                <input type="text" id="lastname" name="lastname" placeholder="Last Name" required="" onChange={handleInputChange} />
                <button disabled={loading} className="btn btn-lg btn-primary btn-block btn-homepage" type="submit"><span className="fa fa-user-plus" aria-hidden="true"></span> Signup</button>
              </form>
              <p>Already have an account? <Link to="/login">Login here</Link></p>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
