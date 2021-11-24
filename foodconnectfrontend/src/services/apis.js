
import axios from "./index";

export const login = async (formData) => {

  return axios.post('/auth/login', {}, {
    headers: {
      Authorization: `Basic ${formData}`
    }
  });
};

export const register = async (formData, body) => {
  return axios.post('/auth/signup', body, {
    headers: {
      Authorization: `Basic ${formData}`
    }
  });
};

export const confirmEmail = async (body) => {
  return axios.post('/auth/confirm_signup', body);
};






export const getProfile = async () => {
  return axios.get('/auth/profile');
};


export const getAllBreadcrumbs = async () => {
  return axios.get('/trail/getTrail');
};

export const getFriendsList = async () => {
  let uuid = await localStorage.getItem('userId');
  return axios.get(`/friends/list/?uuid=${uuid}/`);
};



export const getReviews = async (restaurantId) => {
  return axios.get(`/reviews/getReview?restaurant_id=${restaurantId}`);
};

export const getFriendsReviews = async (restaurantId, uuid) => {
  return axios.get(`/trail/getVisitedFriends?restaurant_id=${restaurantId}`);
};


function getAllReviews(id) {
  setloading(true);
  getReviews(id || restaurantDetail?.id).then(response => {
    if (response?.data && response?.data?.success) {
      setreviews(response?.data?.review);
      setloading(false);
    }
  }).catch(err => {
    console.log(err, 'err');
    setloading(false);
  }
  );
}
export const addReview = async (body) => {
  const formData = getFormData(body);
  return axios.post(`/reviews/addReview`, formData);
};



export const addTrail = async (body) => {
  return axios.post(`/trail/addTrail`, body);
};



export const getFriendsByName = async (name) => {
  return axios.get(`/friends/search/?name=${name}`);
};


export const getFriendRequests = async () => {
  return axios.get('/friends/requests/');
};

export const getSentFriendRequests = async () => {
  return axios.get('/friends/requests/sent/');
};



export const sendFriendRequest = async (uuid) => {
  return axios.post('/friends/add/', {
    "to_user": uuid,
    "message": "Hello"
  });
};

export const cancelFriendRequest = async (id) => {
  return axios.get(`/friends/cancel/${id}`);
};

export const acceptFriendRequest = async (id) => {
  return axios.get(`/friends/accept/${id}/`);
};

export const rejectFriendRequest = async (id) => {
  return axios.get(`/friends/reject/${id}/`);
};


export const getRestaurantsList = ({ latitude, longitude }) => {
  return axios.get(`/trail/restaurants?long=${longitude}&lat=${latitude}`);
};


export const getRecommendations = ({ latitude, longitude }) => {
  return axios.get(`/trail/restaurants?long=${longitude}&lat=${latitude}`);
};



function getFormData(body) {
  let formData = new FormData();
  for (let [key, value] of Object.entries(body)) {
    if (key === 'files') {
      for (let file of value) {
        formData.append(key, file);
      }
    } else {
      if (typeof value === 'object' && key !== 'file') {
        formData.append(key, JSON.stringify(value));
      } else {
        formData.append(key, value);
      }
    }
  }
  return formData;
}

