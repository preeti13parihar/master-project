import React, { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";
import Footer from "../../components/footer";
import HeaderDashboard from "../../components/header/header";
import ProfileCards from "../../components/ProfileCards/index";
import Image from "../../images/default-profile.png";
import { getAllBreadcrumbs, getProfile } from "../../services/apis";
import "./profile.css";

export default function Profile() {

  const [loading, setloading] = useState(false);
  const [profileData, setprofileData] = useState(null);
  const [trailCount, settrailCount] = useState(0);
  const [friendCount, setfriendCount] = useState(0);
  const [trails, settrails] = useState([]);

  useEffect(() => {
    showMap();
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
    }
    );
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


  function showMap() {
    if (window?.navigator?.geolocation) {
      window?.navigator?.geolocation.getCurrentPosition(function (p) {
        var LatLng = new google.maps.LatLng(p.coords.latitude, p.coords.longitude);
        var mapOptions = {
          center: LatLng,
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("dvMap"), mapOptions);
        var marker = new google.maps.Marker({
          position: LatLng,
          map: map,
          title: "<div style = 'height:60px;width:200px'><b>Your location:</b><br />Latitude: " + p.coords.latitude + "<br />Longitude: " + p.coords.longitude
        });
        google.maps.event.addListener(marker, "click", function (e) {
          var infoWindow = new google.maps.InfoWindow();
          infoWindow.setContent(marker.title);
          infoWindow.open(map, marker);
        });
      });
    } else {
      alert('Geo Location feature is not supported in this browser.');
    }
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
              {/* <div className="gmap_canvas">
                <iframe
                  id="gmap_canvas"
                  src="https://maps.google.com/maps?q=university%20of%20san%20francisco&t=&z=13&ie=UTF8&iwloc=&output=embed"
                  frameborder="0"
                  scrolling="no"
                  marginheight="0"
                  marginwidth="0"
                ></iframe>
              </div> */}
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
      <Footer />
    </>
  );
}
