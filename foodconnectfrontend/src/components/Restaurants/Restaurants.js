import React from "react";
import "./../../index.css";
import { useEffect , useState } from "react";
import axios from "axios";
import { Card, Button } from "react-bootstrap";

function Restaurants() {
  const [restaurantList, setRestaurantList] = useState([]);

  const loadRestaurants = async () => {
    const response = await axios.get("http://localhost:8000/restaurants");
    // console.log(response.status);
      console.log(response.data);
      setRestaurantList(response.data.businesses);
      console.log(restaurantList);
  };

  useEffect(() => {
    loadRestaurants();
  }, []);
  
  const renderCard = (card, index) => {
    return (
      <Card style={{ width: "18rem" }} key={index} className="box">
        <Card.Img variant="top" src={card.image_url} />
        <Card.Body>
          <Card.Title>{card.name}</Card.Title>
          <Card.Text>
            {card.location.address1},{card.location.city}, {card.location.state}{" "}
            {card.location.zip == "" ? "," : null} {card.location.zip}
          </Card.Text>
          <Card.Text>
            <div>
              <div>
                <span class="icon-star _537e4"></span>
                <span>4.5</span>
              </div>
              <div>•</div>
              <div>28 MINS</div>
              <div>•</div>
              <div class="nVWSi">₹450 FOR TWO</div>
            </div>
          </Card.Text>
          <Card.Text>{card.phone}</Card.Text>
        </Card.Body>
      </Card>
    );
  }
  return (
    <div className="grid">{restaurantList.map((renderCard))}
    </div>
  );
}

export default Restaurants;
