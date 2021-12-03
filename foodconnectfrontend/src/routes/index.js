import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import ConfirmUser from "../containers/ConfirmUser";
import FriendsProfile from "../containers/Friends/index";
import Friends from "../containers/Friends/index";
import Home from "../containers/Home";
import Login from "../containers/Login";
import Profile from "../containers/Profile";
import RestaurantsDetailPage from "../containers/Restaurants/DetailPage";
import Restaurants from "../containers/Restaurants/index";
import Friendstrail from "../containers/Profile/Friendstrail";
import SignUp from "../containers/SignUp";
export default function Routes() {
  return (
    <Router history={history}>
      {/* <Switch> */}
      <Route name="Home" exact path="/" component={Home} />
      <Route name="Login" path="/login" component={Login} />
      <Route name="SignUp" path="/sign-up" component={SignUp} />
      <Route name="Confirm User" path="/confirm-email" component={ConfirmUser} />
      <Route name="Profile" path="/profile" component={Profile} />
      <Route name="Restaurants" path="/restaurants" component={Restaurants} />
      <Route
        name="RestaurantsDetailPage"
        path="/restaurants-detail"
        component={RestaurantsDetailPage}
      />
      <Route
        name="friendsTrail"
        path="/friendsTrail/:uuid"
        component={Friendstrail}
      />

      <Route name="RestaurantsDetailPage" path="/Friends" component={Friends} />
      {/* </Switch> */}
    </Router>
  );
}
