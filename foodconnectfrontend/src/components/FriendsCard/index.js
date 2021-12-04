import React from "react";
import Image from "../../images/default-profile.png";
import "./friendcard.css";
import { Link, useHistory } from 'react-router-dom';


export default function FriendsCard({ friend }) {

  // const [uuis, setuuid] = useState("");

const history = useHistory()
  async function handleClick() {
    await localStorage.setItem("image_url",friend.image_url || friend?.image || Image)
    history.push(`/friendsTrail/${friend?.to_user}`);
  }

  return (
    <>
     
       {/* <Link to={`/friendsTrail/${friend?.to_user}/${friend?.image || friend?.image_url }`}> */}
      <div onClick={handleClick}className="friend-list">


        <div className="friend-image">
       
          <img  src={friend?.image_url || friend?.image || Image} alt="" />
            
        </div>
         
        <div className="friend-text">
          <h5 o >{friend?.first_name}{" "}{friend?.last_name} </h5>
        </div>
           
      </div>
  {/* </Link> */}
     
    </>
  );
}
