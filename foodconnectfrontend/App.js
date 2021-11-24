import React from "react";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Routes from "./src/routes";
const App = () => {
  return (
    <>
      <Routes />
      <ToastContainer />
    </>
  );
};
export default App;
