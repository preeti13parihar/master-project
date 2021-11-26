import { GoogleMap, Marker, useJsApiLoader } from '@react-google-maps/api';
import React, { useEffect, useState } from 'react';

const containerStyle = {
  width: '700px',
  height: '550px'
};


function MyComponent({ trails = [{
  latitude: 31.46361,
  longitude: 75.2555209,
  visit_id: 890
}, {
  latitude: 32.48361,
  longitude: 73.2555209,
  visit_id: 892
}] }) {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: "AIzaSyAFq0L2qq9LDiM0b143FckAU13kND3qW4U"
  });

  const [currentLocation, setcurrentLocation] = useState({});
  const [map, setMap] = React.useState(null);

  const onLoad = React.useCallback(function callback(map) {
    const bounds = new window.google.maps.LatLngBounds();
    map.fitBounds(bounds);
    setMap(map);
  }, []);

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

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null);
  }, []);

  console.log(currentLocation, 'hjkl');


  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={currentLocation}
      zoom={15}
      onLoad={onLoad}
      onUnmount={onUnmount}
    >
      <Marker
        key={89}
        position={currentLocation}
      />

      {
        trails?.map(item => <Marker
          key={item.visit_id}
          position={{ lat: parseFloat(item.latitude), lng: parseFloat(item.longitude) }}
          icon={{ url: "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png" }}
        />)
      }
      <></>
    </GoogleMap>
  ) : <></>;
}

export default React.memo(MyComponent);