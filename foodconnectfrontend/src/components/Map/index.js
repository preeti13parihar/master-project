import GoogleMapReact from 'google-map-react';
import React, { useEffect, useState } from 'react';
import './map.css';

const Map = () => {

  const [currentLocation, setcurrentLocation] = useState({});

  const location = {
    address: '1600 Amphitheatre Parkway, Mountain View, california.',
    lat: 37.42216,
    lng: -122.08427,
  };

  useEffect(() => {
    if (window?.navigator && window?.navigator?.geolocation) {
      window?.navigator?.geolocation?.getCurrentPosition(pos => {
        const coords = pos.coords;
        setcurrentLocation({
          lat: coords.latitude,
          lng: coords.longitude
        });
      });
    }
  }, []);

  return <div className="map">
    <div className="google-map">
      <GoogleMapReact
        bootstrapURLKeys={{ key: 'AIzaSyAFq0L2qq9LDiM0b143FckAU13kND3qW4U' }}
        defaultCenter={currentLocation}
        center={currentLocation}
        defaultZoom={15}
      >
        {
          currentLocation.lat && <LocationPin
            lat={currentLocation.lat}
            lng={currentLocation.lng}
            text={currentLocation.address}
          />
        }

      </GoogleMapReact>
    </div>
  </div>;
};

const LocationPin = ({ text }) => (
  <div className="pin">
    {/* <Icon icon={locationIcon} className="pin-icon" /> */}
    <span className="fa fa-map-marker" style={{ fontSize: 40, color: 'red' }} ></span>
  </div>
);

export default Map;