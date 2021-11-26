import "bootstrap/dist/css/bootstrap.min.css";
import React, { useEffect, useState } from "react";
import { Button, Modal, Spinner, Tab, Tabs } from "react-bootstrap";
import { toast } from "react-toastify";
import Footer from "../../components/footer";
import HeaderDashboard from "../../components/header/header";
import ImageUpload from "../../components/ImageUploader/index";
import StarRating from "../../components/Stars/index";
import ProfileImage from "../../images/default-profile.png";
import { addReview, addTrail, getFriendsReviews, getReviews } from "../../services/apis";
import "./restaurants.css";


function MyVerticallyCenteredModal(props) {
  console.log(props, 'props props props', props.restaurantId);

  const initForm = {
    "rating": 0,
    "review": "",
    "recommended_dishes": "",
    files: []
  };

  const [formData, setformData] = useState(initForm);
  const [loading, setloading] = useState(false);

  function handleInputChange(event) {
    const { value, name } = event.target;
    formData[name] = value;
    setformData({ ...formData });
  }

  function postReview() {
    setloading(true);
    addReview({ ...formData, restaurant_id: props.restaurantId }).then(response => {
      if (response?.data) {
        toast.success("Review Added Successfully");
        props.onHide();
        props?.successCallback();
        setformData(initForm);
        setloading(false);
      }
    }).catch(err => {
      toast.error('Internal Server Error');
      console.log(err, 'err');
    }
    );


  }

  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton></Modal.Header>
      <Modal.Body>
        <form
          className="d-flex flex-column review-form"
        >
          <label for="email">Review</label>
          <textarea placeholder="Whats Your Review ..." required="" name="review" onChange={handleInputChange} />
          <label>Ratings</label>
          <StarRating onChange={(value) => handleInputChange({ target: { value, name: 'rating' } })} />
          <ImageUpload onChange={(value) => handleInputChange({ target: { value, name: 'files' } })} />
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button className="btn-add" onClick={postReview} disabled={loading}>
          <i className="fa fa-star-o mr-2" aria-hidden="true"></i>Add Review
        </Button>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  );
}
export default function RestaurantsDetailPage() {
  const [modalShow, setModalShow] = useState(false);
  const [restaurantDetail, setRestaurantDetail] = useState(null);
  const [reviews, setreviews] = useState([]);
  const [images, setimages] = useState([]);
  const [loading, setloading] = useState(false);
  const [friendsReviews, setfriendsReviews] = useState([]);
  const [hasUserVisited, setHaseUserVisted] = useState(true);
  const [userName, setuserName] = useState('');


  useEffect(async () => {
    const restaurant = await localStorage.getItem('restaurant');
    const userId = await localStorage.getItem('userId');
    console.log(restaurant, 'restaurant restaurant');

    if (restaurant) {
      const rst = JSON.parse(restaurant);

      getAllReviews(rst?.id);
      getFriendReviews(rst?.id, userId);
      setRestaurantDetail(rst);
    }

  }, []);

  function getAllReviews(id) {
    setloading(true);
    getReviews(id || restaurantDetail?.id).then(response => {
      if (response?.data && response?.data?.success) {
        setreviews(response?.data?.review);
        setuserName(response?.data?.userName);
        setimages(response?.data?.images);
        setloading(false);
      }
    }).catch(err => {
      console.log(err, 'err');
      setloading(false);
    }
    );
  }


  function getFriendReviews(id) {
    getFriendsReviews(id || restaurantDetail?.id).then(response => {
      if (response?.data && response?.data?.success) {
        setfriendsReviews(response?.data?.visitedFriends);
        setHaseUserVisted(response?.data?.hasUserVisited);
      }
    }).catch(err => {
      console.log(err, 'err');
      setloading(false);
    }
    );
  }


  const getRating = (number) => {
    const array = Array.from(Array(number).keys());
    return array.map(item => <i class="fa fa-star" aria-hidden="true"></i>);

  };


  const handleAddTrail = () => {
    const { coordinates, location, id, image_url, name, phone, price } = restaurantDetail;

    let formdata = { ...coordinates, ...location, restaurant_id: id, image_url, name, phone, price };

    addTrail(formdata).then(response => {
      if (response?.data) {
        toast.success("Trail Added Successfully");
        setHaseUserVisted(true);
      }
    }).catch(err => {
      console.log(err, 'err');
      setloading(false);
    }
    );
  };


  return (
    <>
      <HeaderDashboard />
      <div className="restaurants-detail">
        <div className="container">
          <div className="detail-image">
            <img src={restaurantDetail?.image_url} alt="" />
          </div>
          <div className="detail-bottom">
            <h3>{restaurantDetail?.name}</h3>
            <p>
              <i class="fa fa-map-marker" aria-hidden="true"></i>
              {restaurantDetail?.location?.address1} {restaurantDetail?.location?.city}, {restaurantDetail?.location?.state} {restaurantDetail?.location?.zip_code}
            </p>
            <a href="tel:1-408-909-0709" className="tel">
              <i class="fa fa-phone" aria-hidden="true"></i>
              {restaurantDetail?.display_phone}
            </a>
            <div className="buttons">
              <button className="review" onClick={() => setModalShow(true)}>
                <i class="fa fa-star-o" aria-hidden="true"></i>
                Add Review
              </button>
              <MyVerticallyCenteredModal
                show={modalShow}
                onHide={() => setModalShow(false)}
                restaurantId={restaurantDetail?.id}
                successCallback={getAllReviews}
              />
              {
                !hasUserVisited && <button onClick={handleAddTrail}>
                  <i class="sc-rbbb40-1 iFnyeo" size="16" color="#F57082">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="#F57082"
                      width="16"
                      height="16"
                      viewBox="0 0 20 20"
                      aria-labelledby="icon-svg-title- icon-svg-desc-"
                      role="img"
                      class="sc-rbbb40-0 kMNrPk"
                    >
                      <title>bookmark-add</title>
                      <path d="M12.38 7.8h-1.66v-1.68c0-0.26-0.22-0.46-0.48-0.46v0h-0.48c-0.26 0-0.48 0.2-0.48 0.46v0 1.68h-1.66c-0.26 0-0.48 0.2-0.48 0.48v0 0.46c0 0.28 0.22 0.48 0.48 0.48v0h1.66v1.68c0 0.26 0.22 0.46 0.48 0.46v0h0.48c0.26 0 0.48-0.2 0.48-0.46v0-1.68h1.66c0.26 0 0.48-0.2 0.48-0.48v0-0.46c0-0.28-0.22-0.48-0.48-0.48v0zM15.020 0.9h-10.020c-1.060 0-1.92 0.84-1.92 1.9v0 16.42c0 0.28 0.16 0.5 0.36 0.62v0c0.12 0.060 0.24 0.1 0.38 0.1s0.24-0.040 0.36-0.1v0l5.82-3.52 5.82 3.52c0.1 0.060 0.24 0.1 0.38 0.1v0c0 0 0 0 0 0 0.12 0 0.24-0.040 0.34-0.1v0c0.22-0.12 0.36-0.34 0.36-0.62v-16.46c-0.020-1.040-0.86-1.86-1.88-1.86v0zM15.48 17.96l-5.1-3.080c-0.12-0.060-0.24-0.1-0.38-0.1s-0.26 0.040-0.38 0.1v0l-5.1 3.080v-15.24c0.040-0.22 0.22-0.4 0.46-0.4 0 0 0 0 0.020 0v0h10.020c0 0 0 0 0 0 0.24 0 0.44 0.2 0.46 0.44v0z"></path>
                    </svg>
                  </i>
                Add Trail
              </button>
              }

            </div>
          </div>
          <Tabs
            className="mt-4"
            defaultActiveKey="profile"
            id="uncontrolled-tab-example"
          >
            <Tab eventKey="profile" title="My Review">

              <h3 className="mt-3">Reviews</h3>
              {
                loading ?
                  <Spinner animation="grow" />
                  :
                  reviews?.map(review => <ReviewItem review={review} userName={userName} key={review?.review_id} getRating={getRating} />)
              }
            </Tab>
            <Tab eventKey="Review" title="Friends Review">
              {
                friendsReviews?.map(frnd => {
                  return frnd.reviews?.map(rev => {
                    return <>

                      <div className="review-head">
                        <div className="review-image">
                          <img src={ProfileImage} alt="profile" />
                        </div>
                        <div className="review-text">
                          <h4>{frnd?.first_name} {frnd?.last_name}</h4>
                          <span>
                            {
                              getRating(rev?.rating)
                            } {rev?.rating}
                          </span>
                        </div>
                      </div>
                      <div className="review-content">
                        <p>
                          {rev?.review}
                        </p>
          <div className="gallery">
            {
              rev?.images?.map(im => <div className="gallery-image">
                <img src={im.images_url} alt="" />
              </div>)
            }
                        </div>
                      </div>
                    </>;
                  });
                })
              }

            </Tab>
          </Tabs>
        </div>
      </div>
      <Footer />
    </>
  );

  function ReviewItem({ review, getRating, userName }) {
    return (
      <>
        <div className="review-head">
          <div className="review-image">
            <img src={ProfileImage} alt="profile" />
          </div>
          <div className="review-text">
            <h4>{userName || ''}</h4>
            <span>
              {getRating(review?.rating)} {review?.rating}
            </span>
          </div>
        </div>
        <div className="review-content">
          <p>
            {review?.review}
          </p>
          <div className="gallery">
            {
              review?.images?.map(im => <div className="gallery-image">
                <img src={im.images_url} alt="" />
              </div>)
            }

          </div>
        </div>
      </>
    );
  }

}



