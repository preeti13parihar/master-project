import React, { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";
import Card from "../../components/Cards";
import Footer from "../../components/footer";
import HeaderDashboard from "../../components/header/header";
import { getRestaurantsList } from "../../services/apis";
import "./restaurants.css";

export default function Restaurants() {

  const [restaurantsList, setrestaurantsList] = useState([]);
  const [list, setList] = useState([]);
  const [loading, setloading] = useState(false);

  useEffect(() => {

    getRestaurants();

  }, []);

  function getRestaurants() {
    setloading(true);
    if (navigator?.geolocation) {
      navigator?.geolocation?.getCurrentPosition((pst) => {
        console.log('1111111', pst);
        console.log(pst.coords.latitude,pst.coords.longitude)
        getRestaurantsList(
          // pst?.coords || 

          // { longitude: -73.935242, latitude: 40.730610 }).then(res => {
            { longitude: pst.coords.longitude, latitude: pst.coords.latitude }).then(res => {
            setrestaurantsList(res?.data?.restaurants?.businesses || []);
            setList(res?.data?.restaurants?.businesses || []);
            setloading(false);
          }).catch(err => {
            setloading(false);
          });
      });
    }
  }

  function handleFilter(event) {
    let string = event?.target?.value;
    if (string === '') {
      setList(restaurantsList);
      return;
    }
    let filteredData = restaurantsList?.filter(rst => rst.name?.includes(string));
    setList(filteredData);
  }

  return (
    <>
      <HeaderDashboard handleFilter={handleFilter} />
      <div className="restaurants">
        <div className="container">
          <h2>Restaurants</h2>
          <div className="restaurants-bottom">
            <h3>( {list?.length} Results Found )</h3>
            {
              loading ?
                <Spinner animation="grow" />
                :
                <div className="cards">
                  {list?.map(restaurant => <Card restaurant={restaurant} />)}
                </div>
            }
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}
