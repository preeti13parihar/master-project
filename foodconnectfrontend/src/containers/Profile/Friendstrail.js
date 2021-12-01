import React, { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";
import { useParams } from "react-router";
import Card from "../../components/Cards";
import Footer from "../../components/footer";
import HeaderDashboard from "../../components/header/header";
import MapComponent from "../../components/Map/index2";
import ProfileCards from "../../components/ProfileCards/index";
import Image from "../../images/default-profile.png";
import { getFriendsProfile,getAllBreadcrumbs, getProfile, getRecommendations, updateProfilePic } from "../../services/apis";
import "./profile.css";

export default function Profile(props) {

console.log(props)
  const [loading, setloading] = useState(false);
  const [profileData, setprofileData] = useState(null);
  const [trailCount, settrailCount] = useState(0);
  const [friendCount, setfriendCount] = useState(0);
  const [trails, settrails] = useState([]);
  const [recommendations, setrecommendations] = useState([]);
  const {uuid}=useParams()
   const [image_url, setimage] = useState(null);


  useEffect(async () => {
    getSetAllBreadcrumbs();
    // setloading(true);
    const image=await localStorage.getItem("image_url")
    setimage(image)
    // getPrf();
    // Get Recommendations
    // setloading(true);
    if (navigator?.geolocation) {
      navigator?.geolocation?.getCurrentPosition((pst) => {
        getRecommendations(
          pst?.coords || 
          { longitude: -73.935242, latitude: 40.730610 }).then(response => {
            if (response?.data) {
              let dataList = response.data?.restaurants?.businesses;
              // if (dataList.length > 5) {
              //   dataList.length = 5;
              // }
              setrecommendations(dataList);
            }
          }).catch(err => {
            console.log(err, 'err');
          });
      });
    }

  }, []);


  function getPrf(params) {
    getProfile().then(response => {
      if (response?.data) {
        setloading(false);
        setprofileData(response.data);
        localStorage.setItem('userId', response.data?.uuid);
      }
    }).catch(err => {
      console.log(err, 'err');
      setloading(false);
    });
  }



  function getSetAllBreadcrumbs() {
    console.log(uuid,"uuid")
    getFriendsProfile(uuid).then(response => {
      if (response?.data) {
        settrailCount(response?.data?.trailCount);
        setfriendCount(response?.data?.friendCount);
        settrails(response?.data?.trails);
      }
    }).catch(err => {
      console.log(err, 'err');
    }
    );
  }

 
  function uploadImage(event) {
    
    console.log(event, 'event', event.target.files);
    let data = new FormData();
    data.append('file', event.target.files[0]);

    updateProfilePic(data).then(response => {
      if (response?.data) {
        getPrf();
      }
    }).catch(err => {
      console.log(err, 'err');
    });
  }


  return (
    <>
      <HeaderDashboard />
      <div className="profile-header">
        <div className="container">
          <div className="profile-header-inner">
            {
              loading ?
                <Spinner animation="grow" />
                :
                <div className="left">
                  <div>
                    <div className="profile-image">
                      <img src= {image_url || Image }  alt="none" 
                  />
                    </div>
                  </div>


                  <div className="profile-details">
                    <h2>{profileData?.first_name} {profileData?.last_name}</h2>
                    <p>
                       FRIEND'S PROFILE
                </p>
                    <div className="profile-stats">
                      <div className="profile-breadcrumbs">
                        <h3>Trails</h3>
                        <span>{trailCount}</span>
                      </div>
                      <div>
                        <h3>Friends</h3>
                        <span>{friendCount}</span>
                      </div>
                    </div>
                  </div>
                </div>
            }
          </div>
        </div>
      </div>
      <div className="profile-bottom">
        <div className="container">
          <div className="map-wrap">
            <div className="mapouter">
              <div id="dvMap">

              </div>
              <MapComponent
                trails={trails}
              />
            </div>
          </div>
          <div className="trail">
            <h4>Friends Trail</h4>
            <div className="trail-list">
              {
                trails?.map(trail => <ProfileCards data={trail} />)
              }
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </>
  );
}