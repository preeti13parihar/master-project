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
          <h5>{friend?.first_name}{" "}{friend?.last_name} </h5>
        </div>
      </div>
    </>
  );
}
