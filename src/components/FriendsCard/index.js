import React from "react";
import Image from "../../images/default-profile.png";
import "./friendcard.css";
export default function FriendsCard({ friend }) {
  return (
    <>
      <div className="friend-list">
        <div className="friend-image">
          <img src={Image} alt="" />
        </div>
        <div className="friend-text">
          <h5>{friend?.first_name}</h5>
          <p>
            <i class="fa fa-map-marker" aria-hidden="true"></i>
            {friend?.address1} {friend?.city}, {friend?.state} {friend?.zip_code}
          </p>
          <a href="tel:1-408-909-0709" className="tel">
            <i class="fa fa-phone" aria-hidden="true"></i>
            {friend?.phone}
          </a>
        </div>
      </div>
    </>
  );
}
