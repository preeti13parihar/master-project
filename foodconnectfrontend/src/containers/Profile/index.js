import React, { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";
import Card from "../../components/Cards";
import Footer from "../../components/footer";
import HeaderDashboard from "../../components/header/header";
import MapComponent from "../../components/Map/index2";
import ProfileCards from "../../components/ProfileCards/index";
import Image from "../../images/default-profile.png";
import { getAllBreadcrumbs, getProfile, getRecommendations } from "../../services/apis";
import "./profile.css";

export default function Profile() {

  const [loading, setloading] = useState(false);
  const [profileData, setprofileData] = useState(null);
  const [trailCount, settrailCount] = useState(0);
  const [friendCount, setfriendCount] = useState(0);
  const [trails, settrails] = useState([]);
  const [recommendations, setrecommendations] = useState([]);

  useEffect(() => {
    getSetAllBreadcrumbs();
    setloading(true);
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


    // Get Recommendations
    setloading(true);
    if (navigator?.geolocation) {
      navigator?.geolocation?.getCurrentPosition((pst) => {
        getRecommendations(
          // pst?.coords || 
          { longitude: -73.935242, latitude: 40.730610 }).then(response => {
            if (response?.data) {
              let dataList = response.data?.restaurants?.businesses;
              if (dataList.length > 5) {
                dataList.length = 5;
              }
              setrecommendations(dataList);
            }
          }).catch(err => {
            console.log(err, 'err');
          });
      });
    }

  }, []);



  function getSetAllBreadcrumbs() {
    getAllBreadcrumbs().then(response => {
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
                  <div className="profile-image">
                    <img src={Image} alt="none" />
                  </div>
                  <div className="profile-details">
                    <h2>{profileData?.first_name} {profileData?.last_name}</h2>
                    <p>
                      <i class="fa fa-map-marker" aria-hidden="true"></i>Santa
                  Clara, CA 95054
                </p>
                    <div className="profile-stats">
                      <div className="profile-breadcrumbs">
                        <h3>Breadcrumbs</h3>
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
            <h4>Recent Trail</h4>
            <div className="trail-list">
              {
                trails?.map(trail => <ProfileCards data={trail} />)
              }
            </div>
          </div>
        </div>
      </div>
      <div className="restaurants">
        <div className="container">
          <h2>Top 5 Restaurants</h2>
          <div className="restaurants-bottom">
            <div className="cards">
              {recommendations?.map(restaurant => <Card restaurant={restaurant} />)}
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}