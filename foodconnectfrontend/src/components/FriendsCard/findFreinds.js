import React, { useState } from "react";
import { toast } from "react-toastify";
import Image from "../../images/default-profile.png";
import { acceptFriendRequest, cancelFriendRequest, rejectFriendRequest, sendFriendRequest } from "../../services/apis";
import "./friendcard.css";

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


    return (
        <div className="friend-list">
            <div className="friend-image">
                <img src={Image} alt="" />
            </div>
            <div className="friend-text">
                <h5>{friend?.first_name} {friend?.last_name}</h5>
                {/* <p>
                    <i class="fa fa-map-marker" aria-hidden="true"></i>Santa Clara, CA
                    95054
                </p>
                <a href="tel:1-408-909-0709" className="tel">
                    <i class="fa fa-phone" aria-hidden="true"></i>
                    +1-408-909-0709
                </a> */}
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