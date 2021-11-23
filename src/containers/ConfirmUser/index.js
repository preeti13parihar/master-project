import React, { useEffect, useState } from "react";
import { useHistory, useLocation } from 'react-router-dom';
import { toast } from "react-toastify";
import Footer from "../../components/footer";
import Header from "../../components/header";
import { confirmEmail } from "../../services/apis";
import './index.css';

const initForm = {
  passcode: null
};


function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

export default function SignUp(props) {

  const [loading, setloading] = useState(false);
  const history = useHistory();
  const [formData, setFormData] = useState(initForm);
  const query = useQuery();

  useEffect(() => {

    console.log(query.get('email'), 'queryParams', props.location);
  }, []);

  function handleInputChange(event) {
    if (!event) return;
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  }


  function handleSignUp(e) {
    e.preventDefault();
    setloading(true);


    const body = {
      "username": query.get('email'),
      "password": formData.passcode,
      "force_alias_creation": false
    };

    confirmEmail(body).then(response => {
      if (response?.data) {
        toast.success('Registered Succeefully');
        setloading(false);
        history.push(`/login`);
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
              <h2>Confirm Email</h2>
            </div>
            <div className="confirm-form">
              <form onSubmit={handleSignUp}>
                <label htmlFor="email">Enter passcode </label>
                <input type="number" id="passcode" name="passcode" required onChange={handleInputChange} />
                <button disabled={loading} className="btn btn-lg btn-primary btn-block btn-homepage" type="submit">
                  Confirm</button>
              </form>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}


