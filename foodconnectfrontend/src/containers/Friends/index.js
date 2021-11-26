import "bootstrap/dist/css/bootstrap.min.css";
import React, { useEffect, useState } from "react";
import { Spinner, Tab, Tabs } from "react-bootstrap";
import Footer from "../../components/footer";
import FindFriend from "../../components/FriendsCard/findFreinds";
import FriendCard from "../../components/FriendsCard/index";
import HeaderDashboard from "../../components/header/header";
import { getFriendRequests, getFriendsByName, getFriendsList, getSentFriendRequests, getSuggestedFriends } from "../../services/apis";
import "./friends.css";

export default function Friends() {

  const [loading, setloading] = useState(false);
  const [searchLoading, setsearchLoading] = useState(false);
  const [friendsList, setfriendsList] = useState([]);
  const [searchedFriends, setsearchedFriends] = useState([]);
  const [outerTab, setouterTab] = useState('my-friends');
  const [searchText, setsearchText] = useState('');
  const [friendRequests, setfriendRequests] = useState([]);
  const [sentfriendRequests, setsentfriendRequests] = useState([]);
  const [suggestedFrieds, setsuggestedFrieds] = useState([]);

  useEffect(() => {
    getSetFriendsList();
    getSetSuggestedFriends();
  }, []);

  function getSetFriendsList() {
    setloading(true);
    getFriendsList().then(response => {
      if (response?.data) {
        setfriendsList(response?.data);
        setloading(false);
      }
    }).catch(err => {
      console.log(err, 'err');
      setloading(false);
    }
    );
  }

  function getSetSuggestedFriends() {
    getSuggestedFriends().then(response => {
      if (response?.data) {
        setsuggestedFrieds(response?.data?.suggestions || []);
      }
    }).catch(err => {
      console.log(err, 'err');
    }
    );
  }


  useEffect(() => {
    if (outerTab === 'requests') {
      setloading(true);
      getFriendRequests().then(response => {
        if (response?.data) {
          setfriendRequests(response?.data);
          setloading(false);
        }
      }).catch(err => {
        console.log(err, 'err');
        setloading(false);
      }
      );

      getSentFriendRequests().then(response => {
        if (response?.data) {
          setsentfriendRequests(response?.data);
        }
      }).catch(err => {
        console.log(err, 'err');
        setloading(false);
      }
      );

    }
  }, [outerTab]);

  function handleKeyDown(event) {
    console.log(event.target.value, 'event.target.value');

    if (event.key === 'Enter' && event?.target?.value !== '') {
      setloading(true);
      getFriendsByName(event?.target?.value).then(res => {
        console.log(res);
        setloading(false);
        if (res.data) {
          setsearchedFriends(res.data);
        }
      }).catch(err => {
        console.log(err, 'err');
        setloading(false);
      });
    }
  }

  function filterFriendRequests(id, fieldName = 'id') {
    const filteredData = friendRequests.filter(rq => rq[fieldName] != id);
    console.log(filteredData, 'filteredData');
    setfriendRequests(filteredData);
  }

  function filterSearchedFriends(id) {
    const filteredData = searchedFriends.filter(rq => rq.id != id);
    setsearchedFriends(filteredData);
  }


  return (
    <>
      <HeaderDashboard />
      <div className="friends">
        <div className="container">

          <div className="friends-inner">
            <Tabs
              className="mt-4"
              id="uncontrolled-tab-example"
              activeKey={outerTab}
              onSelect={(k) => setouterTab(k)}
            >
              <Tab eventKey="my-friends" title="My Friends">
                <div className="my-friend">
                  <h2>My Friends</h2>
                  <h6>( {friendsList?.length} Results Found )</h6>
                  {
                    loading ?
                      <Spinner animation="grow" />
                      :
                      <div className="friend-cards">
                        {/* <FriendCard /> */}
                        {
                          friendsList?.map(friend => <FriendCard friend={friend} />)
                        }
                      </div>
                  }
                </div>
              </Tab>
              <Tab eventKey="requests" title="Friends Request">
                <Tabs
                  className="mt-4 friends-req"
                  defaultActiveKey="received"
                  id="uncontrolled-tab-example"
                >
                  <Tab eventKey="received" title="Received">
                    {
                      loading ? <Spinner animation="grow" /> :

                        <div className="friend-cards">
                          {
                            friendRequests?.map(request =>
                              <FindFriend friend={request}
                                filterFriendRequests={filterFriendRequests}
                                type="received" />)
                          }
                        </div>
                    }
                  </Tab>
                  <Tab eventKey="sent" title="Sent">
                    {
                      loading ? <Spinner animation="grow" /> :

                        <div className="friend-cards">
                          {
                            sentfriendRequests?.map(request =>
                              <FindFriend friend={request}
                                type="sent"
                                filterFriendRequests={filterFriendRequests} />)
                          }
                        </div>
                    }
                  </Tab>
                </Tabs>
              </Tab>
              <Tab eventKey="find" title="Find Friends">
                <h3>FIND FRIENDS</h3>
                <div className="search">
                  <input type="text" placeholder="Search by name" onKeyDown={handleKeyDown} />
                  <i class="fa fa-search" aria-hidden="true"></i>
                </div>
                {
                  searchLoading ? <Spinner animation="grow" /> :

                    <div className="friend-cards">
                      {
                        searchedFriends?.map(friend =>
                          <FindFriend friend={friend}
                            filterSearchedFriends={filterSearchedFriends} />)
                      }
                    </div>
                }
              </Tab>
            </Tabs>
          </div>
          <h3 className="p-3">Friends Recommendation:</h3>
          <div className=" row">
            {
              suggestedFrieds?.map(friend =>
                <div className="col-lg-6">
                  <FriendCard friend={friend}
                    filterSearchedFriends={filterSearchedFriends} />
                </div>)
            }
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}
