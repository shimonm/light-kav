import {ToastAndroid} from "react-native";
// import btoa from 'btoa';
import utf8 from 'utf8'
import base64 from 'base-64'
import uuid from 'uuid';

const BASE_URL = "http://rpc.arbok.hackbtc18.offchain.rocks/";

export default class CLightningService {
  constructor() {
    // this.client = jayson.client.http({
    //   host: HOST,
    //   headers: {"Authorization": "Basic "+btoa("api-token:3oxreKoJ0V6jPA")}
    // });
  }
  _post(method, params) {

    return fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "Authorization": "Basic "+base64.encode(utf8.encode("api-token:3oxreKoJ0V6jPA"))
      },
      body: JSON.stringify({
        "jsonrpc":"2.0",
        "method": method,
        "params":params,
        "id": uuid()})
    }).then((response) => response.json())
      .catch((error) => {
        // console.error(error);
        ToastAndroid.show(error, ToastAndroid.SHORT);          
      });
  }
  pay(payment_request) {
    // return client.request('pay', [payment_request], function(err, response) {
    //   if(err) throw err;
    //   return response;
    // });
    return this._post('pay', [payment_request])
  }
}
