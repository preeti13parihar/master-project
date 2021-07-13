import './App.css';
import Login from './components/Login/Login';
import Restaurants from './components/Restaurants/Restaurants';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Register from './components/Register/Register';
import { useState } from "react";
import Header from "./components/Header/Header";
import RestaurantDetails from './components/RestaurantDetails/RestaurantDetails';

function App() {
  const [errorMessage, updateErrorMessage] = useState(null);

  return (
    <div className="App">
      <Router>
        <Route exact path="/" exact={true}>
          <Login showError={updateErrorMessage} />
        </Route>
        <Route exact path="/register">
          <Register showError={updateErrorMessage} />
        </Route>
        <Route exact path="/restaurants">
          <Header />
          <Restaurants showError={updateErrorMessage} />
        </Route>
        <Route exact path="/restaurantsDetails">
          <RestaurantDetails />
        </Route>
      </Router>
    </div>
  );
}

export default App;
