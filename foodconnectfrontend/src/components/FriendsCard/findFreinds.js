import React, { useState } from "react";
import { toast } from "react-toastify";
import Image from "../../images/default-profile.png";
import { acceptFriendRequest, cancelFriendRequest, rejectFriendRequest, sendFriendRequest } from "../../services/apis";
import "./friendcard.css";
import { useHistory } from "react-router-dom";

export default function FindFreinds({ friend, type = 'new', filterSearchedFriends, filterFriendRequests }) {

    const [btnLoading, setbtnLoading] = useState(false);

    const sendFrndRequest = () => {
        setbtnLoading(true);
        sendFriendRequest(friend?.uuid || friend?.uuid).then(response => {
            if (response?.data) {
                setbtnLoading(false);
                filterSearchedFriends(friend?.uuid);
                toast.success('Request Sent');

            }
        }).catch(err => {
            console.log(err, 'err');
            setbtnLoading(false);
        }
        );
    };

    const cancelFrndRequest = () => {
        setbtnLoading(true);
        cancelFriendRequest(friend?.id).then(response => {
            if (response?.data) {
                setbtnLoading(false);
                filterFriendRequests(friend?.id);
                toast.success('Request Canceled');

            }
        }).catch(err => {
            console.log(err, 'err');
            setbtnLoading(false);
        }
        );
    };


    const acceptFrndRequest = () => {
        setbtnLoading(true);
        acceptFriendRequest(friend?.id).then(response => {
            if (response?.data) {
                setbtnLoading(false);
                filterFriendRequests(friend?.id);
                toast.success('Request Accepted');
            }
        }).catch(err => {
            console.log(err, 'err');
            setbtnLoading(false);
        }
        );
    };


    const rejectFrndRequest = () => {
        setbtnLoading(true);
        rejectFriendRequest(friend?.id).then(response => {
            if (response?.data) {
                setbtnLoading(false);
                filterFriendRequests(friend?.id, 'id');
                toast.success('Request Rejected');
            }
        }).catch(err => {
            console.log(err, 'err');
            setbtnLoading(false);
        }
        );
    };

    const history = useHistory()
    async function handleClick() {
    await localStorage.setItem("image_url",friend.image_url || friend?.image || Image)
    history.push(`/friendsTrail/${friend?.uuid}`);
  }

    return (
        <div  className="friend-list">
            <div onClick={handleClick} className="friend-image">
                <img src={friend?.image_url || friend.image || Image} alt="" />
              <div >
              </div>
            </div>
            <div className="friend-text">
                <h5>{friend?.first_name} {friend?.last_name}</h5>
            </div>
            {
                type === 'new' ? <button disabled={btnLoading} onClick={sendFrndRequest}><i class="fa fa-plus" aria-hidden="true"></i></button> :
                    type === 'sent' ? <button disabled={btnLoading} onClick={cancelFrndRequest}><i class="fa fa-times" aria-hidden="true"></i></button> :
                        <div style={{ display: 'grid' }}>
                            <button disabled={btnLoading} onClick={acceptFrndRequest}><i class="fa fa-check" aria-hidden="true"></i></button>
                            <button disabled={btnLoading} onClick={rejectFrndRequest}><i class="fa fa-times" aria-hidden="true"></i></button>
                        </div>
            }

        </div>
    );
}