import React from "react";
import { Link } from "react-router-dom";
import "./profilecard.css";
export default function Card({ data }) {
  return (
    <>
      <Link>
        <div className="trail-items">
          <div className="trail-image">
            <img src={data?.image_url} alt="" />
          </div>
          <div className="item-text">
            <h5>{data?.name}</h5>
            <p>
              <i class="fa fa-map-marker" aria-hidden="true"></i>
              {data?.address1} {data?.city}, {data?.state} {data?.zip_code}
            </p>
            <a href="tel:1-408-909-0709" className="tel">
              <i class="fa fa-phone" aria-hidden="true"></i>
              {data?.phone}
            </a>
          </div>
        </div>
      </Link>
    </>
  );
}
