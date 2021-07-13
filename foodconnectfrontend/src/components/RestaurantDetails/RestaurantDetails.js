import React from 'react'
import { Image } from 'react-bootstrap'
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import { useState , useEffect } from "react";
import axios from "axios";
import { Restaurant } from '@material-ui/icons';
import Restaurants from "../Restaurants/Restaurants";

function RestaurantDetails() {
  const [restaurantDetails, getRestaurantDetails] = useState({});

  const getRestaurant = async () => {
      const response = await axios.get("http://localhost:8000/restaurantDetails");
      // console.log(response.status);
      console.log(response.data);
      getRestaurantDetails(response.data);
      console.log(restaurantDetails);
    };
  
    useEffect(() => {
      getRestaurant();
    }, {});
  
    return (
      <div>
        <Image
          src="https://b.zmtcdn.com/data/pictures/6/16840926/ea76fb5d3edf4934bc7cd5f54b669c46_featured_v2.jpg?fit=around|771.75:416.25&crop=771.75:416.25;*,*"
          fluid
        />
        
        <h2> {restaurantDetails.name} </h2>
        <section>
            <a>{restaurantDetails.rating}</a>
            <a>{restaurantDetails.price}</a>
            <a>{restaurantDetails.phone}</a>
        </section>
        

        <Tabs
          defaultActiveKey="profile"
          id="uncontrolled-tab-example"
          className="mb-3"
        >
          <Tab eventKey="home" title="Your Review">
            <Restaurants />
          </Tab>
          <Tab eventKey="profile" title="Friend Review"></Tab>
        </Tabs>
      </div>
    );
}

export default RestaurantDetails
