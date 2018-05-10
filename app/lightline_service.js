import {ToastAndroid} from "react-native";

const BASE_URL = "http://7abdb7b6.ngrok.io/";

export default class LightLineService {
  constructor() {

  }
  _post(endpoint, params) {
    return fetch(BASE_URL + endpoint, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    }).then((response) => response.json())
      .catch((error) => {
        // console.error(error);
        ToastAndroid.show(error, ToastAndroid.SHORT);          
      });
  }
  register() {
    /*
     * Response structure:
     {
       success: true/false
     }
    */
    const username = 'username';
    const password = 'password';
    return this._post("register", {
      username, password
    });
  }
  howmuch(userToken, rideCode) {
    /*
     * Response structure:
    {
      success: true/false,
      data: {
        amount: 0,
        payment_request: "JKafHR#"
      }
    }
    */
   return this._post("howmuch",
    {
      user_token: userToken,
      ride_code: rideCode
    });
  }
}
