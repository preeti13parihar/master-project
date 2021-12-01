import React from "react";
import { useHistory } from "react-router-dom";
import "./cards.css";
export default function Card({ restaurant }) {

  const history = useHistory();

  async function handleClick() {
    console.log(restaurant,"restau")
    await localStorage.setItem('restaurant', JSON.stringify(restaurant));
    history.push(`/restaurants-detail`);
  }

  const { image_url, name, id, review_count, rating, location, display_phone } = restaurant || {};
  return (
    <>
      <div className="card">
    
        {/* <Link className="image" to={`/restaurants-detail`}> */}
        <div className="image">
          <img onClick={handleClick} src={image_url} alt="restaurant-image" />
        </div>
        {/* </Link> */}
        {/* <Link to={`/restaurants-detail/${id}`}> */}
        <h3 onClick={handleClick}>{name}</h3>
        {/* </Link> */}
        <p>
          <span className="rate">
            {rating}<i className="fa fa-star" ariaHidden="true"></i>
          </span>
          Rated
        </p>
        <p>
          <i className="fa fa-map-marker" ariaHidden="true"></i>
          {location?.address1} {location?.city}, {location?.state} {location?.zip_code}
        </p>
        <a href="tel:1-408-909-0709" className="tel">
          <i className="fa fa-phone" ariaHidden="true"></i>
          {display_phone}
        </a>
      </div>
    </>
  );
}
